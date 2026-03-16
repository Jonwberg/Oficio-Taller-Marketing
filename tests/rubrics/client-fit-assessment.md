# Rubric: Client Fit Assessment
**Agent:** Elena
**Deliverable:** Fit summary sent to Marcela after first meeting (DG-02)

## Schema (Execution Agent validates — pass/fail)
Required fields: meeting_notes, assessment_dimensions, recommendation, rationale

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All four assessment dimensions present: design engagement level, budget realism relative to program, scope clarity, collaborative working style indicators
3: Three of four dimensions present
1: Missing design engagement or budget realism assessment

**Accuracy (1–5)**
5: Meeting notes attributed correctly (what the client said vs Elena's interpretation clearly separated)
3: Notes summarized but attribution clear from context
1: Notes mixed with interpretation, no way to distinguish

**Clarity (1–5)**
5: Recommendation is explicit — "proceed", "decline", or "request more information" — no ambiguity
3: Recommendation implied but not stated directly
1: No recommendation present

**State Sync (1–5)**
5: Asana state updated to discovery_completed; fit summary sent to Marcela via correct channel
3: Summary sent but state not updated
1: Neither summary sent nor state updated

**Timing (1–5)**
5: Fit assessment sent to Marcela within 24h of first meeting
3: Sent within 48h
1: Not sent or excessive delay

**Decision Readiness (1–5)**
5: Any red flags documented with specific evidence from meeting; Marcela can decide immediately
3: Red flags mentioned but not substantiated
1: Marcela cannot make a fit decision from this assessment without follow-up

## Auto-Fail Conditions
- No explicit recommendation (proceed / decline / more info)
- Any of the four required assessment dimensions missing
