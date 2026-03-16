# Rubric: Architectural Design
**Agent:** Felipe
**Deliverable:** Detailed architectural design set (Segment F, DG-08)

## Schema (Execution Agent validates — pass/fail)
Required fields: design_set_status, concept_reflection_confirmed, area_program_compliance, structural_coordination_notes

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Design set reflects approved concept; all rooms from area program present; structural coordination notes included; material specs consistent with concept approval
3: Most rooms present; one minor program omission
1: Rooms missing from area program, or concept not reflected

**Accuracy (1–5)**
5: No unexplained departures from approved concept; sizes match area program targets
3: Minor size variance but program intent preserved
1: Major departure from concept without documented reason

**Clarity (1–5)**
5: Design is complete enough for engineering handoff — no open design questions remain
3: Mostly complete; one area flagged for later resolution
1: Multiple open design questions remain before engineering can begin

**State Sync (1–5)**
5: State moves architectural_design_in_progress → architectural_design_approved
3: State updated but intermediate tracking missing
1: No state update

**Timing (1–5)**
5: Architectural design delivered within expected window after concept approval
3: Minor delay
1: Significant delay or design not produced

**Decision Readiness (1–5)**
5: Marcela can approve and hand off to Emilio immediately
3: Nearly ready; one clarification needed
1: Design cannot proceed to engineering without rework

## Auto-Fail Conditions
- Rooms from area program missing in design
- Concept not reflected (unexplained departures)
- No structural coordination notes
