---
name: resume-project
description: Resume a pipeline paused at a Marcela gate. Reads the latest Gmail reply on the review thread, dispatches Celia to process the decision, and routes to the next agent. Run manually after Marcela replies.
---

# Resume Project

Resume the pipeline for a project waiting for a Marcela gate decision.

## Usage

```
/resume-project [project_id]
```

Example:
```
/resume-project PRJ-2026-0316-carlos-mendoza
```

---

## Protocol

### Step 1: Load state

Read `projects/[project_id]/state.json`.

**Check preconditions:**
- If `project_state` ≠ `"awaiting_decision"`: report "Project [project_id] is not waiting for a decision. Current state: [project_state]" and stop.
- If `awaiting_gate` is null: report "No gate is pending for [project_id]" and stop.
- Determine thread to check:
  - Gates DG-04 and DG-05: use `architect_email_thread_id`
  - All other gates: use `review_thread_id`

### Step 2: Check for reply

```bash
python entrega/gmail_client.py read_latest_reply --thread "[thread_id]"
```

**If output is empty, null, or "None":**
Report: "No reply yet for [awaiting_gate] on project [project_id]. Check again after Marcela responds."
Stop. Do not dispatch Celia.

**If output contains a reply:**
Capture the reply text. Proceed.

### Step 3: Dispatch Celia

Dispatch Celia via the Agent tool with exactly this context:
- `project_id`: [project_id]
- `awaiting_gate`: [from state.json]
- `reply_text`: [the raw email reply text from Step 2]
- `state_summary`: project_type, client_name, and any relevant flags from state.json (feedback_type, revision_count)

Celia will:
1. Parse the decision
2. Write `decision-event.json`
3. Update `state.json` and Asana
4. Dispatch the correct next agent

---

## Notes

- This skill handles ALL Marcela gates (DG-01 through DG-11)
- DG-04 and DG-05 are architect email gates — they use `architect_email_thread_id` from state.json, not `review_thread_id`
- Multiple projects can be in `awaiting_decision` state simultaneously — run `/resume-project` separately for each
- There is no automatic polling in Phase 1. Run this skill after Marcela's email notification appears in your inbox.
- A future build will add a cron-based poller that auto-runs `/resume-project` for all pending projects
