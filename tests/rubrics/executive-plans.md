# Rubric: Executive Plans
**Agent:** Hugo
**Deliverable:** Final integrated plan set (Segment H, DG-10)

## Schema (Execution Agent validates — pass/fail)
Required fields: plan_set_components (cross_sections, full_plan_book, technical_coordination), engineering_integration_confirmed, conflicts_resolved, client_signoff_milestone

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required components present: cross sections, full plan book, technical coordination layer; all engineering inputs from Emilio's package integrated
3: All components present but one engineering system drawing missing
1: Missing cross sections or plan book incomplete

**Accuracy (1–5)**
5: No unresolved coordination conflicts between architectural and engineering drawings
3: Minor discrepancy documented with resolution noted
1: Unresolved conflicts that affect construction

**Clarity (1–5)**
5: Package is self-contained — no references to documents not included; client can review without back-reference
3: Mostly self-contained; one external reference
1: Package incomplete; client cannot review without additional documents

**State Sync (1–5)**
5: State moves executive_plans_in_progress → executive_plans_approved; client sign-off logged as milestone
3: State updated but sign-off not logged
1: No state update

**Timing (1–5)**
5: Executive plans produced after budget alignment approval and before Ofelia begins bidding; no bidding begins without it
3: Minor delay but plans exist before bidding phase starts
1: Plans not produced before bidding phase or not produced at all

**Decision Readiness (1–5)**
5: Marcela can approve and hand off to Ofelia for bidding immediately
3: Nearly ready; one minor correction needed
1: Plans require rework before bidding

## Auto-Fail Conditions
- Missing cross sections
- Unresolved engineering coordination conflicts
- Any required system drawing absent
