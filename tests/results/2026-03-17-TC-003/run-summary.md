# TC-003 Run Summary
**Run ID:** 2026-03-17-TC-003
**Test Case:** Wellness Retreat — commercial_hotel with hydrologic study
**Date:** 2026-03-17
**Scored:** 2026-03-17 (Test Decision Gate + Gap Analysis Agent)
**Mode:** Simulated
**Final State:** `project_closed` ✅

---

## Scored Segment Table

| Segment | Agents | Deliverables | Avg Score | Celia Routing | Status |
|---------|--------|--------------|-----------|---------------|--------|
| A | Lupe | lead-record | 4.50 | N/A (no Celia at A) | ✅ PASS |
| B | Lupe, Elena, Celia (DG-01, DG-02) | lead-summary, discovery-questionnaire*, client-fit-assessment | 4.54 | DG-01 fail (comment=null), DG-02 fail (comment=null) | ⚠️ PARTIAL — discovery-questionnaire auto-fail (language) |
| C | Ana, Sol, Celia (DG-03) | area-program, cost-basis, site-readiness-report | 4.61 | DG-03 pass ✅ | ✅ PASS |
| D | Tomás, Bruno, Renata, Legal, Rosa, Celia (DG-04, 05, 06) | scope-of-work, budget, proposal, legal-review, client-communication | 4.50 | DG-04 fail (comment=null), DG-05 fail (comment=null), DG-06 fail (comment=null) | ✅ PASS (deliverables all pass; Celia routing systematic gap) |
| E | Pablo | project-schedule | 4.40 | N/A (no Celia at E) | ✅ PASS |
| F | Andrés, Felipe, Celia (DG-07, DG-08) | concept-review, architectural-design | 4.50 | DG-07 pass ✅, DG-08 fail (comment=null) | ✅ PASS |
| G | Emilio, Bruno, Celia (DG-09) | engineering-package, budget-alignment | 4.50 | DG-09 pass ✅ | ✅ PASS |
| H | Hugo, Celia (DG-10) | executive-plans | 4.42 | DG-10 fail (comment=null) | ✅ PASS |
| I | Ofelia, Paco, Celia (DG-11) | bid-comparison, permit-status | 4.64 | DG-11 pass ✅ | ✅ PASS |
| J | Controller, Tax | invoice, tax-filing | 4.00 | N/A (no Celia at J) | ✅ PASS (operational gaps: bank placeholders, CFDI placeholder) |

---

## Score Summary

| Metric | Value |
|--------|-------|
| Deliverable scorecards (22) | Avg 4.44 |
| Celia routing scorecards (11) | Avg 4.36 |
| **Overall average (33 scorecards)** | **4.41** |
| Deliverables passed | 21/22 |
| Celia routing passed | 4/11 |
| Auto-fail triggers | 2 (discovery-questionnaire language; Celia comment=null ×7) |

---

## TC-003 Critical Checks

| Check | Result |
|-------|--------|
| Sol requests BOTH topo AND hydrologic study (arroyo) | ✅ PASS |
| commercial_hotel SOW template applied | ✅ PASS |
| hospitality_compliance_clause present | ✅ PASS |
| Emilio includes greywater system | ✅ PASS |
| Emilio includes av_system | ✅ PASS |
| Emilio includes solar system | ✅ PASS |
| 3 bids collected (commercial_hotel minimum) | ✅ PASS |
| All Celia payloads use route_to (not routed_to) | ✅ PASS |
| Final state: project_closed | ✅ PASS |

---

## Key Gaps (see gap-analysis.md for full detail)

| Gap ID | Severity | Finding |
|--------|----------|---------|
| GAP-001 | HIGH | Celia drops reviewer comment in 7/11 gates (DG-01, 02, 04, 05, 06, 08, 10). Systematic. Auto-fail per rubric. |
| GAP-002 | MEDIUM | Discovery questionnaire sent in Spanish to English-speaking client (James Hartwell). Language auto-fail triggered. |
| GAP-003 | MEDIUM | Bank name and CLABE are placeholders in budget.json and invoice.json — client cannot pay without these. |
| GAP-004 | LOW | Lead record lacks verbatim raw message field (summarized instead). |
| GAP-005 | LOW | Tax filing has CFDI placeholder; only M3 invoice file present (M1, M2 not found in project folder). |
| GAP-006 | LOW | Budget alignment options have no savings estimates. |
| GAP-007 | LOW | Concept review not logged as past timestamped event. |

---

## Scorecard Files

| Scorecard | File |
|-----------|------|
| Segment A — lead-record | segment-A-lead-record-scorecard.json |
| Segment B — lead-summary | segment-B-lead-summary-scorecard.json |
| Segment B — discovery-questionnaire | segment-B-discovery-questionnaire-scorecard.json |
| Segment B — client-fit-assessment | segment-B-client-fit-assessment-scorecard.json |
| Segment B — Celia DG-01 | segment-B-celia-routing-DG01-scorecard.json |
| Segment B — Celia DG-02 | segment-B-celia-routing-DG02-scorecard.json |
| Segment C — area-program | segment-C-area-program-scorecard.json |
| Segment C — cost-basis | segment-C-cost-basis-scorecard.json |
| Segment C — site-readiness | segment-C-site-readiness-scorecard.json |
| Segment C — Celia DG-03 | segment-C-celia-routing-DG03-scorecard.json |
| Segment D — scope-of-work | segment-D-scope-of-work-scorecard.json |
| Segment D — budget | segment-D-budget-scorecard.json |
| Segment D — proposal | segment-D-proposal-scorecard.json |
| Segment D — legal-review | segment-D-legal-review-scorecard.json |
| Segment D — client-communication | segment-D-client-communication-scorecard.json |
| Segment D — Celia DG-04 | segment-D-celia-routing-DG04-scorecard.json |
| Segment D — Celia DG-05 | segment-D-celia-routing-DG05-scorecard.json |
| Segment D — Celia DG-06 | segment-D-celia-routing-DG06-scorecard.json |
| Segment E — project-schedule | segment-E-project-schedule-scorecard.json |
| Segment F — concept-review | segment-F-concept-review-scorecard.json |
| Segment F — architectural-design | segment-F-architectural-design-scorecard.json |
| Segment F — Celia DG-07 | segment-F-celia-routing-DG07-scorecard.json |
| Segment F — Celia DG-08 | segment-F-celia-routing-DG08-scorecard.json |
| Segment G — engineering-package | segment-G-engineering-package-scorecard.json |
| Segment G — budget-alignment | segment-G-budget-alignment-scorecard.json |
| Segment G — Celia DG-09 | segment-G-celia-routing-DG09-scorecard.json |
| Segment H — executive-plans | segment-H-executive-plans-scorecard.json |
| Segment H — Celia DG-10 | segment-H-celia-routing-DG10-scorecard.json |
| Segment I — bid-comparison | segment-I-bid-comparison-scorecard.json |
| Segment I — permit-status | segment-I-permit-status-scorecard.json |
| Segment I — Celia DG-11 | segment-I-celia-routing-DG11-scorecard.json |
| Segment J — invoice | segment-J-invoice-scorecard.json |
| Segment J — tax-filing | segment-J-tax-filing-scorecard.json |

Full gap analysis: `gap-analysis.md`
