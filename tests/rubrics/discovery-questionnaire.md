# Rubric: Discovery Questionnaire
**Agent:** Elena
**Deliverable:** Questionnaire sent to lead after Marcela approval (Segment B)

## Schema (Execution Agent validates — pass/fail)
Required fields: sent_to, sent_at, project_type_question, budget_question, timeline_question, location_question

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Covers all 8 required topics: project type, approximate size, site location, budget range, desired timeline, special requirements, design style preferences, site ownership status
3: 6–7 topics covered, one minor omission
1: Missing budget or project type question

**Accuracy (1–5)**
5: Questions are tailored to the project type from the lead summary (residential vs commercial vs civic)
3: Generic questionnaire sent without project type adjustment
1: Questions are inappropriate for the lead context

**Clarity (1–5)**
5: Questions are conversational, warm, and inviting — not a bureaucratic form
3: Questions are clear but feel formal or cold
1: Questions are confusing or off-putting

**State Sync (1–5)**
5: Asana state updated to followup_sent; lead status updated to "responded" when reply received
3: Questionnaire sent but Asana not updated
1: No state update

**Timing (1–5)**
5: Questionnaire sent within 24h of lead qualification
3: Sent within 48h
1: Sent after 48h or not at all

**Language (1–5)**
5: Questionnaire language matches the client's communication language exactly (Spanish if inbound was Spanish; English if inbound was English)
3: Mostly correct language but one phrase or question in wrong language
1: Questionnaire sent in entirely wrong language when client language is clearly identifiable from inbound message

**Decision Readiness (1–5)**
5: Questionnaire will produce responses that allow Elena to prepare a complete fit assessment
3: Most questions are useful; one or two gaps in coverage
1: Questionnaire will not produce enough information for fit assessment

## Auto-Fail Conditions
- Questionnaire sent to wrong contact (not the inbound lead)
- Budget question absent
- Project type not addressed
- Questionnaire sent in wrong language when client language is unambiguously identified from inbound message
