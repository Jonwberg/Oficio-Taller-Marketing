# Google Sheets Data Layer Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace hand-crafted JSON files with a Google Sheets workbook as the canonical source of truth, with a sync script that regenerates the existing JSON files consumed by all dashboards.

**Architecture:** `SheetsClient` wraps `gspread` for read/write/update operations. `setup_sheets.py` is a one-time migration script that creates the workbook structure and seeds it from the existing JSON files. `sheets_sync.py` reads all sheets, runs cascade calculations, and writes `data/financial-model.json` and `data/project-timelines.json` in their exact existing formats.

**Tech Stack:** Python 3.10+, `gspread` (Google Sheets API), `google-auth`, `pytest`, `pytest-mock`

**Spec:** `docs/superpowers/specs/2026-03-21-google-sheets-data-layer-design.md`

---

## File Map

| File | Action | Responsibility |
|---|---|---|
| `scripts/sheets_client.py` | CREATE | Sheets API wrapper — read, append, update, upsert |
| `scripts/sheets_sync.py` | CREATE | Pull Sheets → cascade calculations → emit JSON |
| `scripts/setup_sheets.py` | CREATE | One-time: create tabs + seed from existing JSON |
| `tests/test_sheets_client.py` | CREATE | Unit tests for SheetsClient |
| `tests/test_sheets_sync.py` | CREATE | Unit tests for cascade calculation functions |
| `docs/setup/google-sheets-setup.md` | CREATE | Step-by-step Google Cloud manual setup |
| `requirements.txt` | CREATE | Top-level deps: gspread, python-dotenv |
| `.gitignore` | MODIFY | Add `credentials.json` |

---

## Chunk 1: Infrastructure and SheetsClient

### Task 1: Setup infrastructure

**Files:**
- Modify: `.gitignore`
- Create: `requirements.txt`
- Create: `docs/setup/google-sheets-setup.md`

- [ ] **Step 1: Add credentials.json to .gitignore**

Open `.gitignore` and add `credentials.json` after the existing `token.json` line:

```
credentials.json
```

Also check if `credentials.json` was already accidentally committed:
```bash
git ls-files credentials.json
```
If the command returns output, run `git rm --cached credentials.json` to stop tracking it.

- [ ] **Step 2: Create top-level requirements.txt**

Create `requirements.txt` at the project root:

```
# Python 3.10+ required (uses list[dict] type hints and match syntax)
gspread==6.1.2
google-auth==2.29.0
python-dotenv==1.0.1
```

- [ ] **Step 3: Install dependencies**

```bash
pip install -r requirements.txt
```

Expected: packages install without errors. Also add `python-dotenv==1.0.1` to `entrega/requirements.txt` so both requirement files stay in sync.

- [ ] **Step 4: Create docs/setup/ directory and setup guide**

Create `docs/setup/google-sheets-setup.md`:

```markdown
# Google Sheets Setup Guide

Follow these steps **in order** before running any scripts.

## Step 1: Create a Google Cloud project

1. Go to https://console.cloud.google.com
2. Click "New Project" → name it `oficio-taller-studio` → Create

## Step 2: Enable APIs

1. In the left menu → APIs & Services → Library
2. Search "Google Sheets API" → Enable
3. Search "Google Drive API" → Enable

## Step 3: Create a service account

1. APIs & Services → Credentials → Create Credentials → Service Account
2. Name: `studio-sync` → Create and continue → Done
3. Click the service account → Keys tab → Add Key → JSON
4. Download the file → rename it `credentials.json` → place at project root

## Step 4: Note the service account email

On the service account page, copy the email address.
It looks like: `studio-sync@oficio-taller-studio.iam.gserviceaccount.com`

## Step 5: Create the spreadsheet

1. Go to https://sheets.google.com
2. Create a new blank spreadsheet
3. Rename it: **Oficio Taller — Studio Data**

## Step 6: Share the spreadsheet with the service account

1. Click Share (top right)
2. Paste the service account email
3. Set role to **Editor**
4. Uncheck "Notify people" → Share

## Step 7: Get the spreadsheet ID

From the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit`
Copy the `SPREADSHEET_ID` part.

## Step 8: Create .env file

Create `.env` at the project root:

```
GOOGLE_SHEETS_ID=your_spreadsheet_id_here
GOOGLE_CREDENTIALS_PATH=credentials.json
```

## Step 9: Run setup script

```bash
python scripts/setup_sheets.py
```

