# Segment J — Controller — M3 Invoice

## Agent: Controller
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Milestone: M3 — Architectural Design Approved
## final_milestone: false

---

Step 1: Read state.json, scope-of-work.json, project-schedule.json.
- M3: 20% × $180,000 = $36,000 USD
- due_date: 2026-09-09

Step 2: Previous invoice.json exists (M2) — running_total was $63,000
Copied invoice.json to invoice-previous.json as backup.
New running_total = $63,000 + $36,000 = $99,000

Step 3: Written invoice.json
- milestone_name: M3 — Architectural Design Approved
- amount: $36,000 USD
- currency: USD
- running_total: $99,000
Deleted invoice-previous.json (write succeeded)

Step 4: ASANA_UNAVAILABLE: would update invoice task

Step 5: final_milestone = false — do NOT dispatch Tax. Stop.
