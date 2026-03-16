# Rubric: Budget
**Agent:** Bruno
**Deliverable:** Itemized project budget with payment schedule (Segment D, feeds directly into Renata's proposal — no separate gate)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, client_name, milestone_name, amount, payment_instructions, currency, line_items

Note: `line_items` must be an array. `milestone_name` labels the first payment milestone; all milestones are covered across `line_items` entries.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; line_items array covers every SOW phase; all 5 payment milestones present with name, percentage, trigger event, and MXN amount
3: All required fields present but one payment milestone missing trigger event or one phase missing from line_items
1: Any required field missing, or fewer than 3 payment milestones, or line_items absent

**Accuracy (1–5)**
5: Total of all milestone amounts equals total_estimate from cost-basis.json within 2% (contingency adjustment acceptable); each line_item amount is correctly calculated
3: Total within 5% of cost_basis total_estimate; minor rounding differences in line items
1: Total differs from cost_basis total_estimate by more than 5% without documented justification

**Clarity (1–5)**
5: Client can understand what they are paying for at each milestone; payment_instructions are specific (bank name, CLABE/SWIFT, reference format); currency is explicit (MXN or USD)
3: Milestones labeled but payment_instructions missing one detail; client would need one follow-up question
1: Payment_instructions absent or generic; client cannot pay without additional information

**State Sync (1–5)**
5: Asana task updated to budget_complete; linked to scope-of-work task; budget passed to Renata without delay
3: State updated but not linked to scope-of-work task
1: No Asana update

**Timing (1–5)**
5: Budget produced after Vera confirms architect SOW approval (DG-04); not before; passed to Renata immediately
3: Minor delay after DG-04 but budget exists before Renata begins proposal
1: Budget produced before DG-04 confirmation or not produced before Renata fires

**Decision Readiness**
N/A — No Marcela gate on Bruno's Segment D budget (proceeds directly to Renata per scope boundary). Average score calculated over 5 dimensions.

## Auto-Fail Conditions
- line_items absent or empty array
- payment_instructions absent
- Total budget not reconciled with cost_basis total_estimate (difference > 5% with no documented justification)
- Budget produced before architect SOW approval (DG-04) confirmed
