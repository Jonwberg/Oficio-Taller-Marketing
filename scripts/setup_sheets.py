"""
One-time setup script: creates the Google Sheets workbook structure.
Requires Python 3.10+.
and seeds it with data from data/financial-model.json and data/project-timelines.json.

Run once after completing docs/setup/google-sheets-setup.md.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Add project root to path so scripts module is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.sheets_client import SheetsClient, SHEET_HEADERS

FINANCIAL_MODEL_PATH = Path("data/financial-model.json")
TIMELINES_PATH = Path("data/project-timelines.json")


def create_sheets(client: SheetsClient) -> None:
    """Create all 7 worksheets with header rows."""
    spreadsheet = client._spreadsheet

    existing = [ws.title for ws in spreadsheet.worksheets()]
    for sheet_name, headers in SHEET_HEADERS.items():
        if sheet_name not in existing:
            ws = spreadsheet.add_worksheet(title=sheet_name, rows=500, cols=len(headers))
        else:
            ws = spreadsheet.worksheet(sheet_name)
        # Write header row
        ws.update("A1", [headers])
        print(f"→ {sheet_name}: created with {len(headers)} columns")

    # Delete default Sheet1 if present (Google creates it automatically)
    if "Sheet1" in [ws.title for ws in spreadsheet.worksheets()]:
        spreadsheet.del_worksheet(spreadsheet.worksheet("Sheet1"))


def seed_projects(client: SheetsClient) -> None:
    """Seed Projects and Milestones sheets from existing JSON files."""
    with open(FINANCIAL_MODEL_PATH, encoding="utf-8") as f:
        financial = json.load(f)
    with open(TIMELINES_PATH, encoding="utf-8") as f:
        timelines = json.load(f)

    # Build a lookup from project id → timelines data
    timeline_map = {p["id"]: p for p in timelines["projects"]}

    projects_written = 0
    milestones_written = 0

    for proj in financial["projects"]:
        pid = proj["id"]
        tl = timeline_map.get(pid, {})
        phases = tl.get("phases", {})

        scope_signed = phases.get("scope_signed", {})
        delivery = phases.get("delivery", {})
        construction_end = phases.get("construction_end", {})
        press = phases.get("press", {})

        row = {
            "id": pid,
            "number": tl.get("number", ""),
            "name": proj.get("name", ""),
            "type": proj.get("type", "residential"),
            "tier": proj.get("tier", ""),
            "area_m2": "",
            "cost_per_m2": "",
            "total_budget_mxn": "",
            "fee_pct": 12,
            "estimated_fee_mxn": proj.get("estimated_fee_mxn", ""),
            "scope_year": proj.get("scope_year", ""),
            "scope_signed_date": scope_signed.get("date", ""),
            "delivery_year": proj.get("delivery_year", "") or "",
            "delivery_date": delivery.get("date", ""),
            "construction_end_date": construction_end.get("date", ""),
            "press_date": press.get("date", ""),
            "current_phase": proj.get("current_phase", ""),
            "status": proj.get("status", ""),
            "fy27": "TRUE" if proj.get("fy27") else "FALSE",
            "drive_id": tl.get("drive_id", "") or "",
            "last_known_activity": tl.get("last_known_activity", "") or "",
            "notes": tl.get("notes", "") or "",
        }
        client.append_row("Projects", row)
        projects_written += 1

        for m in proj.get("milestones", []):
            milestone_row = {
                "project_id": pid,
                "milestone_id": m["id"],
                "label": m["label"],
                "pct": m["pct"],
                "amount_mxn": m["amount_mxn"],
                "trigger": m["trigger"],
                "estimated_date": m.get("estimated_date", "") or "",
                "actual_date": "",
                "status": m["status"],
            }
            client.append_row("Milestones", milestone_row)
            milestones_written += 1

    print(f"→ Seeding Projects: {projects_written} rows written")
    print(f"→ Seeding Milestones: {milestones_written} rows written")


if __name__ == "__main__":
    print("→ Creating sheets...")
    client = SheetsClient()
    create_sheets(client)
    print("→ Seeding data from existing JSON files...")
    seed_projects(client)
    print("Setup complete.")
