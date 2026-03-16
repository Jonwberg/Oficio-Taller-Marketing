# Rubric: Celia Decision Routing
**Agent:** Celia
**Deliverable:** Normalized decision event at every Marcela gate

## The 11 Required Payload Fields
project_id, phase, review_item, reviewed_by, decision, comment, timestamp, source_channel, next_action, route_to, sync_to_asana

Note: field is route_to (not routed_to). The production spec's Asana custom field list previously used routed_to — this was corrected. Test against route_to.

## Pass to Agent at DG-07
When Pass to Agent is simulated at DG-07: expected project_state = concept_in_progress (no change); only assigned_agent updates. This is the correct behavior — Pass to Agent does not advance the state.

## Schema (Execution Agent validates — pass/fail)
Required: all 11 payload fields present; timestamp in ISO-8601

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All 11 payload fields present with values; timestamp ISO-8601
3: 10 fields present; one minor omission
1: Any of route_to, next_action, sync_to_asana, or decision missing

**Accuracy (1–5)**
5: Decision parsed correctly (approve / reject / pass_to_agent); correct next agent assigned per production routing table
3: Decision correct but next agent one step off
1: Wrong next agent assigned, or decision type misclassified

**Clarity (1–5)**
5: Reviewer comment preserved verbatim; no truncation or summarization
3: Comment present but slightly paraphrased
1: Comment dropped or replaced with generic text

**State Sync (1–5)**
5: Asana fields updated correctly: decision_status and assigned_agent updated; for Pass to Agent at DG-07: confirm project_state = concept_in_progress (unchanged)
3: Two of three fields updated
1: Asana not updated

**Timing (1–5)**
5: Decision event created immediately upon receiving human response
3: Minor lag
1: Significant delay or decision not captured

**Decision Readiness (1–5)**
5: Next agent receives complete context to begin work immediately
3: Context mostly complete
1: Next agent cannot begin work from this payload

## Auto-Fail Conditions
- Wrong next agent assigned
- Decision type misclassified (approve treated as reject, etc.)
- Asana not updated
- Reviewer comment dropped
- Any of the 11 required payload fields missing
- route_to field missing (routed_to is wrong field name — see note above)
- Pass to Agent at DG-07 changes project_state away from concept_in_progress (state must not change — any other value is a failure)
