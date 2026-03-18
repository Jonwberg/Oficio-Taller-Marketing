# TC-008 Gap Analysis
**Run ID:** 2026-03-17-TC-008
**Test Case:** Edge — Site Complications (hydrology blocker)
**Date:** 2026-03-17
**Scored by:** Decision Gate + Gap Analysis Agent
**Scoring scope:** 22 deliverables + 11 Celia routing events = 33 scorecards total

---

## Overall Result

**All 33 scorecards: PASSED**
**No auto-fails triggered**
**No blocking gaps identified**

---

## Score Summary Table

| Scorecard | Segment | Agent | Avg Score | Auto-Fail | Passed |
|---|---|---|---|---|---|
| lead-record | A | Lupe | 4.67 | No | Yes |
| lead-summary | B | Lupe | 4.67 | No | Yes |
| discovery-questionnaire | B | Elena | 4.43 | No | Yes |
| client-fit-assessment | B | Elena | 4.67 | No | Yes |
| area-program | C | Ana | 4.67 | No | Yes |
| cost-basis | C | Ana | 4.67 | No | Yes |
| site-readiness-report | C | Sol | 4.67 | No | Yes |
| scope-of-work | D | Tomás | 4.50 | No | Yes |
| budget | D | Bruno | 4.00 | No | Yes |
| proposal | D | Renata | 4.67 | No | Yes |
| legal-review | D | Legal | 4.50 | No | Yes |
| client-communication | D | Rosa | 4.63 | No | Yes |
| project-schedule | E | Pablo | 4.60 | No | Yes |
| activation-gate | E | Vera | 5.00 | No | Yes |
| hydrology-resolution | E | Vera | 5.00 | No | Yes |
| concept-review | F | Andrés | 4.67 | No | Yes |
| architectural-design | F | Felipe | 4.50 | No | Yes |
| engineering-package | G | Emilio | 4.17 | No | Yes |
| budget-alignment | G | Bruno | 4.67 | No | Yes |
| executive-plans | H | Hugo | 4.67 | No | Yes |
| bid-comparison | I | Ofelia | 4.67 | No | Yes |
| permit-status | I | Paco | 4.60 | No | Yes |
| invoice | J | Controller | 4.00 | No | Yes |
| tax-filing | J | Tax | 3.80 | No | Yes |
| Celia DG-01 | B | Celia | 4.33 | No | Yes |
| Celia DG-02 | B | Celia | 4.33 | No | Yes |
| Celia DG-03 | C | Celia | 4.67 | No | Yes |
| Celia DG-04 | D | Celia | 4.33 | No | Yes |
| Celia DG-05 | D | Celia | 4.33 | No | Yes |
| Celia DG-06 | D | Celia | 4.33 | No | Yes |
| Celia DG-07 | F | Celia | 4.67 | No | Yes |
| Celia DG-08 | F | Celia | 4.33 | No | Yes |
| Celia DG-09 | G | Celia | 4.67 | No | Yes |
| Celia DG-10 | H | Celia | 4.33 | No | Yes |
| Celia DG-11 | I | Celia | 4.67 | No | Yes |

**Overall average: 4.47 / 5.00**

---

## TC-008 Critical Edge Case Checks

| Check | Required | Result | Score |
|---|---|---|---|
| Sol requests topographic_survey | Yes | PASS — present in required_documents | 5 |
| Sol requests hydrologic_study (stream on site) | CRITICAL AUTO-FAIL if absent | PASS — present in required_documents | 5 |
| activation-gate: gate_status='blocked' | Yes | PASS | 5 |
| activation-gate: blocker='hydrologic_study_pending' | Yes | PASS | 5 |
| activation-gate: site_data_complete=false | Yes | PASS | 5 |
| Pablo NOT dispatched during block | Yes | PASS — vera-activation-blocked.json action='STOP — do not dispatch Pablo' | 5 |
| hydrology-resolution: blocker_resolved=true | Yes | PASS | 5 |
| hydrology-resolution: site_data_complete=true | Yes | PASS | 5 |
| Pablo dispatched only after hydrology resolved | Yes | PASS — schedule start date 2026-04-28 = hydrology study receipt date | 5 |
| scope-of-work: commercial_hotel template | Yes | PASS — CH-001 through CH-005 clauses applied | 5 |
| CH-004 hydrologic setback clause present | Yes | PASS — CONAGUA/CNA cited | 5 |
| Permit corrections: CONAGUA addendum required | Expected edge behavior | PASS — hydrology constraint surfaces at permit stage | 5 |
| Stream setback (15m) carried into design deliverables | Expected | PASS — concept-review, architectural-design, executive-plans all reference 15m setback | 5 |