Expected output:
```
→ Creating sheets...
→ Projects: created with 22 columns
→ Milestones: created with 9 columns
→ Leads: created with 11 columns
→ Invoices: created with 8 columns
→ Bank: created with 7 columns
→ Campaigns: created with 9 columns
→ Assets: created with 7 columns
→ Seeding Projects: 34 rows written
→ Seeding Milestones: 136 rows written
Setup complete.
```

## Step 10: Verify sync

```bash
python scripts/sheets_sync.py
```

Expected: both JSON files written, no errors.
```

- [ ] **Step 5: Commit**

```bash
git add .gitignore requirements.txt docs/setup/google-sheets-setup.md
git commit -m "feat: add Google Sheets setup infrastructure"
```

---

### Task 2: SheetsClient

**Files:**
- Create: `scripts/sheets_client.py`

The `scripts/` directory may not exist yet — create it if needed.

The client follows the same pattern as `entrega/asana_client.py`: module-level class, `__main__` CLI block with `--key value` arg parsing.

**Note on Projects sheet columns:** The spec defines 19 columns for Projects. The implementation adds 3 more (`delivery_date`, `construction_end_date`, `press_date`) to preserve the full phases structure from `project-timelines.json`. Total: 22 columns.

- [ ] **Step 1: Create scripts/sheets_client.py**

```python
"""
Google Sheets API wrapper for Oficio Taller studio agents.

Agents call this via Python import or Bash CLI.
Reads GOOGLE_SHEETS_ID and GOOGLE_CREDENTIALS_PATH from environment.
"""

import os
import sys
import json

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
        creds_path = os.environ.get("GOOGLE_CREDENTIALS_PATH", "credentials.json")
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
```

- [ ] **Step 2: Commit**

```bash
git add scripts/sheets_client.py
git commit -m "feat: add SheetsClient API wrapper"
```

---

### Task 3: SheetsClient tests

**Files:**
- Create: `tests/test_sheets_client.py`

The `tests/` directory may not exist at the project root — create it with an empty `__init__.py` if needed.

- [ ] **Step 1: Write the failing tests**

Create `tests/__init__.py` (empty) and `tests/test_sheets_client.py`:

```python
import pytest
import json
from unittest.mock import MagicMock, patch, call


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("GOOGLE_SHEETS_ID", "test-sheet-id")
    monkeypatch.setenv("GOOGLE_CREDENTIALS_PATH", "fake-creds.json")


@pytest.fixture
def mock_worksheet():
    ws = MagicMock()
    ws.get_all_records.return_value = [
        {"id": "P-001", "name": "Test", "status": "in_process", "area_m2": "200"},
        {"id": "P-002", "name": "Other", "status": "built", "area_m2": "300"},
    ]
    ws.row_values.return_value = ["id", "name", "status", "area_m2"]
    return ws


@pytest.fixture
def client(mock_env, mock_worksheet):
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.worksheet.return_value = mock_worksheet
    mock_gc = MagicMock()
    mock_gc.open_by_key.return_value = mock_spreadsheet

    with patch("gspread.authorize", return_value=mock_gc), \
         patch("google.oauth2.service_account.Credentials.from_service_account_file"):
        from scripts.sheets_client import SheetsClient
        return SheetsClient()


def test_read_sheet_returns_list_of_dicts(client, mock_worksheet):
    rows = client.read_sheet("Projects")
    assert isinstance(rows, list)
    assert rows[0]["id"] == "P-001"
    assert rows[1]["status"] == "built"
    mock_worksheet.get_all_records.assert_called_once_with(default_blank="")


def test_append_row_writes_values_in_header_order(client, mock_worksheet):
    from scripts.sheets_client import SHEET_HEADERS
    client.append_row("Leads", {
        "id": "L-001",
        "date": "2026-03-22",
        "client_name": "Ana García",
        "status": "new",
    })
    args = mock_worksheet.append_row.call_args[0][0]
    headers = SHEET_HEADERS["Leads"]
    assert args[headers.index("id")] == "L-001"
    assert args[headers.index("client_name")] == "Ana García"
    assert args[headers.index("status")] == "new"
    # Fields not provided should be empty string
    assert args[headers.index("email")] == ""


def test_update_row_changes_correct_cell(client, mock_worksheet):
    # Mock returns ["id", "name", "status", "area_m2"] — "status" is col 3 (1-based)
    # This test is internally consistent with the mock; the real Projects sheet has
    # "status" at col 18 — the implementation correctly reads live header positions
    client.update_row("Projects", "P-001", {"status": "built"})
    # row P-001 is index 0 in records → row_num = 2; status is col 3 in the mock
    mock_worksheet.update_cell.assert_called_once_with(2, 3, "built")


