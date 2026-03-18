# Gap Analysis — TC-005 Biblioteca Municipal
## Run ID: 2026-03-17-TC-005
## Scored by: Test Decision Gate + Gap Analysis Agent
## Date: 2026-03-17

---

## Overall Result: PASS

**Overall Average Score: 4.46 / 5.00**

All 22 deliverable scorecards produced. All 11 Celia routing scorecards produced.
No auto-fail conditions triggered across any deliverable.
All TC-005 critical checks passed.

---

## Score Summary by Deliverable

| Scorecard | Agent | Avg Score | Passed | Auto-Fail |
|-----------|-------|-----------|--------|-----------|
| segment-A-lead-record | Lupe | 4.50 | PASS | No |
| segment-B-lead-summary | Lupe | 4.67 | PASS | No |
| segment-B-discovery-questionnaire | Elena | 4.00 | PASS | No |
| segment-B-client-fit-assessment | Elena | 4.67 | PASS | No |
| segment-C-area-program | Ana | 4.67 | PASS | No |
| segment-C-cost-basis | Ana | 4.67 | PASS | No |
| segment-C-site-readiness | Sol | 4.33 | PASS | No |
| segment-D-scope-of-work | Tomás | 4.67 | PASS | No |
| segment-D-budget | Bruno | 4.20 | PASS | No |
| segment-D-proposal | Renata | 4.67 | PASS | No |
| segment-D-legal-review | Legal | 4.50 | PASS | No |
| segment-D-client-communication | Rosa | 4.75 | PASS | No |
| segment-E-project-schedule | Pablo | 4.60 | PASS | No |
| segment-F-concept-review | Andrés | 4.33 | PASS | No |
| segment-F-architectural-design | Felipe | 4.17 | PASS | No |
| segment-G-engineering-package | Emilio | 4.67 | PASS | No |
| segment-G-budget-alignment | Bruno | 4.67 | PASS | No |
| segment-H-executive-plans | Hugo | 4.17 | PASS | No |
| segment-I-bid-comparison | Ofelia | 4.50 | PASS | No |
| segment-I-permit-status | Paco | 4.60 | PASS | No |
| segment-J-invoice | Controller | 4.40 | PASS | No |
| segment-J-tax-filing | Tax | 4.20 | PASS | No |

**Deliverable Average: 4.47**

---

## Celia Routing Score Summary

| Scorecard | Gate | Avg Score | Passed |
|-----------|------|-----------|--------|
| segment-B-celia-routing-DG01 | DG-01 | 4.50 | PASS |
| segment-B-celia-routing-DG02 | DG-02 | 4.50 | PASS |
| segment-C-celia-routing-DG03 | DG-03 | 4.50 | PASS |
| segment-D-celia-routing-DG04 | DG-04 | 4.50 | PASS |
| segment-D-celia-routing-DG05 | DG-05 | 4.17 | PASS |
| segment-D-celia-routing-DG06 | DG-06 | 4.17 | PASS |
| segment-F-celia-routing-DG07 | DG-07 | 4.50 | PASS |
| segment-F-celia-routing-DG08 | DG-08 | 4.50 | PASS |
| segment-G-celia-routing-DG09 | DG-09 | 4.50 | PASS |
| segment-H-celia-routing-DG10 | DG-10 | 4.50 | PASS |
| segment-I-celia-routing-DG11 | DG-11 | 4.50 | PASS |

**Celia Routing Average: 4.44**

---

## TC-005 Critical Checks

| Check | Result | Evidence |
|-------|--------|----------|
| client-fit-assessment treats as INSTITUTIONAL (not individual) | PASS | institutional_notes.client_type=institutional, decision_making_structure=committee/cabildo |
| scope-of-work uses public_civic template | PASS | template_used=sow-public-civic.md |
| scope-of-work includes civic_procurement_clause | PASS | project_type_clause_ids contains civic_procurement_clause |
| scope-of-work includes public_bidding_clause | PASS | project_type_clause_ids contains public_bidding_clause |
| bid-comparison has minimum 2 bids (obra pública) | PASS | bid_count=2, minimum_bids_satisfied=true — AUTO-FAIL NOT TRIGGERED |
| All 11 Celia files use route_to field (not routed_to) | PASS | Verified across all 11 dg-XX.json and decision-event-DG-XX.json files |

---

## Gaps Found

