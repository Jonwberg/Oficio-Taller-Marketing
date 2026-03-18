# Gap Analysis — TC-009
**Run ID:** 2026-03-17-TC-009
**Test Case:** Casa Horizonte — Familia Reyes-Montoya (coastal zone + solar + SEMARNAT corrections)
**Date:** 2026-03-17
**Mode:** LIVE (real Asana + real Gmail)
**Scored by:** Test Decision Gate + Gap Analysis Agent

---

## Overall Score Summary

| Category | Score |
|---|---|
| Total deliverables scored | 22 |
| Celia routing events scored | 11 |
| Total scorecards produced | 33 |
| Auto-fails triggered | 0 |
| Failed scorecards (passed: false) | 0 |
| Overall average score (22 deliverables) | **4.67 / 5.0** |
| Overall average score (11 Celia events) | **4.83 / 5.0** |
| Combined average (all 33 scorecards) | **4.73 / 5.0** |

---

## Deliverable Scores by Segment

| Scorecard | Agent | Average | Passed | Notes |
|---|---|---|---|---|
| segment-A-lead-record | Lupe | 5.00 | ✅ | Perfect score across all 6 dimensions |
| segment-B-lead-summary | Lupe | 4.83 | ✅ | State sync −1 (implicit not explicit in JSON) |
| segment-B-discovery-questionnaire | Elena | 4.86 | ✅ | 7-dimension rubric; state sync −1 |
| segment-B-client-fit-assessment | Elena | 4.83 | ✅ | All 4 dimensions; state sync −1 |
| segment-C-area-program | Ana | 4.67 | ✅ | Accuracy −1: sqm discrepancy flagged (320 vs 356) requires Marcela confirm |
| segment-C-cost-basis | Ana | 4.83 | ✅ | Math verified; state sync −1 |
| segment-C-site-readiness | Sol | 4.67 | ✅ | Coastal/wind checks PASS; clarity −1 (no deadline for client); state sync −1 |
| segment-D-scope-of-work | Tomás | 4.83 | ✅ | All 20 checklist items confirmed; state sync −1 |
| segment-D-budget | Bruno | 4.20 | ✅ | CLABE placeholder in payment_instructions; M2/M3 milestones not explicit objects |
| segment-D-proposal | Renata | 4.83 | ✅ | Fully bilingual, no placeholders; state sync −1 |
| segment-D-legal-review | Legal | 4.67 | ✅ | SEMARNAT advisory present; schema field naming deviates (no ip_rights_status top-level field) |
| segment-D-client-communication | Rosa | 5.00 | ✅ | Perfect score; draft status correct; brand voice excellent |
| segment-E-project-schedule | Pablo | 5.00 | ✅ | Perfect score; SEMARNAT parallel track modeled; all activation conditions met |
| segment-F-concept-review | Andrés | 4.50 | ✅ | Coastal setback deferred to Phase 2 noted; Marcela feedback not verbatim |
| segment-F-architectural-design | Felipe | 4.83 | ✅ | Wind load inputs confirmed; pool RC monolithic; state sync −1 |
| segment-G-engineering-package | Emilio | 4.83 | ✅ | Solar in conditional_systems PASS; all 4 required systems complete; state sync −1 |
| segment-G-budget-alignment | Bruno | 4.83 | ✅ | −17.2% variance; proceed correct; state sync −1 |
| segment-H-executive-plans | Hugo | 4.50 | ✅ | Schema structure deviation (array vs named fields); content complete |
| segment-I-bid-comparison | Ofelia | 4.83 | ✅ | 2 bids; SEMARNAT experience in rationale; state sync −1 |
| segment-I-permit-status | Paco | 4.80 | ✅ | 2 corrections resolved PASS; MIA round correct; state sync −1 |
| segment-J-invoice | Controller | 4.20 | ✅ | CLABE placeholder reduces clarity to 3; amount correct |
| segment-J-tax-filing | Tax | 4.00 | ✅ | RFC + CFDI placeholders; revenue correct; dispatched by Controller PASS |

---

## Celia Routing Scores

| Scorecard | Gate | Route To | Average | Passed |
|---|---|---|---|---|
| segment-B-celia-routing-DG01 | DG-01 | Lupe | 4.83 | ✅ |
| segment-B-celia-routing-DG02 | DG-02 | Ana, Sol (parallel) | 4.83 | ✅ |
| segment-C-celia-routing-DG03 | DG-03 | Tomás | 4.83 | ✅ |
| segment-D-celia-routing-DG04 | DG-04 | Bruno | 4.83 | ✅ |
| segment-D-celia-routing-DG05 | DG-05 | Rosa | 4.83 | ✅ |
| segment-D-celia-routing-DG06 | DG-06 | Rosa | 4.83 | ✅ |
| segment-F-celia-routing-DG07 | DG-07 | Felipe | 4.83 | ✅ |
| segment-F-celia-routing-DG08 | DG-08 | Emilio | 4.83 | ✅ |
| segment-G-celia-routing-DG09 | DG-09 | Hugo | 4.83 | ✅ |
| segment-H-celia-routing-DG10 | DG-10 | Ofelia | 4.83 | ✅ |
| segment-I-celia-routing-DG11 | DG-11 | Paco | 4.83 | ✅ |

All 11 Celia routing events: route_to field used (not routed_to). All 11 payload fields present. All routing decisions correct.

---

## TC-009 Specific Edge Case Results

