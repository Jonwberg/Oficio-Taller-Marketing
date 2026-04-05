# Entrega Pipeline — Data Layer Architecture
**Version:** 1.0 · March 2026

---

## Overview

The Entrega pipeline writes data across four storage systems. Every project has a `project_id` as its primary key. `state.json` is the master state machine — every agent reads it before acting and writes to it after acting. All other JSON files are immutable once their governing gate approves them.

---

## Storage Systems

| System | What lives here | Query method | Who governs |
|---|---|---|---|
| **Local filesystem** `projects/[project_id]/` | All JSON operational documents; milestone sign-off PDFs | Direct file read; `jq` for field extraction | Agent writes; gate approves |
| **Asana** `asana_project_id` in state.json | Tasks, gates, decision statuses, team assignments | Asana API (`asana_client.py`) | Vera + Celia write; Marcela reads |
| **Gmail** `thread_id` fields in state.json | Client email threads; DG review email threads | Gmail API (`gmail_client.py`) | Elena, Rosa, Vera send; Celia reads replies |
| **Google Drive** | Deliverable PDFs, signed contracts, area estimation spreadsheets, source ALCANCE docs | Drive API or manual upload | Marcela + Legal manage |

---

## Data Layers

### Layer 0 — System
- `state.json` — master state machine, initialized by Lupe A, updated by every agent

### Layer 1 — Ingest (Segment A)
- `lead-record.json` — raw classified lead

### Layer 2 — Discovery (Segment B)
- `lead-summary.json` — enriched lead context
- `discovery-questionnaire.json` — 9-field client questionnaire
- `client-fit-assessment.json` — 4-dimension fit scoring

### Layer 3 — Program (Segment C, parallel)
- `area-program.json` — room-by-room matrix with m² + sqft
- `cost-basis.json` — preliminary MXN cost estimate
- `site-readiness-report.json` — site document status

### Layer 4 — Commercial (Segment D)
- `scope-of-work.json` — phase deliverables + payment schedule
- `budget.json` — itemized budget with milestone amounts
- `proposal.json` — bilingual ES+EN client proposal
- `legal-review.json` — IP/clause compliance review
- `client-communication.json` — outbound client message

### Layer 5 — Contract (Segments E–F)
- `contract-signed.pdf` — executed master agreement
- `milestone-signoff-M[N].pdf` — change-freeze sign-offs (M1–M4)

### Layer 6 — Execution (Segments G–J)
- `project-schedule.json` — phase dates + Asana milestones
- `concept-review.json` — conceptual design assessment
- `architectural-design-package.json` — drawing set status
- `engineering-package.json` — structural + MEP integration
- `budget-alignment.json` — variance vs. original cost-basis
- `executive-plans-package.json` — complete construction document set

### Layer 7 — Procurement (Segment K)
- `bid-comparison-matrix.json` — contractor bid analysis
- `permits-package.json` — permit submission + approval record

### Layer 8 — Event Log (All segments)
- `decision-event.json` — Celia writes one per gate (11 total per project). **Append-only. Never modified.**

---

## Document Schemas

### state.json
```json
{
  "project_id": "string",
  "client_name": "string",
  "client_email": "string",
  "project_type": "standalone_residential | residential_in_development | commercial_hotel | commercial_health_center | public_civic",
  "project_state": "new_lead | awaiting_decision | area_program_complete | active_in_progress | ...",
  "awaiting_gate": "DG-01 | DG-02 | ... | DG-11 | null",
  "review_thread_id": "string (Gmail thread ID)",
  "client_questionnaire_thread_id": "string",
  "asana_project_id": "string",
  "tasks": {
    "lead_review": "string (Asana task ID)",
    "fit_gate": "string",
    "area_program": "string",
    "cost_basis_gate": "string",
    "sow_gate": "string",
    "proposal_gate": "string",
    "client_decision": "string"
  },
  "area_program_complete": "boolean",
  "site_data_complete": "boolean",
  "milestone_M1_signed": "boolean",
  "milestone_M2_signed": "boolean",
  "milestone_M3_signed": "boolean",
  "milestone_M4_signed": "boolean",
  "contract_signed_at": "ISO-8601 | null",
  "contract_currency": "MXN | USD | CAD"
}
```

### decision-event.json (event log — 11 per project)
```json
{
  "project_id": "string",
  "phase": "string",
  "review_item": "string",
  "reviewed_by": "Marcela",
  "decision": "approve | reject | pass_to_agent",
  "comment": "string | null",
  "timestamp": "ISO-8601",
  "source_channel": "gmail | slack | manual",
  "next_action": "string",
  "route_to": "agent_name | null",
  "sync_to_asana": "boolean"
}
```

