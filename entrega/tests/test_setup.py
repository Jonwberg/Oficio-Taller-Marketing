import json
import pytest
from unittest.mock import patch, MagicMock, call
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import setup as ws_setup


PERMANENT_PROJECTS = [
    "Leads",
    "Finanzas",
    "Legal",
    "Impuestos",
    "Handoffs",
    "Decisiones",
]


def test_dry_run_lists_all_six_projects(capsys):
    ws_setup.run(dry_run=True, team_gid="team_test")
    captured = capsys.readouterr()
    for project in PERMANENT_PROJECTS:
        assert project in captured.out


def test_dry_run_does_not_call_asana(monkeypatch):
    calls = []
    monkeypatch.setattr("setup.asana.create_project", lambda *a, **kw: calls.append(a) or "proj_001")
    ws_setup.run(dry_run=True, team_gid="team_test")
    assert len(calls) == 0, "dry_run should not call asana.create_project"


def test_run_creates_all_six_projects(monkeypatch, tmp_path):
    monkeypatch.setenv("ASANA_PAT", "test_token")
    monkeypatch.setattr("setup.FIELD_MAP_PATH", str(tmp_path / "custom_field_map.json"))
    monkeypatch.setattr("setup._get_workspace_gid", lambda t: "ws_test")
    monkeypatch.setattr("setup._create_custom_field", lambda n, t, w: f"gid_{n}")
    created = []
    monkeypatch.setattr(
        "setup.asana.create_project",
        lambda name, team, sections, fields: created.append(name) or f"proj_{name}"
    )
    ws_setup.run(dry_run=False, team_gid="team_test")
    for project in PERMANENT_PROJECTS:
        assert project in created


def test_leads_project_has_correct_sections(monkeypatch, tmp_path):
    monkeypatch.setenv("ASANA_PAT", "test_token")
    monkeypatch.setattr("setup.FIELD_MAP_PATH", str(tmp_path / "custom_field_map.json"))
    monkeypatch.setattr("setup._get_workspace_gid", lambda t: "ws_test")
    monkeypatch.setattr("setup._create_custom_field", lambda n, t, w: f"gid_{n}")
    section_map = {}
    def capture_project(name, team, sections, fields):
        section_map[name] = sections
        return f"proj_{name}"
    monkeypatch.setattr("setup.asana.create_project", capture_project)
    ws_setup.run(dry_run=False, team_gid="team_test")
    assert "New" in section_map["Leads"]
    assert "Qualified" in section_map["Leads"]
    assert "Discarded" in section_map["Leads"]


def test_decisiones_project_has_correct_sections(monkeypatch, tmp_path):
    monkeypatch.setenv("ASANA_PAT", "test_token")
    monkeypatch.setattr("setup.FIELD_MAP_PATH", str(tmp_path / "custom_field_map.json"))
    section_map = {}
    def capture_project(name, team, sections, fields):
        section_map[name] = sections
        return f"proj_{name}"
    monkeypatch.setattr("setup.asana.create_project", capture_project)
    monkeypatch.setattr("setup._get_workspace_gid", lambda t: "ws_test")
    monkeypatch.setattr("setup._create_custom_field", lambda n, t, w: f"gid_{n}")
    ws_setup.run(dry_run=False, team_gid="team_test")
    assert "Approve" in section_map["Decisiones"]


def test_run_writes_custom_field_map(monkeypatch, tmp_path):
    monkeypatch.setenv("ASANA_PAT", "test_token")
    map_path = tmp_path / "custom_field_map.json"
    monkeypatch.setattr("setup.FIELD_MAP_PATH", str(map_path))
    monkeypatch.setattr("setup._get_workspace_gid", lambda t: "ws_test")
    monkeypatch.setattr("setup._create_custom_field", lambda n, t, w: f"gid_{n}")
    monkeypatch.setattr("setup.asana.create_project", lambda *a, **kw: "proj_001")
    ws_setup.run(dry_run=False, team_gid="team_test")
    assert map_path.exists(), "custom_field_map.json must be written by setup.run()"
    field_map = json.loads(map_path.read_text())
    assert "project_state" in field_map
    assert "decision_status" in field_map
    assert field_map["project_state"] == "gid_project_state"


def test_dry_run_does_not_write_field_map(monkeypatch, tmp_path):
    map_path = tmp_path / "custom_field_map.json"
    monkeypatch.setattr("setup.FIELD_MAP_PATH", str(map_path))
    ws_setup.run(dry_run=True, team_gid="team_test")
    assert not map_path.exists(), "dry_run must not write custom_field_map.json"
