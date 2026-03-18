# Gap Analysis — TC-004 Centro de Salud
**Run ID:** 2026-03-17-TC-004
**Date:** 2026-03-17
**Project type:** commercial_health_center (COFEPRIS)
**Scored by:** Decision Gate + Gap Analysis Agent

---

## Overall Score Summary

| Deliverable | Agent | Segment | Avg Score | Pass |
|---|---|---|---|---|
| lead-record | Lupe | A | 4.50 | ✅ |
| lead-summary | Lupe | B | 4.67 | ✅ |
| discovery-questionnaire | Elena | B | 4.29 | ✅ |
| client-fit-assessment | Elena | B | 4.67 | ✅ |
| area-program | Ana | C | 4.67 | ✅ |
| cost-basis | Ana | C | 4.67 | ✅ |
| site-readiness-report | Sol | C | 4.17 | ✅ |
| scope-of-work | Tomás | D | 4.67 | ✅ |
| budget | Bruno | D | 3.80 | ✅ |
| proposal | Renata | D | 4.50 | ✅ |
| legal-review | Legal | D | 4.67 | ✅ |
| client-communication | Rosa | D | 4.75 | ✅ |
| project-schedule | Pablo | E | 4.60 | ✅ |
| concept-review | Andrés | F | 4.50 | ✅ |
| architectural-design | Felipe | F | 4.67 | ✅ |
| engineering-package | Emilio | G | 4.67 | ✅ |
| budget-alignment | Bruno | G | 4.67 | ✅ |
| executive-plans | Hugo | H | 4.33 | ✅ |
| bid-comparison | Ofelia | I | 4.67 | ✅ |
| permit-status | Paco | I | 4.60 | ✅ |
| invoice | Controller | J | 4.00 | ✅ |
| tax-filing | Tax | J | 4.20 | ✅ |

**Deliverable average (22 items): 4.47**

| Celia DG | Segment | Avg Score | Pass |
|---|---|---|---|
| DG-01 | B | 4.67 | ✅ |
| DG-02 | B | 4.67 | ✅ |
| DG-03 | C | 4.67 | ✅ |
| DG-04 | D | 4.67 | ✅ |
| DG-05 | D | 4.67 | ✅ |
| DG-06 | D | 4.67 | ✅ |
| DG-07 | F | 4.67 | ✅ |
| DG-08 | F | 4.67 | ✅ |
| DG-09 | G | 4.67 | ✅ |
| DG-10 | H | 4.67 | ✅ |
| DG-11 | I | 4.67 | ✅ |

**Celia routing average (11 events): 4.67**

**Overall run average (all 33 scored items): 4.53**

---

## TC-004 Specific Checks

| Check | Result | Evidence |
|---|---|---|
| commercial_health_center template applied | ✅ PASS | `scope-of-work.json` sow_template_applied = `docs/templates/sow/sow-commercial-health-center.md` |
| health_authority_compliance_clause present | ✅ PASS | `scope-of-work.json` project_type_clauses includes `health_authority_compliance_clause` |
| cofepris_compliance_clause present | ✅ PASS | `scope-of-work.json` project_type_clauses includes `cofepris_compliance_clause` |
| COFEPRIS as explicit deliverable (auto-fail check) | ✅ PASS | COFEPRIS named in Phases 1, 2, 3, 4, and 6 deliverables |
| medical_gas_systems in conditional_systems | ✅ PASS | `engineering-package.json` conditional_systems=['medical_gas_systems', 'specialized_hvac'] |
| specialized_hvac in conditional_systems | ✅ PASS | As above |
| No hydrologic study for flat urban lot (auto-fail check) | ✅ PASS | `site-readiness-report.json` required_documents=['topographic_survey'] only — no hydrologic study |
| All Celia payloads use route_to (not routed_to) | ✅ PASS | All 11 DG events use route_to field |
| Final state: project_closed | ✅ PASS | state.json (implied by run summary) |
| 3+ contractor bids with COFEPRIS experience | ✅ PASS | `bid-comparison.json` has 3 bids, all clinical_experience='verified' |

**All TC-004 specific checks: PASS**

---

