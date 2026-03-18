# Celia — DG-11 Decision Routing
**Agent:** Celia
**Project:** PRJ-2026-0316-familia-reyes-montoya
**Gate:** DG-11
**Run:** 2026-03-16-TC-009

---

## Step 1: Input Context

**Gate:** DG-11
**Marcela's raw reply:**
> "Approve"

**state.json at time of receipt:**
- project_state: awaiting_decision
- awaiting_gate: DG-11
- review_thread_id: THREAD-DG11-PRJ-2026-0316

---

## Step 2: Parse Decision

Reply text: "Approve"
Decision: `approve`
Comment: null (no text after keyword)

---

## Step 3: Write decision-event.json

All 11 fields present. Field name: `route_to` (correct — not `routed_to`).

```json
{
  "project_id": "PRJ-2026-0316-familia-reyes-montoya",
  "phase": "DG-11",
  "review_item": "bid-comparison",
  "reviewed_by": "Marcela",
  "decision": "approve",
  "comment": null,
  "timestamp": "2026-03-16T11:45:00-07:00",
  "source_channel": "email",
  "next_action": "dispatch_paco",
  "route_to": "Paco",
  "sync_to_asana": true
}
```

Written to: `projects/PRJ-2026-0316-familia-reyes-montoya/decision-event.json`

---

## Step 4: Update state.json

Per DG-11 approve routing table:
- project_state → `contractor_selected`
- awaiting_gate → `null`
- review_thread_id → `null`

state.json updated:
```json
{
  "project_state": "contractor_selected",
  "awaiting_gate": null,
  "review_thread_id": null
}
```

---

## Step 5: Asana Update

Gate-to-task-key: DG-11 → tasks.contractor_selection_gate (null)

```bash
python entrega/asana_client.py update_field \
  --task_id null \
  --field decision_status \
  --value approve
```

tasks.contractor_selection_gate is null — ASANA_UNAVAILABLE context.
Logging: ASANA_UNAVAILABLE: would update decision_status → approve for DG-11 (tasks.contractor_selection_gate).

---

## Step 6: Route to Next Agent

DG-11 Approve → dispatch **Paco**

Dispatching Paco with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- context: bid-comparison.json approved; contractor selected: Constructora del Pacífico, S.A. de C.V.
- Instruction: "Submit coastal zone permit application for project PRJ-2026-0316-familia-reyes-montoya. Jurisdiction: Municipio de Los Cabos / SEMARNAT coastal zone. Read bid-comparison.json to note the selected contractor. TC-009 edge: permit may cycle through pending_corrections before approval."

---

## Celia DG-11 Complete

route_to: Paco
decision: approve
project_state advanced to: contractor_selected
