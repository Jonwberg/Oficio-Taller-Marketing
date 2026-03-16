# Production Agents — Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the three Python infrastructure modules (`asana_client.py`, `gmail_client.py`, `setup.py`) that all 20 production agents call via Bash — no agent hits an API directly.

**Architecture:** Three focused modules in `entrega/`. `asana_client.py` wraps Asana REST API using `requests`. `gmail_client.py` wraps Gmail API using `google-api-python-client`. `setup.py` is a one-time scaffold script that creates the Asana workspace structure. All modules read credentials from environment variables.

**Tech Stack:** Python 3.10+, requests, google-api-python-client, google-auth-oauthlib, pytest, pytest-mock

---

## File Structure

```
entrega/
  asana_client.py          ← Asana REST API wrapper (9 functions + get_field helper)
  gmail_client.py          ← Gmail API wrapper (6 functions)
  setup.py                 ← One-time Asana workspace scaffold; writes custom_field_map.json
  custom_field_map.json    ← Written by setup.py; maps field names to Asana GIDs
  requirements.txt         ← Python dependencies
  .env.example             ← Environment variable template
  tests/
    __init__.py
    test_asana_client.py   ← Unit tests for asana_client (mock HTTP)
    test_gmail_client.py   ← Unit tests for gmail_client (mock Gmail service)
    test_setup.py          ← Tests for setup dry-run output

projects/
  .gitkeep                 ← Empty directory tracked in git (agent outputs go here)
```

---

## Chunk 1: Project Setup + asana_client.py

### Task 1: Project Setup

**Files:**
- Create: `entrega/requirements.txt`
- Create: `entrega/.env.example`
- Create: `entrega/tests/__init__.py`
- Create: `projects/.gitkeep`

- [ ] **Step 1: Create `entrega/requirements.txt`**

```
requests==2.31.0
google-api-python-client==2.118.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
pytest==8.1.1
pytest-mock==3.14.0
requests-mock==1.11.0
```

- [ ] **Step 2: Create `entrega/.env.example`**

```
# Copy to .env and fill in values before running any entrega scripts
ASANA_PAT=your_asana_personal_access_token_here
GMAIL_CREDENTIALS_PATH=/absolute/path/to/gmail-credentials.json
MARCELA_EMAIL=marcela@oficiotaller.com
ARCHITECT_EMAIL=arquitecto@example.com
```

- [ ] **Step 3: Create empty test init and projects directory**

```bash
mkdir -p entrega/tests
touch entrega/tests/__init__.py
mkdir -p projects
touch projects/.gitkeep
```

- [ ] **Step 4: Install dependencies**

```bash
cd entrega && pip install -r requirements.txt
```

Expected: All packages install without error.

- [ ] **Step 5: Commit**

```bash
git add entrega/requirements.txt entrega/.env.example entrega/tests/__init__.py projects/.gitkeep
git commit -m "feat: add entrega infrastructure scaffold — requirements, env template, test init"
```

---

### Task 2: asana_client.py

**Files:**
- Create: `entrega/asana_client.py`
- Create: `entrega/tests/test_asana_client.py`

The Asana REST API base URL is `https://app.asana.com/api/1.0`. All requests use `Authorization: Bearer {ASANA_PAT}`. All responses return `{"data": {...}}`.

- [ ] **Step 1: Write the failing tests**

Create `entrega/tests/test_asana_client.py`:

```python
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
    gid = asana.create_project("Leads", "team_123", ["New", "Done"], [])
    assert gid == "proj_abc"

def test_create_project_sends_name_and_team(requests_mock):
    requests_mock.post(
        "https://app.asana.com/api/1.0/projects",
        json={"data": {"gid": "proj_abc"}}
    )
    asana.create_project("Leads", "team_123", ["New"], [])
    body = requests_mock.last_request.json()
    assert body["data"]["name"] == "Leads"
    assert body["data"]["team"] == "team_123"

# ── create_task ──────────────────────────────────────────────────────────────

def test_create_task_returns_gid(requests_mock):
    # First call: get sections for project
    requests_mock.get(
        "https://app.asana.com/api/1.0/projects/proj_abc/sections",
        json={"data": [{"gid": "sec_001", "name": "Lead Review"}]}
    )
    # Second call: create task in section
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
    # get_task call to read existing notes
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
```

- [ ] **Step 2: Install requests-mock and run tests to verify they fail**

```bash
cd entrega && pip install requests-mock && python -m pytest tests/test_asana_client.py -v 2>&1 | head -30
```

Expected: `ImportError: No module named 'asana_client'` or similar import error.

- [ ] **Step 3: Implement `entrega/asana_client.py`**