### client-fit-assessment.json
```json
{
  "meeting_notes": "string",
  "assessment_dimensions": {
    "design_engagement": { "score": 1-5, "evidence": "string" },
    "budget_realism":    { "score": 1-5, "evidence": "string" },
    "scope_clarity":     { "score": 1-5, "evidence": "string" },
    "collaborative_style": { "score": 1-5, "evidence": "string" }
  },
  "recommendation": "proceed | decline | request_more_information",
  "rationale": "string"
}
```

### area-program.json
```json
{
  "date": "ISO date",
  "project": "string",
  "clients": "string",
  "budget": "number | null",
  "covered_areas": {
    "house": [{ "name": "CAPS", "width_m": 0, "depth_m": 0, "total_m2": 0, "total_sqft": 0 }],
    "house_walls_and_circulations_pct": 20,
    "house_walls_and_circulations_m2": 0,
    "house_subtotal_m2": 0,
    "house_subtotal_sqft": 0,
    "garage": [...],
    "covered_outdoor": [...]
  },
  "total_covered_m2": 0,
  "uncovered_areas": [...],
  "total_uncovered_m2": 0,
  "total_design_m2": 0,
  "total_sqm": 0,
  "assumptions": ["string"]
}
```

### cost-basis.json
```json
{
  "cost_per_sqm": 0,
  "base_construction_cost": 0,
  "architecture_fee_pct": 12,
  "architecture_fee": 0,
  "engineering_allowance": 0,
  "contingency_pct": 10,
  "total_estimate": 0,
  "assumptions": ["string"]
}
```

---

## Governance Rules

### Immutability
| Document | Becomes immutable after | Can change via |
|---|---|---|
| lead-record.json | DG-01 approval | — |
| lead-summary.json | DG-02 approval | — |
| discovery-questionnaire.json | DG-02 approval | — |
| client-fit-assessment.json | DG-02 approval | — |
| area-program.json | DG-03 approval | Re-run Ana (requires DG-03 reject) |
| cost-basis.json | DG-03 approval | Re-run Ana (requires DG-03 reject) |
| site-readiness-report.json | DG-03 approval | — |
| scope-of-work.json | DG-04 approval | Change order (post-contract) |
| budget.json | DG-05 approval | Change order (post-contract) |
| proposal.json | DG-05 approval | Revision round (pre-DG-06) |
| legal-review.json | DG-05 approval | — |
| client-communication.json | DG-06 approval | Revision round (DG-06 loop) |
| contract-signed.pdf | Client signature | Amendment / change order only |
| milestone-signoff-M[N].pdf | Client signature | Change order required for any post-signoff change |
| project-schedule.json | Project completion | Change order |
| decision-event.json | **Never modified** | Append-only |

### Write Permissions (which agent writes each document)
| Document | Primary writer | Can update |
|---|---|---|
| state.json | Lupe A (init) | All agents (their respective fields only) |
| lead-record.json | Lupe A | — |
| lead-summary.json | Lupe B | — |
| discovery-questionnaire.json | Elena | — |
| client-fit-assessment.json | Elena | — |
| area-program.json | Ana | Ana (on DG-03 reject + redo) |
| cost-basis.json | Ana | Ana (on DG-03 reject + redo) |
| site-readiness-report.json | Sol | Sol (status updates) |
| decision-event.json | Celia | **Append only — never update** |
| scope-of-work.json | Tomás | Tomás (on DG-04 reject) |
| budget.json | Bruno D | Bruno D (on DG-05 reject) |
| proposal.json | Renata | Renata (on DG-05 reject) |
| legal-review.json | Legal | — |
| client-communication.json | Rosa | Rosa (revision rounds) |
| contract-signed.pdf | Legal | — |
| milestone-signoff-M[N].pdf | Legal | — |
| project-schedule.json | Pablo | Pablo |
| concept-review.json | Andrés | Andrés (on DG-07 pass) |
| architectural-design-package.json | Felipe | Felipe (on DG-08 reject) |
| engineering-package.json | Emilio | Emilio (on DG-09 reject) |
| budget-alignment.json | Bruno G | — |
| executive-plans-package.json | Hugo | Hugo (on DG-10 reject) |
| bid-comparison-matrix.json | Ofelia | Ofelia (on DG-11 reject) |
| permits-package.json | Paco | Paco (status updates) |