## Auto-Fail Review

No auto-fail conditions triggered across any of the 33 scored items.

Checks performed:
- lead-record: received_at present, status present, legitimate lead not classified as spam ✅
- lead-summary: not empty, source present, classification not "unknown" ✅
- discovery-questionnaire: budget_question present, project_type present, language correct ✅
- client-fit-assessment: explicit recommendation present, all 4 dimensions present ✅
- area-program: total_sqm present, all spaces have size, assumptions present ✅
- cost-basis: assumptions present, total_estimate present, architecture_fee present ✅
- site-readiness-report: topo included, no hydrologic study for flat lot ✅
- scope-of-work: payment schedule present, exclusions present, correct project type template ✅
- budget: line_items present, payment_instructions present, total consistent ✅
- proposal: Spanish present, English present, no placeholder text, budget matches ✅
- legal-review: IP reviewed, no open unresolved flags (advisory only), full proposal reviewed ✅
- client-communication: draft status, project_reference present, no confidential info ✅
- project-schedule: phases array present, milestone_dates present ✅
- concept-review: all 5 deliverables confirmed, presentation_milestone logged ✅
- architectural-design: all rooms present, concept reflected, structural notes present ✅
- engineering-package: all required systems present, no undeclared pending inputs ✅
- budget-alignment: contractor source documented, explicit recommendation present ✅
- executive-plans: no unresolved conflicts, required systems present ✅
- bid-comparison: comparison matrix present, not single bid treated as selection ✅
- permit-status: jurisdiction specific, submitted_at present, corrections array present, approved_at consistent with status ✅
- invoice: total USD 216,000 matches running_total ✅
- tax-filing: revenue matches Controller total, RFC present, jurisdiction correct ✅
- Celia DG-01 through DG-11: all 11 payload fields present, route_to used (not routed_to), no wrong agent assignments ✅

---

## Identified Gaps

### GAP-001 — Payment Schedule Inconsistency (Medium priority)
**Location:** `budget.json` → `invoice.json` → `scope-of-work.json`
**Description:** Three different payment schedule structures are used:
- `scope-of-work.json` uses a 5-milestone schedule: M1=25%, M2=15%, M3=20%, M4=25%, M5=15% (total: 100%)
- `budget.json` uses a 6-phase allocation: Ph1=20%, Ph2=25%, Ph3=15%, Ph4=25%, Ph5=10%, Ph6=5% (total: 100%)
- `invoice.json` uses a 3-milestone schedule from seed data: M1=40%, M2=30%, M3=30% (total: 100%)

All three total USD 216,000 — no financial discrepancy. However milestone-level amounts diverge, and the invoice payment_schedule_note explicitly cites 'seed data' as the override. The invoiced M1 amount ($86,400 = 40%) does not match the M1 amount in the signed SOW ($54,000 = 25%). In production this would create a contract vs invoice discrepancy.

**Impact:** No auto-fail triggered (totals match). Accuracy score for invoice docked to 3.
**Recommendation:** Establish a single authoritative payment schedule source — the signed SOW. Budget.json should mirror the SOW milestone schedule. Invoice.json should draw from the SOW payment_schedule, not seed data. The seed data payment_schedule (40/30/30) appears to be a construction-phase schedule, not the architecture fee schedule.

---

### GAP-002 — discovery-questionnaire: sent_to field is null (Low priority)
**Location:** `discovery-questionnaire.json`, field `sent_to`
**Description:** The `sent_to` field is null — the recipient is not recorded. The rubric schema requires this field, and the questionnaire was sent to the inbound lead (Dra. Carmen Valdez). This is a data population gap, not a wrong-recipient error (no auto-fail), but it means the deliverable does not trace which contact received the questionnaire.
**Impact:** Minor schema completeness gap. No functional failure.
**Recommendation:** Elena should populate `sent_to` with the lead contact identifier (email address or WhatsApp number) when dispatching the questionnaire.

---

