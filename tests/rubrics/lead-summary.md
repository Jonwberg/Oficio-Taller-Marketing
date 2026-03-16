# Rubric: Lead Summary
**Agent:** Lupe
**Deliverable:** Structured summary sent to Marcela for review (DG-01)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, source_channel, raw_message, initial_assessment, recommended_action

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Source, channel, raw message, classification, and initial assessment all present
3: Most fields present, one minor omission
1: Missing source or raw message

**Accuracy (1–5)**
5: Project type classified correctly; legitimacy assessment is defensible
3: Classification approximately right but arguable
1: Wrong classification or legitimacy assessment contradicts message content

**Clarity (1–5)**
5: Marcela can make approve/reject/pass decision in under 30 seconds from this summary
3: Summary provides context but requires a follow-up read of the raw message
1: Unclear or confusing; Marcela cannot decide without more information

**State Sync (1–5)**
5: Asana state updated to lead_summary_sent_to_marcela
3: Summary sent but Asana state not updated
1: Neither sent nor state updated

**Timing (1–5)**
5: Summary sent promptly after lead creation
3: Minor delay, summary eventually sent
1: Summary never sent or excessive delay

**Decision Readiness (1–5)**
5: Summary includes a clear recommended action (approve / reject / pass) with brief rationale
3: Context provided but no recommendation
1: Summary requires Marcela to research before deciding

## Auto-Fail Conditions
- Summary is empty
- source field is missing
- Classification is "unknown" without written explanation