```python
"""
Asana REST API wrapper for Oficio Taller production agents.

All agents call these functions via Bash — no agent hits the API directly.
Reads ASANA_PAT from environment.

Usage from agent bash call:
    python entrega/asana_client.py create_task <project_gid> <section> <name> <fields_json> <tag>
"""

import os
import json
import sys
import requests

ASANA_BASE = "https://app.asana.com/api/1.0"


def _headers() -> dict:
    pat = os.environ.get("ASANA_PAT")
    if not pat:
        raise EnvironmentError("ASANA_PAT environment variable not set")
    return {
        "Authorization": f"Bearer {pat}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def create_project(name: str, team_gid: str, sections: list, custom_fields: list) -> str:
    """Create an Asana project and its sections. Returns project gid.

    custom_fields: list of dicts with keys "name", "type" (text|enum|number).
    GIDs for created custom fields are appended to CUSTOM_FIELD_MAP_PATH if set.
    """
    payload = {
        "data": {
            "name": name,
            "team": team_gid,
            "default_view": "list",
        }
    }
    resp = requests.post(f"{ASANA_BASE}/projects", headers=_headers(), json=payload)
    resp.raise_for_status()
    project_gid = resp.json()["data"]["gid"]

    for section_name in sections:
        _create_section(project_gid, section_name)

    return project_gid


def _create_section(project_gid: str, name: str) -> str:
    payload = {"data": {"name": name, "project": project_gid}}
    resp = requests.post(f"{ASANA_BASE}/sections", headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def _get_section_gid(project_gid: str, section_name: str) -> str | None:
    resp = requests.get(f"{ASANA_BASE}/projects/{project_gid}/sections", headers=_headers())
    resp.raise_for_status()
    for section in resp.json()["data"]:
        if section["name"] == section_name:
            return section["gid"]
    return None


def create_task(project_gid: str, section_name: str, name: str, fields: dict, tag: str) -> str:
    """Create a task in a project section. Returns task gid."""
    section_gid = _get_section_gid(project_gid, section_name)

    payload = {
        "data": {
            "name": name,
            "projects": [project_gid],
            "memberships": [{"project": project_gid, "section": section_gid}] if section_gid else [],
            "notes": f"Agent: {tag}\n\n" + json.dumps(fields, indent=2, ensure_ascii=False),
        }
    }
    if fields:
        payload["data"]["custom_fields"] = fields

    resp = requests.post(f"{ASANA_BASE}/tasks", headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def complete_task(task_gid: str, comment: str = None) -> None:
    """Mark a task complete and optionally add a closing comment."""
    payload = {"data": {"completed": True}}
    resp = requests.put(f"{ASANA_BASE}/tasks/{task_gid}", headers=_headers(), json=payload)
    resp.raise_for_status()

    if comment:
        add_comment(task_gid, "system", comment)


def move_task(task_gid: str, section_gid: str) -> None:
    """Move a task to a different section."""
    payload = {"data": {"section": section_gid}}
    resp = requests.post(f"{ASANA_BASE}/tasks/{task_gid}/addProject", headers=_headers(), json=payload)
    resp.raise_for_status()


CUSTOM_FIELD_MAP_PATH = os.path.join(os.path.dirname(__file__), "custom_field_map.json")


def _load_field_map() -> dict:
    """Load custom field name → GID map written by setup.py. Returns empty dict if not found."""
    if os.path.exists(CUSTOM_FIELD_MAP_PATH):
        with open(CUSTOM_FIELD_MAP_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def update_field(task_gid: str, field_name: str, value: str) -> None:
    """Update a custom field on a task by field name.

    Uses custom_field_map.json (written by setup.py) for actual GID-based updates.
    Falls back to notes-based storage as [CF:field_name] value if map not found.
    Use get_field() to read values back consistently regardless of storage method.
    """
    field_map = _load_field_map()

    if field_name in field_map:
        # Use real custom field GID
        payload = {"data": {"custom_fields": {field_map[field_name]: value}}}
        resp = requests.put(f"{ASANA_BASE}/tasks/{task_gid}", headers=_headers(), json=payload)
        resp.raise_for_status()
    else:
        # Notes fallback — used before setup.py has run
        task = get_task(task_gid)
        existing_notes = task.get("notes", "")
        marker = f"[CF:{field_name}]"
        new_entry = f"{marker} {value}"
        if marker in existing_notes:
            lines = existing_notes.split("\n")
            lines = [new_entry if marker in l else l for l in lines]
            updated_notes = "\n".join(lines)
        else:
            updated_notes = existing_notes + f"\n{new_entry}" if existing_notes else new_entry
        payload = {"data": {"notes": updated_notes}}
        resp = requests.put(f"{ASANA_BASE}/tasks/{task_gid}", headers=_headers(), json=payload)
        resp.raise_for_status()


def get_field(task: dict, field_name: str) -> str | None:
    """Read a custom field value from a task dict. Checks custom_fields then notes fallback."""
    field_map = _load_field_map()
    if field_name in field_map:
        gid = field_map[field_name]
        for cf in task.get("custom_fields", []):
            if cf.get("gid") == gid:
                return cf.get("text_value") or cf.get("enum_value", {}).get("name")
    # Notes fallback
    marker = f"[CF:{field_name}]"
    for line in task.get("notes", "").split("\n"):
        if marker in line:
            return line.replace(marker, "").strip()
    return None


def add_comment(task_gid: str, agent_name: str, body: str) -> str:
    """Add a comment to a task signed with the agent name. Returns story gid."""
    text = f"— {agent_name}\n\n{body}"
    payload = {"data": {"text": text}}
    resp = requests.post(f"{ASANA_BASE}/tasks/{task_gid}/stories", headers=_headers(), json=payload)
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def get_task(task_gid: str) -> dict:
    """Return task data dict."""
    resp = requests.get(f"{ASANA_BASE}/tasks/{task_gid}", headers=_headers())
    resp.raise_for_status()
    return resp.json()["data"]


def create_dependency(task_gid: str, depends_on_gid: str) -> None:
    """Make task_gid depend on depends_on_gid."""
    payload = {"data": {"dependencies": [depends_on_gid]}}
    resp = requests.post(
        f"{ASANA_BASE}/tasks/{task_gid}/addDependencies",
        headers=_headers(),
        json=payload
    )
    resp.raise_for_status()


def create_subtask(parent_gid: str, name: str, fields: dict) -> str:
    """Create a subtask under parent_gid. Returns subtask gid."""
    payload = {
        "data": {
            "name": name,
            "notes": json.dumps(fields, indent=2, ensure_ascii=False),
        }
    }
    resp = requests.post(
        f"{ASANA_BASE}/tasks/{parent_gid}/subtasks",
        headers=_headers(),
        json=payload
    )
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


# ── CLI interface for agents calling via Bash ────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "create_task":
        project_gid, section, name, fields_json, tag = sys.argv[2:7]
        fields = json.loads(fields_json) if fields_json != "{}" else {}
        gid = create_task(project_gid, section, name, fields, tag)
        print(gid)

    elif cmd == "complete_task":
        task_gid = sys.argv[2]
        comment = sys.argv[3] if len(sys.argv) > 3 else None
        complete_task(task_gid, comment)
        print("ok")

    elif cmd == "update_field":
        task_gid, field_name, value = sys.argv[2:5]
        update_field(task_gid, field_name, value)
        print("ok")

    elif cmd == "add_comment":
        task_gid, agent_name, body = sys.argv[2:5]
        story_gid = add_comment(task_gid, agent_name, body)
        print(story_gid)

    elif cmd == "get_task":
        task_gid = sys.argv[2]
        print(json.dumps(get_task(task_gid), indent=2, ensure_ascii=False))

    elif cmd == "create_subtask":
        parent_gid, name, fields_json = sys.argv[2:5]
        fields = json.loads(fields_json)
        gid = create_subtask(parent_gid, name, fields)
        print(gid)

    elif cmd == "create_project":
        name, team_gid, sections_json = sys.argv[2], sys.argv[3], sys.argv[4]
        sections = json.loads(sections_json)
        gid = create_project(name, team_gid, sections, [])
        print(gid)

    elif cmd == "move_task":
        task_gid, section_gid = sys.argv[2], sys.argv[3]
        move_task(task_gid, section_gid)
        print("ok")

    elif cmd == "create_dependency":
        task_gid, depends_on_gid = sys.argv[2], sys.argv[3]
        create_dependency(task_gid, depends_on_gid)
        print("ok")

    elif cmd == "get_field":
        task_gid, field_name = sys.argv[2], sys.argv[3]
        task = get_task(task_gid)
        value = get_field(task, field_name)
        print(value if value is not None else "NULL")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd entrega && python -m pytest tests/test_asana_client.py -v
```

