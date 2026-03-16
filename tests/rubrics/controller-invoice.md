# Rubric: Controller Invoice
**Agent:** Controller
**Deliverable:** Invoice issued at each payment milestone (Segment J)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, client_name, milestone_name, amount, due_date, payment_instructions, currency, running_total

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; running total of invoiced vs total contract value included
3: All fields present but running total missing
1: Any required field missing

**Accuracy (1–5)**
5: Invoice amount exactly matches the amount in Bruno's payment schedule for this milestone
3: Amount within 1% of schedule (rounding)
1: Amount differs from payment schedule

**Clarity (1–5)**
5: Payment instructions are specific (bank name, account, reference) — client can pay without follow-up
3: Instructions present but one detail missing
1: Payment instructions absent or generic

**State Sync (1–5)**
5: Invoice issued only AFTER milestone trigger confirmed by Vera; not before
3: Invoice issued within acceptable window of trigger
1: Invoice issued before milestone trigger confirmed

**Timing (1–5)**
5: Invoice issued promptly after milestone trigger
3: Minor delay (24–48h)
1: Significant delay or invoice not issued

**Decision Readiness (1–5)**
N/A — Controller invoice is outbound to client; no human decision gate

## Auto-Fail Conditions
- Invoice amount differs from Bruno's payment schedule
- Invoice issued before milestone trigger confirmed by Vera
- Payment instructions absent