---

## Analytics Data Model

### Operational Tables (extract from JSON files)

**projects** — one row per project
```
project_id PK, client_name, client_email, project_type, project_state,
start_date, contract_signed_at, contract_currency, total_design_m2,
architecture_fee_mxn, asana_project_id
```

**leads** — from lead-record.json
```
project_id FK, source_channel, category, received_at, status
```

**clients** — from state.json + client-fit-assessment.json
```
project_id FK, client_name, client_email, language,
fit_design_engagement, fit_budget_realism, fit_scope_clarity, fit_collaborative_style,
fit_avg_score, fit_recommendation
```

**gate_decisions** — from decision-event.json (11 rows per project)
```
decision_id PK, project_id FK, gate_id (DG-01..DG-11), phase, decision,
decided_at, comment, route_to, days_in_stage
```

**area_rooms** — from area-program.json (one row per room)
```
project_id FK, section (house|garage|covered_outdoor|uncovered),
room_name, width_m, depth_m, total_m2, total_sqft, notes
```

**milestones** — from budget.json payment_schedule
```
project_id FK, milestone_id (M1..M4), name, percentage, amount_mxn,
amount_usd, triggered_at, paid_at
```

**bid_comparison** — from bid-comparison-matrix.json
```
project_id FK, contractor_name, bid_total, timeline_weeks,
is_recommended, notes
```

### Analytical Tables (derived for BI)

**fact_pipeline_event** — pipeline funnel analysis
```
project_id, gate_id, decision, days_in_stage, stage_start, stage_end,
revision_rounds (count of pass_to_agent before approve)
```

**fact_financial** — revenue and cost tracking
```
project_id, project_type, total_design_m2, cost_per_sqm,
base_construction_cost, architecture_fee, total_estimate,
m1_amount, m2_amount, m3_amount, m4_amount, currency,
budget_variance_pct (from budget-alignment.json)
```

**fact_revision** — revision activity
```
project_id, phase, gate_id, revision_round, reason_category
```

**dim_project** — project dimensions
```
project_id, project_type, client_language, client_location,
contract_currency, total_sqm_band (small/medium/large)
```

### Key Metrics

| Metric | Source documents | Formula |
|---|---|---|
| Lead-to-contract rate | decision-event.json | Projects reaching DG-06 approve / total projects |
| Avg days: ingest → contract | state.json, decision-event.json | DG-06.decided_at − lead-record.received_at |
| Avg days per stage | gate_decisions | stage_end − stage_start per gate |
| Revision rate | gate_decisions | COUNT(pass_to_agent) per gate per project |
| Fee per m² (architecture) | area-program + budget | architecture_fee / total_design_m2 |
| Budget variance | cost-basis + budget-alignment | (aligned_total − original_estimate) / original_estimate |
| Fit score to close rate | client-fit-assessment + gate_decisions | fit_avg_score grouped by DG-06 outcome |
| Payment collection lag | milestones | paid_at − triggered_at per milestone |

---

## Data Lineage Summary

```
inbound message
    └── lead-record.json (Lupe A)
        └── lead-summary.json (Lupe B)
            ├── discovery-questionnaire.json (Elena)
            └── client-fit-assessment.json (Elena)
                ├── area-program.json (Ana) ──────────────────────────────┐
                ├── cost-basis.json (Ana) ──────────────────────────────  │
                └── site-readiness-report.json (Sol)                      │
                                                                           │
area-program.json + cost-basis.json                                        │
    └── scope-of-work.json (Tomás) ← sow-[type].md template              │
        └── budget.json (Bruno D)                                          │
            └── proposal.json (Renata) ← area-program.json ─────────────-┘
                └── legal-review.json (Legal)
                    └── client-communication.json (Rosa)
                        └── [DG-06 approve]
                            └── contract-signed.pdf (Legal)
                                ← contract-mx.md OR contract-us-ca.md
                                ← scope-of-work.json (Exhibit A)
                                └── project-schedule.json (Pablo)
                                    └── concept-review.json (Andrés)
                                        └── architectural-design-package.json (Felipe)
                                            └── engineering-package.json (Emilio)
                                                └── budget-alignment.json (Bruno G)
                                                    └── executive-plans-package.json (Hugo)
                                                        └── bid-comparison-matrix.json (Ofelia)
                                                            └── permits-package.json (Paco)
                                                                └── [Construction Begins]

decision-event.json (Celia) ← written at every gate, reads every document
```