### GAP-001: Discovery Questionnaire — Residential Framing for Institutional Client
**Severity:** Minor
**Deliverable:** discovery-questionnaire.json
**Agent:** Elena
**Affected Score:** clarity (3/5), accuracy (4/5)
**Description:** Several questions use residential/personal framing inappropriate for a Dirección de Obras Públicas institutional client:
- "¿Cuál es el estilo de vida o la atmósfera que quiere que el proyecto refleje?" — irrelevant to a government library
- "¿Casa habitación, ampliación, proyecto interior?" — inapplicable project types listed
- No question about procurement constraints, committee approval process, or institutional decision-making structure
**Impact:** Elena receives responses that help with fit assessment but miss institutional governance context. Partial coverage of TC-005 institutional client dimensions.
**Recommendation:** Elena's questionnaire template should include an institutional/government branch with questions about procurement framework, approval authority, committee structure, and official program documents (programa arquitectónico from contracting entity).

---

### GAP-002: Lead Record — Raw Message Not Stored Verbatim
**Severity:** Minor
**Deliverable:** lead-record.json
**Agent:** Lupe
**Affected Score:** completeness (4/5)
**Description:** The rubric scores 5 for raw message stored verbatim in the task body. The lead-record.json contains a structured summary in the `summary` field rather than the raw email body verbatim. The raw email is preserved in lead-summary.json, but not in the lead-record itself.
**Impact:** Lead record is functional and all required fields are present. The raw message is available in lead-summary.json. Minor gap in completeness standard.
**Recommendation:** Lupe should store the original inbound message verbatim in the lead-record body field in addition to the structured summary, or add a dedicated `raw_message` field mirroring lead-summary.json.

---

### GAP-003: Concept Review — Presentation Event Date Not Logged
**Severity:** Minor
**Deliverable:** concept-review.json
**Agent:** Andrés
**Affected Score:** completeness (4/5)
**Description:** The rubric requires "in-person presentation logged as milestone with date." The `presentation_milestone` field in concept-review.json contains "M2 — Concept Design Approved" (a payment milestone name), not a presentation event date (e.g., "Presentation to technical committee: 2026-04-10").
**Impact:** The concept approval is captured, but the actual presentation event (date, attendees, format) is not documented.
**Recommendation:** Andrés should add a `presentation_event` field with date, attendees, and format distinct from the payment milestone reference.

---

### GAP-004: Concept Review — Review Notes Are Checklist Confirmation, Not Captured Feedback
**Severity:** Minor
**Deliverable:** concept-review.json
**Agent:** Andrés
**Affected Score:** accuracy (4/5)
**Description:** `review_notes` describes the design (accessible entry, courtyard, civic art wall, solar) and concludes "Recommend approval." The rubric calls for Marcela's specific feedback captured verbatim — not a design description by the agent.
**Impact:** The review record does not preserve what Marcela actually said during the concept review. This reduces traceability of the approval.
**Recommendation:** Andrés should capture Marcela's verbatim feedback (even if brief: "Approved — civic character strong, proceed to architectural design") rather than generating a design description.

---

### GAP-005: Architectural Design — Foundation Type Open at Engineering Handoff
**Severity:** Minor
**Deliverable:** architectural-design.json
**Agent:** Felipe
**Affected Score:** clarity (4/5), decision_readiness (4/5)
**Description:** structural_coordination_notes states "Foundation type under review — flat municipal land, soil study results pending engineer review." This means one design question remains open at the engineering handoff.
**Impact:** Emilio's engineering package does not flag this as a pending item (engineering-package.json marks all_inputs_confirmed=true). The gap between Felipe's pending and Emilio's confirmed creates a minor consistency question — either the soil study was received before Phase 3 (plausible, given site_docs_complete=true in state.json) or Emilio assumed foundations.
**Recommendation:** Felipe should either resolve foundation type before DG-08 or explicitly flag it in engineering-package.json as a conditional item. Emilio should confirm receipt of soil study before marking all_inputs_confirmed=true.

---

### GAP-006: Executive Plans — Schema Field Mismatch and Missing client_signoff_milestone
**Severity:** Minor
**Deliverable:** executive-plans.json
**Agent:** Hugo
**Affected Score:** completeness (4/5), clarity (4/5), decision_readiness (4/5)
**Description:** The rubric requires schema fields: `plan_set_components` (with `cross_sections`, `full_plan_book`, `technical_coordination`), `engineering_integration_confirmed`, `conflicts_resolved`, `client_signoff_milestone`. The deliverable uses a `components` array instead of the exact schema, and `client_signoff_milestone` is absent.
**Impact:** All drawing types are present in the components array (cross sections included in sheet list), so the auto-fail condition (missing cross sections) is not triggered. However, the contracting entity's formal acceptance of the plan set is not explicitly captured, which creates a gap in the paper trail for a government project where formal written acceptance is important.
**Recommendation:** Hugo should use the exact schema field names from the rubric and add a `client_signoff_milestone` field logging the contracting entity's written acceptance of the executive plans (important for obra pública projects where milestone approvals are formal government acts).