**All 13 TC-008 critical checks: PASSED**

---

## Gaps Identified

### Gap 1 — Engineering Package: All Consultants TBD (Minor)
**Deliverable:** engineering-package.json
**Dimension:** Completeness, Accuracy (scored 4 each)
**Finding:** All five engineering disciplines (structural, electrical, lighting, water, solar) list the responsible engineer as "TBD — to be contracted." The package declares all_inputs_confirmed=true, but no consultant inputs are actually confirmed received because no consultants have been contracted.
**Impact:** Low in simulated run — system declares completion and proceeds correctly. In production, this would require actual engineer engagement before DG-09 can fire.
**Recommendation:** In future runs, seed data should include named engineering consultants to enable full confirmation tracking. An auto-fail condition should flag all_inputs_confirmed=true when any consultant is TBD.

### Gap 2 — SOW Checklist: Items 10, 12, 20 Incomplete (Minor)
**Deliverable:** scope-of-work.json
**Dimension:** Completeness (scored 4)
**Finding:** Three of the 20 SOW checklist items are absent or incomplete:
- Item 10 (irrigation scope) — not explicitly included or excluded
- Item 12 (local contractor cost validation plan) — not formally described in SOW
- Item 20 (e-signature path) — no e-signature mechanism defined
**Impact:** Low — these are process gaps, not substantive scope errors. The commercial_hotel template is correctly applied with 5 project-type clauses.
**Recommendation:** Add an irrigation exclusion statement (or confirm it is part of landscape exclusion), document the contractor cost validation approach in the SOW, and define the e-signature path.

### Gap 3 — Discovery Questionnaire: Language Mismatch (Minor)
**Deliverable:** discovery-questionnaire.json
**Dimension:** Language (scored 4)
**Finding:** Questionnaire sent in Spanish to a client who wrote in English ("Good morning, I have a 15,000sqm property..."). The studio context (Mexico-based, BCS projects) makes Spanish defensible, but strict rubric interpretation requires matching the client's inbound language.
**Impact:** Very low — the questionnaire is well-crafted and the client is engaging in a Mexico-based project. Not a blocking issue.
**Recommendation:** Elena should detect client inbound language and default to matching it on first outreach, with an optional note that the studio operates bilingually.

### Gap 4 — Budget: M1-Only Invoice Structure (Minor)
**Deliverable:** budget.json
**Dimension:** Completeness (scored 4)
**Finding:** The budget.json file structures as an M1 invoice rather than a full three-milestone payment schedule. M2 and M3 are implicit in the line items total but not presented as separate milestone rows with trigger events.
**Impact:** Low — M2 and M3 invoices are in separate Controller files. The proposal.json contains the full three-milestone breakdown. No payment data is missing from the system.
**Recommendation:** Bruno's budget deliverable should include all three milestone rows in a summary_milestones array for completeness, even when structured as an M1-first invoice.

### Gap 5 — Tax Filing: CFDI Placeholder (Minor)
**Deliverable:** tax-filing.json
**Dimension:** Clarity (scored 3)
**Finding:** cfdi_reference='[CFDI — TO BE GENERATED BY ACCOUNTANT]' — a placeholder. Filing cannot be traced to Controller invoices from this document alone.
**Impact:** Test-mode limitation — expected in a simulated run. No production impact if CFDI generation is handled by the accountant post-run.
**Recommendation:** In production runs, seed the CFDI generation process so the Tax agent can receive and record the reference. Consider adding a cfdi_status field ('pending_accountant_generation' vs 'received') to make the incomplete state explicit rather than a placeholder string.

