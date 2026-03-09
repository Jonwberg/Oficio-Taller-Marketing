#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
Publish a website project page to Cargo CMS via Playwright browser automation.
Cargo has no public API — this script opens the Cargo editor in a browser
and presents the approved copy and asset instructions for manual entry.

Session is saved after first login so subsequent runs don't require re-login.

Usage:
    python publish-cargo.py <campaign-id> <sequence-number>
"""

import json
import time
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGNS_DIR = ROOT / "campaigns"
SESSION_FILE = ROOT / "publisher" / ".cargo-session.json"
CARGO_DASHBOARD = "https://cargo.site/dashboard"


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def find_campaign_dir(campaign_id: str) -> Path:
    for status in ("approved", "pending"):
        candidate = CAMPAIGNS_DIR / status / campaign_id
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Campaign '{campaign_id}' not found in approved/ or pending/")


def load_post_data(campaign_id: str, sequence: int) -> dict:
    campaign_dir = find_campaign_dir(campaign_id)

    brief       = load_json(campaign_dir / "brief.json")
    copy_data   = load_json(campaign_dir / "copy.json")
    visual_data = load_json(campaign_dir / "visual-plan.json")
    strategy    = load_json(campaign_dir / "strategy.json")

    post_copy   = next((p for p in copy_data.get("posts", [])   if p.get("sequence") == sequence), None)
    post_visual = next((p for p in visual_data.get("posts", []) if p.get("sequence") == sequence), None)
    post_strat  = next((p for p in strategy.get("post_sequence", []) if p.get("sequence") == sequence), None)

    if not post_copy:
        raise ValueError(f"No copy found for sequence {sequence} in campaign {campaign_id}")

    platform = post_copy.get("platform", "")
    if platform != "website":
        raise ValueError(f"Sequence {sequence} is for '{platform}', not 'website'. Use the correct publish script.")

    return {
        "campaign_id": campaign_id,
        "sequence": sequence,
        "project_name": brief.get("project_name", campaign_id),
        "location": brief.get("location", ""),
        "year": brief.get("year", ""),
        "post_type": post_copy.get("post_type", "website_project_page"),
        "copy_es": post_copy.get("copy_es", ""),
        "copy_en": post_copy.get("copy_en", ""),
        "cover_asset": post_visual.get("cover_asset", "") if post_visual else "",
        "selected_assets": post_visual.get("selected_assets", []) if post_visual else [],
        "asset_order": post_visual.get("asset_order", []) if post_visual else [],
        "framing_notes": post_visual.get("framing_notes", "") if post_visual else "",
        "color_notes": post_visual.get("color_notes", "") if post_visual else "",
        "alt_texts": {
            "es": post_visual.get("alt_text_es", "") if post_visual else "",
            "en": post_visual.get("alt_text_en", "") if post_visual else "",
        },
        "publish_date": post_strat.get("publish_date", "") if post_strat else "",
    }


def print_posting_brief(data: dict):
    """Print a clean content brief for the editor to follow."""
    sep = "=" * 60

    print(f"\n{sep}")
    print(f"CARGO PUBLISH BRIEF")
    print(f"Campaign: {data['campaign_id']}  |  Sequence: {data['sequence']}")
    print(f"Project:  {data['project_name']} — {data['location']} — {data['year']}")
    print(f"Type:     {data['post_type'].replace('_', ' ').title()}")
    if data['publish_date']:
        print(f"Date:     {data['publish_date']}")
    print(sep)

    print("\n── SPANISH COPY ─────────────────────────────────────────")
    print(data["copy_es"])

    print("\n── ENGLISH COPY ─────────────────────────────────────────")
    print(data["copy_en"])

    print("\n── ASSETS ───────────────────────────────────────────────")
    if data["cover_asset"]:
        print(f"Cover/Hero: {data['cover_asset']}")
    if data["asset_order"]:
        print("Asset order:")
        for i, asset in enumerate(data["asset_order"], 1):
            print(f"  {i}. {asset}")
    elif data["selected_assets"]:
        print("Selected assets:")
        for asset in data["selected_assets"]:
            print(f"  - {asset}")

    if data["framing_notes"]:
        print(f"\nFraming notes: {data['framing_notes']}")
    if data["color_notes"]:
        print(f"Color notes: {data['color_notes']}")

    if data["alt_texts"]["es"]:
        print(f"\nAlt text (ES): {data['alt_texts']['es']}")
    if data["alt_texts"]["en"]:
        print(f"Alt text (EN): {data['alt_texts']['en']}")

    print(sep)


def update_publish_log(campaign_id: str, sequence: int, url: str = "", notes: str = ""):
    campaign_dir = find_campaign_dir(campaign_id)
    log_path = campaign_dir / "publish-log.json"

    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    else:
        log = {
            "campaign_id": campaign_id,
            "started_at": datetime.now().isoformat(),
            "posts_published": [],
            "posts_pending": [],
            "completed_at": None,
            "canal_notes": ""
        }

    # Remove from pending if present
    log["posts_pending"] = [p for p in log.get("posts_pending", []) if p.get("sequence") != sequence]

    # Add to published
    existing = next((p for p in log.get("posts_published", []) if p.get("sequence") == sequence), None)
    entry = {
        "sequence": sequence,
        "platform": "website",
        "post_type": "website_project_page",
        "published_at": datetime.now().isoformat(),
        "url": url,
        "status": "published",
        "notes": notes
    }
    if existing:
        log["posts_published"] = [p for p in log["posts_published"] if p.get("sequence") != sequence]
    log["posts_published"].append(entry)

    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"✓ Publish log updated for sequence {sequence}")


# ── Main ──────────────────────────────────────────────────────────────────────

def publish_to_cargo(campaign_id: str, sequence: int):
    data = load_post_data(campaign_id, sequence)
    print_posting_brief(data)

    context_options = {}
    if SESSION_FILE.exists():
        context_options["storage_state"] = str(SESSION_FILE)
        print("\n✓ Loading saved Cargo session...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(**context_options)
        page = context.new_page()

        print("Opening Cargo dashboard...")
        page.goto(CARGO_DASHBOARD, timeout=30000)
        time.sleep(2)

        # Check if login is needed
        if "login" in page.url.lower() or "signin" in page.url.lower():
            print("\n" + "=" * 50)
            print("CARGO LOGIN REQUIRED")
            print("Please log in to Cargo in the browser window.")
            print("Press Enter here when you are logged in and on the dashboard.")
            print("=" * 50)
            input()

            # Save session
            SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
            context.storage_state(path=str(SESSION_FILE))
            print(f"✓ Cargo session saved to {SESSION_FILE}")

        print("\n" + "=" * 60)
        print("CARGO IS OPEN IN YOUR BROWSER.")
        print()
        print("Follow these steps:")
        print("  1. Create a new project page in Cargo")
        print("  2. Set the title to the project name above")
        print("  3. Paste the SPANISH COPY into the main content area")
        print("  4. Add a separator, then paste the ENGLISH COPY below it")
        print("  5. Upload assets in the order listed above")
        print("  6. Set the cover/hero image as specified")
        print("  7. Add alt text to each image")
        print("  8. Publish the page")
        print()
        print("Once the page is LIVE, paste its URL below.")
        print("=" * 60)

        live_url = input("\nPaste the live Cargo page URL (or press Enter to skip): ").strip()
        notes = ""
        if not live_url:
            notes = "URL not provided at publish time"
            print("Note: URL not recorded. Update publish-log.json manually.")

        browser.close()

    update_publish_log(campaign_id, sequence, url=live_url, notes=notes)

    if live_url:
        print(f"\n✓ Cargo page published: {live_url}")
    print("Done. Proceed to the next sequence.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    campaign_id = args[0]
    try:
        sequence = int(args[1])
    except ValueError:
        print(f"ERROR: sequence must be a number, got '{args[1]}'")
        sys.exit(1)

    try:
        publish_to_cargo(campaign_id, sequence)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