---

### GAP-007: Bid Comparison — Individual Bid Line Items Not Present
**Severity:** Minor
**Deliverable:** bid-comparison.json
**Agent:** Ofelia
**Affected Score:** completeness (4/5)
**Description:** The rubric requires bids array with `line_items` per bid (cost breakdown). bid-comparison.json has bids with contractor, amount_mxn, timeline_weeks, and notes, but no line_items breakdown.
**Impact:** Marcela and the contracting entity cannot evaluate unit cost differences between bids without line items. For obra pública procurement, a detailed line-item comparison (catálogo de conceptos by bid) is typically required.
**Recommendation:** Ofelia should request line-item breakdowns (catálogo de conceptos) from each contractor and include them in the bid comparison matrix.

---

### GAP-008: DG-05 and DG-06 Dual-Routing Ambiguity (Structural Pattern Issue)
**Severity:** Low
**Affected Gates:** DG-05, DG-06
**Agent:** Celia
**Affected Score:** accuracy (4/5), clarity (4/5) for both gates
**Description:** DG-05 and DG-06 each have two files (dg-XX.json and decision-event-DG-XX.json) that route to different agents: DG-05 routes to Vera (internal architect review) in dg-05.json and to Rosa (client send) in decision-event-DG-05.json. Similarly DG-06 routes to Vera in dg-06.json and to Legal in decision-event-DG-06.json. The dual files reflect two sub-steps within a single gate ID, creating ambiguity about which is the authoritative routing event.
**Impact:** No functional routing failure — both steps execute correctly and the correct agents receive the correct tasks. However, the event model conflates two distinct routing steps under one gate ID, which complicates audit trails.
**Recommendation:** Consider separating DG-05 into DG-05a (internal architect review → Vera) and DG-05b (client proposal send → Rosa), and DG-06 into DG-06a (client proposal accepted → Legal) and DG-06b (activation → Vera). This aligns the event model with the routing reality.

---

### GAP-009: Legal Review — Public Civic Clause Legal Validity Not Explicitly Confirmed
**Severity:** Low
**Deliverable:** legal-review.json
**Agent:** Legal
**Affected Score:** completeness (4/5)
**Description:** The legal review confirms IP rights clear and raises one advisory flag on government payment timing. However, it does not explicitly confirm that the public_civic clauses (civic_procurement, public_bidding_compliance) are legally sound under the applicable Ley de Adquisiciones.
**Impact:** For a public institutional client under obra pública procurement, the legal validity of the procurement framework clauses is the primary legal risk. The review covers payment risk but not the core procurement law compliance question.
**Recommendation:** Legal should add explicit confirmation that public_civic SOW clauses comply with applicable federal or state procurement law (Ley de Adquisiciones / Ley de Obras Públicas y Servicios Relacionados).

---

### GAP-010: Celia — Consistent comment=null Across All 11 Gates
**Severity:** Low
**Affected Gates:** All 11 (DG-01 through DG-11)
**Agent:** Celia
**Affected Score:** clarity (4/5) across all Celia routing scorecards
**Description:** All 11 decision events have comment=null. In a real production run, Marcela would provide commentary at some decision points (particularly DG-05 proposal approval, DG-07 concept approval, DG-11 contractor selection) that should be captured verbatim.
**Impact:** Audit trail lacks Marcela's reasoning at key decision points. For a government project where decisions may be reviewed by oversight bodies, preserved reviewer commentary is important.
**Recommendation:** In live production runs, Celia should prompt for and capture Marcela's comment at each gate, even if brief. A null comment field should trigger a prompt for at least a brief note before the decision event is finalized.

---