Expected output:
```
test_asana_client.py::test_create_project_returns_gid PASSED
test_asana_client.py::test_create_project_sends_name_and_team PASSED
test_asana_client.py::test_create_task_returns_gid PASSED
test_asana_client.py::test_create_task_includes_tag PASSED
test_asana_client.py::test_complete_task_marks_done PASSED
test_asana_client.py::test_update_field_uses_notes_fallback_when_no_map PASSED
test_asana_client.py::test_update_field_uses_gid_when_map_exists PASSED
test_asana_client.py::test_get_field_reads_notes_fallback PASSED
test_asana_client.py::test_add_comment_includes_agent_signature PASSED
test_asana_client.py::test_get_task_returns_task_data PASSED
test_asana_client.py::test_create_dependency_posts_to_dependencies PASSED
test_asana_client.py::test_create_subtask_returns_gid PASSED
test_asana_client.py::test_move_task_posts_to_add_project PASSED

13 passed
```

- [ ] **Step 5: Commit**

```bash
git add entrega/asana_client.py entrega/tests/test_asana_client.py
git commit -m "feat: add asana_client.py with 9 API wrapper functions, get_field helper, and 13 passing tests"
```

---

## Chunk 2: gmail_client.py + setup.py

### Task 3: gmail_client.py

**Files:**
- Create: `entrega/gmail_client.py`
- Create: `entrega/tests/test_gmail_client.py`

