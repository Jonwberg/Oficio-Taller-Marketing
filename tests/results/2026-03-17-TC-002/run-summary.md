# TC-002 Run Summary
**Run ID:** 2026-03-17-TC-002
**Test Case:** Casa Vista — residential_in_development with HOA
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `project_closed` ✅
**Scored:** 2026-03-17 by Test Decision Gate + Gap Analysis Agent

---

## Segment Results

| Segment | Agents | Result |
|---------|--------|--------|
| A | Lupe | ✅ PASS |
| B | Lupe, Celia, Elena, Celia | ✅ PASS |
| C | Ana, Sol, Vera, Celia | ⚠️ PASS (1 Celia routing gap — DG-03) |
| D | Tomás, Vera, Bruno, Renata, Legal, Vera, Rosa, Celia | ✅ PASS |
| E | Vera, Pablo | ✅ PASS |
| F | Andrés, Celia, Felipe, Celia | ✅ PASS |
| G | Emilio, Bruno, Celia | ✅ PASS |
| H | Hugo, Celia | ✅ PASS |
| I | Ofelia, Celia, Paco | ✅ PASS |
| J | Vera, Controller ×3, Tax | ✅ PASS |

**Overall: 10/10 segments PASS (1 routing gap identified in Segment C Celia DG-03)**

---

## Scored Deliverable Table

| Segment | Deliverable | Agent | Avg Score | Passed |
|---------|-------------|-------|-----------|--------|
| A | lead-record | Lupe | 4.33 | PASS |
| B | lead-summary | Lupe | 4.67 | PASS |
| B | discovery-questionnaire | Elena | 4.57 | PASS |
| B | client-fit-assessment | Elena | 4.67 | PASS |
| B | Celia DG-01 | Celia | 4.17 | PASS |
| B | Celia DG-02 | Celia | 3.83 | PASS |
| C | area-program | Ana | 4.67 | PASS |
| C | cost-basis | Ana | 4.50 | PASS |
| C | site-readiness-report | Sol | 4.50 | PASS |
| C | Celia DG-03 | Celia | 3.33 | **FAIL** |
| D | scope-of-work | Tomás | 4.67 | PASS |
| D | budget | Bruno | 4.00 | PASS |
| D | proposal | Renata | 4.67 | PASS |
| D | legal-review | Legal | 4.67 | PASS |
| D | client-communication | Rosa | 4.75 | PASS |
| D | Celia DG-06 | Celia | 4.17 | PASS |
| E | project-schedule | Pablo | 4.40 | PASS |
| F | concept-review | Andrés | 4.33 | PASS |
| F | architectural-design | Felipe | 4.67 | PASS |
| F | Celia DG-07 | Celia | 4.17 | PASS |
| F | Celia DG-08 | Celia | 4.17 | PASS |
| G | engineering-package | Emilio | 4.67 | PASS |
| G | budget-alignment | Bruno | 4.67 | PASS |
| G | Celia DG-09 | Celia | 4.17 | PASS |
| H | executive-plans | Hugo | 4.50 | PASS |
| H | Celia DG-10 | Celia | 4.17 | PASS |
| I | bid-comparison | Ofelia | 4.67 | PASS |
| I | permit-status | Paco | 4.60 | PASS |
| I | Celia DG-11 | Celia | 4.67 | PASS |
| J | invoice | Controller | 4.20 | PASS |
| J | tax-filing | Tax | 4.00 | PASS |

**Overall average score: 4.37 / 5.00**
**Scorecards written: 31**
**Auto-fails: 0**
**PASS: 30 / 31 | FAIL: 1 / 31**

---

## Key Verification Points

