# Segment J — Controller — M2 Invoice

## Agent: Controller
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Milestone: M2 — Concept Design Approved
## final_milestone: false

---

Step 1: Read state.json, scope-of-work.json, project-schedule.json.
- M2: 15% × $180,000 = $27,000 USD
- due_date: 2026-05-20

Step 2: Previous invoice.json exists (M1) — running_total was $36,000
Copied invoice.json to invoice-previous.json as backup.
New running_total = $36,000 + $27,000 = $63,000

Step 3: Written invoice.json
- milestone_name: M2 — Concept Design Approved
- amount: $27,000 USD
- currency: USD
- running_total: $63,000
Deleted invoice-previous.json (write succeeded)

Step 4: ASANA_UNAVAILABLE: would update invoice task

Step 5: final_milestone = false — do NOT dispatch Tax. Stop.