Gmail API uses OAuth2. The credentials file (`GMAIL_CREDENTIALS_PATH`) is a service account or OAuth client credentials JSON. The module builds a `googleapiclient.discovery` service object and uses `users().messages()` endpoints.

- [ ] **Step 1: Write the failing tests**

Create `entrega/tests/test_gmail_client.py`:

```python
import base64
import pytest
from unittest.mock import patch, MagicMock, call
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import gmail_client as gmail


@pytest.fixture(autouse=True)
def set_env(monkeypatch, tmp_path):
    creds_file = tmp_path / "creds.json"
    creds_file.write_text('{"installed": {"client_id": "test"}}')
    monkeypatch.setenv("GMAIL_CREDENTIALS_PATH", str(creds_file))


def make_mock_service(thread_id="thread_abc", message_text="Approve"):
    """Build a mock Gmail service that returns predictable data."""
    service = MagicMock()

    # send returns a message with threadId
    service.users().messages().send().execute.return_value = {
        "id": "msg_001",
        "threadId": thread_id
    }

    # list returns messages for the thread
    encoded = base64.urlsafe_b64encode(message_text.encode()).decode()
    service.users().messages().list().execute.return_value = {
        "messages": [{"id": "msg_002", "threadId": thread_id}]
    }
    service.users().messages().get().execute.return_value = {
        "id": "msg_002",
        "threadId": thread_id,
        "payload": {
            "body": {"data": encoded}
        }
    }
    return service


# ── send_review_request ──────────────────────────────────────────────────────

def test_send_review_request_returns_thread_id():
    mock_service = make_mock_service(thread_id="thread_review_001")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        thread_id = gmail.send_review_request(
            to="marcela@oficiotaller.com",
            subject="DG-01: Lead Review — Casa Torres",
            body="Please approve or reject this lead."
        )
    assert thread_id == "thread_review_001"

def test_send_review_request_sends_to_correct_recipient():
    mock_service = make_mock_service()
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_review_request("marcela@oficiotaller.com", "Subject", "Body")
    call_args = mock_service.users().messages().send.call_args
    raw = base64.urlsafe_b64decode(call_args[1]["body"]["raw"] + "==").decode()
    assert "marcela@oficiotaller.com" in raw

# ── read_latest_reply ────────────────────────────────────────────────────────

def test_read_latest_reply_returns_message_text():
    mock_service = make_mock_service(message_text="Approve — looks good")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_latest_reply("thread_abc")
    assert text == "Approve — looks good"

def test_read_latest_reply_returns_none_when_no_messages():
    mock_service = make_mock_service()
    mock_service.users().messages().list().execute.return_value = {"messages": []}
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_latest_reply("thread_empty")
    assert text is None

# ── send_reminder ────────────────────────────────────────────────────────────

def test_send_reminder_replies_on_same_thread():
    mock_service = make_mock_service(thread_id="thread_abc")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_reminder("thread_abc", "marcela@oficiotaller.com", "24h reminder.")
    call_args = mock_service.users().messages().send.call_args
    body_dict = call_args[1]["body"]
    # Thread binding: message body must include threadId to reply on same thread
    assert body_dict.get("threadId") == "thread_abc"

# ── send_escalation ──────────────────────────────────────────────────────────

def test_send_escalation_sends_email():
    mock_service = make_mock_service()
    with patch.object(gmail, "_get_service", return_value=mock_service):
        gmail.send_escalation("thread_abc", "marcela@oficiotaller.com", "48h escalation.")
    assert mock_service.users().messages().send().execute.called

# ── send_client_email ────────────────────────────────────────────────────────

def test_send_client_email_returns_thread_id():
    mock_service = make_mock_service(thread_id="thread_client_001")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        thread_id = gmail.send_client_email(
            to="cliente@example.com",
            subject="Cuestionario de Descubrimiento",
            body="Buenos días, le enviamos el cuestionario."
        )
    assert thread_id == "thread_client_001"

# ── read_client_reply ────────────────────────────────────────────────────────

def test_read_client_reply_returns_text():
    mock_service = make_mock_service(message_text="Hola, adjunto los documentos.")
    with patch.object(gmail, "_get_service", return_value=mock_service):
        text = gmail.read_client_reply("thread_client_001")
    assert text == "Hola, adjunto los documentos."
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd entrega && python -m pytest tests/test_gmail_client.py -v 2>&1 | head -20
```