def test_update_row_raises_if_not_found(client, mock_worksheet):
    with pytest.raises(KeyError, match="not found"):
        client.update_row("Projects", "P-999", {"status": "built"})


def test_upsert_row_appends_when_not_found(client, mock_worksheet):
    from scripts.sheets_client import SHEET_HEADERS
    client.upsert_row("Projects", {"id": "P-003", "name": "New"})
    mock_worksheet.append_row.assert_called_once()


def test_upsert_row_updates_when_found(client, mock_worksheet):
    client.upsert_row("Projects", {"id": "P-001", "status": "built"})
    mock_worksheet.update_cell.assert_called()
    mock_worksheet.append_row.assert_not_called()


def test_missing_sheet_id_raises(monkeypatch):
    monkeypatch.delenv("GOOGLE_SHEETS_ID", raising=False)
    monkeypatch.setenv("GOOGLE_CREDENTIALS_PATH", "fake.json")
    with patch("gspread.authorize"), \
         patch("google.oauth2.service_account.Credentials.from_service_account_file"):
        from scripts import sheets_client
        import importlib
        importlib.reload(sheets_client)
        with pytest.raises(EnvironmentError, match="GOOGLE_SHEETS_ID"):
            sheets_client.SheetsClient()
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_sheets_client.py -v
```

Expected: ImportError or ModuleNotFoundError on `scripts.sheets_client` (module exists but gspread may not be installed yet, or import path issues).

- [ ] **Step 3: Fix any import path issues**

If `scripts` is not on the Python path, create `scripts/__init__.py` (empty file).

Run again:
```bash
pytest tests/test_sheets_client.py -v
```

Expected: tests FAIL with assertion errors (implementation not complete yet), not import errors.

- [ ] **Step 4: Verify tests pass against the implementation written in Task 2**

```bash
pytest tests/test_sheets_client.py -v
```

Expected output:
```
tests/test_sheets_client.py::test_read_sheet_returns_list_of_dicts PASSED
tests/test_sheets_client.py::test_append_row_writes_values_in_header_order PASSED
tests/test_sheets_client.py::test_update_row_changes_correct_cell PASSED
tests/test_sheets_client.py::test_update_row_raises_if_not_found PASSED
tests/test_sheets_client.py::test_upsert_row_appends_when_not_found PASSED
tests/test_sheets_client.py::test_upsert_row_updates_when_found PASSED
tests/test_sheets_client.py::test_missing_sheet_id_raises PASSED
7 passed
```

- [ ] **Step 5: Commit**

```bash
git add tests/__init__.py tests/test_sheets_client.py scripts/__init__.py
git commit -m "test: add SheetsClient unit tests"
```

---

## Chunk 2: Setup Script, Sync Script, and Verification

### Task 4: setup_sheets.py (one-time migration)

**Files:**
- Create: `scripts/setup_sheets.py`

This script runs once after the manual Google Cloud setup. It creates all 7 worksheets with the correct header rows, then seeds Projects and Milestones from the existing JSON files.

- [ ] **Step 1: Write scripts/setup_sheets.py**

```python
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

    # Delete the default "Sheet1" if it exists
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
            "area_m2": "",  # not in existing JSON — leave blank for manual entry
            "cost_per_m2": "",  # same
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
```

- [ ] **Step 2: Commit**

```bash
git add scripts/setup_sheets.py
git commit -m "feat: add setup_sheets migration script"
```

---

### Task 5: sheets_sync.py cascade calculations (pure functions + tests first)

**Files:**
- Create: `scripts/sheets_sync.py`
- Create: `tests/test_sheets_sync.py`

Write the tests first, then implement.

- [ ] **Step 1: Write tests/test_sheets_sync.py**

```python
"""Tests for sheets_sync.py cascade calculation functions."""
import pytest
from datetime import date


def test_calc_budget():
    from scripts.sheets_sync import calc_budget
    assert calc_budget(200, 20000) == 4_000_000
    assert calc_budget(0, 20000) == 0
    assert calc_budget("", 20000) == 0   # blank area → 0


def test_calc_fee():
    from scripts.sheets_sync import calc_fee
    assert calc_fee(4_000_000, 12) == 480_000
    assert calc_fee(0, 12) == 0
    assert calc_fee(925000, "") == 0     # blank pct → 0


def test_calc_milestone_amounts():
    from scripts.sheets_sync import calc_milestone_amounts
    amounts = calc_milestone_amounts(1_000_000)
    assert amounts == [300_000, 200_000, 200_000, 300_000]


