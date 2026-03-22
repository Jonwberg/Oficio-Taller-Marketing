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

# Static top-level content for financial-model.json — NOT stored in Sheets
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

# Static top-level content for project-timelines.json — NOT stored in Sheets
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

    for idx, m in enumerate(milestone_rows[:4]):
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
            "status": m.get("status") or calc_statuses[idx],
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
    }
    if project_row.get("last_known_activity"):
        record["last_known_activity"] = project_row["last_known_activity"]
    if project_row.get("notes"):
        record["notes"] = project_row["notes"]
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
        # Filter out rows with missing milestone_id, then sort M1→M4
        proj_milestones = [m for m in proj_milestones if m.get("milestone_id", "").startswith("M")]
        proj_milestones.sort(key=lambda m: int(m.get("milestone_id", "M0")[1:] or 0))
        financial_projects.append(build_financial_project(proj, proj_milestones))

    ordered_financial = {
        "_schema": FINANCIAL_STATIC["_schema"],
        "_last_updated": date.today().isoformat(),
        "_description": FINANCIAL_STATIC["_description"],
        "_data_disclaimer": FINANCIAL_STATIC["_data_disclaimer"],
        "assumptions": FINANCIAL_STATIC["assumptions"],
        "projects": financial_projects,
    }
    with open(FINANCIAL_MODEL_PATH, "w", encoding="utf-8") as f:
        json.dump(ordered_financial, f, ensure_ascii=False, indent=2)
    print(f"→ data/financial-model.json written ({len(financial_projects)} projects)")

    # Build and write project-timelines.json
    timeline_projects = [build_timeline_project(proj) for proj in projects]
    ordered_timelines = {
        "_schema": TIMELINES_STATIC["_schema"],
        "_last_updated": date.today().isoformat(),
        "_data_sources": TIMELINES_STATIC["_data_sources"],
        "_confidence_notes": TIMELINES_STATIC["_confidence_notes"],
        "benchmarks": TIMELINES_STATIC["benchmarks"],
        "projects": timeline_projects,
    }
    with open(TIMELINES_PATH, "w", encoding="utf-8") as f:
        json.dump(ordered_timelines, f, ensure_ascii=False, indent=2)
    print(f"→ data/project-timelines.json written ({len(timeline_projects)} projects)")

    print("Sync complete.")


if __name__ == "__main__":
    sync()
