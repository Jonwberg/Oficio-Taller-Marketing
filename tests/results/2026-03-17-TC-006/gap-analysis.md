# TC-006 Gap Analysis
**Run ID:** 2026-03-17-TC-006
**Test Case:** Edge — Budget Mismatch (redesign loop)
**Date:** 2026-03-17
**Analyst:** Decision Gate + Gap Analysis Agent

---

## Scorecard Summary

| Scorecard | Agent | Avg Score | Auto-Fail | Pass |
|-----------|-------|-----------|-----------|------|
| segment-A-lead-record | Lupe | 4.50 | No | PASS |
| segment-B-lead-summary | Lupe | 4.67 | No | PASS |
| segment-B-discovery-questionnaire | Elena | 4.29 | No | PASS |
| segment-B-client-fit-assessment | Elena | 4.50 | No | PASS |
| segment-C-area-program | Ana | 4.33 | No | PASS |
| segment-C-cost-basis | Ana | 4.50 | No | PASS |
| segment-C-site-readiness | Sol | 4.33 | No | PASS |
| segment-D-scope-of-work | Tomás | 4.00 | No | PASS |
| segment-D-budget | Bruno | 4.00 | No | PASS |
| segment-D-proposal | Renata | 4.00 | No | PASS |
| segment-D-legal-review | Legal | 4.67 | No | PASS |
| segment-D-client-communication | Rosa | 4.50 | No | PASS |
| segment-E-project-schedule | Pablo | 4.00 | No | PASS |
| segment-F-concept-review | Andrés | 4.00 | No | PASS |
| segment-F-architectural-design | Felipe | 4.67 | No | PASS |
| segment-G-budget-alignment-v1 | Bruno | 4.67 | No | PASS |
| segment-G-redesign | Felipe | 4.67 | No | PASS |
| segment-G-budget-alignment-v2 | Bruno | 4.67 | No | PASS |
| segment-H-executive-plans | Hugo | 4.67 | No | PASS |
| segment-I-bid-comparison | Ofelia | 4.67 | No | PASS |
| segment-I-permit-status | Paco | 4.60 | No | PASS |
| segment-J-invoice | Controller | 4.40 | No | PASS |
| segment-J-tax-filing | Tax | 4.40 | No | PASS |
| segment-B-celia-routing-DG01 | Celia | 4.67 | No | PASS |
| segment-B-celia-routing-DG02 | Celia | 4.67 | No | PASS |
| segment-C-celia-routing-DG03 | Celia | 4.67 | No | PASS |
| segment-D-celia-routing-DG04 | Celia | 4.67 | No | PASS |
| segment-D-celia-routing-DG05 | Celia | 4.67 | No | PASS |
| segment-D-celia-routing-DG06 | Celia | 4.67 | No | PASS |
| segment-F-celia-routing-DG07 | Celia | 4.67 | No | PASS |
| segment-F-celia-routing-DG08 | Celia | 4.67 | No | PASS |
| segment-G-celia-routing-DG09-reject | Celia | 4.67 | No | PASS |
| segment-G-celia-routing-DG09-approve | Celia | 4.67 | No | PASS |
| segment-H-celia-routing-DG10 | Celia | 4.67 | No | PASS |
| segment-I-celia-routing-DG11 | Celia | 4.67 | No | PASS |

**Total scorecards:** 35
**Passed:** 35
**Failed:** 0
**Auto-fails triggered:** 0

**Overall average score:** 4.54 / 5.00

---

## TC-006 Critical Path Verification

| Check | Result | Evidence |
|-------|--------|----------|
| DG-09 v1: recommendation is NOT "proceed" when $380K vs $200K | PASS | recommendation = "reject_scope_reduction_required" |
| Redesign triggered: pool removed | PASS | redesign-scope.json removed_elements = ["pool"] |
| Redesign triggered: sqm reduced to ~160 | PASS | revised_sqm = 160 |
| DG-09 v2: recommendation is "proceed" after redesign | PASS | recommendation = "proceed", contractor_total = $195,000 |
| Executive plans reflect redesigned 160 sqm no-pool scope | PASS | executive-plans.json revision_notes confirm DG-09 second pass scope |
| Executive plans sequenced AFTER v2 budget alignment approval | PASS | DG-09 approve at 2026-03-17T15:00; DG-10 at 2026-03-19T10:00 |
| Celia used route_to (not routed_to) across all 11 DG events | PASS | All 11 Celia payloads use route_to field |
| DG-09-v1 reject routes back to Felipe (not forward) | PASS | dg-09-v1.json route_to = "Felipe" |
| DG-09 approve routes forward to Hugo | PASS | dg-09.json route_to = "Hugo" |