Expected: `ImportError: No module named 'gmail_client'`

- [ ] **Step 3: Implement `entrega/gmail_client.py`**

```python
"""
Gmail API wrapper for Oficio Taller production agents.

Handles all email operations: Marcela review gates and client-facing communications.
Reads GMAIL_CREDENTIALS_PATH from environment.

First-run OAuth: will open browser for consent. Session saved to token.json beside credentials.

Usage from agent bash call:
    python entrega/gmail_client.py send_review_request <to> <subject> <body>
    python entrega/gmail_client.py read_latest_reply <thread_id>
    python entrega/gmail_client.py send_client_email <to> <subject> <body>
    python entrega/gmail_client.py read_client_reply <thread_id>
"""

import os
import sys
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
SENDER = "me"


def _get_service():
    """Build and return authenticated Gmail service. Handles OAuth flow."""
    creds_path = os.environ.get("GMAIL_CREDENTIALS_PATH")
    if not creds_path:
        raise EnvironmentError("GMAIL_CREDENTIALS_PATH environment variable not set")

    creds_file = Path(creds_path)
    token_file = creds_file.parent / "token.json"

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            creds = flow.run_local_server(port=0)
        token_file.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def _build_message(to: str, subject: str, body: str, thread_id: str = None) -> dict:
    """Build a Gmail API message dict."""
    msg = MIMEMultipart("alternative")
    msg["To"] = to
    msg["From"] = SENDER
    msg["Subject"] = subject
    if thread_id:
        msg["In-Reply-To"] = thread_id
        msg["References"] = thread_id

    msg.attach(MIMEText(body, "plain", "utf-8"))

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = {"raw": raw}
    if thread_id:
        result["threadId"] = thread_id
    return result


def _decode_body(payload: dict) -> str:
    """Extract plain text body from a Gmail message payload."""
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"] + "==").decode("utf-8")

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data", "")
                if data:
                    return base64.urlsafe_b64decode(data + "==").decode("utf-8")
    return ""


def send_review_request(to: str, subject: str, body: str) -> str:
    """Send a new review request email to Marcela. Returns Gmail thread_id."""
    service = _get_service()
    message = _build_message(to, subject, body)
    result = service.users().messages().send(userId=SENDER, body=message).execute()
    return result["threadId"]


def read_latest_reply(thread_id: str) -> str | None:
    """
    Return the text of the latest reply in a thread, or None if no reply yet.

    Returns None when the thread has 0 or 1 messages (the original review request).
    A reply exists only when len(messages) >= 2.
    """
    service = _get_service()
    results = service.users().messages().list(
        userId=SENDER,
        q=f"threadId:{thread_id}"
    ).execute()

    messages = results.get("messages", [])
    if len(messages) < 2:
        # 0 messages: thread not found. 1 message: only the original send, no reply yet.
        return None

    # Get the latest message (last in list = most recent)
    latest_id = messages[-1]["id"]
    msg = service.users().messages().get(
        userId=SENDER, id=latest_id, format="full"
    ).execute()
    return _decode_body(msg["payload"]) or None


def send_reminder(thread_id: str, to: str, body: str) -> None:
    """Reply on the same thread at 24h with a reminder."""
    service = _get_service()
    subject = "Re: [Recordatorio] Revisión pendiente"
    message = _build_message(to, subject, body, thread_id=thread_id)
    service.users().messages().send(userId=SENDER, body=message).execute()


def send_escalation(thread_id: str, to: str, body: str) -> None:
    """Reply on the same thread at 48h with an escalation to Marcela."""
    service = _get_service()
    subject = "Re: [URGENTE] Revisión pendiente — 48h sin respuesta"
    message = _build_message(to, subject, body, thread_id=thread_id)
    service.users().messages().send(userId=SENDER, body=message).execute()


def send_client_email(to: str, subject: str, body: str) -> str:
    """Send a client-facing email (questionnaire, proposal, doc request). Returns thread_id."""
    service = _get_service()
    message = _build_message(to, subject, body)
    result = service.users().messages().send(userId=SENDER, body=message).execute()
    return result["threadId"]


def read_client_reply(thread_id: str) -> str | None:
    """Return latest client reply text, or None if no reply yet."""
    return read_latest_reply(thread_id)


# ── CLI interface for agents calling via Bash ────────────────────────────────

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "send_review_request":
        to, subject, body = sys.argv[2], sys.argv[3], sys.argv[4]
        thread_id = send_review_request(to, subject, body)
        print(thread_id)

    elif cmd == "read_latest_reply":
        thread_id = sys.argv[2]
        text = read_latest_reply(thread_id)
        print(text if text else "NO_REPLY")

    elif cmd == "send_reminder":
        thread_id, to, body = sys.argv[2], sys.argv[3], sys.argv[4]
        send_reminder(thread_id, to, body)
        print("ok")

    elif cmd == "send_escalation":
        thread_id, to, body = sys.argv[2], sys.argv[3], sys.argv[4]
        send_escalation(thread_id, to, body)
        print("ok")

    elif cmd == "send_client_email":
        to, subject, body = sys.argv[2], sys.argv[3], sys.argv[4]
        thread_id = send_client_email(to, subject, body)
        print(thread_id)

    elif cmd == "read_client_reply":
        thread_id = sys.argv[2]
        text = read_client_reply(thread_id)
        print(text if text else "NO_REPLY")

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd entrega && python -m pytest tests/test_gmail_client.py -v
```