| Check | Required | Score Impact | Result |
|---|---|---|---|
| site-readiness: coastal_zone_permit present | CRITICAL auto-fail if absent | None — present | ✅ PASS |
| site-readiness: wind_load_study present | CRITICAL auto-fail if absent | None — present | ✅ PASS |
| engineering-package: solar in conditional_systems | Score down if missing | None — solar present | ✅ PASS |
| permit-status: ≥2 corrections, all resolved | Score down if absent/unresolved | None — 2 corrections, both resolved | ✅ PASS |
| tax-filing: dispatched_by Controller (not Vera) | Score down if wrong dispatcher | None — Controller dispatched Tax | ✅ PASS |
| legal-review: SEMARNAT disclosure advisory | Score down if absent | None — advisory present and specific | ✅ PASS |

**All 6 TC-009 specific edge cases: PASS**

---

## Gaps Identified

### GAP-001: Environment Placeholder Fields (Medium Priority)
**Files affected:** invoice.json, tax-filing.json, budget.json (payment_instructions)
**Issue:** CLABE, RFC, and CFDI reference fields contain placeholder strings ('[CLABE — TO BE CONFIGURED IN .env]', '[RFC — TO BE CONFIGURED IN .env]', '[CFDI — TO BE GENERATED BY ACCOUNTANT]'). These reduce clarity scores to 3 in invoice.json and tax-filing.json.
**Impact:** In a real engagement, a client receiving an invoice with '[BANK_NAME]' cannot pay without a follow-up. For the live test, this is an environment configuration gap, not an agent logic gap.
**Recommendation:** Configure .env before production use. Consider adding a validation step in Controller to reject invoice generation if CLABE is still a placeholder.
**Severity:** Low for test validity (no auto-fail); Medium for production readiness.

### GAP-002: Schema Naming Deviations (Low Priority)
**Files affected:** legal-review.json (missing top-level ip_rights_status, compliance_flags), executive-plans.json (plan_set_components array instead of named cross_sections/full_plan_book/technical_coordination fields)
**Issue:** Rubric schemas specify certain top-level field names that the deliverables address via different structures (arrays, nested objects).
**Impact:** Scoring penalty of −1 on completeness for legal-review and −1 on completeness/clarity for executive-plans. No functional information is missing — all content is present.
**Recommendation:** Align agent output schemas with rubric field specifications. The rubric field list is the contract — agents should output fields with exact names.
**Severity:** Low. Does not affect decision quality. Clean up for rubric compliance.

### GAP-003: Celia Comment Field Always Null (Low Priority)
**Files affected:** All 11 decision events (DG-01 through DG-11)
**Issue:** The comment field is null in all 11 decision events. When Marcela approves without notes, this is appropriate. However, the rubric scores Clarity at 4 (not 5) when comment is null, because the rubric expects the reviewer comment to be preserved verbatim, including the absence of a comment to be explicitly stated as an intentional null (which it is here).
**Impact:** Consistency penalty of −1 on clarity across all 11 Celia events. Average Celia score is 4.83 instead of potential 5.0.
**Recommendation:** This is acceptable behavior for clean approvals. No change needed — scoring reflects the rubric correctly. For future test cases with reject or pass-to-agent decisions, verify that actual reviewer comments are captured verbatim.
**Severity:** Informational only.

### GAP-004: Area Program sqm Discrepancy Requires Marcela Confirmation (Low Priority)
**Files affected:** area-program.json
**Issue:** Client stated 'approximately 320 sqm' but programmed total is 356 sqm (including covered terrace and pool deck as full structural areas). Ana correctly flags this in the assumptions section but leaves it as an open item for Marcela to confirm with the client.
**Impact:** Accuracy scored 4 (not 5). No auto-fail. The discrepancy is appropriately disclosed.
**Recommendation:** In production, Marcela should confirm which sqm definition applies (enclosed vs total) before cost basis is finalized. Document the client confirmation to close this assumption.
**Severity:** Low for test; requires action in production.

### GAP-005: State Sync Scoring Pattern (Informational)
**Files affected:** Most deliverables (11 of 22 scored 4 on state_sync)
**Issue:** State sync is scored 4 on most deliverables because the JSON files do not include an explicit 'asana_task_id' or 'state_updated_to' field. However, the real Asana GIDs are confirmed in state.json, proving actual sync occurred.
**Impact:** Systematic −1 on state_sync across most deliverables. This reflects the rubric correctly — the rubric tests for evidence within the deliverable JSON itself.
**Recommendation:** For TC-009 as the live reference run, this scoring pattern establishes the baseline. Agents could include an asana_task_gid field in their output JSON to achieve state_sync: 5 without requiring external verification from state.json.
**Severity:** Informational — live Asana integration confirmed regardless.

---

## TC-009 as Quality Baseline

TC-009 is the live reference run. The combined average of 4.73/5.0 with zero auto-fails and zero failed scorecards establishes this as the quality baseline for the system. All critical path edge cases passed (coastal permit, wind load study, SEMARNAT corrections cycle, solar engineering, Controller dispatch chain). The gaps identified are limited to:
- Environment configuration items (placeholders in financial fields)
- Schema naming alignment opportunities
- Consistent null comments on clean approvals

No gaps were found in agent logic, routing correctness, or decision quality.

---

## Benchmark for Future Test Runs

| Metric | TC-009 Baseline |
|---|---|
| Combined average (all scorecards) | 4.73 / 5.0 |
| Deliverable average | 4.67 / 5.0 |
| Celia routing average | 4.83 / 5.0 |
| Auto-fail rate | 0% |
| Pass rate | 100% (33/33) |
| TC-009 specific checks | 6/6 PASS |

Any future run scoring below 4.5 combined average, or triggering any auto-fail, or failing any TC-009 specific edge case check, represents a regression from this baseline.
