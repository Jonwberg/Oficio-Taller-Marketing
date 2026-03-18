# Celia — DG-02 Decision Routing Output
**run_id:** 2026-03-16-TC-009
**tc_id:** TC-009
**segment:** B
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**agent:** Celia
**gate:** DG-02
**executed_at:** 2026-03-16T12:00:00-07:00

---

## Step 1: Parse Decision

Marcela reply (simulated per seed data `architect_response: "approve"`):
> "Approve"

Parsed decision: `approve`
Comment: null (no text after decision keyword)

---

## Step 2: decision-event-dg02.json Written

Written to: `projects/PRJ-2026-0316-familia-reyes-montoya/decision-event-dg02.json`

```json
{
  "project_id": "PRJ-2026-0316-familia-reyes-montoya",
  "phase": "DG-02",
  "review_item": "client-fit-assessment",
  "reviewed_by": "Marcela",
  "decision": "approve",
  "comment": null,
  "timestamp": "2026-03-16T12:00:00-07:00",
  "source_channel": "email",
  "next_action": "Dispatch Ana (area program + cost basis) and Sol (site readiness) in parallel",
  "route_to": "Ana, Sol",
  "sync_to_asana": true
}
```

---

## Step 3: state.json Update

- `awaiting_gate` → null
- `review_thread_id` → null
- `project_state` → `discovery_complete` (DG-02 approve routing)

---

## Step 4: Asana Update

ASANA_UNAVAILABLE: would update decision_status = approve for DG-02 on task ASANA_UNAVAILABLE

---

## Step 5: Routing

DG-02 approve → dispatch **Ana** AND **Sol** in parallel.

**Ana dispatched with:**
- project_id: PRJ-2026-0316-familia-reyes-montoya
- state.json content (discovery_complete, standalone_residential)
- lead-summary.json content
- Instruction: "Begin Segment C area program and cost basis for project PRJ-2026-0316-familia-reyes-montoya"

**Sol dispatched with:**
- project_id: PRJ-2026-0316-familia-reyes-montoya
- state.json content
- Site information from lead-summary.json: coastal Pacific-facing, Cerritos BCS, 3,000m², strong prevailing wind, salt air, coastal scrub to sand, flat to gently sloping
- Instruction: "Begin Segment C site readiness assessment for project PRJ-2026-0316-familia-reyes-montoya. Do NOT dispatch Tomás or any downstream agent when complete — set state.json site_data_complete flag only."

Both dispatched in same response message (parallel). Ana triggers DG-03 only after both area_program_complete AND site_data_complete flags are true.

---

## Fallbacks Logged

- ASANA_UNAVAILABLE: would update decision_status = approve for DG-02 (task: ASANA_UNAVAILABLE)

---

## Schema Validation

Required fields: project_id, phase, review_item, reviewed_by, decision, comment, timestamp, source_channel, next_action, route_to, sync_to_asana

- project_id: PRESENT — PRJ-2026-0316-familia-reyes-montoya
- phase: PRESENT — DG-02
- review_item: PRESENT — client-fit-assessment
- reviewed_by: PRESENT — Marcela
- decision: PRESENT — approve
- comment: PRESENT — null (acceptable; no comment provided)
- timestamp: PRESENT — ISO-8601 confirmed (2026-03-16T12:00:00-07:00)
- source_channel: PRESENT — email
- next_action: PRESENT — parallel dispatch of Ana and Sol
- route_to: PRESENT — Ana, Sol (correct field name route_to, not routed_to)
- sync_to_asana: PRESENT — true

Routing check: DG-02 approve → Ana + Sol in parallel — CORRECT per Celia routing table

**Schema: PASS**
