# Gap Analysis — TC-003 Wellness Retreat
**Run ID:** 2026-03-17-TC-003
**Test Case:** Wellness Retreat — commercial_hotel with hydrologic study
**Date Scored:** 2026-03-17
**Scored by:** Test Decision Gate + Gap Analysis Agent

---

## Overall Scorecard Summary

| Deliverable | Agent | Segment | Avg Score | Auto-Fail | Passed |
|---|---|---|---|---|---|
| lead-record | Lupe | A | 4.50 | No | Yes |
| lead-summary | Lupe | B | 4.67 | No | Yes |
| discovery-questionnaire | Elena | B | 4.29 | YES | **No** |
| client-fit-assessment | Elena | B | 4.67 | No | Yes |
| area-program | Ana | C | 4.67 | No | Yes |
| cost-basis | Ana | C | 4.67 | No | Yes |
| site-readiness-report | Sol | C | 4.50 | No | Yes |
| scope-of-work | Tomás | D | 4.67 | No | Yes |
| budget | Bruno | D | 3.80 | No | Yes |
| proposal | Renata | D | 4.67 | No | Yes |
| legal-review | Legal | D | 4.50 | No | Yes |
| client-communication | Rosa | D | 4.88 | No | Yes |
| project-schedule | Pablo | E | 4.40 | No | Yes |
| concept-review | Andrés | F | 4.33 | No | Yes |
| architectural-design | Felipe | F | 4.67 | No | Yes |
| engineering-package | Emilio | G | 4.67 | No | Yes |
| budget-alignment | Bruno | G | 4.33 | No | Yes |
| executive-plans | Hugo | H | 4.67 | No | Yes |
| bid-comparison | Ofelia | I | 4.67 | No | Yes |
| permit-status | Paco | I | 4.60 | No | Yes |
| invoice | Controller | J | 4.20 | No | Yes |
| tax-filing | Tax | J | 3.80 | No | Yes |

**Deliverable average (22 scorecards):** 4.44

## Celia Routing Scorecard Summary

| Gate | Segment | Avg Score | Comment Captured | celia_routing_correct | Passed |
|---|---|---|---|---|---|
| DG-01 | B | 4.17 | No (null) | False | **No** |
| DG-02 | B | 4.17 | No (null) | False | **No** |
| DG-03 | C | 4.67 | Yes | True | Yes |
| DG-04 | D | 4.17 | No (null) | False | **No** |
| DG-05 | D | 4.17 | No (null) | False | **No** |
| DG-06 | D | 4.17 | No (null) | False | **No** |
| DG-07 | F | 4.67 | Yes | True | Yes |
| DG-08 | F | 4.17 | No (null) | False | **No** |
| DG-09 | G | 4.67 | Yes | True | Yes |
| DG-10 | H | 4.17 | No (null) | False | **No** |
| DG-11 | I | 4.67 | Yes | True | Yes |

**Celia routing average (11 scorecards):** 4.36
**Celia comment capture rate:** 4/11 (36%) — DG-03, DG-07, DG-09, DG-11

**Combined overall average (33 scorecards):** 4.41

---

## TC-003 Critical Checks

| Critical Check | Result | Evidence |
|---|---|---|
| Sol requests BOTH topographic_survey AND hydrologic_study | PASS | site-readiness-report.json required_documents includes both; hydrologic_study rationale explicitly cites seasonal arroyo on south boundary |
| commercial_hotel SOW template applied | PASS | scope-of-work.json project_type_clauses includes commercial_hotel_standard_clause |
| hospitality_compliance_clause present | PASS | scope-of-work.json project_type_clauses includes hospitality_compliance_clause with SECTUR + COFEPRIS detail |
| Emilio includes greywater system | PASS | engineering-package.json systems_status.greywater = complete, NOM-015-CONAGUA, sized for 20-unit hotel |
| Emilio includes av_system | PASS | engineering-package.json systems_status.av_system = complete, in-room + public areas + network backbone |
| Emilio includes solar | PASS | engineering-package.json systems_status.solar = complete, 100kWp total |
| 2+ bids in bid-comparison | PASS | bid-comparison.json has 3 bids (Constructora Baja Sur, Desarrollos Pacífico Norte, Grupo Constructivo Los Cabos) |
| All Celia events use route_to (not routed_to) | PASS | All 11 dg-*.json files use route_to field |

---

## Gaps Found

