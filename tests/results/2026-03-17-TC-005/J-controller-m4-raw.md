# Segment J — Controller — M4 Invoice

## Agent: Controller
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Milestone: M4 — Construction Documents Delivered
## final_milestone: false

---

Step 1: Read state.json, scope-of-work.json, project-schedule.json.
- M4: 25% × $180,000 = $45,000 USD
- due_date: 2027-01-27

Step 2: Previous invoice.json exists (M3) — running_total was $99,000
Copied invoice.json to invoice-previous.json as backup.
New running_total = $99,000 + $45,000 = $144,000

Step 3: Written invoice.json
- milestone_name: M4 — Construction Documents Delivered
- amount: $45,000 USD
- currency: USD
- running_total: $144,000
Deleted invoice-previous.json (write succeeded)

Step 4: ASANA_UNAVAILABLE: would update invoice task

Step 5: final_milestone = false — do NOT dispatch Tax. Stop.