def test_calc_milestone_amounts_zero():
    from scripts.sheets_sync import calc_milestone_amounts
    assert calc_milestone_amounts(0) == [0, 0, 0, 0]


def test_calc_milestone_status_built():
    from scripts.sheets_sync import calc_milestone_statuses
    statuses = calc_milestone_statuses("complete", "built")
    assert statuses == ["collected", "collected", "collected", "collected"]


def test_calc_milestone_status_scope_signed():
    from scripts.sheets_sync import calc_milestone_statuses
    # Only M1 trigger (scope_signed) is reached
    statuses = calc_milestone_statuses("scope_signed", "in_process")
    assert statuses == ["collected", "projected", "projected", "projected"]


def test_calc_milestone_status_anteproyecto():
    from scripts.sheets_sync import calc_milestone_statuses
    # M1, M2, M3 triggers reached (scope_signed, conceptual, anteproyecto)
    statuses = calc_milestone_statuses("anteproyecto", "in_process")
    assert statuses == ["collected", "collected", "collected", "projected"]


def test_derive_milestone_date_from_scope_signed_date():
    from scripts.sheets_sync import derive_milestone_date
    # M1: 0 weeks from 2025-07-01 → 2025-07
    assert derive_milestone_date("2025-07-01", None, 0) == "2025-07"
    # M2: +10 weeks from 2025-07-01 → ~2025-09
    assert derive_milestone_date("2025-07-01", None, 1) == "2025-09"
    # M3: +20 weeks from 2025-07-01 → ~2025-11
    assert derive_milestone_date("2025-07-01", None, 2) == "2025-11"
    # M4: +32 weeks from 2025-07-01 → ~2026-02
    assert derive_milestone_date("2025-07-01", None, 3) == "2026-02"


def test_derive_milestone_date_fallback_to_scope_year():
    from scripts.sheets_sync import derive_milestone_date
    # No scope_signed_date, use scope_year 2022 → anchor 2022-01-01
    assert derive_milestone_date("", 2022, 0) == "2022-01"


def test_derive_milestone_date_no_anchor_returns_empty():
    from scripts.sheets_sync import derive_milestone_date
    assert derive_milestone_date("", "", 0) == ""


def test_build_financial_project_record():
    """Output record must match exact financial-model.json structure."""
    from scripts.sheets_sync import build_financial_project

    project_row = {
        "id": "73-barra", "name": "73_BARRA PRIETA", "type": "residential",
        "tier": "large_residential", "status": "in_process", "fy27": "TRUE",
        "scope_year": "2025", "delivery_year": "",
        "current_phase": "anteproyecto", "estimated_fee_mxn": "1850000",
        "notes": "",
    }
    milestones = [
        {"project_id": "73-barra", "milestone_id": "M1", "label": "Advance",
         "pct": "30", "amount_mxn": "555000", "trigger": "scope_signed",
         "estimated_date": "2025-07", "actual_date": "", "status": "collected"},
        {"project_id": "73-barra", "milestone_id": "M2", "label": "Conceptual",
         "pct": "20", "amount_mxn": "370000", "trigger": "conceptual",
         "estimated_date": "2025-10", "actual_date": "", "status": "collected"},
        {"project_id": "73-barra", "milestone_id": "M3", "label": "Anteproyecto",
         "pct": "20", "amount_mxn": "370000", "trigger": "anteproyecto",
         "estimated_date": "2026-01", "actual_date": "", "status": "collected"},
        {"project_id": "73-barra", "milestone_id": "M4", "label": "Ejecutivo",
         "pct": "30", "amount_mxn": "555000", "trigger": "ejecutivo",
         "estimated_date": "2026-04", "actual_date": "", "status": "projected"},
    ]

    record = build_financial_project(project_row, milestones)

    assert record["id"] == "73-barra"
    assert record["estimated_fee_mxn"] == 1850000
    assert record["fy27"] is True
    assert record["status"] == "in_process"
    assert len(record["milestones"]) == 4
    assert record["milestones"][0]["amount_mxn"] == 555000
    assert record["milestones"][3]["status"] == "projected"
    # Must NOT have keys with wrong names
    assert "estimated_fee" not in record
    assert "amount" not in record["milestones"][0]
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
pytest tests/test_sheets_sync.py -v
```

Expected: ImportError (`scripts.sheets_sync` does not exist yet).

- [ ] **Step 3: Write scripts/sheets_sync.py**

```python
"""
Sync script: reads Google Sheets → runs cascade calculations → writes JSON files.
Requires Python 3.10+.

Usage: python scripts/sheets_sync.py

Regenerates:
  data/financial-model.json
  data/project-timelines.json
"""

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))

