# TC-007 — Edge: Bad Lead (Spam)

**Type:** N/A
**Complexity:** Edge case — spam detection and discard
**Seed data:** `tests/data/TC-007-seed.json`

## Scenario
An Instagram DM from a fake marketing account offering social media followers.
Lupe should detect this as spam, archive the lead, and trigger no downstream agents.

## Key Verification Points
- Lupe classifies category as "spam" (Segment A)
- No lead summary sent to Marcela — lead archived immediately
- No Elena, Ana, Sol, or any downstream agent dispatched
- Asana lead task created with status "discarded"
- Final state: lead_screened (not lead_summary_sent_to_marcela)

## Expected Final State
lead_screened (discarded, not forwarded)

## Edge Conditions
- This test STOPS at Segment A — do not continue to Segment B
- A false positive (legitimate lead incorrectly classified as spam) would be a Critical failure