### GAP-001: Celia comment capture — Systematic failure (7/11 gates)
**Severity:** HIGH
**Affected gates:** DG-01, DG-02, DG-04, DG-05, DG-06, DG-08, DG-10
**Finding:** In 7 of 11 decision gates, Celia's dg-*.json event has `comment=null` while the corresponding human decision file (dg-*.json Marcela version) contains a substantive reviewer comment. The comment field is populated in the other 4 gates (DG-03, DG-07, DG-09, DG-11), demonstrating the capability is present but not consistently applied.
**Root cause hypothesis:** Celia's event creation logic does not reliably copy the reviewer's comment from the human decision record into the routing payload. The pattern of null vs. non-null appears inconsistent, suggesting a conditional path or race condition in comment extraction.
**Rubric impact:** Per the Celia routing rubric, "Reviewer comment dropped" is an auto-fail condition. 7 of 11 events technically trigger this condition.
**Risk:** Downstream agents may lack context for decisions made by Marcela (e.g., DG-04 drops the confirmation that both commercial_hotel clauses were verified; DG-10 drops M3 invoice trigger context).
**Recommendation:** Fix Celia's comment extraction to always capture the reviewer's comment from the human decision record, defaulting to the comment field in the source decision document even if empty string rather than null.

### GAP-002: Discovery questionnaire language mismatch
**Severity:** MEDIUM
**Affected deliverable:** discovery-questionnaire.json (Elena, Segment B)
**Finding:** Questionnaire was sent in Spanish. Client James Hartwell's inbound email was entirely in English. The rubric auto-fail condition "questionnaire sent in wrong language when client language is unambiguously identified from inbound message" is triggered.
**Impact:** Client proceeded successfully (discovery call completed, fit assessment produced), indicating the client is likely bilingual. However, sending Spanish to an English-speaking client risks a poor first impression and is a process error.
**Recommendation:** Elena should detect inbound message language and mirror it for the questionnaire. A simple heuristic: if the raw_message field in lead-summary.json is in English, send questionnaire in English first (with Spanish offered).

### GAP-003: Payment instruction placeholders in budget and invoice
**Severity:** MEDIUM
**Affected deliverables:** budget.json (Bruno, Segment D), invoice.json (Controller, Segment J)
**Finding:** Both budget.json and invoice.json contain placeholder values: `[BANK_NAME]` and `[CLABE — TO BE CONFIGURED IN .env]`. A client receiving these documents cannot initiate payment without a follow-up.
**Impact:** Operational gap — in production, this would require a manual step to populate before any document is sent to the client. If not caught before delivery, it creates friction at the moment of contract signing.
**Recommendation:** Populate bank details from a firm-level configuration object (`.env` or equivalent config file) at document generation time. These are static firm-level constants and should never appear as placeholders in client-facing deliverables.

### GAP-004: Lead record — raw message not preserved verbatim
**Severity:** LOW
**Affected deliverable:** lead-record.json (Lupe, Segment A)
**Finding:** lead-record.json summary field contains a structured interpretation of the inbound message, not the raw verbatim text. The rubric score 5 requires "raw message stored verbatim in task body." The verbatim message is preserved in lead-summary.json (raw_message field) but not in lead-record.json.
**Impact:** Minor — raw message is preserved elsewhere in the project folder. Not a decision-blocking gap.
**Recommendation:** Lead record should include a raw_message field mirroring the verbatim inbound text. This is the Asana task body equivalent.

### GAP-005: Tax filing — CFDI reference placeholder and unverified M1/M2 invoices
**Severity:** LOW
**Affected deliverable:** tax-filing.json (Tax, Segment J)
**Finding:** (1) cfdi_reference is a placeholder (`[CFDI — TO BE GENERATED BY ACCOUNTANT]`). (2) Only one invoice file (invoice.json, M3) exists in the project folder. If M1 and M2 invoices were issued as separate documents, they should also be present for revenue reconciliation.
**Impact:** Filing is structurally complete with correct revenue total (USD 420,000 = sum of all three milestones). However, traceability to source invoices is not possible from the project folder alone.
**Recommendation:** (1) Populate CFDI references when Tax agent produces the filing (can be a simulated reference in test mode). (2) Ensure Controller issues separate invoice files for each milestone (M1 at contract signing, M2 at concept approval, M3 at executive plans approval) — all three should be present in the project folder.

