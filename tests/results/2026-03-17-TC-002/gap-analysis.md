# Gap Analysis — TC-002
**Run ID:** 2026-03-17-TC-002
**Test Case:** Casa Vista — residential_in_development with HOA
**Date:** 2026-03-17
**Scored by:** Test Decision Gate + Gap Analysis Agent

---

## Segment Score Table

| Segment | Deliverable | Agent | Avg Score | Auto-Fail | Passed |
|---------|-------------|-------|-----------|-----------|--------|
| A | lead-record | Lupe | 4.33 | No | PASS |
| B | lead-summary | Lupe | 4.67 | No | PASS |
| B | discovery-questionnaire | Elena | 4.57 | No | PASS |
| B | client-fit-assessment | Elena | 4.67 | No | PASS |
| B | Celia DG-01 | Celia | 4.17 | No | PASS |
| B | Celia DG-02 | Celia | 3.83 | No | PASS |
| C | area-program | Ana | 4.67 | No | PASS |
| C | cost-basis | Ana | 4.50 | No | PASS |
| C | site-readiness-report | Sol | 4.50 | No | PASS |
| C | Celia DG-03 | Celia | 3.33 | No | **FAIL** |
| D | scope-of-work | Tomás | 4.67 | No | PASS |
| D | budget | Bruno | 4.00 | No | PASS |
| D | proposal | Renata | 4.67 | No | PASS |
| D | legal-review | Legal | 4.67 | No | PASS |
| D | client-communication | Rosa | 4.75 | No | PASS |
| D | Celia DG-06 | Celia | 4.17 | No | PASS |
| E | project-schedule | Pablo | 4.40 | No | PASS |
| F | concept-review | Andrés | 4.33 | No | PASS |
| F | architectural-design | Felipe | 4.67 | No | PASS |
| F | Celia DG-07 | Celia | 4.17 | No | PASS |
| F | Celia DG-08 | Celia | 4.17 | No | PASS |
| G | engineering-package | Emilio | 4.67 | No | PASS |
| G | budget-alignment | Bruno | 4.67 | No | PASS |
| G | Celia DG-09 | Celia | 4.17 | No | PASS |
| H | executive-plans | Hugo | 4.50 | No | PASS |
| H | Celia DG-10 | Celia | 4.17 | No | PASS |
| I | bid-comparison | Ofelia | 4.67 | No | PASS |
| I | permit-status | Paco | 4.60 | No | PASS |
| I | Celia DG-11 | Celia | 4.67 | No | PASS |
| J | invoice | Controller | 4.20 | No | PASS |
| J | tax-filing | Tax | 4.00 | No | PASS |

**Overall average:** 4.37 / 5.00
**Deliverables scored:** 31
**Auto-fails:** 0
**Scorecards PASS:** 30 / 31
**Scorecards FAIL:** 1 / 31

---

## TC-002 Specific Checks

| Check | Result | Evidence |
|-------|--------|----------|
| HOA coordination clause in scope-of-work.json | PASS | project_type_clauses: "hoa_coordination_clause" present |
| Covenant review clause in scope-of-work.json | PASS | project_type_clauses: "covenant_review_clause" present |
| Area program notes 7m height limit | PASS | assumptions: "HOA height limit of 7m is taken into account for massing — 337 sqm program distributed across two stories to stay under 7m; no three-story configuration" |
| No hydrologic study in site-readiness-report | PASS | Only topo, HOA guidelines, and escrituras requested — no hydrologic study for slight-slope site |
| Client fit assessment uses standard individual scoring | PASS | Four-dimension individual assessment (not institutional): design_engagement, budget_realism, scope_clarity, collaborative_style |

---

## GAP Entries

### GAP-TC002-001 — Celia DG-03: route_to incorrectly set to 'Marcela'

**Severity:** Medium
**Segment:** C
**Gate:** DG-03
**Agent:** Celia
**Scorecard:** segment-C-celia-routing-DG03-scorecard.json
**Score:** 3.33 / 5.00 (FAIL)

