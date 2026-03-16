# Rubric: Client Communication
**Agent:** Rosa
**Deliverable:** Any outbound client message (status updates, proposals, revision acknowledgements)

## Schema (Execution Agent validates — pass/fail)
Required fields: channel, message_body, project_reference, status (draft — awaiting approval)

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Message includes project name, relevant context, clear action requested
3: Project name present but context incomplete
1: No project reference

**Accuracy (1–5)**
5: Message accurately reflects the current project state and any decisions made
3: Mostly accurate but one minor factual gap
1: Inaccurate or misleading information about project status

**Clarity (1–5)**
5: One clear next step for the client; no ambiguity about what is expected of them
3: Next step implied but not explicit
1: Client cannot determine what to do from this message

**State Sync (1–5)**
5: Message in draft status — Marcela approval required before send; Asana status updated after approval
3: Draft but Asana not updated
1: Message sent without Marcela approval

**Timing (1–5)**
5: Message drafted promptly after triggering event
3: Minor delay
1: Significant delay or message not drafted

**Decision Readiness (1–5)**
5: Marcela can approve this message in under 60 seconds
3: Message nearly ready but one phrase needs adjustment
1: Message requires significant rework before approval

## Auto-Fail Conditions
- Message sent without Marcela approval
- Project reference missing
- Confidential internal information included in client-facing message
