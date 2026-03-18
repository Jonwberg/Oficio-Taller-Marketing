# TC-003 Run Summary
**Run ID:** 2026-03-17-TC-003
**Test Case:** Wellness Retreat — commercial_hotel with hydrologic study
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
| Sol requests BOTH topo AND hydrologic study (arroyo) | ✅ PASS |
| commercial_hotel SOW template + hospitality_compliance_clause | ✅ PASS |
| Emilio includes greywater and AV systems | ✅ PASS |
| 2+ bids collected (Segment I) | ✅ PASS |
| All Celia payloads use route_to (not routed_to) | ✅ PASS |
| Final state: project_closed | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-003/`
