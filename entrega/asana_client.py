"""
Asana REST API wrapper for Oficio Taller production agents.

All agents call these functions via Bash — no agent hits the API directly.
Reads ASANA_PAT from environment.
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
    """Create an Asana project and its sections. Returns project gid."""
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
    """
    field_map = _load_field_map()

    if field_name in field_map:
        payload = {"data": {"custom_fields": {field_map[field_name]: value}}}
        resp = requests.put(f"{ASANA_BASE}/tasks/{task_gid}", headers=_headers(), json=payload)
        resp.raise_for_status()
    else:
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


if __name__ == "__main__":
    import sys

    def _parse_args(argv):
        """Parse --key value pairs from argv, returning a dict."""
        kwargs = {}
        i = 0
        while i < len(argv):
            if argv[i].startswith("--"):
                key = argv[i][2:]
                value = argv[i + 1] if i + 1 < len(argv) else ""
                # Try to decode JSON for complex values (dicts, lists)
                try:
                    value = json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    pass
                kwargs[key] = value
                i += 2
            else:
                i += 1
        return kwargs

    if len(sys.argv) < 2:
        print("Usage: python asana_client.py <function_name> [--key value ...]")
        sys.exit(1)

    cmd = sys.argv[1]
    kwargs = _parse_args(sys.argv[2:])

    fn_map = {
        "create_project": create_project,
        "create_task": create_task,
        "complete_task": complete_task,
        "update_field": update_field,
        "get_field": get_field,
        "add_comment": add_comment,
        "get_task": get_task,
        "create_dependency": create_dependency,
        "create_subtask": create_subtask,
        "move_task": move_task,
    }

    if cmd not in fn_map:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

    result = fn_map[cmd](**kwargs)
    if result is not None:
        print(json.dumps(result) if isinstance(result, (dict, list)) else result)
