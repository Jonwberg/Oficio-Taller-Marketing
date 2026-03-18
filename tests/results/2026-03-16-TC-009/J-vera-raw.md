# Vera — Segment J: Construction Tracking
**run_id:** 2026-03-16-TC-009
**agent:** Vera
**mode:** construction_tracking
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**timestamp:** 2026-03-16

---

## Step 1: Read context

Read `projects/PRJ-2026-0316-familia-reyes-montoya/state.json`:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- project_state: bidding_in_progress
- client_name: Familia Reyes-Montoya
- tasks.construction: null
- tasks.invoice: null
- tasks.tax_filing: null

Read `projects/PRJ-2026-0316-familia-reyes-montoya/project-schedule.json`:
- phases: 6 phases total
- milestone_dates:
  - M1_contract_signing: 2026-03-16
  - M2_concept_approved: 2026-04-17
  - M3_executive_plans_approved: 2026-09-04
  - M4_permits_obtained: 2026-12-11
  - M5_construction_admin_final: 2027-06-30

Payment milestones per SOW (scope-of-work.json payment_schedule):
- M1 — Contract Signing: $36,000 USD (40%) — trigger: Signed SOW + first payment received
- M2 — Concept Design Approved: $27,000 USD (30%) — trigger: Client written approval of Phase 1 conceptual design
- M3 — Executive Plans Approved: $27,000 USD (30%) — trigger: Executive plans package approved by client

---

## Step 2: Initialize construction tracking

### Update state.json

Writing state update:
```json
{
  "project_state": "construction_in_progress"
}
```

state.json updated: `project_state` → `construction_in_progress`

### Update Asana

```bash
python entrega/asana_client.py update_field \
  --task_id null \
  --field project_state \
  --value construction_in_progress
```

**LOG: ASANA_UNAVAILABLE** — tasks.construction is null; Asana unavailable in test environment. Continuing per protocol.

```bash
python entrega/asana_client.py add_comment \
  --task_id null \
  --agent Vera \
  --body "Construction phase initialized. 3 payment milestone phases tracked per SOW. First milestone: M1 — Contract Signing — 2026-03-16."
```

**LOG: ASANA_UNAVAILABLE** — continuing.

---

## Step 3: Dispatch Controller — Milestone 1 (M1)

Milestone: M1 — Contract Signing
milestone_number: 1
final_milestone: false

M1 is not the final milestone. Dispatching Controller with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- milestone_name: "Contract Signed"
- milestone_number: 1
- final_milestone: false
- Instruction: "Generate invoice for milestone Contract Signed for project PRJ-2026-0316-familia-reyes-montoya."

**→ Controller dispatched for M1**

Log next milestone: M2 — Concept Design Approved — 2026-04-17.

---

## Step 4: Dispatch Controller — Milestone 2 (M2)
*(Re-dispatched after M1 Controller completes)*

Milestone: M2 — Concept Design Approved
milestone_number: 2
final_milestone: false

Dispatching Controller with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- milestone_name: "Concept Approved"
- milestone_number: 2
- final_milestone: false
- Instruction: "Generate invoice for milestone Concept Approved for project PRJ-2026-0316-familia-reyes-montoya."

**→ Controller dispatched for M2**

Log next milestone: M3 — Executive Plans Approved — 2026-09-04.

---

## Step 5: Dispatch Controller — Milestone 3 (M3)
*(Re-dispatched after M2 Controller completes)*

Milestone: M3 — Executive Plans Approved
milestone_number: 3
final_milestone: true

M3 IS the final milestone. Dispatching Controller with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- milestone_name: "Executive Plans Approved"
- milestone_number: 3
- final_milestone: true
- Instruction: "Generate invoice for milestone Executive Plans Approved for project PRJ-2026-0316-familia-reyes-montoya. This is the final milestone."

**NOTE (per TC-009 spec and Vera protocol): Vera does NOT dispatch Tax. Tax will be dispatched by Controller after the final invoice is written.**

**→ Controller dispatched for M3 (final_milestone: true)**

---

## Summary

| Action | Status |
|--------|--------|
| Read project-schedule.json | PASS |
| state.json updated: construction_in_progress | PASS |
| Asana update | ASANA_UNAVAILABLE (expected fallback) |
| Controller dispatched M1 | PASS |
| Controller dispatched M2 | PASS |
| Controller dispatched M3 (final) | PASS |
| Tax dispatched by Vera | NOT DONE — correct; Tax dispatched by Controller only |
