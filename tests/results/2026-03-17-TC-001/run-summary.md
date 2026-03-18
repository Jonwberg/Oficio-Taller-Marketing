# TC-001 Run Summary
**Run ID:** 2026-03-17-TC-001
**Test Case:** Casa Moderna — standalone_residential happy path
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `project_closed` ✅

## Segment Results

| Segment | Agents | Avg Score | Auto-Fail | Celia/Vera OK | Result |
|---------|--------|-----------|-----------|---------------|--------|
| A | Lupe | 4.33 | — | N/A | PASS |
| B | Lupe, Celia, Elena | 4.54 | — | ✓ | PASS |
| C | Ana, Sol, Vera, Celia | 4.34 | — | ✓ | PASS |
| D | Tomás, Vera, Bruno, Renata, Legal, Rosa, Celia | 3.88 | budget.json ⚠ | ✓ | FAIL |
| E | Vera, Pablo | 3.80 | — | N/A | PASS (gaps) |
| F | Andrés, Celia, Felipe | 4.34 | — | ✓ | PASS |
| G | Emilio, Bruno, Celia | 4.61 | — | ✓ | PASS |
| H | Hugo, Celia | 4.42 | — | ✓ | PASS |
| I | Ofelia, Celia, Paco | 3.83 | permit-status.json ⚠ | ✓ | FAIL |
| J | Vera, Controller, Tax | 3.90 | — | N/A | PASS (gaps) |

**Overall average score: 4.36 / 5.0**
**Scorecards written: 31 (22 deliverable + 9 Celia routing)**
**Auto-fail triggers: 2**

## Summary

The pipeline ran end-to-end cleanly with strong performance in Segments B, G, and H (all averaging above 4.4). Two auto-fail conditions were identified: Bruno's budget.json is missing four required schema fields (project_name, client_name, milestone_name, payment_instructions), and Paco's permit-status.json is missing submitted_at and jurisdiction — the two most structurally incomplete deliverables in the run. Celia's routing was correct at all nine gates (all 11 payload fields present, all route_to values verified correct), which is the strongest result in the test. The highest scoring segment was G (Engineering + Budget Alignment at 4.61); the lowest scoring individual deliverable was Bruno's budget.json at 2.60.

## Key Verification Points

| Check | Result |
|-------|--------|
| standalone_residential SOW template applied | ✅ PASS |
| No hydrologic study (flat site) | ✅ PASS |
| DG-07 route_to field (not routed_to) | ✅ PASS |
| All 11 Celia payload fields at every gate | ✅ PASS |
| All Celia route_to values correct | ✅ PASS |
| Final state: project_closed | ✅ PASS |
| budget.json required fields complete | ❌ FAIL — missing project_name, client_name, milestone_name, payment_instructions |
| permit-status.json required fields complete | ❌ FAIL — missing submitted_at, jurisdiction |
| Construction start after permit approval | ❌ FAIL — schedule shows construction 2026-09-15, permit approved 2026-11-01 |
| project-schedule.json dependencies field | ⚠ GAP — field absent |
| client-communication.json status=draft | ⚠ GAP — status='sent' before Marcela approval |

Full results: `tests/results/2026-03-17-TC-001/`
Gap analysis: `tests/results/2026-03-17-TC-001/gap-analysis.md`
