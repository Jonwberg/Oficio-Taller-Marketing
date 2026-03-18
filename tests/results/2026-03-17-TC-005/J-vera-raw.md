# Segment J — Vera — Construction Tracking

## Agent: Vera (mode: construction_tracking)
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Triggered by: Paco (permit approved)

---

Step 1: Read project-schedule.json.
- 6 phases total; construction milestones M1–M5
- M1 already processed at contract signing
- Initialize construction tracking for milestone invoicing

State updated: project_state = construction_in_progress
ASANA_UNAVAILABLE: would update construction task to construction_in_progress

Step 2: Process construction milestones per operator dispatch.

Dispatching Controller for each milestone (M1 through M5 per schedule):

M1 — Contract Signing ($36,000 / 20%) — final_milestone: false
M2 — Concept Design Approved ($27,000 / 15%) — final_milestone: false
M3 — Architectural Design Approved ($36,000 / 20%) — final_milestone: false
M4 — Construction Documents Delivered ($45,000 / 25%) — final_milestone: false
M5 — Construction Start Authorized ($36,000 / 20%) — final_milestone: TRUE

At M5: Controller dispatches Tax (NOT Vera — Controller dispatches Tax per protocol).
