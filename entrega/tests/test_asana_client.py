import json
import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import asana_client as asana

# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ASANA_PAT", "test_token_123")

def mock_response(data, status=200):
    m = MagicMock()
    m.status_code = status
    m.json.return_value = {"data": data}
    m.raise_for_status = MagicMock()
    return m

# ── create_project ───────────────────────────────────────────────────────────

def test_create_project_returns_gid(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/projects",
        json={"data": {"gid": "proj_abc", "name": "Leads"}}
    )
    requests_mock.post(
        "https://app.asana.com/api/1.0/sections",
        json={"data": {"gid": "sec_001"}}
    )
    gid = asana.create_project("Leads", "team_123", ["New", "Done"], [])
    assert gid == "proj_abc"

def test_create_project_sends_name_and_team(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/projects",
        json={"data": {"gid": "proj_abc"}}
    )
    requests_mock.post(
        "https://app.asana.com/api/1.0/sections",
        json={"data": {"gid": "sec_001"}}
    )
    asana.create_project("Leads", "team_123", ["New"], [])
    history = requests_mock.request_history
    projects_req = next(r for r in history if "/projects" in r.url)
    body = projects_req.json()
    assert body["data"]["name"] == "Leads"
    assert body["data"]["team"] == "team_123"

# ── create_task ──────────────────────────────────────────────────────────────

def test_create_task_returns_gid(requests_mock):
    requests_mock.get(
        "https://app.asana.com/api/1.0/projects/proj_abc/sections",
        json={"data": [{"gid": "sec_001", "name": "Lead Review"}]}
    )
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks",
        json={"data": {"gid": "task_xyz"}}
    )
    gid = asana.create_task("proj_abc", "Lead Review", "Review inbound lead", {}, "Lupe")
    assert gid == "task_xyz"

def test_create_task_includes_tag(requests_mock):
    requests_mock.get(
        "https://app.asana.com/api/1.0/projects/proj_abc/sections",
        json={"data": [{"gid": "sec_001", "name": "Lead Review"}]}
    )
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks",
        json={"data": {"gid": "task_xyz"}}
    )
    asana.create_task("proj_abc", "Lead Review", "Review lead", {}, "Lupe")
    body = requests_mock.last_request.json()
    assert body["data"]["name"] == "Review lead"

# ── complete_task ────────────────────────────────────────────────────────────

def test_complete_task_marks_done(requests_mock):
    requests_mock.put(
        "https://app.asana.com/api/1.0/tasks/task_xyz",
        json={"data": {"gid": "task_xyz", "completed": True}}
    )
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks/task_xyz/stories",
        json={"data": {"gid": "story_001"}}
    )
    asana.complete_task("task_xyz", comment="Lead archived.")
    body = requests_mock.request_history[0].json()
    assert body["data"]["completed"] is True

# ── update_field + get_field ──────────────────────────────────────────────────

def test_update_field_uses_notes_fallback_when_no_map(requests_mock, tmp_path, monkeypatch):
    """When custom_field_map.json doesn't exist, stores value in notes as [CF:name] value."""
    monkeypatch.setattr(asana, "CUSTOM_FIELD_MAP_PATH", str(tmp_path / "nonexistent.json"))
    requests_mock.get(
        "https://app.asana.com/api/1.0/tasks/task_xyz",
        json={"data": {"gid": "task_xyz", "notes": "", "custom_fields": []}}
    )
    requests_mock.put(
        "https://app.asana.com/api/1.0/tasks/task_xyz",
        json={"data": {"gid": "task_xyz"}}
    )
    asana.update_field("task_xyz", "decision_status", "awaiting")
    body = requests_mock.last_request.json()
    assert "[CF:decision_status] awaiting" in body["data"]["notes"]


def test_update_field_uses_gid_when_map_exists(requests_mock, tmp_path, monkeypatch):
    """When custom_field_map.json exists, uses actual custom field GID."""
    map_file = tmp_path / "custom_field_map.json"
    map_file.write_text('{"decision_status": "gid_12345"}')
    monkeypatch.setattr(asana, "CUSTOM_FIELD_MAP_PATH", str(map_file))
    requests_mock.put(
        "https://app.asana.com/api/1.0/tasks/task_xyz",
        json={"data": {"gid": "task_xyz"}}
    )
    asana.update_field("task_xyz", "decision_status", "awaiting")
    body = requests_mock.last_request.json()
    assert body["data"]["custom_fields"]["gid_12345"] == "awaiting"


def test_get_field_reads_notes_fallback(tmp_path, monkeypatch):
    """get_field can read values stored via notes fallback."""
    monkeypatch.setattr(asana, "CUSTOM_FIELD_MAP_PATH", str(tmp_path / "nonexistent.json"))
    task = {"notes": "[CF:decision_status] awaiting\n[CF:project_state] lead_received", "custom_fields": []}
    assert asana.get_field(task, "decision_status") == "awaiting"
    assert asana.get_field(task, "project_state") == "lead_received"
    assert asana.get_field(task, "missing_field") is None

# ── add_comment ──────────────────────────────────────────────────────────────

def test_add_comment_includes_agent_signature(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks/task_xyz/stories",
        json={"data": {"gid": "story_001"}}
    )
    asana.add_comment("task_xyz", "Lupe", "Lead classified as spam.")
    body = requests_mock.last_request.json()
    assert "Lupe" in body["data"]["text"]
    assert "Lead classified as spam." in body["data"]["text"]

# ── get_task ─────────────────────────────────────────────────────────────────

def test_get_task_returns_task_data(requests_mock):
    requests_mock.get(
        "https://app.asana.com/api/1.0/tasks/task_xyz",
        json={"data": {"gid": "task_xyz", "name": "Review lead", "completed": False}}
    )
    task = asana.get_task("task_xyz")
    assert task["gid"] == "task_xyz"
    assert task["completed"] is False

# ── create_dependency ────────────────────────────────────────────────────────

def test_create_dependency_posts_to_dependencies(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks/task_xyz/addDependencies",
        json={"data": {}}
    )
    asana.create_dependency("task_xyz", "task_abc")
    body = requests_mock.last_request.json()
    assert "task_abc" in str(body)

# ── create_subtask ───────────────────────────────────────────────────────────

def test_create_subtask_returns_gid(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks/parent_xyz/subtasks",
        json={"data": {"gid": "subtask_001"}}
    )
    gid = asana.create_subtask("parent_xyz", "Phase 1 milestone", {"due_on": "2026-04-01"})
    assert gid == "subtask_001"

# ── move_task ────────────────────────────────────────────────────────────────

def test_move_task_posts_to_add_project(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/tasks/task_xyz/addProject",
        json={"data": {}}
    )
    asana.move_task("task_xyz", "sec_new")
    body = requests_mock.last_request.json()
    assert body["data"]["section"] == "sec_new"
