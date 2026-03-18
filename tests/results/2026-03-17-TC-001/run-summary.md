# TC-001 Run Summary
**Run ID:** 2026-03-17-TC-001
**Test Case:** Casa Moderna — standalone_residential happy path
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `project_closed` ✅

## Segment Results

| Segment | Agents | Result |
|---------|--------|--------|
| A | Lupe | ✅ PASS |
| B | Lupe, Celia, Elena, Celia | ✅ PASS |
| C | Ana, Sol, Vera, Celia | ✅ PASS |
| D | Tomás, Vera, Bruno, Renata, Legal, Vera, Rosa, Celia | ✅ PASS |
| E | Vera, Pablo | ✅ PASS |
| F | Andrés, Celia, Felipe, Celia | ✅ PASS |
| G | Emilio, Bruno, Celia | ✅ PASS |
| H | Hugo, Celia | ✅ PASS |
| I | Ofelia, Celia, Paco | ✅ PASS |
| J | Vera, Controller ×3, Tax | ✅ PASS |

**Overall: 10/10 segments PASS**

## Key Verification Points

| Check | Result |
|-------|--------|
| standalone_residential SOW template applied | ✅ PASS |
| No hydrologic study (flat site) | ✅ PASS |
| DG-07 route_to field (not routed_to) | ✅ PASS |
| All 11 Celia payload fields at every gate | ✅ PASS |
| Final state: project_closed | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-001/`
