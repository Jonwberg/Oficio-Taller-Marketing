# Rubric: Scope of Work
**Agent:** Tomás
**Deliverable:** Full SOW document (Segment D, reviewed at DG-04)

## 20-Item Checklist (all must be present)
1. Conceptual design phase defined with deliverables
2. Architectural design phases defined with deliverables
3. Executive architectural plans included with deliverables
4. Optional architectural supervision clause included
5. Landscape architecture scope stated (or explicitly excluded)
6. Structural engineering collaboration defined
7. Electrical engineering scope included
8. Lighting design scope stated
9. Water systems scope defined
10. Irrigation scope included (or explicitly excluded)
11. Solar systems scope included (or explicitly excluded)
12. Local contractor cost validation planned
13. Payment schedule with milestone names, percentages, and trigger events
14. Deliverables listed by phase with specifics
15. Responsibilities matrix assigning every major deliverable to a named party
16. Exclusions documented with specifics (not generic)
17. Revision assumptions stated per phase
18. Timeline structure clear with phase sequence
19. Project-type-specific clauses included (see below)
20. E-signature path defined

## Project-Type Clause Requirements
- standalone_residential: standard residential clauses
- residential_in_development: HOA coordination clause + covenant review clause
- commercial_hotel: hospitality compliance clause + brand standards coordination
- commercial_health_center: health authority compliance clause + medical equipment coordination
- public_civic: civic procurement clause + public bidding compliance

## Schema (Execution Agent validates — pass/fail)
Required sections: scope_phases, payment_schedule, responsibilities_matrix, exclusions, revision_assumptions, project_type_clauses

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All 20 checklist items present and complete; correct project-type-specific clauses applied
3: 17–19 items present; project-type clause missing or incomplete
1: Any of the 20 items missing

**Accuracy (1–5)**
5: Deliverables per phase match the production pipeline exactly; responsibilities name real parties
3: Minor mismatch in deliverable description but structure correct
1: Wrong project type template applied

**Clarity (1–5)**
5: Client can sign this document with full understanding of what they are buying
3: Clear to a professional but dense for a client
1: Ambiguous scope or unclear deliverables

**State Sync (1–5)**
5: Asana state updated to scope_in_preparation then scope_sent_for_architect_review
3: Partial update
1: No Asana update

**Timing (1–5)**
5: SOW produced after area program and cost basis are confirmed and before architect SOW review email is sent
3: Minor delay but SOW exists before Vera sends the DG-04 architect email
1: Not produced before DG-04 fires or not produced at all

**Decision Readiness (1–5)**
5: Architect reviewer can approve or flag specific sections immediately
3: Document ready but some sections need clarification
1: Architect cannot evaluate without significant additional information

## Auto-Fail Conditions
- Payment schedule missing
- Exclusions section absent
- Project type template not applied (wrong or generic clauses)
- Any of the 20 checklist items completely absent
