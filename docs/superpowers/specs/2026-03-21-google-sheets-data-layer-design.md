# Google Sheets Data Layer — Design Spec
**Date:** 2026-03-21
**Project:** Oficio Taller — Studio Data Layer

---

## Goal

Replace hand-crafted JSON files with a Google Sheets workbook as the canonical source of truth for all studio data. Agents extract data from source documents and write rows to Sheets. A sync script pulls from Sheets, runs cascade calculations, and regenerates the JSON files that the existing dashboards already consume — with no changes to any dashboard.

---

## Architecture

```
Source documents (scope PDFs, invoices, bank statements, photos)
    ↓  agents extract → write rows via sheets_client.py
Google Sheets workbook: "Oficio Taller — Studio Data"
  ├── Projects      (master record per project)
  ├── Milestones    (payment schedule rows)
  ├── Leads         (inquiries and conversion tracking)
  ├── Campaigns     (campaign briefs, platforms, metrics)
  ├── Invoices      (billing records)
  ├── Bank          (bank statement rows, reconciliation)
  └── Assets        (photo inventory, Drive links)
         ↓  scripts/sheets_sync.py (on demand)
data/project-timelines.json    ← unchanged format
data/financial-model.json      ← unchanged format
         ↓
Studio OS dashboards (zero changes required)
```

**Credentials:** Google Cloud service account. Key stored as `credentials.json` (gitignored). Spreadsheet ID stored in `.env` as `GOOGLE_SHEETS_ID`.

---

## Workbook Schema

### Projects
One row per project. Raw inputs only — calculated fields are derived by `sheets_sync.py`.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `73-barra` |
| name | string | Project display name |
| type | string | `residential` \| `commercial` |
| tier | string | `small_residential` \| `mid_residential` \| `large_residential` \| `commercial` |
| area_m2 | number | Gross area in square metres |
| cost_per_m2 | number | Estimated construction cost per m² (MXN) |
| total_budget | number | **Calculated:** `area_m2 × cost_per_m2` |
| fee_pct | number | Architecture fee percentage (default: 12) |
| estimated_fee | number | **Calculated:** `total_budget × fee_pct / 100` |
| scope_year | number | Year scope was signed |
| delivery_year | number | Year delivered (null if in-process) |
| current_phase | string | `scope_signed` \| `conceptual` \| `anteproyecto` \| `ejecutivo` \| `complete` |
| status | string | `built` \| `in_process` |
| fy27 | boolean | TRUE if FY27 marketing priority |
| notes | string | Free text |

### Milestones
One row per payment milestone. Four rows per project (136 total for 34 projects).

| Column | Type | Notes |
|---|---|---|
| project_id | string | Foreign key → Projects.id |
| milestone_id | string | `M1` – `M4` |
| label | string | `Advance` \| `Conceptual` \| `Anteproyecto` \| `Ejecutivo` |
| pct | number | Payment percentage (30/20/20/30) |
| amount | number | **Calculated:** `estimated_fee × pct / 100` |
| trigger | string | `scope_signed` \| `conceptual` \| `anteproyecto` \| `ejecutivo` |
| estimated_date | string | `YYYY-MM` format |
| actual_date | string | `YYYY-MM` format (null until paid) |
| status | string | `collected` \| `projected` |

### Leads
One row per client inquiry.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `L-001` |
| date | string | `YYYY-MM-DD` |
| client_name | string | |
| email | string | |
| phone | string | |
| source | string | `instagram` \| `referral` \| `website` \| `direct` |
| project_type | string | `residential` \| `commercial` \| `other` |
| budget_range | string | e.g. `3M-5M` |
| status | string | `new` \| `contacted` \| `qualified` \| `converted` \| `lost` |
| notes | string | |
| converted_to_project_id | string | FK → Projects.id when converted |

### Invoices
One row per invoice issued.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `INV-001` |
| project_id | string | FK → Projects.id |
| invoice_number | string | Official invoice/folio number |
| date | string | `YYYY-MM-DD` |
| amount_mxn | number | Invoice amount |
| status | string | `issued` \| `paid` \| `overdue` \| `cancelled` |
| payment_date | string | `YYYY-MM-DD` (null until paid) |
| notes | string | |

### Bank
One row per bank statement line item.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `BNK-001` |
| date | string | `YYYY-MM-DD` |
| description | string | Bank description text |
| amount_mxn | number | Positive = credit, negative = debit |
| type | string | `credit` \| `debit` |
| category | string | `fee_payment` \| `expense` \| `tax` \| `transfer` \| `other` |
| matched_invoice_id | string | FK → Invoices.id (null if unmatched) |

