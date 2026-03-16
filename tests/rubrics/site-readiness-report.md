# Rubric: Site Readiness Report
**Agent:** Sol
**Deliverable:** Site document request and status update (Segment C — Vera status update, not Celia gate)

## Schema (Execution Agent validates — pass/fail)
Required fields: required_documents, request_sent_at, current_status, blockers

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Required documents correctly identified based on site_conditions from seed data; topo always required; hydrologic study required when stream/slope/wetland present
3: Topo requested but hydrologic study missed when conditions warrant it
1: Topo not included in requirements

**Accuracy (1–5)**
5: Document requirements match site conditions exactly (no over-requesting, no under-requesting)
3: One document over-requested or slightly wrong
1: Wrong documents requested for site type

**Clarity (1–5)**
5: Client receives clear instructions with document specifications and deadline
3: Instructions sent but deadline missing
1: No clear instructions to client

**State Sync (1–5)**
5: Asana state updated from site_data_pending to site_data_complete when received; blocker logged when overdue
3: Status updated but blocker not logged when overdue
1: No Asana update

**Timing (1–5)**
5: Document request issued concurrently with area program work (parallel tracks)
3: Minor lag but within acceptable window
1: Request not issued until after area program complete (defeats purpose of parallel track)

**Decision Readiness (1–5)**
5: Vera can assess activation readiness from this report at any time
3: Status readable but incomplete
1: Vera cannot assess document readiness

## Auto-Fail Conditions
- Topo map not included in requirements
- No Asana status update
- Blocker not logged when documents are overdue and activation is pending