### Gap 6 — Controller Invoice: Payment Instructions Placeholders (Minor)
**Deliverable:** invoice.json
**Dimension:** Clarity (scored 3)
**Finding:** Bank name and CLABE are .env placeholders. Client cannot pay without follow-up.
**Impact:** Test-mode limitation only. In production, .env configuration resolves this before any invoice is issued.
**Recommendation:** Ensure .env bank configuration is verified before any live run. Add a pre-flight check that rejects invoice issuance if BANK_NAME or CLABE are placeholder values.

### Gap 7 — Celia DG-01/02/04/05/06/08/10: Null Comments (Cosmetic)
**Deliverables:** Seven Celia decision events with comment=null
**Dimension:** Clarity (scored 3 each)
**Finding:** Seven of eleven Celia events have comment=null. The rubric prefers confirmed "no comment" over null for traceability.
**Impact:** Cosmetic — all are clean approvals where Marcela provided no specific feedback. The null accurately represents the decision event state.
**Recommendation:** Celia should emit comment: "No comment — clean approve" or similar when Marcela provides no comment, rather than null. This preserves the rubric's traceability requirement and makes the review log more auditable.

---

## TC-008 Edge Case Lifecycle Summary

The hydrology blocker edge case was correctly handled end-to-end:

1. **Sol** (Segment C) — correctly identified both topo AND hydrologic study as required. Logged blocker with 6-week estimate.
2. **Vera** (activation-gate.json) — correctly blocked activation with site_data_complete=false and blocker='hydrologic_study_pending'.
3. **vera-activation-blocked.json** — explicitly states "STOP — do not dispatch Pablo." Pablo was NOT dispatched.
4. **hydrology-study-received.json** — received 2026-04-28, ~6 weeks after block. blocker_resolved=true, site_data_complete=true.
5. **vera-activation-approved.json** — all three conditions met. Pablo dispatched.
6. **Pablo** (project-schedule.json) — schedule correctly starts 2026-04-28. Hydrologic constraint (15m setback) carried into Phase 1 deliverables.
7. **Concept through Executive Plans** — 15m setback and spa repositioning tracked through all design phases.
8. **Permit** (permit-status.json) — CONAGUA addendum required during permit corrections, resolved with hydrologic study documentation. The constraint surfaces correctly at the regulatory stage.

This is a complete and correctly-simulated edge case lifecycle. No gaps in the critical path.

---

## Scores by Segment

| Segment | Deliverables | Average Score |
|---|---|---|
| A | 1 | 4.67 |
| B | 4 (incl. 2 Celia) | 4.44 |
| C | 4 (incl. 1 Celia) | 4.67 |
| D | 7 (incl. 3 Celia) | 4.38 |
| E | 3 (incl. activation-gate + hydrology) | 4.87 |
| F | 4 (incl. 2 Celia) | 4.54 |
| G | 3 (incl. 1 Celia) | 4.50 |
| H | 2 (incl. 1 Celia) | 4.50 |
| I | 3 (incl. 1 Celia) | 4.65 |
| J | 2 | 3.90 |

**Highest scoring segment:** E (4.87) — TC-008 edge case correctly executed
**Lowest scoring segment:** J (3.90) — test-mode placeholder limitations in CFDI and bank details

---

## Recommendations for Next Test Run

1. Seed named engineering consultants in engineering-package.json for full confirmation tracking
2. Resolve SOW checklist items 10/12/20 (irrigation exclusion, contractor validation plan, e-signature path)
3. Elena language detection: match client inbound language on first outreach
4. Bruno: include full three-milestone summary in budget.json alongside M1 invoice
5. Celia: replace null comments with explicit "no comment — clean approve" for auditability
6. Pre-flight .env check for bank/CLABE before invoice issuance
7. CFDI generation process: seed accountant handoff to allow Tax agent to receive and record reference

---

*Gap analysis generated by Decision Gate + Gap Analysis Agent for run 2026-03-17-TC-008*
