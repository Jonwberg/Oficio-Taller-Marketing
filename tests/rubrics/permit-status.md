# Rubric: Permit Status
**Agent:** Paco
**Deliverable:** Permit submission and tracking record (Segment I, no Marcela gate — Paco fires after contractor selected at DG-11)

## Schema (Execution Agent validates — pass/fail)
Required fields: submitted_at, jurisdiction, status, corrections (array), approved_at

Note: `corrections` is an array (empty array `[]` is valid when status is not "corrections_required"). `approved_at` may be null if permit not yet approved.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; jurisdiction names the specific authority (e.g., "Municipio de San Pedro Garza García — Desarrollo Urbano"); status is one of: submitted, under_review, corrections_required, approved; corrections array populated with specific items when status is corrections_required
3: All fields present but jurisdiction is generic (city name only); or corrections array empty when status is corrections_required
1: Any required field absent; or approved_at present while status is not approved

**Accuracy (1–5)**
5: Jurisdiction matches project location from state.json client_address or project context; submitted_at is after contractor selection confirmed (DG-11); correction items match actual permit reviewer feedback
3: Jurisdiction correct but authority name slightly wrong; submitted_at timing plausible
1: Wrong jurisdiction; submitted_at predates contractor selection

**Clarity (1–5)**
5: Vera can trigger construction phase start immediately from this document when status is approved; correction items are specific enough for action
3: Status clear but corrections lack specifics; Vera needs one follow-up to act
1: Status ambiguous; Vera cannot determine whether to unlock construction

**State Sync (1–5)**
5: Asana permit task updated at each status change: submitted → under_review → corrections_required / approved; construction phase unlocked in Asana when approved
3: Asana updated at submission and approval but not at intermediate steps
1: No Asana update

**Timing (1–5)**
5: Submission initiated promptly after DG-11 contractor selection; status updates reflected within reasonable processing window
3: Minor delay in submission initiation but within acceptable range
1: Permit submitted before contractor selection or not submitted at all

**Decision Readiness**
N/A — No Marcela gate; Paco → Vera (auto-unlock) on approval. Average score over 5 dimensions.

## Auto-Fail Conditions
- jurisdiction absent or entirely generic ("Mexico")
- submitted_at absent
- corrections array absent (even empty array required when no corrections)
- approved_at populated while status is not "approved"
- Permit submitted before DG-11 contractor selection confirmed