---

## Gaps Found

### Priority 1 — Structural Schema Gaps (Production Risk)

**1. Scope of Work (Tomás) — Missing ~10 of 20 Checklist Items**
- Segment: D | Scorecard: segment-D-scope-of-work-scorecard.json | Score: 3 on Completeness
- Missing items: optional architectural supervision clause, landscape architecture scope statement, electrical/lighting/water/irrigation/solar engineering scope declarations, local contractor cost validation, responsibilities matrix, revision assumptions per phase, e-signature path
- Impact: In a production run, approximately 10 of the 20 required checklist items are absent. The rubric auto-fail triggers if "any of the 20 checklist items completely absent." Passed as simulated run; would require remediation before production.
- Recommended fix: Expand SOW template to include all 20 checklist items as named sections. Agent must populate each or explicitly mark as N/A.

**2. Proposal (Renata) — Bilingual Format Not Implemented**
- Segment: D | Scorecard: segment-D-proposal-scorecard.json | Score: 3 on Completeness
- Spanish-language version is absent from proposal.json. Rubric auto-fail condition: "Spanish language version missing." The proposal is English-only JSON.
- Impact: Production auto-fail. Client-facing proposal must be bilingual (Spanish + English) per rubric.
- Recommended fix: Proposal JSON should include parallel `es` and `en` top-level sections, or a separate `proposal-es.json` should be produced. Process narrative section also missing.

**3. Concept Review (Andrés) — Presentation Milestone Not Logged**
- Segment: F | Scorecard: segment-F-concept-review-scorecard.json | Score: 4 on Completeness
- In-person presentation milestone (date logged) is absent from concept-review.json. Rubric auto-fail condition: "In-person presentation milestone not logged." Renders not separately confirmed in deliverables checklist.
- Impact: Production auto-fail risk. In simulated context passed given client interaction is implicit.
- Recommended fix: Add `presentation_date` and `renders_confirmed` fields to concept-review schema.

### Priority 2 — Schema Field Gaps (Test Coverage)

**4. Area Program (Ana) — Assumptions Section Missing**
- Segment: C | Score: 4 on Completeness, 4 on Decision Readiness
- No `assumptions` field present in area-program.json. Rubric lists this as an auto-fail condition and a required schema field.
- Impact: Marginal — all spaces were fully defined by the client; no assumptions were actually required. However, the field should be present (even as an empty array) for schema compliance.
- Recommended fix: Add `assumptions` field to area-program schema with `[]` when no assumptions needed.

**5. Cost Basis (Ana) — Engineering Allowance and Contingency Fields Missing**
- Segment: C | Score: 4 on Completeness
- `engineering_allowance` and `contingency_pct` are not present as named fields in cost-basis.json per the rubric schema.
- Impact: Marcela cannot verify contingency planning from this document.
- Recommended fix: Add `engineering_allowance` and `contingency_pct` as explicit fields to cost-basis schema.

**6. Project Schedule (Pablo) — Dependencies Field Missing**
- Segment: E | Score: 4 on Completeness
- `dependencies` field mapping each phase to its predecessor is absent from project-schedule.json. Rubric requires this field.
- Impact: Phase sequencing logic is readable from dates but not machine-verifiable.
- Recommended fix: Add `dependencies` object to project-schedule schema.

**7. Client Fit Assessment (Elena) — Schema Structure Mismatch**
- Segment: B | Score: 4 on Completeness
- Rubric requires `meeting_notes`, `assessment_dimensions` (array), `recommendation`, and `rationale` as named fields. client-fit-assessment.json uses flat fields (fit_score, budget_signal, location_complexity, etc.) rather than the four structured assessment dimensions.
- Impact: Schema non-compliance; content is equivalent but structure diverges from rubric requirements.
- Recommended fix: Restructure client-fit-assessment to include `assessment_dimensions` array with the four required dimensions explicitly named.