Expected:
```
test_gmail_client.py::test_send_review_request_returns_thread_id PASSED
test_gmail_client.py::test_send_review_request_sends_to_correct_recipient PASSED
test_gmail_client.py::test_read_latest_reply_returns_message_text PASSED
test_gmail_client.py::test_read_latest_reply_returns_none_when_no_messages PASSED
test_gmail_client.py::test_send_reminder_replies_on_same_thread PASSED
test_gmail_client.py::test_send_escalation_sends_email PASSED
test_gmail_client.py::test_send_client_email_returns_thread_id PASSED
test_gmail_client.py::test_read_client_reply_returns_text PASSED

8 passed
```

- [ ] **Step 5: Commit**

```bash
git add entrega/gmail_client.py entrega/tests/test_gmail_client.py
git commit -m "feat: add gmail_client.py with 6 email functions and 8 passing tests"
```

---

### Task 4: setup.py

**Files:**
- Create: `entrega/setup.py`
- Create: `entrega/tests/test_setup.py`

`setup.py` creates the 6 permanent Asana projects with their sections and custom field schemas. It accepts `--dry-run` to print what it would create without making API calls.

- [ ] **Step 1: Write the failing tests**

Create `entrega/tests/test_setup.py`:

```python
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


def test_decisiones_project_has_correct_sections(monkeypatch):
    section_map = {}
    def capture_project(name, team, sections, fields):
        section_map[name] = sections
        return f"proj_{name}"
    monkeypatch.setattr("setup.asana.create_project", capture_project)
    monkeypatch.setattr("setup._get_workspace_gid", lambda t: "ws_test")
    monkeypatch.setattr("setup._create_custom_field", lambda n, t, w: f"gid_{n}")
    ws_setup.run(dry_run=False, team_gid="team_test")
    assert "Approve" in section_map["Decisiones"] or "Decisions" in section_map["Decisiones"]


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
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd entrega && python -m pytest tests/test_setup.py -v 2>&1 | head -20
```

Expected: `ImportError: No module named 'setup'`

- [ ] **Step 3: Implement `entrega/setup.py`**