### GAP-006: Budget alignment — no savings estimates per option
**Severity:** LOW
**Affected deliverable:** budget-alignment.json (Bruno, Segment G)
**Finding:** Three options for resolving the 74.4% budget gap are named (phase construction, revisit budget, reduce scope) but no estimated savings amount is provided for any option. The rubric requires "if redesign, specific scope elements named with estimated savings."
**Impact:** Marcela received the gap analysis with options but no financial sizing of each option. She resolved the gap through client discussion rather than from this document. In a higher-stakes decision, the absence of savings estimates could delay the decision.
**Recommendation:** Bruno should provide at least order-of-magnitude savings estimates for each recommended option (e.g., "deferring spa to Phase 2 saves approximately MXN 15–20M").

### GAP-007: Concept review — presentation not logged as past event
**Severity:** LOW
**Affected deliverable:** concept-review.json (Andrés, Segment F)
**Finding:** `presentation_milestone` is set to "M2 — Concept Approved" as a label/reference, not as a timestamped past event. The rubric requires "in-person presentation logged as milestone with date." The review_notes are written as a pre-presentation checklist ("ready for Marcela's approval at DG-07") rather than post-presentation documentation.
**Impact:** Mild — the concept was clearly approved (DG-07 confirms). But the review record looks forward rather than documenting what occurred, which reduces its audit value.
**Recommendation:** After concept presentation, Andrés should update concept-review.json with a `presentation_date` field and convert review_notes to past-tense documentation of what was reviewed and approved.

---

## TC-003 Discriminating Condition Assessment

TC-003 is specifically designed to test whether the system correctly handles a `commercial_hotel` project with a `seasonal arroyo` site condition requiring a `hydrologic_study`. All three critical discriminating behaviors were executed correctly:

1. **Sol (site-readiness-report):** Correctly identified and requested the hydrologic study with specific rationale citing the seasonal arroyo. This is the highest-stakes check — a failure here would have caused the project to proceed without mandatory site documentation.

2. **Tomás (scope-of-work):** Correctly applied the `commercial_hotel` template with both required clauses (`commercial_hotel_standard_clause` and `hospitality_compliance_clause`). SECTUR and COFEPRIS compliance are explicitly addressed.

3. **Emilio (engineering-package):** Correctly included all three TC-003 conditional systems: greywater, av_system, and solar. The arroyo was explicitly addressed across all engineering disciplines in the `arroyo_coordination_note`.

4. **Ofelia (bid-comparison):** 3 bids collected — meets both the SOW minimum (3) and the rubric minimum (2+).

---

## Segments: Pass/Fail Summary

| Segment | Status | Notes |
|---|---|---|
| A | PASS | Lead record minor completeness gap (no verbatim raw message) |
| B | PARTIAL PASS | Discovery questionnaire fails language auto-fail; fit assessment and lead summary both pass; Celia DG-01/DG-02 fail on comment=null |
| C | PASS | Site readiness critical check passed (topo + hydrologic); area program and cost basis both strong |
| D | PASS | All four Segment D deliverables pass; Celia DG-04/05/06 fail on comment=null; budget/invoice have placeholder bank details |
| E | PASS | Project schedule complete with 6 phases, realistic durations, all milestones |
| F | PASS | Concept review and architectural design both pass; Celia DG-07 passes, DG-08 fails on comment=null |
| G | PASS | Engineering package critical checks all pass (greywater, AV, solar); budget alignment correctly escalated |
| H | PASS | Executive plans 13 components complete, all integrated |
| I | PASS | 3 bids collected, permit approved with corrections resolved |
| J | PARTIAL PASS | Invoice and tax filing pass structurally; bank detail placeholders and CFDI placeholder are operational gaps |

---

## Priority Recommendations

1. **CRITICAL (fix before next run):** Fix Celia comment extraction — 7/11 gates drop Marcela's comment. This is a systematic architectural issue in the routing event creation logic.

2. **HIGH (fix before production):** Populate bank name and CLABE from firm config — these should never reach a client document as placeholders.

3. **MEDIUM:** Elena language detection — detect inbound message language and mirror for questionnaire. Low engineering effort, high client experience impact.

4. **LOW:** Controller should issue separate invoice files for M1, M2, and M3. Tax agent should generate a CFDI reference stub in test mode.

5. **LOW:** Budget alignment should include savings estimates per recommended option.

6. **LOW:** Concept review should be updated post-presentation with timestamp and past-tense documentation.
