# Rubric: Budget Alignment Analysis
**Agent:** Bruno
**Deliverable:** Contractor pricing vs client budget analysis (Segment G, DG-09)

## Schema (Execution Agent validates — pass/fail)
Required fields: contractor_pricing_source, contractor_total, client_budget, variance_amount, variance_pct, recommendation

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Contractor pricing from at least one source with source documented; comparison clearly presented; variance calculated ($ and %); explicit recommendation
3: Pricing present but source not documented; recommendation present
1: No contractor pricing source, or no recommendation

**Accuracy (1–5)**
5: Variance correctly calculated; recommendation matches the data (aligned → proceed; misaligned → redesign)
3: Minor variance calculation error but recommendation still correct
1: Recommendation contradicts the data

**Clarity (1–5)**
5: Proceed or redesign — no ambiguity; if redesign, specific scope elements named with estimated savings
3: Recommendation present but redesign scope not specified
1: Ambiguous recommendation; Marcela cannot decide without more information

**State Sync (1–5)**
5: State moves budget_alignment_pending → budget_aligned or budget_misaligned correctly
3: State updated but wrong value
1: No state update

**Timing (1–5)**
5: Analysis delivered promptly after engineering package complete
3: Minor delay
1: Not delivered or excessive delay

**Decision Readiness (1–5)**
5: Marcela can approve or require redesign immediately from this document
3: Mostly ready; one clarification needed
1: Cannot make the budget alignment decision from this document

## Auto-Fail Conditions
- No contractor pricing source documented
- No explicit recommendation (proceed vs redesign)
