#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
Move a completed campaign from campaigns/approved/ to campaigns/published/.
Records completion timestamp in publish-log.json before moving.

Usage:
    python move-to-published.py <campaign-id>
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGNS_DIR = ROOT / "campaigns"


def move_to_published(campaign_id: str):
    src = CAMPAIGNS_DIR / "approved" / campaign_id
    dst = CAMPAIGNS_DIR / "published" / campaign_id

    if not src.exists():
        print(f"ERROR: Campaign '{campaign_id}' not found in campaigns/approved/")
        sys.exit(1)

    if dst.exists():
        print(f"ERROR: Campaign '{campaign_id}' already exists in campaigns/published/")
        print("If you need to overwrite it, remove the destination folder first.")
        sys.exit(1)

    # Confirm CEO decision is approved before moving
    decision_path = src / "ceo-decision.json"
    if decision_path.exists():
        decision_data = json.loads(decision_path.read_text(encoding="utf-8"))
        if decision_data.get("decision") != "approved":
            print(f"ERROR: CEO decision is '{decision_data.get('decision')}', not 'approved'.")
            print("Cannot move to published without CEO approval.")
            sys.exit(1)
    else:
        print("WARNING: No ceo-decision.json found. Proceeding anyway — confirm this was approved.")
        confirm = input("Type 'yes' to continue: ").strip().lower()
        if confirm != "yes":
            print("Cancelled.")
            sys.exit(0)

    # Update publish log with completion timestamp
    log_path = src / "publish-log.json"
    if log_path.exists():
        log = json.loads(log_path.read_text(encoding="utf-8"))
    else:
        log = {
            "campaign_id": campaign_id,
            "started_at": "",
            "posts_published": [],
            "posts_pending": [],
            "completed_at": None,
            "canal_notes": ""
        }

    log["completed_at"] = datetime.now().isoformat()
    log_path.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")

    # Move the folder
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))

    # Print summary
    posts_published = log.get("posts_published", [])
    print(f"\n✓ Campaign '{campaign_id}' moved to campaigns/published/")
    print(f"  Posts published: {len(posts_published)}")
    for post in posts_published:
        url = post.get("url", "no URL recorded")
        print(f"  - [{post.get('platform')}] Sequence {post.get('sequence')}: {url}")
    print()
    print("Next step: notify Rafael to add this campaign to the quarterly tracking list.")
    print(f"  @Rafael Campaign {campaign_id} is now in campaigns/published/. Please add it to your tracking list.")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    move_to_published(sys.argv[1])