| Check | Result |
|-------|--------|
| residential_in_development SOW template applied | ✅ PASS |
| HOA coordination clause in SOW | ✅ PASS |
| Covenant review clause in SOW | ✅ PASS |
| Area program notes 7m height limit | ✅ PASS |
| All Celia payloads use route_to (not routed_to) | ✅ PASS |
| Final state: project_closed | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-002/`

---

## Decision Gate Summary

| Gate | Decision | Route To | Notes |
|------|----------|----------|-------|
| DG-01 | approve | Lupe (Segment B) | Lead reviewed and approved |
| DG-02 | approve | Ana + Sol (parallel) | Fit assessment score 4.5/5 — proceed |
| DG-03 | approve | Tomás | Cost basis and area program approved |
| DG-04 | approve | Bruno | SOW architect review approved |
| DG-05 | approve | Rosa | Proposal approved — legal review: approved_with_advisory |
| DG-06 | approve | Legal (contract begins) | Client proposal delivery approved |
| DG-07 | approve | Felipe | Concept design approved; HOA early feedback received |
| DG-08 | approve | Emilio | Architectural design approved; HOA submission in progress |
| DG-09 | approve | Hugo | Budget alignment 9.09% variance — within 10% proceed threshold |
| DG-10 | approve | Ofelia | Executive plans approved; HOA approval stamp included |
| DG-11 | approve | Paco | Constructora Los Cabos selected (2 bids; development pre-approved) |

---

## HOA Compliance Trace

This section traces the HOA requirements through the pipeline artifacts:

| HOA Requirement | Source (seed data) | Verified In |
|----------------|-------------------|-------------|
| Contemporary style only | hoa_details.style_restrictions | concept-review.json (material_direction, color_direction), architectural-design.json (hoa_style_constraints_applied.style), scope-of-work.json (deliverables Phase 2 covenant checklist) |
| Natural stone and stucco facade | hoa_details.material_restrictions | concept-review.json (material_direction: "natural volcanic stone + white stucco"), architectural-design.json (facade_materials confirmed), scope-of-work.json (Phase 2 deliverables) |
| 7m height limit | hoa_details.height_limit_m: 7 | concept-review.json (space_arrangement: "ridge height 6.8m"), architectural-design.json (actual_ridge_height_m: 6.8), scope-of-work.json (Phase 2 deliverables), area-program.json (assumptions: HOA height limit noted) |
| No flat roofs over 2 floors | hoa_details.style_restrictions | concept-review.json (3d_model notes), architectural-design.json (flat_roof_over_2_floors: false) |
| HOA design review submission | residential_in_development type | site-readiness-report.json (HOA design guidelines requested), scope-of-work.json Phase 2 deliverables, executive-plans.json (HOA approval stamp), sol.md Step 2 (HOA guidelines required) |

---

## File Manifest

**Project directory:** `projects/PRJ-2026-0317-tc002-casa-vista/`

### Segment A
- `state.json`
- `lead-record.json`

### Segment B
- `lead-summary.json`
- `discovery-questionnaire.json`
- `client-fit-assessment.json`
- `decision-event-dg01.json`
- `decision-event-dg02.json`

### Segment C
- `area-program.json`
- `cost-basis.json`
- `site-readiness-report.json`

### Segment D
- `scope-of-work.json`
- `budget.json`
- `proposal.json`
- `legal-review.json`
- `client-communication.json`
- `decision-event-dg03.json`
- `decision-event-dg04.json`
- `decision-event-dg05.json`
- `decision-event-dg06.json`

### Segment E
- `project-schedule.json`

### Segment F
- `concept-review.json`
- `architectural-design.json`
- `decision-event-dg07.json`
- `decision-event-dg08.json`

### Segment G
- `engineering-package.json`
- `budget-alignment.json`
- `decision-event-dg09.json`

### Segment H
- `executive-plans.json`
- `decision-event-dg10.json`

### Segment I
- `bid-comparison.json`
- `permit-status.json`
- `decision-event-dg11.json`

### Segment J
- `invoice.json`
- `tax-filing.json`

**Total files:** 35

---

## Notes and Observations

1. **Sol's site-readiness-report.json** includes topographic survey, HOA design guidelines (Residencial Vista del Mar), and property title — three documents rather than the minimum one (topo only) because the project type is `residential_in_development` and the slope condition is "slight slope" (topo always required) plus the HOA guidelines requirement per Sol's spec Step 2.

2. **Payment schedule in USD:** Seed data provides payment_schedule in USD; scope-of-work.json preserves USD per Tomás spec ("If the payment schedule is in USD, preserve the currency as-is; do not convert"). Budget.json and invoice.json also use USD.

3. **Legal review:** Result is `approved_with_advisory` (not `approved`) — the advisory flag is that IP ownership is implied but not explicit in the proposal body. This is non-blocking and DG-05 proceeds per Legal spec.

4. **Engineering conditional systems:** Three conditional systems are included (irrigation, solar, av) per seed data special_features: ["pool", "solar", "smart_home"]. Irrigation is included per template default for residential.

5. **Bid comparison:** Two bids received per TC-002 expected flow ("multiple bids" noted for Segment G). No single-bid escalation triggered. Constructora Los Cabos selected.

6. **Dispatcher chain for Tax:** Vera (Segment J) → dispatches Controller at each milestone → Controller (final_milestone: true) → dispatches Tax. This chain is verified in both Vera.md and Controller.md specs.
