# TC-006 — Edge: Budget Mismatch

**Type:** standalone_residential
**Complexity:** Edge case — budget misalignment requiring redesign
**Seed data:** `tests/data/TC-006-seed.json`

## Scenario
Miguel Torres wants a 216sqm house with pool in Los Cabos on a $200K budget.
Contractor pricing at Segment G comes in at $380K — nearly double the budget.
Bruno recommends redesign: remove pool, reduce to 160sqm. After redesign,
contractor pricing at $195K aligns with budget.

## Key Verification Points
- DG-09 (Budget Alignment): Bruno simulates Reject — budget_misaligned state set
- Redesign loop triggers (back to Felipe per feedback_type)
- After redesign: second DG-09 produces budget_aligned state
- Executive plans only begin after budget_aligned confirmed

## Expected Final State
closed (after redesign loop resolves)

## Edge Conditions
- budget_misaligned state must be set before redesign — not skipped
- executive_plans_in_progress must NOT appear before budget_aligned
