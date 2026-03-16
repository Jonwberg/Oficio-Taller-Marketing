# Rubric: Cost Basis
**Agent:** Ana
**Deliverable:** Preliminary cost estimate (Segment C, reviewed at DG-03)

## Schema (Execution Agent validates — pass/fail)
Required fields: cost_per_sqm, base_construction_cost, architecture_fee_pct, architecture_fee, engineering_allowance, contingency_pct, total_estimate, assumptions

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present: cost/sqm basis with source, base cost, arch fee %, arch fee $, engineering allowance, contingency %, total, assumptions list
3: Most fields present, one minor omission
1: Total missing or architecture fee absent

**Accuracy (1–5)**
5: Math is correct — base cost = area × cost/sqm; total = sum of all components
3: Small arithmetic error but structure is right
1: Major calculation error or unsupported cost/sqm claim

**Clarity (1–5)**
5: Clearly labeled as preliminary estimate; assumptions documented with specifics
3: Labeled as preliminary but assumptions generic
1: Not labeled as preliminary; no assumptions

**State Sync (1–5)**
5: Asana cost_basis_ready state set; linked to area program task
3: State set but not linked
1: No Asana update

**Timing (1–5)**
5: Cost basis produced concurrently with area program finalization
3: Slight lag but produced before DG-03
1: Not produced before Marcela review

**Decision Readiness (1–5)**
5: Marcela can assess budget feasibility immediately from this document
3: Some gaps but general picture clear
1: Cannot assess budget feasibility from this document

## Auto-Fail Conditions
- No assumptions section
- Total estimate missing
- Architecture fee absent
