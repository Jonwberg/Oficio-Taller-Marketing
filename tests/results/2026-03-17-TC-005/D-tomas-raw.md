# Segment D — Tomás — Scope of Work

## Agent: Tomás
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Triggered by: DG-03 Approve

---

Step 1: Read state.json, area-program.json, cost-basis.json.
- project_type: public_civic
- total_sqm: 2,000
- architecture_fee (seed data explicit): $180,000 USD

Step 2: Load SOW template.
Loaded: docs/templates/sow/sow-public-civic.md ✓

Step 3: Derive payment schedule amounts.
- Template: public_civic → 20/15/20/25/20
- Total architecture fee: $180,000 USD (from seed data)
- M1 Contract Signing: 20% × $180,000 = $36,000 USD
- M2 Concept Design Approved: 15% × $180,000 = $27,000 USD
- M3 Architectural Design Approved: 20% × $180,000 = $36,000 USD
- M4 Construction Documents Delivered: 25% × $180,000 = $45,000 USD
- M5 Construction Start Authorized: 20% × $180,000 = $36,000 USD

Step 4: Written scope-of-work.json
- 6 phases (Conceptual Design → Permitting; Phase 7 supervision NOT included — template says optional)
- Payment schedule: 20/15/20/25/20 ✓
- All 5 project_type_clauses from template verbatim: civic_procurement, public_bidding_compliance, government_approval_timeline, optional_supervision, esignature ✓
- Landscape + irrigation included by default per template ✓
- Solar included (in seed data special_features and program) ✓
- Phase 5 note: licitación pública managed by contracting entity; Oficio Taller prepares technical documents only ✓
- Permit process noted as expected to be longer than residential (public project) ✓

Step 5: ASANA_UNAVAILABLE: would complete scope_of_work task

Step 6: State updated: project_state = scope_sent_for_architect_review
Dispatching Vera (mode: architect_sow_review) for DG-04.