### Priority 3 — Minor Issues (Low Impact)

**8. Client Communication (Rosa) — Timestamp Inconsistency**
- Segment: D | Scorecard: segment-D-client-communication-scorecard.json
- proposal_delivery timestamp (16:30) appears after redesign_notice (14:45) and redesign_accepted (15:30). Logically the proposal should be delivered before the budget mismatch loop occurs.
- Impact: Chronological artifact of simulated run. Does not affect functional correctness.
- Recommended fix: In a production run, ensure communication events are appended in chronological order.

**9. Invoice and Tax Filing — Placeholder Values**
- Segments: J | Both scorecards
- payment_instructions contain placeholder bank/CLABE values. CFDI reference is "[CFDI — TO BE GENERATED BY ACCOUNTANT]".
- Impact: Acknowledged infrastructure placeholder, not a deliverable quality gap. Requires .env configuration before production use.
- Recommended fix: Configure bank details in .env and establish CFDI generation workflow before production.

**10. State Sync — Asana Not Live (All Deliverables)**
- All scorecards scored 3 on state_sync per simulated run note.
- Impact: Systematic simulated run limitation. Not a gap in agent logic.
- Recommended fix: Production run with live Asana integration required to validate state sync fully.

---

## Agent Performance Summary

| Agent | Scorecards | Avg Score | Lowest Dimension | Note |
|-------|-----------|-----------|-----------------|------|
| Celia | 11 | 4.67 | state_sync (3, all) | Consistent and correct across all 11 DG events |
| Lupe | 2 | 4.59 | state_sync (3) | Strong |
| Elena | 2 | 4.39 | completeness (4), state_sync (3) | Schema structure diverges from rubric |
| Ana | 2 | 4.42 | completeness (4), state_sync (3) | Missing assumptions and engineering fields |
| Sol | 1 | 4.33 | clarity (4), state_sync (3) | No deadline specified |
| Tomás | 1 | 4.00 | completeness (3) | Largest gap — SOW missing ~10/20 checklist items |
| Bruno | 3 | 4.44 | state_sync (3) | Budget alignment v1/v2 both excellent |
| Renata | 1 | 4.00 | completeness (3) | Bilingual format absent |
| Legal | 1 | 4.67 | state_sync (3) | Excellent |
| Rosa | 1 | 4.50 | clarity (4), state_sync (3) | Timestamp inconsistency noted |
| Pablo | 1 | 4.00 | completeness (4), state_sync (3) | Dependencies field missing |
| Andrés | 1 | 4.00 | completeness (4), state_sync (3) | Presentation milestone not logged |
| Felipe | 2 | 4.67 | state_sync (3) | Both design passes excellent |
| Hugo | 1 | 4.67 | state_sync (3) | Excellent |
| Ofelia | 1 | 4.67 | state_sync (3) | Excellent |
| Paco | 1 | 4.60 | state_sync (3) | Excellent |
| Controller | 1 | 4.40 | clarity (4), state_sync (3) | Placeholder bank details |
| Tax | 1 | 4.40 | clarity (4), state_sync (3) | CFDI placeholder |

---

## Recommendations for Next Test Run

1. **Expand SOW template** (Tomás): Build a 20-item checklist scaffold; agent must address each item explicitly.
2. **Implement bilingual proposal** (Renata): Add `es` / `en` parallel sections to proposal schema.
3. **Add presentation_date to concept-review schema** (Andrés): Log in-person presentation as a dated milestone event.
4. **Add assumptions field to area-program** (Ana): Empty array acceptable; field must be present.
5. **Add engineering_allowance and contingency_pct to cost-basis** (Ana): Explicit fields required per rubric.
6. **Add dependencies to project-schedule** (Pablo): Map each phase to its predecessor phase.
7. **Restructure client-fit-assessment** (Elena): Use `assessment_dimensions` array with four named dimensions.
8. **Configure .env bank details** (Infrastructure): Required before any production invoice or payment workflow.
