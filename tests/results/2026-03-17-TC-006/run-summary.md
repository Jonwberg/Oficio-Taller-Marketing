# TC-006 Run Summary
**Run ID:** 2026-03-17-TC-006
**Test Case:** Edge — Budget Mismatch (redesign loop)
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
| G | Emilio, Bruno (reject), Felipe (redesign), Bruno (approve), Celia | ✅ PASS |
| H | Hugo, Celia | ✅ PASS |
| I | Ofelia, Celia, Paco | ✅ PASS |
| J | Vera, Controller ×3, Tax | ✅ PASS |

**Overall: 10/10 segments PASS**

## Key Verification Points

| Check | Result |
|-------|--------|
| DG-09 first pass: budget_misaligned (reject) | ✅ PASS |
| Redesign loop triggered: pool removed, 160sqm | ✅ PASS |
| DG-09 second pass: budget_aligned (approve) | ✅ PASS |
| Executive plans only after budget_aligned | ✅ PASS |
| All Celia payloads use route_to (not routed_to) | ✅ PASS |
| Final state: project_closed | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-006/`
