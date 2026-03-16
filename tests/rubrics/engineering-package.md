# Rubric: Engineering Package
**Agent:** Emilio
**Deliverable:** Complete engineering coordination package (Segment G, feeds DG-09)

## Schema (Execution Agent validates — pass/fail)
Required fields: systems_status (structural, electrical, lighting, water), conditional_systems, all_inputs_confirmed, conflicts_resolved

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required systems present and confirmed (structural, electrical, lighting, water); conditional systems addressed (irrigation if landscaping in scope, solar if in scope, AV if in scope); no pending consultant inputs
3: Required systems present; one conditional system not addressed
1: Any required system absent

**Accuracy (1–5)**
5: Engineering package explicitly declared complete and ready for budget alignment; all consultant inputs confirmed received
3: Mostly complete but one consultant input still pending
1: Pending inputs declared complete when they are not

**Clarity (1–5)**
5: Any design conflicts identified during engineering are documented with proposed resolutions
3: Conflicts noted but not resolved
1: Conflicts ignored or not documented

**State Sync (1–5)**
5: States move structural_engineering_in_progress and systems_engineering_in_progress to budget_alignment_pending
3: State partially updated
1: No state update

**Timing (1–5)**
5: Package complete before Bruno begins contractor pricing; no budget alignment begins without confirmed engineering package
3: Minor delay (external consultant timeline is acceptable reason); package exists before DG-09
1: Package declared incomplete when DG-09 fires, or significantly delayed without documented reason

**Decision Readiness (1–5)**
5: Bruno can proceed to contractor pricing immediately
3: Mostly ready; one minor item outstanding
1: Cannot proceed to budget alignment without additional engineering work

## Auto-Fail Conditions
- Any required system absent (structural, electrical, lighting, water)
- Pending consultant inputs undeclared when package marked complete
