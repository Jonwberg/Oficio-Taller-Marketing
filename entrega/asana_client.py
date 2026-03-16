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
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd == "create_task":
        project_gid, section, name, fields_json, tag = sys.argv[2:7]
        fields = json.loads(fields_json) if fields_json != "{}" else {}
        gid = create_task(project_gid, section, name, fields, tag)
        print(gid)

    elif cmd == "complete_task":
        task_gid = sys.argv[2]
        comment = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
        complete_task(task_gid, comment)
        print("ok")

    elif cmd == "update_field":
        task_gid, field_name, value = sys.argv[2], sys.argv[3], sys.argv[4]
        update_field(task_gid, field_name, value)
        print("ok")

    elif cmd == "add_comment":
        task_gid, agent_name = sys.argv[2], sys.argv[3]
        body = " ".join(sys.argv[4:])
        story_gid = add_comment(task_gid, agent_name, body)
        print(story_gid)

    elif cmd == "get_task":
        task_gid = sys.argv[2]
        import json as _json
        print(_json.dumps(get_task(task_gid)))

    elif cmd == "complete_task" and "--task_id" in sys.argv:
        # named arg form: python asana_client.py complete_task --task_id X --comment Y
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--task_id")
        parser.add_argument("--comment", default=None)
        args, _ = parser.parse_known_args(sys.argv[2:])
        complete_task(args.task_id, args.comment)
        print("ok")

    elif cmd == "create_subtask":
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--parent_id")
        parser.add_argument("--name")
        parser.add_argument("--fields", default="{}")
        args, _ = parser.parse_known_args(sys.argv[2:])
        fields = json.loads(args.fields)
        gid = create_subtask(args.parent_id, args.name, fields)
        print(gid)

    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
