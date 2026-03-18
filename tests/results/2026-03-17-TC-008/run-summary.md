# TC-008 Run Summary
**Run ID:** 2026-03-17-TC-008
**Test Case:** Edge — Site Complications (hydrology blocker)
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
| E | Vera (blocked — hydrology pending 6 wks), Pablo (after resolution) | ✅ PASS |
| F | Andrés, Celia, Felipe, Celia | ✅ PASS |
| G | Emilio, Bruno, Celia | ✅ PASS |
| H | Hugo, Celia | ✅ PASS |
| I | Ofelia, Celia, Paco | ✅ PASS |
| J | Vera, Controller ×3, Tax | ✅ PASS |

**Overall: 10/10 segments PASS**

## Key Verification Points

| Check | Result |
|-------|--------|
| Sol requests BOTH topo AND hydrologic study (stream on site) | ✅ PASS |
| Activation gate blocked: activation_delayed_by_hydrology | ✅ PASS |
| Vera holds activation gate — does NOT activate until study received | ✅ PASS |
| site_data_pending state set explicitly before hydrology resolved | ✅ PASS |
| All Celia payloads use route_to (not routed_to) | ✅ PASS |
| Final state: project_closed | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-008/`
