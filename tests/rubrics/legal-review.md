# Rubric: Legal Review
**Agent:** Legal
**Deliverable:** Clause review of proposal before architect approval gate (Segment D, DG-05)

## Schema (Execution Agent validates — pass/fail)
Required fields: reviewed_by, reviewed_at, ip_rights_status, compliance_flags, approval_status

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All proposal clauses reviewed; IP and usage rights addressed; project-type-specific compliance verified
3: Most sections reviewed; IP rights checked but compliance flags generic
1: IP section not reviewed

**Accuracy (1–5)**
5: Compliance issues correctly identified with proposed resolution paths
3: Flag raised but resolution path not proposed
1: Known compliance issue missed

**Clarity (1–5)**
5: Output is either a clean approval or a specific flag list with resolution — no ambiguity
3: Mostly clear but some "may need to review" language
1: "Looks okay" without evidence of review

**State Sync (1–5)**
5: Asana legal review task completed; result linked to proposal task
3: Review done but not linked
1: No Asana update

**Timing (1–5)**
5: Review completed concurrently with Renata's proposal assembly (parallel)
3: Minor lag but done before architect gate
1: Not done before architect gate fires

**Decision Readiness (1–5)**
5: Vera can proceed to architect gate immediately on clean approval; flags are actionable
3: Approval given but some ambiguity remains
1: Cannot determine if it is safe to proceed

## Auto-Fail Conditions
- IP and usage rights section not reviewed
- Approval given with open unresolved flags
- No evidence that the full proposal was reviewed
