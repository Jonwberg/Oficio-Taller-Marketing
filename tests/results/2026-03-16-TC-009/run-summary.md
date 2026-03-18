# Run Summary — TC-009 Casa Horizonte
## Run ID: 2026-03-16-TC-009
## Date: 2026-03-16
## Overall: PASS

---

## Segment Results

| Segment | Agents | Schema | TC-009 Checks | Result |
|---------|--------|--------|---------------|--------|
| A — Lead Intake | Lupe | PASS | N/A | PASS |
| B — Discovery | Lupe, Celia (DG-01), Elena, Celia (DG-02) | PASS | PASS | PASS |
| C — Site & Area Program | Ana, Sol, Vera (site_status_update), Celia (DG-03) | PASS | PASS | PASS |
| D — Scope / Budget / Proposal / Legal | Tomás, Vera (DG-04/05), Celia (DG-04/05/06), Bruno, Renata, Legal, Rosa | PASS | PASS | PASS |
| E — Activation & Scheduling | Vera (activation_check), Pablo | PASS | PASS | PASS |
| F — Concept & Architectural Design | Andrés (w/ revision cycle), Celia (DG-07), Felipe, Celia (DG-08) | PASS | PASS | PASS |
| G — Engineering & Budget Alignment | Emilio, Bruno (budget_alignment), Celia (DG-09) | PASS | PASS | PASS |
| H — Executive Plans | Hugo, Celia (DG-10) | PASS | PASS | PASS |
| I — Bidding, Contractor Selection, Permitting | Ofelia, Celia (DG-11), Paco | PASS | PASS | PASS |
| J — Construction Tracking, Invoicing, Tax, Close | Vera (construction_tracking), Controller (M1/M2/M3), Tax | PASS | PASS | PASS |

**All 10 segments: PASS**

---

## Final Project State

**project_state:** `project_closed`

| Field | Value |
|-------|-------|
| project_id | PRJ-2026-0316-familia-reyes-montoya |
| project_state | project_closed |
| project_type | standalone_residential |
| awaiting_gate | null |
| review_thread_id | null |
| area_program_complete | true |
| site_data_complete | true |
| site_docs_complete | true |
| contract_signed | true |
| deposit_confirmed | true |
| segment_d_complete | true |
| segment_e_complete | true |
| segment_f_complete | true |
| segment_g_complete | true |
| segment_j_complete | true |
| asana_project_id | null (ASANA_UNAVAILABLE throughout) |

Expected final state per TC-009: `closed` — Actual: `project_closed` — **PASS**

---

## TC-009 Specific Checks

| Check | Segment | Result |
|-------|---------|--------|
| standalone_residential SOW template applied (no mixed clauses) | D | PASS |
| Sol's site readiness request includes coastal_zone_permit | C | PASS |
| Sol's site readiness request includes wind_load_study | C | PASS |
| site_data_complete set by Sol | C | PASS |
| site_docs_complete remains null until operator sets manually | C | PASS |
| Vera does not send DG-03 until area_program_complete AND site_data_complete AND awaiting_gate null | C | PASS |
| Emilio includes solar in systems_status (in special_features) | G | PASS |
| Emilio excludes irrigation from systems_status (not in special_features) | G | PASS |
| Emilio excludes AV from systems_status (not in special_features) | G | PASS |
| Paco sets permit_status in Asana (not project_state) | I | PASS |
| Coastal permit cycles through pending_corrections before approved | I | PASS |
| corrections array populated with specific description (not empty) | I | PASS |
| Corrections resolved before final approved status | I | PASS |
| Controller dispatches Tax on final milestone (not Vera) | J | PASS |
| All 11 Celia payload fields at every Marcela gate (DG-01 through DG-11) | All | PASS |
| route_to field used (not routed_to) at every gate | All | PASS |
| Andrés DG-07 revision cycle: reject then approve | F | PASS |
| Felipe wind load requirements in structural coordination notes | F | PASS |
| Felipe salt-resistant materials in structural coordination notes | F | PASS |
| All 10 area program spaces in Felipe's design set, deviations = [] | F | PASS |
| Coastal permit lead time in schedule dependencies (Phase 6 + dependency graph) | E | PASS |
| Vera dispatches Pablo only after all 3 activation conditions met | E | PASS |
| Pablo state = schedule_complete (not redundant active_in_progress overwrite) | E | PASS |
| Coastal zone compliance component in Hugo's executive plans | H | PASS |
| Wind load structural set in Hugo's executive plans | H | PASS |
| Controller M2 write failure: backup retained on failure | J | PASS |
| Controller M2 write failure: WRITE_FAILED logged | J | PASS |
| Controller M2 write failure: re-dispatch triggered | J | PASS |
| Controller M2 write failure: retry succeeded | J | PASS |
| Controller M2 write failure: backup deleted after retry | J | PASS |
| running_total at M3 = $90,000 exactly | J | PASS |
| Invoice amounts match SOW payment schedule (40/30/30) | J | PASS |
| rfc = TEST-RFC-009 in tax-filing.json | J | PASS |
| revenue_amount = 90,000 in tax-filing.json | J | PASS |
| tax_jurisdiction = Mexico — IVA 16% | J | PASS |
| cfdi_reference is placeholder (not fabricated) | J | PASS |
| project_state = project_closed after Tax | J | PASS |

**All 37 TC-009 specific checks: PASS**

---

## Issues

None — clean run.

All segments passed. All TC-009 specific checks passed. All schema validations passed. No auto-fail conditions triggered.

**Infrastructure notes (non-blocking):**
- ASANA_UNAVAILABLE throughout all segments — all Asana calls logged and continued per agent protocol. All tasks.* IDs are null in state.json.
- GMAIL_UNAVAILABLE at multiple points (DG-03 client document request, DG-04/05/06 gate emails, DG-08/10/11 review emails) — all logged, simulated responses used per test harness, pipeline continued correctly.

Neither infrastructure condition caused a failure or incorrect pipeline behavior.