### Campaigns
One row per marketing campaign.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `CAM-001` |
| name | string | Campaign display name |
| project_ids | string | Comma-separated project IDs |
| platforms | string | Comma-separated: `instagram,youtube,website` |
| start_date | string | `YYYY-MM-DD` |
| end_date | string | `YYYY-MM-DD` |
| status | string | `pending` \| `active` \| `complete` |
| reach | number | Total impressions/reach |
| inquiries_generated | number | Leads attributed to this campaign |

### Assets
One row per photo or video asset.

| Column | Type | Notes |
|---|---|---|
| id | string | e.g. `AST-001` |
| project_id | string | FK → Projects.id |
| filename | string | Original filename |
| drive_url | string | Google Drive share URL |
| asset_type | string | `photo` \| `video` \| `process_image` \| `drawing` |
| caption | string | Short description |
| used_in_campaigns | string | Comma-separated campaign IDs |

---

## Cascade Calculations

All calculations run in `scripts/sheets_sync.py`, not in Sheets. Sheets stores raw inputs only.

```
area_m2 × cost_per_m2                    → total_budget
total_budget × fee_pct / 100             → estimated_fee
estimated_fee × [0.30, 0.20, 0.20, 0.30] → milestone amounts (M1–M4)
current_phase → milestone statuses        → collected vs projected
scope_year + phase durations              → milestone estimated_dates (if not set)
```

Phase duration defaults (from existing assumptions):
- `estudios_previos`: 3 weeks
- `conceptual_anteproyecto`: 10 weeks
- `ejecutivo`: 12 weeks

---

## Files

| File | Action | Purpose |
|---|---|---|
| `scripts/sheets_client.py` | CREATE | Sheets API wrapper — read/write rows by tab name |
| `scripts/sheets_sync.py` | CREATE | Pull Sheets → calculate → write JSON files |
| `scripts/setup_sheets.py` | CREATE | One-time: create workbook, tabs, headers; seed from existing JSON |
| `credentials.json` | CREATE (gitignored) | Google service account key |
| `.env` | CREATE (gitignored) | `GOOGLE_SHEETS_ID=...` |
| `docs/setup/google-sheets-setup.md` | CREATE | Step-by-step Google Cloud setup instructions |
| `.gitignore` | MODIFY | Add `credentials.json` and `.env` |
| `data/project-timelines.json` | NO CHANGE | Still the format dashboards consume |
| `data/financial-model.json` | NO CHANGE | Still the format dashboards consume |
| All `docs/plans/*.html` | NO CHANGE | Dashboards unchanged |

---

## Google Cloud Setup (manual steps)

Documented in `docs/setup/google-sheets-setup.md`:

1. Create a Google Cloud project
2. Enable the Google Sheets API and Google Drive API
3. Create a service account, download `credentials.json`
4. Share the Sheets workbook with the service account email (Editor access)
5. Copy the workbook ID from the URL into `.env` as `GOOGLE_SHEETS_ID`

---

## Sync Command

```bash
python scripts/sheets_sync.py
# Output:
# → Projects: 34 rows read
# → Milestones: 136 rows read
# → Leads: N rows read
# → Invoices: N rows read
# → Bank: N rows read
# → Campaigns: N rows read
# → Assets: N rows read
# → Calculations complete
# → data/project-timelines.json written
# → data/financial-model.json written
# Sync complete.
```

---

## Agent Usage

```python
from scripts.sheets_client import SheetsClient

client = SheetsClient()

# Write a new lead
client.append_row("Leads", {
    "id": "L-042",
    "date": "2026-03-21",
    "client_name": "Ana García",
    "source": "instagram",
    "status": "new"
})

# Write an extracted invoice
client.append_row("Invoices", {
    "id": "INV-018",
    "project_id": "73-barra",
    "amount_mxn": 555000,
    "date": "2026-03-15",
    "status": "issued"
})

# Read all projects
projects = client.read_sheet("Projects")
```

---

## Migration

`scripts/setup_sheets.py` seeds the workbook with all 34 existing projects and their milestones from the current `data/financial-model.json` — preserving all existing data. After setup, `sheets_sync.py` becomes the only writer to the JSON files.

---

## Out of Scope

- No changes to any dashboard HTML file
- No database (SQLite, Postgres) — Sheets is the store
- No real-time sync — sync is on-demand via CLI command
- No authentication UI — service account only