**Finding:** In `decision-event-dg03.json`, the `route_to` field is populated as `"Marcela"` when it should be `"Tomás"`. At DG-03 (cost-basis approved), the correct next agent is Tomás, who should be dispatched to produce the Segment D scope-of-work. Marcela is the reviewer at DG-03, not the recipient of the routing.

The `next_action` field correctly states `"dispatch_tomas_segment_d"` — creating an internal inconsistency between the two fields. In a live run, a system consuming `route_to` to dispatch the next agent would route to Marcela (wrong), potentially stalling the pipeline or creating a redundant review loop.

**Evidence:**
- `decision-event-dg03.json` → `route_to: "Marcela"` (incorrect)
- `decision-event-dg03.json` → `next_action: "dispatch_tomas_segment_d"` (correct intent)
- Correct value: `route_to: "Tomás"`

**Impact:** In a live execution, this routing error would send the DG-03 dispatch payload to Marcela rather than Tomás. Tomás would not receive the activation signal to begin the SOW. Depending on error-handling design, this could stall Segment D.

**Recommendation:** Correct `route_to` field in `decision-event-dg03.json` to `"Tomás"`. Review Celia's routing table implementation to ensure route_to is populated from the routing table lookup (not from reviewed_by field, which appears to have been incorrectly substituted here).

---

### MINOR OBSERVATIONS (not GAP-level)

**OBS-TC002-001 — Celia comment=null at 8 of 9 gates**
All Celia decision events except DG-11 have `comment=null`. This is technically correct when Marcela provides no written comment, but indicates that no Marcela feedback is being captured through most of the pipeline. Only DG-11 (bid comparison) has a non-null comment. This reduces Celia clarity scores to 3 across most gates. Not a system failure — Marcela did not provide comments — but represents a pattern to watch in live runs.

**OBS-TC002-002 — Invoice and tax-filing use placeholder bank details and CFDI**
`invoice.json` payment_instructions contain `[BANK_NAME]` and `[CLABE — TO BE CONFIGURED IN .env]` placeholders. `tax-filing.json` has `[CFDI — TO BE GENERATED BY ACCOUNTANT]`. These are expected in simulated test mode (seed data is not a live client), but in a live project these would be auto-fail conditions. Production readiness check: confirm .env configuration of bank credentials before first live invoice.

**OBS-TC002-003 — Cost-basis minor rounding inconsistency**
`cost-basis.json` total_estimate field shows 10,230,840 MXN while the arithmetic in assumptions calculates to 10,231,320 MXN — a MXN 480 discrepancy. The assumptions text acknowledges "minor rounding applied" but actually states two different totals (10,231,320 and 10,230,840) within the same assumptions array. Not material (0.005% variance) but an indicator of rounding logic that should be standardized.

**OBS-TC002-004 — Concept review lacks in-person presentation date**
`concept-review.json` → `presentation_milestone: "M2 — Concept Design Approved"` names the milestone but does not log a specific date for the in-person presentation event. Rubric requires the in-person presentation to be logged as a milestone with date. Scored 4 rather than 5 on completeness. Recommend adding a `presentation_date` field to the concept-review schema.

**OBS-TC002-005 — DG-02 route_to captures only Ana (not Sol in parallel)**
`decision-event-dg02.json` → `route_to: "Ana"` while `next_action: "dispatch_ana_and_sol_parallel"`. Sol's parallel dispatch is documented in next_action but not in route_to. In a system consuming route_to for dispatch, Sol may not receive the activation signal from Celia directly. Minor gap — scored 4 rather than 5 on accuracy.

---

## Summary

The TC-002 pipeline is functionally sound across all 10 segments. All TC-002 specific checks (HOA clauses, 7m height limit, no hydrologic study, standard individual fit assessment) pass. The single FAIL is a Celia routing field error at DG-03 (route_to='Marcela' instead of 'Tomás') that would stall the pipeline in a live run. No auto-fail conditions were triggered on any deliverable. Overall average score is 4.37/5.00 — strong performance for a residential_in_development project with full HOA overlay.
