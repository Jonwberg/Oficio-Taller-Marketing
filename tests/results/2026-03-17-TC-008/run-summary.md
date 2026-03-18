# TC-008 Run Summary
**Run ID:** 2026-03-17-TC-008
**Test Case:** Edge — Site Complications (hydrology blocker)
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `project_closed`
**Scored by:** Decision Gate + Gap Analysis Agent

---

## Segment Results

| Segment | Agents | Result |
|---------|--------|--------|
| A | Lupe | PASS |
| B | Lupe, Celia, Elena, Celia | PASS |
| C | Ana, Sol, Vera, Celia | PASS |
| D | Tomás, Vera, Bruno, Renata, Legal, Vera, Rosa, Celia | PASS |
| E | Vera (blocked — hydrology pending 6 wks), Pablo (after resolution) | PASS |
| F | Andrés, Celia, Felipe, Celia | PASS |
| G | Emilio, Bruno, Celia | PASS |
| H | Hugo, Celia | PASS |
| I | Ofelia, Celia, Paco | PASS |
| J | Vera, Controller ×3, Tax | PASS |

**Overall: 10/10 segments PASS**

---

## Scored Deliverable Table

| Deliverable | Segment | Agent | Avg Score | Auto-Fail | Result |
|---|---|---|---|---|---|
| lead-record | A | Lupe | 4.67 | No | PASS |
| lead-summary | B | Lupe | 4.67 | No | PASS |
| discovery-questionnaire | B | Elena | 4.43 | No | PASS |
| client-fit-assessment | B | Elena | 4.67 | No | PASS |
| area-program | C | Ana | 4.67 | No | PASS |
| cost-basis | C | Ana | 4.67 | No | PASS |
| site-readiness-report | C | Sol | 4.67 | No | PASS |
| scope-of-work | D | Tomás | 4.50 | No | PASS |
| budget | D | Bruno | 4.00 | No | PASS |
| proposal | D | Renata | 4.67 | No | PASS |
| legal-review | D | Legal | 4.50 | No | PASS |
| client-communication | D | Rosa | 4.63 | No | PASS |
| project-schedule | E | Pablo | 4.60 | No | PASS |
| activation-gate | E | Vera | 5.00 | No | PASS |
| hydrology-resolution | E | Vera | 5.00 | No | PASS |
| concept-review | F | Andrés | 4.67 | No | PASS |
| architectural-design | F | Felipe | 4.50 | No | PASS |
| engineering-package | G | Emilio | 4.17 | No | PASS |
| budget-alignment | G | Bruno | 4.67 | No | PASS |
| executive-plans | H | Hugo | 4.67 | No | PASS |
| bid-comparison | I | Ofelia | 4.67 | No | PASS |
| permit-status | I | Paco | 4.60 | No | PASS |
| invoice | J | Controller | 4.00 | No | PASS |
| tax-filing | J | Tax | 3.80 | No | PASS |

**Deliverable average: 4.51 / 5.00**

---

## Celia Routing Events

| Gate | Segment | Decision | route_to | All 11 Fields | Avg Score | Result |
|---|---|---|---|---|---|---|
| DG-01 | B | approve | Lupe | Yes | 4.33 | PASS |
| DG-02 | B | approve | Ana, Sol | Yes | 4.33 | PASS |
| DG-03 | C | approve | Tomás | Yes | 4.67 | PASS |
| DG-04 | D | approve | Bruno | Yes | 4.33 | PASS |
| DG-05 | D | approve | Rosa | Yes | 4.33 | PASS |
| DG-06 | D | approve | Legal | Yes | 4.33 | PASS |
| DG-07 | F | approve | Felipe | Yes | 4.67 | PASS |
| DG-08 | F | approve | Emilio | Yes | 4.33 | PASS |
| DG-09 | G | approve | Hugo | Yes | 4.67 | PASS |
| DG-10 | H | approve | Ofelia | Yes | 4.33 | PASS |
| DG-11 | I | approve | Paco | Yes | 4.67 | PASS |

**Celia routing average: 4.45 / 5.00**
**All 11 gates: route_to field used (not routed_to)**

---

## Overall Averages

| Category | Avg Score |
|---|---|
| Deliverables (24 scorecards) | 4.51 |
| Celia routing (11 scorecards) | 4.45 |
| **Combined (35 scorecards)** | **4.49** |

---

## TC-008 Critical Check Results

| Check | Result |
|-------|--------|
| Sol requests BOTH topo AND hydrologic study (stream on site) | PASS |
| Activation gate blocked: gate_status='blocked' | PASS |
| Blocker correctly identified: hydrologic_study_pending | PASS |
| site_data_complete=false during block | PASS |
| Pablo NOT dispatched during hydrology block | PASS |
| Vera holds activation gate — does NOT activate until study received | PASS |
| hydrology-study-received: blocker_resolved=true | PASS |
| hydrology-study-received: site_data_complete=true | PASS |
| Pablo dispatched only after hydrology resolved | PASS |
| scope-of-work: commercial_hotel template (CH-001 through CH-005) | PASS |
| CH-004 hydrologic setback clause (CONAGUA cited) | PASS |
| Stream setback (15m) tracked through design phases | PASS |
| Permit correction: CONAGUA addendum required and resolved | PASS |
| All Celia payloads use route_to (not routed_to) | PASS |
| Final state: project_closed | PASS |

**15/15 TC-008 critical checks: PASS**

---

## Gap Summary (Non-Blocking)

| Gap | Segment | Severity | Type |
|---|---|---|---|
| Engineering consultants all TBD — all_inputs_confirmed=true declared without actual confirmations | G | Minor | Data completeness |
| SOW checklist items 10/12/20 absent (irrigation, contractor validation, e-signature) | D | Minor | Scope completeness |
| Discovery questionnaire sent in Spanish to English-speaking client | B | Minor | Language matching |
| Budget.json structured as M1 invoice only — M2/M3 not in summary_milestones | D | Minor | Structure completeness |
| Tax filing: CFDI reference is placeholder | J | Minor | Test-mode limitation |
| Invoice: bank/CLABE are .env placeholders | J | Minor | Test-mode limitation |
| Celia: 7 of 11 events have comment=null instead of explicit "no comment" | All | Cosmetic | Auditability |

**Blocking gaps: 0**
**Auto-fail conditions triggered: 0**

---

Full scorecards: `tests/results/2026-03-17-TC-008/`
Gap analysis: `tests/results/2026-03-17-TC-008/gap-analysis.md`
