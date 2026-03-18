# Tomás — Segment D Raw Output
**run_id:** 2026-03-16-TC-009
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**agent:** Tomás
**mode:** SOW generation — standalone_residential

---

## Step 1: Context Read

- state.json: project_type = standalone_residential, client_name = Familia Reyes-Montoya
- area-program.json: total_sqm = 320, spaces = 10
- cost-basis.json: total_estimate = MXN 8,703,200, architecture_fee = MXN 825,600
- Seed data: architecture fee fixed at $90,000 USD (40/30/30 schedule per seed)

## Step 2: Template Loaded

Template: `docs/templates/sow/sow-standalone-residential.md`
Project type confirmed: standalone_residential

## Step 3: Payment Schedule Derivation

Seed data provides explicit payment schedule (USD, 40/30/30):
- M1 Contract Signing: 40% × $90,000 = $36,000 USD
- M2 Concept Approved: 30% × $90,000 = $27,000 USD
- M3 Executive Plans Approved: 30% × $90,000 = $27,000 USD
Total: $90,000 USD — matches seed total_architecture_fee_usd

Note: Seed schedule uses 3-milestone structure (40/30/30) per TC-009 specification. Template default is 5-milestone; seed data overrides per Tomás protocol ("if seed data provides an explicit payment schedule, use those amounts instead").

## Step 4: Scope-of-Work.json Written

File: `projects/PRJ-2026-0316-familia-reyes-montoya/scope-of-work.json`

Sections produced:
- scope_phases: 6 phases (Conceptual, Architectural, Engineering Coordination, Executive Plans, Contractor Bidding, Permitting)
- payment_schedule: 3 milestones, USD, 40/30/30
- responsibilities_matrix: 14 entries
- exclusions: 12 specific exclusions (not generic)
- revision_assumptions: per-phase (phases 1–6)
- project_type_clauses: 4 clauses verbatim from standalone_residential template (residential_standard, client_changes, site_conditions, esignature)

**Coastal site conditions noted in:**
- Phase 1: horizon-axis orientation, wind-resistant material palette
- Phase 2: coastal wind load requirements in structural coordination
- Phase 3: coastal zone permit as parallel prerequisite; wind load study dependency
- Phase 4: salt-air resistant materials, wind load rated doors/windows
- Phase 6: coastal zone permit (SEMARNAT/ZOFEMAT) noted as timeline extension risk

**project_type_clauses:** standalone_residential template only — no mixed clauses from other project types.

## Step 5: Asana Update

ASANA_UNAVAILABLE: would complete scope_of_work task for PRJ-2026-0316-familia-reyes-montoya — "Scope of work complete. 6 phases. Payment schedule: $36,000 to $27,000 (USD). Template: standalone_residential."

## Step 6: State Update + Vera Dispatch

state.json updated: project_state → scope_sent_for_architect_review, awaiting_gate → DG-04
awaiting_gate check: was null — no duplicate dispatch warning triggered.
Vera dispatched: mode = architect_sow_review, project_id = PRJ-2026-0316-familia-reyes-montoya

---

## Schema Validation

| Field | Present | Notes |
|---|---|---|
| scope_phases | PASS | 6 phases |
| payment_schedule | PASS | 3 milestones, USD, 40/30/30 |
| responsibilities_matrix | PASS | 14 entries |
| exclusions | PASS | 12 specific exclusions |
| revision_assumptions | PASS | phases 1–6 |
| project_type_clauses | PASS | 4 clauses verbatim from standalone_residential template |

**TC-009 specific check — project_type_clauses uses standalone_residential template (not mixed):** PASS
**Coastal site conditions noted in scope:** PASS
