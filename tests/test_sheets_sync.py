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
