# Rubric: Bid Comparison
**Agent:** Ofelia
**Deliverable:** Contractor bid comparison matrix and recommendation (Segment I, DG-11)

## Schema (Execution Agent validates — pass/fail)
Required fields: bids (array with contractor, total, line_items, timeline, notes), recommendation, recommendation_rationale

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: At least two bids compared; matrix includes contractor name, total, key line items, timeline, notes; one clear recommendation with rationale
3: Two bids but matrix missing one field; recommendation present
1: Single bid treated as selection without Marcela decision gate

**Accuracy (1–5)**
5: Recommendation rationale goes beyond lowest price — track record, timeline, scope understanding cited
3: Recommendation based on price alone with no additional criteria
1: Recommendation contradicts the data in the matrix

**Clarity (1–5)**
5: Marcela can select a contractor immediately from this matrix
3: Mostly clear; one additional clarification needed
1: Marcela cannot make a selection without more information

**State Sync (1–5)**
5: State moves bidding_in_progress → contractor_selected after Marcela decision
3: State updated but sequencing wrong (selected before Marcela decision)
1: No state update

**Timing (1–5)**
5: Bids collected and comparison produced within expected window after executive plans approved
3: Minor delay in collecting bids
1: Significant delay or only one bid collected without documented attempt for more

**Decision Readiness (1–5)**
5: Marcela can select a contractor with confidence from this document
3: Decision possible but one follow-up question likely
1: Cannot select without additional information

## Auto-Fail Conditions
- Single bid treated as final selection without routing to Marcela as a decision
- Comparison matrix absent
