# Segment C — Ana — Area Program + Cost Basis

## Agent: Ana
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Triggered by: DG-02 Approve (parallel with Sol)

---

Step 1: Read state.json, lead-summary.json, client-fit-assessment.json.
- project_type: public_civic
- Program from seed data: 10 spaces, total 2,000m²
- Budget: $1.5M USD approved, $180,000 USD explicit architecture fee

Step 2: Written area-program.json
- 10 spaces (4 restrooms × 30m² = 120m²)
- Total: 2,000m² ✓

Step 3: Written cost-basis.json
- cost_per_sqm: MXN 28,500 (public_civic midpoint)
- base_construction_cost: MXN 57,000,000
- architecture_fee: MXN 6,840,000 (12%)
- engineering_allowance: MXN 1,710,000 (3%)
- contingency: 10%
- total_estimate: MXN 72,105,000
- Note: seed data provides explicit USD architecture fee ($180,000 USD) — used in SOW

Step 4: ASANA_UNAVAILABLE: would complete area program task

Step 5: Set area_program_complete = true
Checking site_data_complete — Sol still running (parallel track)
Wrote state.json with area_program_complete: true only.

STOP — waiting for Sol to complete before DG-03 trigger.
