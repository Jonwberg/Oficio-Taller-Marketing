# TC-009 Run Summary
**Run ID:** 2026-03-17-TC-009
**Test Case:** Casa Horizonte — Familia Reyes-Montoya
**Date:** 2026-03-17
**Mode:** LIVE (real Asana + real Gmail)
**Final State:** `project_closed` ✅

---

## Segment Results

| Segment | Agents | Result | Live Artifacts |
|---------|--------|--------|----------------|
| A | Lupe, Celia | ✅ PASS | Asana GID `1213707386907008`, Gmail `19cfef6d63ede45e` |
| B | Elena, Celia | ✅ PASS | Asana DG-01 `1213707387212379`, DG-02 `1213707395516777`, Gmail `19cfefe78e98fd60`, `19cfefdb3cc4566d` |
| C | Ana, Sol, Vera | ✅ PASS | area-program.json (356 sqm), site-readiness-report.json (3 docs), DG-03 `19cff0be8b4012c8` |
| D | Tomás, Bruno, Renata, Legal, Rosa | ✅ PASS | scope-of-work.json, budget.json (USD 90K), proposal.json, DG-04 `19cff11f664e365c`, DG-05 `19cff140ceeb7cd4`, DG-06 `19cff14bcda640d7`, proposal to client `19cff1532ce051b0` |
| E | Vera, Pablo | ✅ PASS | project-schedule.json (6 phases), Asana `1213707884639976` with 6 subtasks |
| F | Andrés, Felipe | ✅ PASS | concept-review.json, architectural-design.json, DG-07 `19cff30a3373e6cd`, DG-08 `19cff30a9615578e` |
| G | Emilio, Bruno | ✅ PASS | engineering-package.json (solar included), budget-alignment.json (proceed, -17%), DG-09 `19cff30ac578ed1f` |
| H | Hugo | ✅ PASS | executive-plans.json (7 components), DG-10 `19cff32b3083a34d` |
| I | Ofelia, Paco | ✅ PASS | bid-comparison.json (2 bids), permit-status.json (approved, 2 corrections), DG-11 `19cff347d2233683` |
| J | Vera, Controller, Tax | ✅ PASS | invoice.json (M3, USD 90K total), tax-filing.json, state → project_closed |

**Overall: 10/10 segments PASS**

---

## Scored Segment Table (TC-009 Decision Gate Agent Scoring)

| Segment | Deliverable | Agent | Avg Score | Auto-Fail | Passed |
|---------|------------|-------|-----------|-----------|--------|
| A | lead-record | Lupe | 5.00 | No | ✅ |
| B | lead-summary | Lupe | 4.83 | No | ✅ |
| B | discovery-questionnaire | Elena | 4.86 | No | ✅ |
| B | client-fit-assessment | Elena | 4.83 | No | ✅ |
| B | Celia DG-01 routing | Celia | 4.83 | No | ✅ |
| B | Celia DG-02 routing | Celia | 4.83 | No | ✅ |
| C | area-program | Ana | 4.67 | No | ✅ |
| C | cost-basis | Ana | 4.83 | No | ✅ |
| C | site-readiness-report | Sol | 4.67 | No | ✅ |
| C | Celia DG-03 routing | Celia | 4.83 | No | ✅ |
| D | scope-of-work | Tomás | 4.83 | No | ✅ |
| D | budget | Bruno | 4.20 | No | ✅ |
| D | proposal | Renata | 4.83 | No | ✅ |
| D | legal-review | Legal | 4.67 | No | ✅ |
| D | client-communication | Rosa | 5.00 | No | ✅ |
| D | Celia DG-04 routing | Celia | 4.83 | No | ✅ |
| D | Celia DG-05 routing | Celia | 4.83 | No | ✅ |
| D | Celia DG-06 routing | Celia | 4.83 | No | ✅ |
| E | project-schedule | Pablo | 5.00 | No | ✅ |
| F | concept-review | Andrés | 4.50 | No | ✅ |
| F | architectural-design | Felipe | 4.83 | No | ✅ |
| F | Celia DG-07 routing | Celia | 4.83 | No | ✅ |
| F | Celia DG-08 routing | Celia | 4.83 | No | ✅ |
| G | engineering-package | Emilio | 4.83 | No | ✅ |
| G | budget-alignment | Bruno | 4.83 | No | ✅ |
| G | Celia DG-09 routing | Celia | 4.83 | No | ✅ |
| H | executive-plans | Hugo | 4.50 | No | ✅ |
| H | Celia DG-10 routing | Celia | 4.83 | No | ✅ |
| I | bid-comparison | Ofelia | 4.83 | No | ✅ |
| I | permit-status | Paco | 4.80 | No | ✅ |
| I | Celia DG-11 routing | Celia | 4.83 | No | ✅ |
| J | invoice | Controller | 4.20 | No | ✅ |
| J | tax-filing | Tax | 4.00 | No | ✅ |

**Deliverable average (22 scorecards):** 4.67 / 5.0
**Celia routing average (11 scorecards):** 4.83 / 5.0
**Combined average (33 scorecards):** 4.73 / 5.0
**Auto-fail rate:** 0%
**Pass rate:** 33/33 (100%)

---

## TC-009 Key Verification Points

| Check | Required | Result |
|-------|----------|--------|
| `standalone_residential` SOW template applied (Segment D) | ✅ | PASS |
| Sol's site readiness includes `coastal_zone_permit` in required_documents | ✅ | PASS |
| Sol's site readiness includes `wind_load_study` in required_documents | ✅ | PASS |
| `site_data_complete` set by Sol; `site_docs_complete` null until operator sets | ✅ | PASS |
| Vera does NOT send DG-03 until both flags true AND `awaiting_gate` null | ✅ | PASS |
| Emilio includes `solar` in `systems_status` | ✅ | PASS |
| Paco sets `permit_status` in Asana (not `project_state`) | ✅ | PASS |
| Controller dispatches Tax at final milestone (not Vera) | ✅ | PASS |
| All 11 Celia decision events have `route_to` field (not `routed_to`) | ✅ | PASS — DG-01 through DG-11 all use `route_to` |
| SEMARNAT corrections array populated before approved | ✅ | PASS — 2 correction rounds documented |
| Payment schedule 40/30/30 in USD from seed data | ✅ | PASS |

**All 11 key verification points: PASS**

---

## Edge Conditions Exercised

| Edge Condition | Status |
|---------------|--------|
| Coastal permit adds lead time — SEMARNAT Phase 6 starts in parallel with Phase 2 (2026-04-28) | ✅ |
| `corrections` array in permit-status.json populated (2 rounds) before `approved` | ✅ |
| Wind load study affects structural engineering — Emilio notes coastal conditions in structural entry | ✅ |
| `site_docs_complete` distinction from `site_data_complete` — operator sets manually | ✅ |
| Solar in scope → Emilio includes `solar` in conditional_systems | ✅ |
| Controller dispatches Tax (not Vera) at `final_milestone: true` | ✅ |

---

## Live Integration Summary

**Asana:** 30 tasks created across Leads, Finanzas, Legal, Decisiones, Handoffs projects. All tasks completed with milestone comments.

**Gmail:** 14 real emails sent:
- DG-01 through DG-11 review emails to Marcela
- Client questionnaire, site document request, proposal delivery

**Total architecture fee collected:** USD 90,000 (3 milestones × running_total = $90,000 confirmed)

**Final project state:** `project_closed`