```python
"""
One-time Asana workspace scaffold for Oficio Taller.

Run once before any production agents fire. Creates permanent projects,
sections, and custom field schemas. Writes custom_field_map.json mapping
field names to Asana GIDs — used by asana_client.update_field().

Usage:
    python entrega/setup.py --team=<team_gid>          # live run
    python entrega/setup.py --team=<team_gid> --dry-run # preview only

Find your team GID at: https://app.asana.com/api/1.0/teams?organization=<workspace_gid>
or from the URL when viewing a team in Asana.
"""

import sys
import json
import os
import argparse
import requests
import asana_client as asana

ASANA_BASE = "https://app.asana.com/api/1.0"
FIELD_MAP_PATH = os.path.join(os.path.dirname(__file__), "custom_field_map.json")

# Custom fields to create in the workspace (shared across all projects)
CUSTOM_FIELDS = [
    {"name": "project_state",    "type": "text"},
    {"name": "decision_status",  "type": "text"},
    {"name": "assigned_agent",   "type": "text"},
    {"name": "feedback_type",    "type": "text"},
    {"name": "revision_count",   "type": "number"},
    {"name": "client_fit_status","type": "text"},
    {"name": "deposit_status",   "type": "text"},
    {"name": "permit_status",    "type": "text"},
]

# ── Workspace definition ─────────────────────────────────────────────────────

PERMANENT_PROJECTS = [
    {
        "name": "Leads",
        "sections": ["New", "Reviewing", "Qualified", "Discarded"],
        "description": "All inbound leads from Lupe. Permanent record.",
    },
    {
        "name": "Finanzas",
        "sections": ["Pending", "In Review", "Approved", "Paid"],
        "description": "CFO, Controller, FP&A, Finance Ops tasks.",
    },
    {
        "name": "Legal",
        "sections": ["Pending Review", "In Review", "Approved", "Flagged"],
        "description": "All legal review tasks across all pods.",
    },
    {
        "name": "Impuestos",
        "sections": ["Upcoming", "In Progress", "Filed"],
        "description": "Tax obligations and filings.",
    },
    {
        "name": "Handoffs",
        "sections": ["Pending", "Completed"],
        "description": "Auto-created tasks at pipeline transition events.",
    },
    {
        "name": "Decisiones",
        "sections": ["Approve", "Reject", "Pass to Agent", "Archived"],
        "description": "Celia's normalized decision log. One task per human decision.",
    },
]


# ── Runner ───────────────────────────────────────────────────────────────────

def _create_custom_field(name: str, field_type: str, workspace_gid: str) -> str:
    """Create a workspace-level custom field. Returns GID."""
    headers = {
        "Authorization": f"Bearer {os.environ['ASANA_PAT']}",
        "Content-Type": "application/json",
    }
    payload = {
        "data": {
            "name": name,
            "resource_subtype": field_type,
            "workspace": workspace_gid,
        }
    }
    resp = requests.post(f"{ASANA_BASE}/custom_fields", headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()["data"]["gid"]


def _get_workspace_gid(team_gid: str) -> str:
    """Resolve workspace GID from team GID."""
    headers = {"Authorization": f"Bearer {os.environ['ASANA_PAT']}"}
    resp = requests.get(f"{ASANA_BASE}/teams/{team_gid}", headers=headers)
    resp.raise_for_status()
    return resp.json()["data"]["organization"]["gid"]


def run(dry_run: bool, team_gid: str) -> dict:
    """
    Create all permanent Asana projects and workspace custom fields.
    Writes custom_field_map.json with field name → GID mappings.

    Returns dict of {project_name: project_gid}.
    In dry_run mode, prints what would be created and returns empty dict.
    """
    created = {}

    if dry_run:
        for project_def in PERMANENT_PROJECTS:
            name = project_def["name"]
            sections = project_def["sections"]
            description = project_def.get("description", "")
            print(f"[DRY RUN] Would create project: {name}")
            print(f"          Sections: {', '.join(sections)}")
            print(f"          Description: {description}")
            print()
        print("[DRY RUN] Would create custom fields:")
        for cf in CUSTOM_FIELDS:
            print(f"          {cf['name']} ({cf['type']})")
        print(f"[DRY RUN] Would write: {FIELD_MAP_PATH}")
        return {}

    # Live run
    workspace_gid = _get_workspace_gid(team_gid)

    # Create custom fields and build the GID map
    field_map = {}
    for cf in CUSTOM_FIELDS:
        print(f"Creating custom field: {cf['name']}...")
        gid = _create_custom_field(cf["name"], cf["type"], workspace_gid)
        field_map[cf["name"]] = gid
        print(f"  ✓ {cf['name']} ({gid})")

    # Write the GID map so asana_client.update_field() can use real custom fields
    with open(FIELD_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(field_map, f, indent=2)
    print(f"\n✓ Wrote custom_field_map.json ({len(field_map)} fields)")

    # Create permanent projects
    for project_def in PERMANENT_PROJECTS:
        name = project_def["name"]
        sections = project_def["sections"]
        print(f"Creating project: {name}...")
        gid = asana.create_project(name, team_gid, sections, [])
        created[name] = gid
        print(f"  ✓ Created {name} ({gid})")

    print("\nWorkspace scaffold complete.")
    print("Save these project GIDs to your .env or a config file:")
    for name, gid in created.items():
        print(f"  ASANA_{name.upper()}_GID={gid}")

    return created


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold Oficio Taller Asana workspace")
    parser.add_argument("--team", required=True, help="Asana team GID")
    parser.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = parser.parse_args()

    run(dry_run=args.dry_run, team_gid=args.team)
```

- [ ] **Step 4: Run tests and verify they pass**

```bash
cd entrega && python -m pytest tests/test_setup.py -v
```

Expected:
```
test_setup.py::test_dry_run_lists_all_six_projects PASSED
test_setup.py::test_dry_run_does_not_call_asana PASSED
test_setup.py::test_run_creates_all_six_projects PASSED
test_setup.py::test_leads_project_has_correct_sections PASSED
test_setup.py::test_decisiones_project_has_correct_sections PASSED
test_setup.py::test_run_writes_custom_field_map PASSED
test_setup.py::test_dry_run_does_not_write_field_map PASSED

7 passed
```

- [ ] **Step 5: Commit**

```bash
git add entrega/setup.py entrega/tests/test_setup.py
git commit -m "feat: add setup.py for one-time Asana workspace scaffold with dry-run support"
```

---

## Chunk 3: Full Test Run + Verification

### Task 5: Full test suite + state.json template

**Files:**
- Create: `entrega/state_template.json`
- Modify: `entrega/tests/` — run all tests together

- [ ] **Step 1: Create `entrega/state_template.json`**

