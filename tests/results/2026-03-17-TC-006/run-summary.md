# TC-006 Run Summary
**Run ID:** 2026-03-17-TC-006
**Test Case:** Edge — Budget Mismatch (redesign loop)
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `project_closed`
**Scored by:** Decision Gate + Gap Analysis Agent
**Scoring date:** 2026-03-17

---

## Segment Results

| Segment | Agents | Result |
|---------|--------|--------|
| A | Lupe | PASS |
| B | Lupe, Celia, Elena, Celia | PASS |
| C | Ana, Sol, Vera, Celia | PASS |
| D | Tomás, Vera, Bruno, Renata, Legal, Vera, Rosa, Celia | PASS |
| E | Vera, Pablo | PASS |
| F | Andrés, Celia, Felipe, Celia | PASS |
| G | Emilio, Bruno (reject), Felipe (redesign), Bruno (approve), Celia | PASS |
| H | Hugo, Celia | PASS |
| I | Ofelia, Celia, Paco | PASS |
| J | Vera, Controller ×3, Tax | PASS |

**Overall: 10/10 segments PASS**

---

## Scorecard Results

| Scorecard | Agent | Avg Score | Pass |
|-----------|-------|-----------|------|
| segment-A-lead-record | Lupe | 4.50 | PASS |
| segment-B-lead-summary | Lupe | 4.67 | PASS |
| segment-B-discovery-questionnaire | Elena | 4.29 | PASS |
| segment-B-client-fit-assessment | Elena | 4.50 | PASS |
| segment-C-area-program | Ana | 4.33 | PASS |
| segment-C-cost-basis | Ana | 4.50 | PASS |
| segment-C-site-readiness | Sol | 4.33 | PASS |
| segment-D-scope-of-work | Tomás | 4.00 | PASS |
| segment-D-budget | Bruno | 4.00 | PASS |
| segment-D-proposal | Renata | 4.00 | PASS |
| segment-D-legal-review | Legal | 4.67 | PASS |
| segment-D-client-communication | Rosa | 4.50 | PASS |
| segment-E-project-schedule | Pablo | 4.00 | PASS |
| segment-F-concept-review | Andrés | 4.00 | PASS |
| segment-F-architectural-design | Felipe | 4.67 | PASS |
| segment-G-budget-alignment-v1 | Bruno | 4.67 | PASS |
| segment-G-redesign | Felipe | 4.67 | PASS |
| segment-G-budget-alignment-v2 | Bruno | 4.67 | PASS |
| segment-H-executive-plans | Hugo | 4.67 | PASS |
| segment-I-bid-comparison | Ofelia | 4.67 | PASS |
| segment-I-permit-status | Paco | 4.60 | PASS |
| segment-J-invoice | Controller | 4.40 | PASS |
| segment-J-tax-filing | Tax | 4.40 | PASS |
| segment-B-celia-routing-DG01 | Celia | 4.67 | PASS |
| segment-B-celia-routing-DG02 | Celia | 4.67 | PASS |
| segment-C-celia-routing-DG03 | Celia | 4.67 | PASS |
| segment-D-celia-routing-DG04 | Celia | 4.67 | PASS |
| segment-D-celia-routing-DG05 | Celia | 4.67 | PASS |
| segment-D-celia-routing-DG06 | Celia | 4.67 | PASS |
| segment-F-celia-routing-DG07 | Celia | 4.67 | PASS |
| segment-F-celia-routing-DG08 | Celia | 4.67 | PASS |
| segment-G-celia-routing-DG09-reject | Celia | 4.67 | PASS |
| segment-G-celia-routing-DG09-approve | Celia | 4.67 | PASS |
| segment-H-celia-routing-DG10 | Celia | 4.67 | PASS |
| segment-I-celia-routing-DG11 | Celia | 4.67 | PASS |

**Total scorecards:** 35 | **Passed:** 35 | **Failed:** 0 | **Auto-fails:** 0

**Overall average score: 4.54 / 5.00**

---

## Key Verification Points

| Check | Result |
|-------|--------|
| DG-09 first pass: recommendation = reject_scope_reduction_required (not proceed) | PASS |
| Redesign loop triggered: pool removed, 160sqm | PASS |
| DG-09 second pass: recommendation = proceed, contractor_total = $195K | PASS |
| Executive plans only after v2 budget alignment approve | PASS |
| Executive plans reflect 160 sqm no-pool redesigned scope | PASS |
| All Celia payloads use route_to (not routed_to) — 11/11 DG events | PASS |
| DG-09-v1 reject routes to Felipe (redesign, not forward) | PASS |
| DG-09 approve routes to Hugo (forward to executive plans) | PASS |
| Final state: project_closed | PASS |

---

## Gaps Summary (see gap-analysis.md for full detail)

| Priority | Gap | Agent | Impact |
|----------|-----|-------|--------|
| P1 | SOW missing ~10/20 checklist items | Tomás | Production auto-fail risk |
| P1 | Proposal bilingual format absent | Renata | Production auto-fail |
| P1 | Concept review presentation milestone not logged | Andrés | Production auto-fail risk |
| P2 | Area program missing assumptions field | Ana | Schema non-compliance |
| P2 | Cost basis missing engineering_allowance and contingency_pct | Ana | Schema non-compliance |
| P2 | Project schedule missing dependencies field | Pablo | Schema non-compliance |
| P2 | Client fit assessment schema structure mismatch | Elena | Schema non-compliance |
| P3 | Client communication timestamp inconsistency | Rosa | Simulated run artifact |
| P3 | Invoice/tax placeholder bank and CFDI values | Controller/Tax | Infrastructure config required |
| P3 | State sync scored 3 across all deliverables | All | Asana not live in simulation |

Full results: `tests/results/2026-03-17-TC-006/`