### GAP-011: DG-08 and DG-09 — Internal/External Timestamp Divergence
**Severity:** Low (Observation)
**Affected Gates:** DG-08 (divergence: 3.5 months), DG-09 (divergence: 4 months), DG-10 (divergence: 5.5 months)
**Agent:** Celia
**Description:** The dg-XX.json files consistently have earlier timestamps than their decision-event-DG-XX.json counterparts for later-stage gates. For DG-08: dg-08.json=2026-06-01 vs decision-event-DG-08=2026-09-15 (3.5 months). For DG-09: dg-09=2026-07-15 vs decision-event-DG-09=2026-11-25 (4 months). This may reflect a simulation artifact rather than a production bug.
**Impact:** In production, these should be within hours or days of each other. Large divergences suggest either (a) the dg-XX.json files represent an earlier draft of the decision or (b) the event capture model has a timing artifact in simulation.
**Recommendation:** In production, Celia should create both dg-XX.json and decision-event-DG-XX.json simultaneously upon receiving Marcela's decision. Timestamp divergences > 24h should be flagged.

---

### GAP-012: DG-11 — Bid Comparison reviewed_at Post-dates DG-11 Decision
**Severity:** Low (Observation)
**Deliverable:** bid-comparison.json reviewed_at vs dg-11.json / decision-event-DG-11.json timestamps
**Description:** bid-comparison.json has reviewed_at=2027-04-10. dg-11.json has timestamp=2026-10-01. decision-event-DG-11.json has timestamp=2027-04-01. DG-11 fires (2027-04-01) before bid-comparison was reviewed (2027-04-10) by 9 days. This is a minor temporal inconsistency.
**Impact:** Minor — likely a simulation artifact. Functionally the bid comparison decision is correct. In production, the DG-11 decision event should fire after the bid comparison is reviewed and submitted.
**Recommendation:** Timing sequencing: bid-comparison.reviewed_at should precede the DG-11 timestamp. Review the event sequencing for Segment I in the simulation harness.

---

## System-Level Observations

### State Sync (Asana) — Non-Blocking Infrastructure Gap
Every deliverable scores 3/5 on state_sync per the TC-005 scoring note ("State_sync: score 3 — no live Asana"). This is expected, non-blocking, and consistent across the entire run. In production, all ASANA_UNAVAILABLE states would become live Asana task updates.

### Dual-File Decision Event Pattern
All 11 gates have two files (dg-XX.json + decision-event-DG-XX.json). This is a consistent architectural pattern. Most pairs are consistent (same decision, same route_to). Gates DG-05 and DG-06 have intentionally different route_to values reflecting two-step flows. This pattern works correctly but the naming convention conflates step-1 and step-2 of multi-step gates under a single gate ID.

### comment=null Pattern
All 11 Celia decision events have comment=null. This is a systemic gap in the simulation — no Marcela commentary is captured at any gate. For a production run with a real government client, this would be a significant audit-trail gap.

---

## Summary of Gap Severity

| Gap | Severity | Auto-Fail Risk |
|-----|----------|----------------|
| GAP-001: Questionnaire residential framing | Minor | No |
| GAP-002: Lead record raw message not verbatim | Minor | No |
| GAP-003: Concept presentation date not logged | Minor | No |
| GAP-004: Review notes are agent-generated, not Marcela's | Minor | No |
| GAP-005: Foundation type open at engineering handoff | Minor | No |
| GAP-006: Executive plans schema mismatch + missing signoff | Minor | No |
| GAP-007: Bid comparison missing line items | Minor | No |
| GAP-008: DG-05/06 dual-routing ambiguity | Low | No |
| GAP-009: Legal review missing procurement clause validation | Low | No |
| GAP-010: comment=null across all 11 gates | Low | No |
| GAP-011: Internal/external timestamp divergence | Low (Observation) | No |
| GAP-012: DG-11 timing inconsistency | Low (Observation) | No |

**No high-severity gaps. No auto-fail conditions triggered. 12 minor/low gaps, all non-blocking.**

---

## TC-005 Specific Checklist Final Status

| TC-005 Check | Status |
|---|---|
| Institutional client correctly identified throughout | PASS |
| client-fit-assessment: committee/cabildo decision-making noted | PASS |
| scope-of-work: public_civic template (not generic) | PASS |
| scope-of-work: civic_procurement_clause present | PASS |
| scope-of-work: public_bidding_clause present | PASS |
| bid-comparison: minimum 2 bids (obra pública) — NO AUTO-FAIL | PASS |
| Payment schedule: 20/15/20/25/20 public_civic template | PASS |
| All 11 Celia files: route_to field (not routed_to) | PASS |
| Controller dispatches Tax at M5 (not Vera) | PASS |
| state.json final: project_closed | PASS |