This is the template every agent copies when initializing a new project.

```json
{
  "project_id": "",
  "project_state": "lead_received",
  "awaiting_gate": null,
  "review_thread_id": null,
  "architect_email_thread_id": null,
  "asana_project_id": null,
  "client_name": "",
  "client_email": "",
  "project_type": "standalone_residential",
  "area_program_complete": false,
  "site_data_complete": false,
  "revision_count": 0,
  "feedback_type": null,
  "contract_signed": false,
  "site_docs_complete": false,
  "deposit_confirmed": false,
  "tasks": {
    "lead_intake": null,
    "lead_review_gate": null,
    "discovery": null,
    "fit_gate": null,
    "area_program": null,
    "site_readiness": null,
    "cost_basis_gate": null,
    "scope_of_work": null,
    "sow_architect_gate": null,
    "budget": null,
    "proposal": null,
    "legal_review": null,
    "proposal_architect_gate": null,
    "client_proposal": null,
    "activation_gate": null,
    "schedule": null,
    "concept": null,
    "concept_gate": null,
    "architectural_design": null,
    "design_gate": null,
    "engineering": null,
    "budget_alignment": null,
    "budget_alignment_gate": null,
    "executive_plans": null,
    "final_approval_gate": null,
    "bidding": null,
    "contractor_selection_gate": null,
    "permitting": null,
    "construction": null,
    "invoice": null,
    "tax_filing": null
  }
}
```

- [ ] **Step 2: Run complete test suite**

```bash
cd entrega && python -m pytest tests/ -v
```

Expected:
```
tests/test_asana_client.py::test_create_project_returns_gid PASSED
tests/test_asana_client.py::test_create_project_sends_name_and_team PASSED
tests/test_asana_client.py::test_create_task_returns_gid PASSED
tests/test_asana_client.py::test_create_task_includes_tag PASSED
tests/test_asana_client.py::test_complete_task_marks_done PASSED
tests/test_asana_client.py::test_update_field_uses_notes_fallback_when_no_map PASSED
tests/test_asana_client.py::test_update_field_uses_gid_when_map_exists PASSED
tests/test_asana_client.py::test_get_field_reads_notes_fallback PASSED
tests/test_asana_client.py::test_add_comment_includes_agent_signature PASSED
tests/test_asana_client.py::test_get_task_returns_task_data PASSED
tests/test_asana_client.py::test_create_dependency_posts_to_dependencies PASSED
tests/test_asana_client.py::test_create_subtask_returns_gid PASSED
tests/test_asana_client.py::test_move_task_posts_to_add_project PASSED
tests/test_gmail_client.py::test_send_review_request_returns_thread_id PASSED
tests/test_gmail_client.py::test_send_review_request_sends_to_correct_recipient PASSED
tests/test_gmail_client.py::test_read_latest_reply_returns_message_text PASSED
tests/test_gmail_client.py::test_read_latest_reply_returns_none_when_no_messages PASSED
tests/test_gmail_client.py::test_send_reminder_replies_on_same_thread PASSED
tests/test_gmail_client.py::test_send_escalation_sends_email PASSED
tests/test_gmail_client.py::test_send_client_email_returns_thread_id PASSED
tests/test_gmail_client.py::test_read_client_reply_returns_text PASSED
tests/test_setup.py::test_dry_run_lists_all_six_projects PASSED
tests/test_setup.py::test_dry_run_does_not_call_asana PASSED
tests/test_setup.py::test_run_creates_all_six_projects PASSED
tests/test_setup.py::test_leads_project_has_correct_sections PASSED
tests/test_setup.py::test_decisiones_project_has_correct_sections PASSED
tests/test_setup.py::test_run_writes_custom_field_map PASSED
tests/test_setup.py::test_dry_run_does_not_write_field_map PASSED

28 passed
```

- [ ] **Step 3: Verify setup.py dry-run**

```bash
cd entrega && ASANA_PAT=test python setup.py --team=fake_team_gid --dry-run
```

Expected:
```
[DRY RUN] Would create project: Leads
          Sections: New, Reviewing, Qualified, Discarded
          Description: All inbound leads from Lupe. Permanent record.

[DRY RUN] Would create project: Finanzas
...
[DRY RUN] Would create project: Decisiones
          Sections: Approve, Reject, Pass to Agent, Archived
```

- [ ] **Step 4: Final commit**

```bash
git add entrega/state_template.json
git commit -m "feat: add state_template.json — complete project state schema for all 31 pipeline tasks"
git push origin master
```

---

## Definition of Done

- [ ] `python -m pytest entrega/tests/ -v` → 28 passed, 0 failed
- [ ] `python entrega/setup.py --team=fake --dry-run` → lists all 6 projects
- [ ] `entrega/state_template.json` exists with all 31 task slots
- [ ] All files committed and pushed to origin
