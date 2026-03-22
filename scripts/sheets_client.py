"""
Google Sheets API wrapper for Oficio Taller studio agents.
Requires Python 3.10+.

Agents call this via Python import or Bash CLI.
Reads GOOGLE_SHEETS_ID and GOOGLE_CREDENTIALS_PATH from environment.
"""

import os
import sys
import json
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Column order for each sheet — must match the header row in the workbook.
SHEET_HEADERS = {
    "Projects": [
        "id", "number", "name", "type", "tier",
        "area_m2", "cost_per_m2", "total_budget_mxn", "fee_pct", "estimated_fee_mxn",
        "scope_year", "scope_signed_date", "delivery_year", "delivery_date",
        "construction_end_date", "press_date", "current_phase", "status",
        "fy27", "drive_id", "last_known_activity", "notes",
    ],
    "Milestones": [
        "project_id", "milestone_id", "label", "pct", "amount_mxn",
        "trigger", "estimated_date", "actual_date", "status",
    ],
    "Leads": [
        "id", "date", "client_name", "email", "phone", "source",
        "project_type", "budget_range", "status", "notes", "converted_to_project_id",
    ],
    "Invoices": [
        "id", "project_id", "invoice_number", "date", "amount_mxn",
        "status", "payment_date", "notes",
    ],
    "Bank": [
        "id", "date", "description", "amount_mxn", "type", "category", "matched_invoice_id",
    ],
    "Campaigns": [
        "id", "name", "project_ids", "platforms", "start_date", "end_date",
        "status", "reach", "inquiries_generated",
    ],
    "Assets": [
        "id", "project_id", "filename", "drive_url", "asset_type", "caption", "used_in_campaigns",
    ],
}


class SheetsClient:
    def __init__(self):
        load_dotenv()  # Load here, not at module level, so tests can monkeypatch env first
        _project_root = Path(__file__).parent.parent
        creds_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", str(_project_root / "credentials.json"))
        sheet_id = os.environ.get("GOOGLE_SHEETS_ID")
        if not sheet_id:
            raise EnvironmentError("GOOGLE_SHEETS_ID environment variable not set")
        creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        gc = gspread.authorize(creds)
        self._spreadsheet = gc.open_by_key(sheet_id)

    def _worksheet(self, sheet_name: str):
        return self._spreadsheet.worksheet(sheet_name)

    def read_sheet(self, sheet_name: str) -> list[dict]:
        """Return all rows as list of dicts keyed by header row."""
        ws = self._worksheet(sheet_name)
        return ws.get_all_records(default_blank="")

    def append_row(self, sheet_name: str, row: dict) -> None:
        """Append a row. Dict keys must match SHEET_HEADERS for this sheet."""
        headers = SHEET_HEADERS[sheet_name]
        values = [str(row.get(h, "")) for h in headers]
        ws = self._worksheet(sheet_name)
        ws.append_row(values, value_input_option="USER_ENTERED")

    def update_row(self, sheet_name: str, row_id: str, changes: dict, key: str = "id") -> None:
        """Update fields in the first row where key column == row_id."""
        ws = self._worksheet(sheet_name)
        headers = ws.row_values(1)
        records = ws.get_all_records(default_blank="")
        for i, record in enumerate(records):
            if str(record.get(key)) == str(row_id):
                row_num = i + 2  # +1 for 0-index, +1 for header row
                for field, value in changes.items():
                    if field in headers:
                        col = headers.index(field) + 1
                        ws.update_cell(row_num, col, value)
                return
        raise KeyError(f"Row with {key}={row_id!r} not found in {sheet_name}")

    def upsert_row(self, sheet_name: str, row: dict, key: str = "id") -> None:
        """Append if key not found, update if found."""
        records = self.read_sheet(sheet_name)
        row_id = str(row.get(key, ""))
        for record in records:
            if str(record.get(key)) == row_id:
                changes = {k: v for k, v in row.items() if k != key}
                self.update_row(sheet_name, row_id, changes, key=key)
                return
        self.append_row(sheet_name, row)


def _parse_args(argv: list[str]) -> dict:
    """Parse --key value pairs from argv, returning a dict."""
    kwargs = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i][2:]
            value = argv[i + 1] if i + 1 < len(argv) else ""
            try:
                value = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                pass
            kwargs[key] = value
            i += 2
        else:
            i += 1
    return kwargs


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scripts/sheets_client.py <command> <sheet> [--key value ...]")
        print("Commands: read, append, update")
        sys.exit(1)

    cmd = sys.argv[1]
    sheet = sys.argv[2]
    client = SheetsClient()

    if cmd == "read":
        rows = client.read_sheet(sheet)
        print(json.dumps(rows, ensure_ascii=False, indent=2))

    elif cmd == "append":
        kwargs = _parse_args(sys.argv[3:])
        client.append_row(sheet, kwargs)
        print("OK")

    elif cmd == "update":
        if len(sys.argv) < 4:
            print("Usage: python scripts/sheets_client.py update <sheet> <row_id> [--key value ...]")
            sys.exit(1)
        row_id = sys.argv[3]
        kwargs = _parse_args(sys.argv[4:])
        if not kwargs:
            print("Error: no fields provided to update")
            sys.exit(1)
        client.update_row(sheet, row_id, kwargs)
        print("OK")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
