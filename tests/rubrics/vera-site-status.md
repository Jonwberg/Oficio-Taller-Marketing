# Rubric: Vera Site Status Update
**Agent:** Vera
**Deliverable:** Asana site readiness status update (Segment C — no JSON client deliverable)

## Special Handling
Vera does not write a scored JSON deliverable. Her Segment C evaluation is based on her raw text output describing the Asana update she performed. The Decision Gate Agent scores Vera's stated actions against this rubric.

The test-execution agent passes Vera's complete raw output text as the `deliverable` field. The Decision Gate Agent reads this text and scores whether Vera correctly identified and applied the right Asana update.

## Schema (Execution Agent validates — pass/fail)
No JSON schema validation for this segment. Test-execution agent checks that Vera produced any non-empty text output describing her Asana actions. If output is empty, flag as schema_fail.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Asana Field Accuracy (1–5)**
5: Vera's output explicitly states: (a) which Asana task was updated (site_readiness task_id from state.json), (b) which field was set (site_readiness_status), (c) what value was set (matching Sol's current_status from site-readiness-report.json), and (d) what the blockers are if any
3: Vera updated the correct task and field but did not surface blockers explicitly
1: Vera updated wrong task or wrong field, or did not identify any Asana action

**Source Fidelity (1–5)**
5: Vera's status value matches Sol's site-readiness-report.json current_status exactly (not paraphrased); blockers listed match Sol's blockers array
3: Status value semantically correct but not verbatim from Sol's report; blockers partially surfaced
1: Vera's stated status contradicts Sol's report

**Clarity (1–5)**
5: Any human reading Vera's output can immediately confirm what was updated in Asana and why
3: Update described but reasoning not connected to Sol's report
1: Vera's output does not describe a clear Asana action

**State Sync (1–5)**
5: Vera explicitly states state.json was not modified (Sol's completion flag is set by Sol, not Vera) AND that she did not dispatch any downstream agent
3: Vera updated correct Asana field but did not confirm she did not modify state.json
1: Vera attempted to set state.json flags (Sol's responsibility) or attempted to dispatch Tomás directly

**Timing (1–5)**
5: Vera's update fires after Sol's site-readiness-report.json exists and before DG-03 review request is sent
3: Minor timing gap but Vera updated before DG-03
1: Vera fired before Sol's report exists or after DG-03 already sent

## Auto-Fail Conditions
- Vera's output is empty or contains no Asana update description
- Vera dispatched Tomás or any downstream agent (Vera's scope in Segment C is Asana update only — chain continuation is not Vera's role here)
- Vera set state.json site_data_complete flag (Sol sets this, not Vera)
- Vera reported a site status that contradicts Sol's site-readiness-report.json