PHASE_SEQUENCE = ["scope_signed", "conceptual", "anteproyecto", "ejecutivo", "complete"]
MILESTONE_TRIGGERS = ["scope_signed", "conceptual", "anteproyecto", "ejecutivo"]
# Calendar weeks offset from scope_signed_date for each milestone
MILESTONE_WEEK_OFFSETS = [0, 10, 20, 32]

FINANCIAL_MODEL_PATH = Path("data/financial-model.json")
TIMELINES_PATH = Path("data/project-timelines.json")

# Static top-level content for financial-model.json
FINANCIAL_STATIC = {
    "_schema": "1.0",
    "_description": "Studio financial model — all figures estimated from fee formulas, not accounting records.",
    "_data_disclaimer": "Fees derived from tier defaults (m² × construction cost × 12% arch fee). Update estimated_fee_mxn per project to refine. Milestone dates estimated from Drive phase data.",
    "assumptions": {
        "architecture_fee_pct": 12,
        "construction_cost_per_sqm_mxn": {
            "residential_low": 15000,
            "residential_mid": 20000,
            "residential_high": 28000,
            "commercial": 22000,
        },
        "payment_schedule_pct": [30, 20, 20, 30],
        "payment_schedule_labels": [
            "Advance at signing",
            "At conceptual delivery",
            "At anteproyecto delivery",
            "At ejecutivo delivery",
        ],
        "phase_duration_weeks": {
            "estudios_previos": 3,
            "conceptual_anteproyecto": 10,
            "ejecutivo": 12,
        },
        "tier_defaults": {
            "small_residential":  {"sqm_range": "150–200", "fee_min": 350000,  "fee_max": 600000,  "fee_default": 475000},
            "mid_residential":    {"sqm_range": "250–400", "fee_min": 650000,  "fee_max": 1200000, "fee_default": 925000},
            "large_residential":  {"sqm_range": "400+",    "fee_min": 1200000, "fee_max": 2500000, "fee_default": 1850000},
            "commercial":         {"sqm_range": "varies",  "fee_min": 1500000, "fee_max": 3500000, "fee_default": 2500000},
        },
    },
}

