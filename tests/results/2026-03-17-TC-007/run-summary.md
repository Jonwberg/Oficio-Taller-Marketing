# TC-007 Run Summary
**Run ID:** 2026-03-17-TC-007
**Test Case:** Edge — Bad Lead (Spam)
**Date:** 2026-03-17
**Mode:** Simulated
**Final State:** `lead_discarded` ✅

## Segment Results

| Segment | Agent | Result |
|---------|-------|--------|
| A | Lupe | ✅ PASS — classified spam, discarded, pipeline stopped |

**Overall: 1/1 segments PASS**

## Scored Results (Decision Gate Agent)

| Segment | Agent | Deliverable | Avg Score | Auto-Fail | Passed |
|---------|-------|-------------|-----------|-----------|--------|
| A | Lupe | lead-record | 4.17 / 5.0 | false | ✅ PASS |
| A | Lupe | spam-classification | 5.0 / 5.0 | false | ✅ PASS |

**Scorecards written:** 2
**Gap analysis:** `tests/results/2026-03-17-TC-007/gap-analysis.md`

## Key Verification Points

| Check | Result |
|-------|--------|
| Lupe classifies category as "spam" | ✅ PASS |
| No DG-01 sent to Marcela | ✅ PASS |
| No Elena, Ana, Sol, or downstream agent dispatched | ✅ PASS |
| lead-record.json status = "discarded" | ✅ PASS |
| TC-007-segment-A-spam-confirmed.json written | ✅ PASS |
| state.json project_state = "lead_discarded" | ✅ PASS |

Full results: `tests/results/2026-03-17-TC-007/`
