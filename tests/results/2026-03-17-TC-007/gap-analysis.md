# Gap Analysis — 2026-03-17-TC-007

**Test Case:** TC-007 Edge — Bad Lead (Spam Discard)
**Date:** 2026-03-17
**Segments scored:** A only (single-segment TC)
**Total scorecards:** 2

## Overall Scores by Segment

| Segment | Agents | Avg Score (Lead Record) | Avg Score (Spam Classification) | Auto-Fail | Result |
|---------|--------|-------------------------|---------------------------------|-----------|--------|
| A | Lupe | 4.17 | 5.0 | — | PASS |

## Score Detail — Segment A

### Lead Record (DG-01 / Marcela gate)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Completeness | 3/5 | All required fields present; raw message summarized, not verbatim |
| Accuracy | 5/5 | source_channel and spam category both correct |
| Clarity | 4/5 | Summary is immediately clear and evidence-backed for a spam record |
| State Sync | 3/5 | project_state and awaiting_gate correct; Asana task shows ASANA_UNAVAILABLE |
| Timing | 5/5 | discarded_at within 5 seconds of received_at — same session |
| Decision Readiness | 5/5 | All fields sufficient for a discard decision; no downstream review needed |
| **Average** | **4.17** | |

### Spam Classification (TC-007-segment-A-spam-confirmed.json)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Spam reason specific and evidence-based | 5/5 | Four concrete signals cited, including specific URL |
| All spam signals identified | 5/5 | Commercial offer, no qualifying fields, promo link, automated pattern — all captured |
| Classification decision unambiguous | 5/5 | "spam" with no hedging; multi-signal justification |
| **Average** | **5.0** | |

## Critical Findings

None — spam correctly classified and discarded. No false-positive risk. No downstream agents dispatched.

### Minor Gaps (non-blocking)

1. **Completeness score 3 — raw message not verbatim preserved.** The lead-record summary paraphrases the inbound message rather than storing the original text verbatim. For spam records this is low-stakes, but the rubric requires verbatim storage for a score of 5. Future runs should include a `raw_message` field.

2. **State Sync score 3 — Asana unavailable.** The state.json `tasks.lead_intake` value is `ASANA_UNAVAILABLE` rather than a confirmed task ID. This is a simulated-environment limitation, not a logic error in Lupe's behavior, and does not affect the pass verdict.

## Summary

TC-007 Segment A passes cleanly: Lupe correctly identified an inbound commercial spam message, classified it as "spam" with a multi-signal, evidence-based rationale, set status to "discarded", and halted the pipeline — no downstream agents were invoked. The two minor scoring gaps (raw message not verbatim, Asana unavailable) are environmental or rubric-precision issues that carry no operational risk in this edge-case scenario.
