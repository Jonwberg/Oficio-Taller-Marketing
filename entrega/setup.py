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
    Writes custom_field_map.json with field name -> GID mappings.

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
        print(f"  + {cf['name']} ({gid})")

    # Write the GID map so asana_client.update_field() can use real custom fields
    with open(FIELD_MAP_PATH, "w", encoding="utf-8") as f:
        json.dump(field_map, f, indent=2)
    print(f"\n+ Wrote custom_field_map.json ({len(field_map)} fields)")

    # Create permanent projects
    for project_def in PERMANENT_PROJECTS:
        name = project_def["name"]
        sections = project_def["sections"]
        print(f"Creating project: {name}...")
        gid = asana.create_project(name, team_gid, sections, [])
        created[name] = gid
        print(f"  + Created {name} ({gid})")

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