### GAP-003 — discovery-questionnaire: questions not tailored to commercial_health_center context (Low priority)
**Location:** `discovery-questionnaire.json`
**Description:** The project_type_question lists residential/interior examples ('casa habitación, ampliación, proyecto interior, desarrollo inmobiliario') for a lead already identified as a commercial health center. For a warm medical group lead with a detailed clinical program already provided, the questionnaire should have been tailored to confirm COFEPRIS registration status, medical group corporate structure, facility category, and clinical program details rather than asking generic project type questions.
**Impact:** Accuracy and clarity docked from 5 to 4. No functional failure — the questionnaire still produces useful responses.
**Recommendation:** Elena's discovery questionnaire template should branch on project_type from the lead record. When project_type='commercial_health_center', the questionnaire should substitute clinical intake questions for residential examples.

---

### GAP-004 — site-readiness-report: no deadline or client instructions documented (Low priority)
**Location:** `site-readiness-report.json`
**Description:** The deliverable is minimal — only 4 fields (required_documents, request_sent_at, current_status, blockers). No deadline for document submission, no client-facing instructions documented. The rubric scores clarity at 5 when the client receives clear instructions with deadline.
**Impact:** Clarity docked to 3. Decision_readiness docked to 4.
**Recommendation:** Site-readiness-report should include a `deadline` field and a `client_instructions` field documenting what was communicated to the client about document specifications and timing.

---

### GAP-005 — executive-plans: schema uses string array instead of structured object (Low priority)
**Location:** `executive-plans.json`, field `plan_set_components`
**Description:** The rubric specifies `plan_set_components` should be a structured object with `cross_sections`, `full_plan_book`, and `technical_coordination` keys. The deliverable uses a flat string array of 8 component names. The content is present and correct but the schema structure does not match the rubric's required schema.
**Impact:** Completeness docked to 4. Clarity docked to 4 (one external reference to engineering-package.json in notes).
**Recommendation:** Hugo's executive-plans.json output schema should use a structured object with the rubric's required keys. This is a schema conformance issue, not a content issue.

---

### GAP-006 — concept-review: review_notes reflect Andrés's assessment, not Marcela's feedback verbatim (Minor)
**Location:** `concept-review.json`, field `review_notes`
**Description:** The rubric requires review_notes to capture Marcela's specific feedback. The notes present are Andrés's pre-review assessment and recommendation, not a post-review record of what Marcela said. In a simulated run where all approvals are clean, this is inherent to the simulation (no real Marcela feedback to record). However in a production approval flow, the concept-review deliverable should be updated post-DG-07 to include Marcela's actual comments.
**Impact:** Accuracy docked to 4.
**Recommendation:** The concept-review.json should be updated after DG-07 fires to include Marcela's verbatim feedback from her review session. This may require a post-gate update step.

---

### GAP-007 — tax-filing: cfdi_reference is a placeholder, deductibles amount is 0 (Minor)
**Location:** `tax-filing.json`
**Description:** cfdi_reference = '[CFDI — TO BE GENERATED BY ACCOUNTANT]' is a placeholder not traceable to Controller invoices. deductibles array has one entry with amount=0 pending accountant confirmation.
**Impact:** Completeness docked to 4, Clarity docked to 4. No auto-fail.
**Recommendation:** In production, cfdi_reference must be populated with the actual CFDI folio from the SAT-stamped invoice before the tax filing is closed. Deductibles should be confirmed and documented before closing the filing. These are production process gaps, not agent errors.

---

## Summary Assessment

**Zero auto-fails. Zero critical gaps.**

All 22 deliverables and 11 Celia routing events passed. The run demonstrates a complete, coherent TC-004 lifecycle from inbound WhatsApp lead through commercial health center project close, with all COFEPRIS-specific requirements correctly handled.

The most significant gap is GAP-001 (payment schedule inconsistency across three documents). This is a production risk — the client would receive an invoice for $86,400 at M1 against a signed SOW that states $54,000 at M1. This should be resolved before production deployment.

All TC-004 specific checks passed cleanly: commercial_health_center template applied, health_authority_compliance_clause present, cofepris_compliance_clause present, medical_gas_systems and specialized_hvac in conditional_systems, no hydrologic study for flat urban lot.

---

*Generated by Decision Gate + Gap Analysis Agent — 2026-03-17*
