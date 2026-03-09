#!/usr/bin/env python3
"""
Send a CEO campaign approval request via WhatsApp Web (Playwright automation).
Works with a regular WhatsApp account — no Business API required.

First run: will open WhatsApp Web for QR scan. Session is saved after login.
Subsequent runs: uses saved session, no QR scan needed.

Usage:
    python send-whatsapp.py <campaign-id> <approval-url> [--phone=+521234567890]

    Phone can also be set via environment variable: OFICIO_CEO_PHONE
"""

import os
import sys
import json
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("ERROR: playwright not installed. Run: pip install playwright && python -m playwright install chromium")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]
SESSION_FILE = ROOT / "publisher" / ".whatsapp-session.json"
CAMPAIGNS_DIR = ROOT / "campaigns"


def get_ceo_phone(args: list) -> str:
    """Resolve CEO phone from CLI arg or environment variable."""
    for arg in args:
        if arg.startswith("--phone="):
            return arg.split("=", 1)[1].strip()

    env_phone = os.environ.get("OFICIO_CEO_PHONE", "").strip()
    if env_phone:
        return env_phone

    print("ERROR: CEO phone number not set.")
    print("Options:")
    print("  1. Pass as argument:   --phone=+521234567890")
    print("  2. Set env variable:   set OFICIO_CEO_PHONE=+521234567890")
    sys.exit(1)


def find_campaign_dir(campaign_id: str) -> Path:
    for status in ("pending", "approved"):
        candidate = CAMPAIGNS_DIR / status / campaign_id
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Campaign '{campaign_id}' not found.")


def build_message(campaign_id: str, approval_url: str) -> str:
    campaign_dir = find_campaign_dir(campaign_id)
    brief_path = campaign_dir / "brief.json"

    project_name = campaign_id
    if brief_path.exists():
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
        project_name = brief.get("project_name", campaign_id)

    # Load approval package summary if available
    pkg_path = campaign_dir / "approval-package.json"
    summary = ""
    if pkg_path.exists():
        pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
        summary = pkg.get("campaign_summary", "")

    lines = [
        "*Oficio Taller — Aprobación requerida*",
        "",
        f"Proyecto: {project_name}",
        f"Campaña: {campaign_id}",
    ]

    if summary:
        # Add first sentence of Valentina's summary as context
        first_sentence = summary.split(".")[0].strip() + "."
        lines += ["", f"_{first_sentence}_"]

    lines += [
        "",
        "Valentina ha preparado el paquete completo para tu revisión.",
        "",
        f"Revisa y aprueba aquí:\n{approval_url}",
        "",
        "_Puedes aprobar o rechazar con notas directamente desde el enlace._",
    ]

    return "\n".join(lines)


# ── WhatsApp sender ───────────────────────────────────────────────────────────

def send_whatsapp(campaign_id: str, approval_url: str, ceo_phone: str):
    message = build_message(campaign_id, approval_url)

    # Clean phone number for wa.me URL
    phone_clean = ceo_phone.replace("+", "").replace(" ", "").replace("-", "")

    context_options = {}
    if SESSION_FILE.exists():
        print("✓ Loading saved WhatsApp session...")
        context_options["storage_state"] = str(SESSION_FILE)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            **context_options
        )
        page = context.new_page()

        print("Opening WhatsApp Web...")
        page.goto("https://web.whatsapp.com", timeout=30000)

        # Check if we need QR scan
        try:
            # If chat list appears quickly, we're already logged in
            page.wait_for_selector('[data-testid="chat-list"], [data-testid="qrcode"]', timeout=15000)

            if page.is_visible('[data-testid="qrcode"]'):
                print("\n" + "="*50)
                print("QR CODE SCAN REQUIRED")
                print("Open WhatsApp on your phone → Settings → Linked Devices → Link a Device")
                print("Waiting up to 60 seconds for scan...")
                print("="*50)
                page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
                print("✓ WhatsApp Web logged in.")

                # Save session for next time
                SESSION_FILE.parent.mkdir(parents=True, exist_ok=True)
                context.storage_state(path=str(SESSION_FILE))
                print(f"✓ Session saved to {SESSION_FILE}")
            else:
                print("✓ WhatsApp Web ready.")

        except PWTimeout:
            print("ERROR: Timed out waiting for WhatsApp Web to load.")
            browser.close()
            sys.exit(1)

        # Navigate directly to CEO chat
        wa_url = f"https://web.whatsapp.com/send?phone={phone_clean}"
        print(f"\nOpening chat with CEO ({ceo_phone})...")
        page.goto(wa_url, timeout=30000)

        # Wait for message compose box
        try:
            compose_box = page.wait_for_selector(
                '[data-testid="conversation-compose-box-input"]',
                timeout=20000
            )
        except PWTimeout:
            print("ERROR: Could not open CEO chat. Check that the phone number is correct and saved in your contacts.")
            browser.close()
            sys.exit(1)

        # Type the message
        print("Typing message...")
        compose_box.click()
        time.sleep(0.5)

        # Use clipboard paste for reliable multi-line message input
        page.evaluate(f"""
            const el = document.querySelector('[data-testid="conversation-compose-box-input"]');
            el.focus();
        """)

        # Type line by line to handle newlines properly
        for line in message.split("\n"):
            if line:
                compose_box.type(line, delay=10)
            page.keyboard.press("Shift+Enter")

        time.sleep(0.5)

        # Send
        page.keyboard.press("Enter")
        time.sleep(2)

        print(f"\n✓ WhatsApp message sent to CEO ({ceo_phone})")
        print(f"  Campaign: {campaign_id}")
        print(f"  Approval URL: {approval_url}")

        # Brief pause before closing so the message visually confirms sent
        time.sleep(2)
        browser.close()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    campaign_id = args[0]
    approval_url = args[1]
    ceo_phone = get_ceo_phone(args[2:])

    try:
        send_whatsapp(campaign_id, approval_url, ceo_phone)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(0)
