#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
Generate CEO approval page from a campaign package and optionally serve it
with a decision endpoint that writes the CEO's response to a JSON file.

Usage:
    python generate-approval-page.py <campaign-id>           # generate only
    python generate-approval-page.py <campaign-id> --serve   # generate and serve
"""

import json
import re
import sys
import http.server
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

try:
    from jinja2 import Template
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

# ── Paths ────────────────────────────────────────────────────────────────────

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGNS_DIR = ROOT / "campaigns"
APPROVAL_DIR = ROOT / "approval" / "pages"
TEMPLATE_PATH = ROOT / "approval" / "template.html"
DEFAULT_PORT = 8765


# ── Helpers ──────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def find_campaign_dir(campaign_id: str) -> Path:
    """Look in pending/ and approved/ for the campaign folder."""
    for status in ("pending", "approved"):
        candidate = CAMPAIGNS_DIR / status / campaign_id
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        f"Campaign '{campaign_id}' not found in campaigns/pending/ or campaigns/approved/"
    )


# ── Page generator ───────────────────────────────────────────────────────────

def generate_page(campaign_id: str) -> Path:
    campaign_dir = find_campaign_dir(campaign_id)

    brief          = load_json(campaign_dir / "brief.json")
    copy_data      = load_json(campaign_dir / "copy.json")
    strategy       = load_json(campaign_dir / "strategy.json")
    visual         = load_json(campaign_dir / "visual-plan.json")
    approval_pkg   = load_json(campaign_dir / "approval-package.json")
    assets         = load_json(campaign_dir / "assets.json")

    # Set of locally downloaded filenames for existence check
    local_photos_dir = campaign_dir / "photos"
    local_photos = {p.name for p in local_photos_dir.glob("*.JPG")} | {p.name for p in local_photos_dir.glob("*.jpg")} if local_photos_dir.exists() else set()

    # Build filename → drive_file_id lookup (kept for reference / future use)
    photo_ids = {
        p["filename"]: p["drive_file_id"]
        for p in assets.get("photos", [])
        if p.get("drive_file_id")
    }

    # Relative path from approval/pages/ to the photos directory
    photos_base = f"../../campaigns/pending/{campaign_id}/photos"

    def extract_filename(value: str) -> str:
        """Pull the first _DSC*.JPG (or similar) filename from a cover_asset string."""
        if not value:
            return ""
        m = re.search(r'_DSC\d+\.JPG', value, re.IGNORECASE)
        return m.group(0) if m else value.strip()

    # Merge copy posts and visual posts by sequence number
    copy_by_seq = {p["sequence"]: p for p in copy_data.get("posts", [])}
    visual_by_seq = {p["sequence"]: p for p in visual.get("posts", [])}
    all_seqs = sorted(set(copy_by_seq) | set(visual_by_seq))

    combined_posts = []
    for seq in all_seqs:
        cp = copy_by_seq.get(seq, {})
        vp = visual_by_seq.get(seq, {})
        combined_posts.append({
            "sequence": seq,
            "platform": cp.get("platform") or vp.get("platform", ""),
            "post_type": cp.get("post_type") or vp.get("post_type", ""),
            "copy_es": cp.get("copy_es", ""),
            "copy_en": cp.get("copy_en", ""),
            "hashtags": cp.get("hashtags", []),
            "youtube_title_es": cp.get("youtube_title_es", ""),
            "youtube_title_en": cp.get("youtube_title_en", ""),
            "framing_notes": vp.get("framing_notes", ""),
            "edit_notes": vp.get("edit_notes", ""),
            "flags": vp.get("flags", []),
            "cover_asset": extract_filename(vp.get("cover_asset", "")),
            "asset_order": [extract_filename(f) for f in vp.get("asset_order", []) if extract_filename(f)],
        })

    template_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    template = Template(template_text)

    html = template.render(
        campaign_id=campaign_id,
        project_name=brief.get("project_name") or approval_pkg.get("project_name", campaign_id),
        created_date=datetime.now().strftime("%d %b %Y"),
        campaign_summary=approval_pkg.get("campaign_summary", "Sin resumen disponible."),
        combined_posts=combined_posts,
        photo_ids=photo_ids,
        photos_base=photos_base,
        local_photos=local_photos,
        schedule=strategy.get("post_sequence", []),
    )

    APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
    output_path = APPROVAL_DIR / f"{campaign_id}.html"
    output_path.write_text(html, encoding="utf-8")

    print(f"✓ Approval page generated: {output_path}")
    return output_path


# ── Local server ─────────────────────────────────────────────────────────────

def serve(campaign_id: str, port: int = DEFAULT_PORT):
    """Serve the approval page and capture the CEO's decision."""

    decision_file = find_campaign_dir(campaign_id) / "ceo-decision.json"
    stop_event = threading.Event()

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            # Redirect root to the campaign page
            if self.path in ("/", f"/{campaign_id}", f"/{campaign_id}.html"):
                self.path = f"/approval/pages/{campaign_id}.html"
            super().do_GET()

        def do_POST(self):
            if self.path == "/decision":
                length = int(self.headers.get("Content-Length", 0))
                raw = self.rfile.read(length)
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError:
                    self.send_response(400)
                    self.end_headers()
                    return

                decision_file.write_text(
                    json.dumps(data, indent=2, ensure_ascii=False),
                    encoding="utf-8"
                )

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok": true}')

                decision = data.get("decision", "unknown")
                notes = data.get("notes", "")
                print(f"\n{'='*50}")
                print(f"CEO DECISION: {decision.upper()}")
                if notes:
                    print(f"Notes: {notes}")
                print(f"Saved to: {decision_file}")
                print(f"{'='*50}")
                print("\nServer will stop in 3 seconds...")
                threading.Timer(3, stop_event.set).start()
            else:
                self.send_response(404)
                self.end_headers()

        def log_message(self, format, *args):
            pass  # Suppress request logs for cleaner output

    # Serve from the project root so relative paths work
    import os
    os.chdir(ROOT)

    server = http.server.HTTPServer(("localhost", port), Handler)
    url = f"http://localhost:{port}/{campaign_id}.html"

    print(f"\n{'='*50}")
    print(f"Approval page live at:")
    print(f"  {url}")
    print(f"Waiting for CEO decision... (Ctrl+C to stop)")
    print(f"{'='*50}\n")

    # Open in browser automatically
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    while not stop_event.is_set():
        server.handle_request()

    server.server_close()
    print("Server stopped.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    campaign_id = args[0]
    should_serve = "--serve" in args
    port = DEFAULT_PORT

    for arg in args:
        if arg.startswith("--port="):
            try:
                port = int(arg.split("=")[1])
            except ValueError:
                pass

    try:
        generate_page(campaign_id)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if should_serve:
        serve(campaign_id, port)