# Static top-level content for project-timelines.json
TIMELINES_STATIC = {
    "_schema": "1.0",
    "_data_sources": [
        "Google Drive folder metadata (02. PROYECTOS)",
        "ALCANCE_BASE.docx (Dec 2020) — phase duration targets",
        "Drive search results for ALCANCE documents",
        "Entrega pipeline decision-event.json (future projects)",
    ],
    "_confidence_notes": {
        "migration_feb_2018": "Feb 21, 2018 Drive dates across pre-2019 projects = mass migration event. Not actual work dates. Pre-2019 project durations estimated.",
        "migration_oct_2021": "Oct 4, 2021 dates across Casa Pomona subfolders = second migration event. Reliable data resumes Jan 27, 2022.",
        "estimated_dates": "Scope dates estimated at (Drive last-modified date minus estimated project duration). Confidence: low.",
    },
    "benchmarks": {
        "source": "ALCANCE_BASE.docx (Dec 16, 2020) + Casa Pomona confirmed data",
        "payment_schedule": {
            "advance_pct": 30,
            "at_conceptual_pct": 20,
            "at_anteproyecto_pct": 20,
            "at_ejecutivo_pct": 30,
        },
        "phases": {
            "estudios_previos":        {"min_wks": 2,  "avg_wks": 3,  "max_wks": 6,  "note": "Site analysis, topographic review, solar study, program interview, sensory documentation"},
            "conceptual_anteproyecto": {"min_wks": 8,  "avg_wks": 10, "max_wks": 14, "note": "ALCANCE_BASE: 8–12 semanas hábiles. Max 2 revision rounds included."},
            "ejecutivo":               {"min_wks": 10, "avg_wks": 12, "max_wks": 18, "note": "ALCANCE_BASE: 12 semanas hábiles from approved anteproyecto + structural received."},
            "total_design":            {"min_wks": 20, "avg_wks": 28, "max_wks": 40, "note": "Estudios + Conceptual + Ejecutivo combined. Calendar weeks."},
            "delivery_to_construction_end": {"min_mos": 12, "avg_mos": 18, "max_mos": 30, "note": "Casa Pomona: Jan 2022 → Mar 2023 = 14 months. Based on 1 confirmed data point."},
            "delivery_to_press":       {"min_mos": 24, "avg_mos": 36, "max_mos": 60, "note": "Casa Pomona: Jan 2022 → Dec 2025 = 47 months. Based on 1 confirmed data point."},
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _to_int(val) -> int | None:
    """Convert value to int, returning None if blank, non-numeric, or zero-ish."""
    try:
        result = int(float(val))
        return result if result != 0 else None
    except (ValueError, TypeError):
        return None


def _parse_bool(val) -> bool:
    """Parse boolean from Sheets string or Python bool."""
    if isinstance(val, bool):
        return val
    return str(val).strip().upper() == "TRUE"


# ---------------------------------------------------------------------------
# Pure calculation functions (testable without network)
# ---------------------------------------------------------------------------

def calc_budget(area_m2, cost_per_m2) -> float:
    """area_m2 × cost_per_m2. Returns 0 if either is blank/zero."""
    try:
        return float(area_m2) * float(cost_per_m2)
    except (ValueError, TypeError):
        return 0.0


def calc_fee(total_budget_mxn, fee_pct) -> float:
    """total_budget_mxn × fee_pct / 100. Returns 0 if either is blank/zero."""
    try:
        return float(total_budget_mxn) * float(fee_pct) / 100
    except (ValueError, TypeError):
        return 0.0


def calc_milestone_amounts(estimated_fee_mxn: float) -> list[float]:
    """Return [M1, M2, M3, M4] amounts from the 30/20/20/30 schedule."""
    pcts = [0.30, 0.20, 0.20, 0.30]
    return [round(estimated_fee_mxn * p) for p in pcts]


def calc_milestone_statuses(current_phase: str, project_status: str) -> list[str]:
    """
    Return ["collected"|"projected", ...] for M1–M4.
    All collected if project_status == "built".
    Otherwise, milestone is collected if its trigger <= current_phase in PHASE_SEQUENCE.
    """
    if project_status == "built":
        return ["collected", "collected", "collected", "collected"]
    try:
        current_idx = PHASE_SEQUENCE.index(current_phase)
    except ValueError:
        current_idx = -1
    return [
        "collected" if PHASE_SEQUENCE.index(trigger) <= current_idx else "projected"
        for trigger in MILESTONE_TRIGGERS
    ]


def derive_milestone_date(scope_signed_date: str, scope_year, milestone_idx: int) -> str:
    """
    Return YYYY-MM string for a milestone based on offset from scope anchor.
    milestone_idx: 0=M1, 1=M2, 2=M3, 3=M4
    Returns "" if no anchor available.
    """
    anchor = None
    if scope_signed_date:
        try:
            anchor = date.fromisoformat(scope_signed_date)
        except ValueError:
            pass
    if anchor is None and scope_year:
        try:
            anchor = date(int(scope_year), 1, 1)
        except (ValueError, TypeError):
            pass
    if anchor is None:
        return ""
    offset_weeks = MILESTONE_WEEK_OFFSETS[milestone_idx]
    target = anchor + timedelta(weeks=offset_weeks)
    return target.strftime("%Y-%m")


def build_financial_project(project_row: dict, milestone_rows: list[dict]) -> dict:
    """
    Build a single project dict in financial-model.json format.
    project_row: dict from Projects sheet
    milestone_rows: list of dicts from Milestones sheet for this project
    """
    fee = float(project_row.get("estimated_fee_mxn") or 0)
    calc_amounts = calc_milestone_amounts(fee)
    calc_statuses = calc_milestone_statuses(
        project_row.get("current_phase", ""),
        project_row.get("status", ""),
    )

    milestones = []
    scope_signed_date = project_row.get("scope_signed_date", "")
    scope_year = project_row.get("scope_year", "")

    for idx, m in enumerate(milestone_rows):
        # Use sheet amount_mxn if set, otherwise calculated
        try:
            amount = int(float(m.get("amount_mxn") or calc_amounts[idx]))
        except (ValueError, TypeError):
            amount = int(calc_amounts[idx])

        # Use sheet estimated_date if set, otherwise derive
        est_date = m.get("estimated_date", "") or derive_milestone_date(scope_signed_date, scope_year, idx)

        milestones.append({
            "id": m["milestone_id"],
            "label": m["label"],
            "pct": int(m.get("pct") or 0),
            "amount_mxn": amount,
            "trigger": m["trigger"],
            "estimated_date": est_date,
            "status": calc_statuses[idx],
        })

    record = {
        "id": project_row["id"],
        "name": project_row.get("name", ""),
        "type": project_row.get("type", "residential"),
        "status": project_row.get("status", ""),
        "fy27": _parse_bool(project_row.get("fy27", "")),
        "tier": project_row.get("tier", ""),
        "estimated_fee_mxn": int(fee),
        "scope_year": _to_int(project_row.get("scope_year")),
        "delivery_year": _to_int(project_row.get("delivery_year")),
        "current_phase": project_row.get("current_phase", ""),
        "milestones": milestones,
    }
    if project_row.get("notes"):
        record["notes"] = project_row["notes"]
    return record


def build_timeline_project(project_row: dict) -> dict:
    """Build a single project dict in project-timelines.json format."""
    phases = {}

    def _phase(date_val: str, confidence: str = "medium", note: str = "") -> dict:
        return {"date": date_val, "confidence": confidence, "note": note}

    if project_row.get("scope_signed_date"):
        phases["scope_signed"] = _phase(project_row["scope_signed_date"])
    if project_row.get("delivery_date"):
        phases["delivery"] = _phase(project_row["delivery_date"])
    if project_row.get("construction_end_date"):
        phases["construction_end"] = _phase(project_row["construction_end_date"])
    if project_row.get("press_date"):
        phases["press"] = _phase(project_row["press_date"])

    record = {
        "id": project_row["id"],
        "name": project_row.get("name", ""),
        "number": project_row.get("number", ""),
        "type": project_row.get("type", "residential"),
        "status": project_row.get("status", ""),
        "fy27": _parse_bool(project_row.get("fy27", "")),
        "drive_id": project_row.get("drive_id") or None,
        "phases": phases,
        "notes": project_row.get("notes", ""),
    }
    if project_row.get("last_known_activity"):
        record["last_known_activity"] = project_row["last_known_activity"]
    return record


# ---------------------------------------------------------------------------
# Main sync function
# ---------------------------------------------------------------------------

def sync():
    from scripts.sheets_client import SheetsClient
    client = SheetsClient()

    # Read all sheets
    projects = client.read_sheet("Projects")
    milestones = client.read_sheet("Milestones")
    leads = client.read_sheet("Leads")
    invoices = client.read_sheet("Invoices")
    bank = client.read_sheet("Bank")
    campaigns = client.read_sheet("Campaigns")
    assets = client.read_sheet("Assets")

    print(f"→ Projects: {len(projects)} rows read")
    print(f"→ Milestones: {len(milestones)} rows read")
    print(f"→ Leads: {len(leads)} rows")
    print(f"→ Invoices: {len(invoices)} rows")
    print(f"→ Bank: {len(bank)} rows")
    print(f"→ Campaigns: {len(campaigns)} rows")
    print(f"→ Assets: {len(assets)} rows")

    # Group milestones by project_id
    milestone_map: dict[str, list] = {}
    for m in milestones:
        pid = m["project_id"]
        milestone_map.setdefault(pid, []).append(m)

    # Build and write financial-model.json
    financial_projects = []
    for proj in projects:
        proj_milestones = milestone_map.get(proj["id"], [])
        # Sort milestones M1→M4
        proj_milestones.sort(key=lambda m: int(m.get("milestone_id", "M0")[1:] or 0))
        financial_projects.append(build_financial_project(proj, proj_milestones))

    financial_output = {
        **FINANCIAL_STATIC,
        "_last_updated": date.today().isoformat(),
        "projects": financial_projects,
    }
    # Reorder keys to match original file order
    ordered_financial = {
        "_schema": financial_output["_schema"],
        "_last_updated": financial_output["_last_updated"],
        "_description": financial_output["_description"],
        "_data_disclaimer": financial_output["_data_disclaimer"],
        "assumptions": financial_output["assumptions"],
        "projects": financial_output["projects"],
    }
    with open(FINANCIAL_MODEL_PATH, "w", encoding="utf-8") as f:
        json.dump(ordered_financial, f, ensure_ascii=False, indent=2)
    print(f"→ data/financial-model.json written ({len(financial_projects)} projects)")

    # Build and write project-timelines.json
    timeline_projects = [build_timeline_project(proj) for proj in projects]
    timelines_output = {
        **TIMELINES_STATIC,
        "_last_updated": date.today().isoformat(),
        "projects": timeline_projects,
    }
    ordered_timelines = {
        "_schema": timelines_output["_schema"],
        "_last_updated": timelines_output["_last_updated"],
        "_data_sources": timelines_output["_data_sources"],
        "_confidence_notes": timelines_output["_confidence_notes"],
        "benchmarks": timelines_output["benchmarks"],
        "projects": timelines_output["projects"],
    }
    with open(TIMELINES_PATH, "w", encoding="utf-8") as f:
        json.dump(ordered_timelines, f, ensure_ascii=False, indent=2)
    print(f"→ data/project-timelines.json written ({len(timeline_projects)} projects)")

    print("Sync complete.")


if __name__ == "__main__":
    sync()
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
pytest tests/test_sheets_sync.py -v
```

Expected output:
```
tests/test_sheets_sync.py::test_calc_budget PASSED
tests/test_sheets_sync.py::test_calc_fee PASSED
tests/test_sheets_sync.py::test_calc_milestone_amounts PASSED
tests/test_sheets_sync.py::test_calc_milestone_amounts_zero PASSED
tests/test_sheets_sync.py::test_calc_milestone_status_built PASSED
tests/test_sheets_sync.py::test_calc_milestone_status_scope_signed PASSED
tests/test_sheets_sync.py::test_calc_milestone_status_anteproyecto PASSED
tests/test_sheets_sync.py::test_derive_milestone_date_from_scope_signed_date PASSED
tests/test_sheets_sync.py::test_derive_milestone_date_fallback_to_scope_year PASSED
tests/test_sheets_sync.py::test_derive_milestone_date_no_anchor_returns_empty PASSED
tests/test_sheets_sync.py::test_build_financial_project_record PASSED
11 passed
```

- [ ] **Step 5: Run the full test suite**

```bash
pytest tests/ -v
```

Expected: all 18 tests pass (7 client + 11 sync).

- [ ] **Step 6: Commit**

```bash
git add scripts/sheets_sync.py tests/test_sheets_sync.py
git commit -m "feat: add sheets_sync with cascade calculations and JSON output"
```

---

### Task 6: Integration verification

This task requires the manual Google Cloud setup to be complete (credentials.json and .env in place).

- [ ] **Step 1: Follow docs/setup/google-sheets-setup.md steps 1–8**

Complete all manual Google Cloud steps. Confirm:
- `credentials.json` exists at project root
- `.env` contains `GOOGLE_SHEETS_ID` and `GOOGLE_CREDENTIALS_PATH`

- [ ] **Step 2: Run setup script**

```bash
python scripts/setup_sheets.py
```

Expected:
```
→ Creating sheets...
→ Projects: created with 22 columns
→ Milestones: created with 9 columns
→ Leads: created with 11 columns
→ Invoices: created with 8 columns
→ Bank: created with 7 columns
→ Campaigns: created with 9 columns
→ Assets: created with 7 columns
→ Seeding data from existing JSON files...
→ Seeding Projects: 34 rows written
→ Seeding Milestones: 136 rows written
Setup complete.
```

If errors occur:
- `SpreadsheetNotFound`: `GOOGLE_SHEETS_ID` is wrong — re-copy from the URL between `/d/` and `/edit`
- `APIError 403`: service account does not have Editor access — re-share the spreadsheet with the service account email
- `FileNotFoundError` on `credentials.json`: `GOOGLE_CREDENTIALS_PATH` points to wrong location — check `.env`
- `EnvironmentError: GOOGLE_SHEETS_ID not set`: `.env` not loaded — confirm `.env` exists at project root

- [ ] **Step 3: Verify spreadsheet in browser**

Open the spreadsheet URL. Confirm:
- 7 sheet tabs visible
- Projects tab has 34 rows of data + 1 header row
- Milestones tab has 136 rows of data + 1 header row

- [ ] **Step 4: Run sync and verify JSON output**

```bash
# Back up originals
cp data/financial-model.json data/financial-model.json.bak
cp data/project-timelines.json data/project-timelines.json.bak

# Run sync
python scripts/sheets_sync.py
```

Expected output matches the sync command described in the spec.

- [ ] **Step 5: Spot-check JSON output**

```bash
python -c "
import json
with open('data/financial-model.json') as f:
    m = json.load(f)
print('Projects:', len(m['projects']))
print('First project:', m['projects'][0]['id'], m['projects'][0]['estimated_fee_mxn'])
print('Keys:', list(m.keys()))
"
```

Expected:
```
Projects: 34
First project: 35-santiago 925000
Keys: ['_schema', '_last_updated', '_description', '_data_disclaimer', 'assumptions', 'projects']
```

- [ ] **Step 6: Confirm dashboards still work**

Open http://127.0.0.1:8787/docs/plans/index.html → navigate to Financial Model and Timeline Dashboard. Both should display normally with data.

- [ ] **Step 7: Commit final state**

```bash
git add scripts/ tests/ requirements.txt .gitignore docs/setup/
git commit -m "feat: complete Google Sheets data layer — client, sync, setup, tests"
```
