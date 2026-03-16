# Rubric: Project Schedule
**Agent:** Pablo
**Deliverable:** Full project timeline with Asana milestone tasks (Segment E, no Marcela gate — activated after contract + deposit confirmed)

## Schema (Execution Agent validates — pass/fail)
Required fields: phases (array), milestone_dates, dependencies

Note: `phases` must be an array of objects. `milestone_dates` maps milestone names to target dates. `dependencies` maps each phase to its predecessor.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: phases array includes every SOW scope_phase; milestone_dates covers all payment trigger milestones; dependencies graph is complete; Asana subtasks created for each phase
3: All phases present but one dependency missing or one Asana subtask not created
1: Any SOW scope_phase absent from schedule, or milestone_dates missing, or dependencies absent

**Accuracy (1–5)**
5: Timeline is realistic for project type and program size (typical residential: 8–14 months; hotel: 16–24 months; health center: 18–26 months); dates are ISO-8601 format; no dependency inversions
3: Timeline realistic but one phase duration seems off; all dates present
1: Timeline clearly unrealistic (e.g., 2-week construction phase for residential) or dependency inversions present

**Clarity (1–5)**
5: Client receives a clear project flow; each phase has a named milestone and target date; critical path is visible
3: Schedule comprehensible but critical path not explicitly marked
1: Schedule is a list of dates without phase names or dependencies

**State Sync (1–5)**
5: Asana milestone tasks created as subtasks with due dates; project_state updated to active_in_progress
3: Asana subtasks created but due dates missing; state update partial
1: No Asana subtasks created

**Timing (1–5)**
5: Schedule produced only after all three activation conditions confirmed by Vera (contract_signed + site_docs_complete + deposit_confirmed all true)
3: One activation condition not yet confirmed but schedule produced without causing downstream issues
1: Schedule produced before activation conditions met

**Decision Readiness**
N/A — No Marcela gate; Pablo fires after activation confirmed. Average score calculated over 5 dimensions.

## Auto-Fail Conditions
- phases array empty or missing
- milestone_dates absent
- Schedule produced before contract_signed + site_docs_complete + deposit_confirmed all true
- Asana subtasks not created
