# Segment E — Vera — Activation Check

## Agent: Vera (mode: activation_check)
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Triggered by: Operator after contract signed + site docs + deposit confirmed

---

Step 1: Read state.json.
- contract_signed: true ✓
- site_docs_complete: true ✓
- deposit_confirmed: true ✓

Step 2a: All three conditions met → dispatch Pablo.

State updated: project_state = active_in_progress

ASANA_UNAVAILABLE: would complete activation_gate task
Dispatching Pablo for project schedule.
