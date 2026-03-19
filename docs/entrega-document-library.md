# Entrega Document Library

**Version:** 1.0
**Last updated:** 2026-03-18
**Maintained by:** Jon Berg / Oficio Taller

This document is the authoritative reference for every file produced and consumed by the Entrega pipeline. It covers three categories:

1. **Reference / Config documents** — static inputs that live outside `projects/`, read by agents but never modified by them
2. **Templates** — blank starting structures used to initialize new projects
3. **Per-project documents** — all files written by agents inside `projects/[project_id]/`

---

## Templates Folder

All templates are stored at `docs/templates/`:

```
docs/templates/
├── json/
│   └── state_template.json          ← project state initializer (Lupe reads this)
└── sow/
    ├── sow-standalone-residential.md
    ├── sow-residential-in-development.md
    ├── sow-commercial-hotel.md
    ├── sow-commercial-health-center.md
    └── sow-public-civic.md
```

### `docs/templates/json/state_template.json`

Blank state.json used to initialize every new project. Contains all pipeline state flags and 30 Asana task ID slots. Lupe copies this file to `projects/[project_id]/state.json` at the start of Segment A.

**Fields:**
- `project_id`, `project_state`, `awaiting_gate`, `review_thread_id`
- `architect_email_thread_id`, `client_questionnaire_thread_id`
- `asana_project_id`, `client_name`, `client_email`, `project_type`
- `area_program_complete`, `site_data_complete`
- `revision_count`, `feedback_type`
- `contract_signed`, `site_docs_complete`, `deposit_confirmed`
- `tasks` — 30 Asana task ID slots (see full list in the file)

### SOW Templates (`docs/templates/sow/`)

Five Markdown templates, one per project type. Each contains:
- Phase structure and deliverables list
- Typical Timeline (weeks per phase)
- Payment schedule skeleton with milestone percentages
- Exclusions list
- Revision assumptions
- Project-type-specific clauses (verbatim legal language)

| Template file | project_type value |
|---|---|
| `sow-standalone-residential.md` | `standalone_residential` |
| `sow-residential-in-development.md` | `residential_in_development` |
| `sow-commercial-hotel.md` | `commercial_hotel` |
| `sow-commercial-health-center.md` | `commercial_health_center` |
| `sow-public-civic.md` | `public_civic` |

---

## Reference / Config Documents

These files live in `entrega/` and are read by agents but never written by them.

| File | Purpose | Read By |
|---|---|---|
| `entrega/custom_field_map.json` | Maps Asana project IDs and custom field GIDs | Lupe (Asana leads project ID) |

---

## Per-Project Documents

All files live at `projects/[project_id]/`. Every field marked **required** must be present and non-null in a passing run; omitting any required field is an auto-fail.

---

### `state.json`

**Written by:** Lupe (initializes from `docs/templates/json/state_template.json`)
**Updated by:** Every agent in the pipeline
**Read by:** Every agent in the pipeline

The single source of truth for pipeline state. Every agent reads this first and writes their updates back before stopping.

**Key fields agents depend on:**

| Field | Type | Description |
|---|---|---|
| `project_state` | string | Current pipeline phase (e.g., `lead_received`, `awaiting_decision`) |
| `awaiting_gate` | string \| null | Active Marcela gate (DG-01 through DG-11) or null |
| `review_thread_id` | string \| null | Gmail thread ID for the current gate review email |
| `area_program_complete` | boolean | Set by Ana when area-program.json is written |
| `site_data_complete` | boolean | Set by Sol when site-readiness-report.json is written |
| `contract_signed` | boolean | Set by operator when contract is confirmed |
| `site_docs_complete` | boolean | Set by operator when all site documents are received |
| `deposit_confirmed` | boolean | Set by operator when deposit clears |
| `revision_count` | integer | Number of proposal revisions (used at DG-06) |
| `feedback_type` | string \| null | Revision type at DG-05/DG-09: `copy`, `scope`, `budget`, `legal` |
| `tasks` | object | 30 Asana task ID slots — all agents reference these |

---

### Segment A — Lead Intake

#### `lead-record.json`

**Written by:** Lupe (Segment A)
**Read by:** Lupe (Segment B)

First record of the inbound inquiry. Captures raw facts — no interpretation.

| Field | Required | Description |
|---|---|---|
| `source_channel` | ✅ | `instagram`, `whatsapp`, `email`, `website`, `referral`, `direct` |
| `category` | ✅ | `project_inquiry`, `speaking`, `collaboration`, `press`, `spam` |
| `received_at` | ✅ | ISO-8601 timestamp |
| `summary` | ✅ | Structured summary: client name, project type, location, program, budget signal |
| `status` | ✅ | `new` (non-spam) or `discarded` (spam) |

#### `TC-007-segment-A-spam-confirmed.json`

**Written by:** Lupe (Segment A, spam path only)
**Read by:** — (audit trail only)

Written only when a lead is classified as spam. Pipeline stops immediately after.

| Field | Required | Description |
|---|---|---|
| `project_id` | ✅ | Project ID |
| `classification` | ✅ | Always `"spam"` |
| `discarded_at` | ✅ | ISO-8601 timestamp |
| `reason` | ✅ | Specific reason the message was classified as spam |

---

### Segment B — Lead Summary

#### `lead-summary.json`

**Written by:** Lupe (Segment B)
**Read by:** Elena, Ana, Sol

Full context document Elena and the parallel Segment C tracks use as their starting point.

| Field | Required | Description |
|---|---|---|
| `project_name` | ✅ | `[client_name] — [project_type] — [location]` |
| `source_channel` | ✅ | From lead-record.json |
| `raw_message` | ✅ | Original inbound message verbatim — do not paraphrase |
| `initial_assessment` | ✅ | 2–3 sentences: classification, program estimate, budget signal, site factors |
| `recommended_action` | ✅ | Always `"proceed to discovery"` at this stage |

---

### Segment B → C — Discovery

#### `discovery-questionnaire.json`

**Written by:** Elena
**Read by:** — (record only; content sent to client via Gmail)

Records the questionnaire that was sent to the client. Language matches the client's inbound language. Uses institutional framing for `public_civic` project types.

| Field | Required | Description |
|---|---|---|
| `sent_to` | ✅ | Client email |
| `sent_at` | ✅ | ISO-8601 timestamp |
| `questionnaire_language` | ✅ | `es` or `en` — matches client's inbound language |
| `project_type_question` | ✅ | Question about project type and land status |
| `budget_question` | ✅ | Question about budget range |
| `timeline_question` | ✅ | Question about timeline and deadlines |
| `location_question` | ✅ | Question about site location and ownership |
| `special_requirements_question` | ✅ | Question about special requirements |
| `design_style_question` | ✅ | Question about design references and style |
| `site_ownership_question` | ✅ | Question about title, encumbrances, prior studies |

#### `client-fit-assessment.json`

**Written by:** Elena
**Read by:** Ana

Four-dimension scored assessment of client fit. Drives the DG-02 recommendation to Marcela.

| Field | Required | Description |
|---|---|---|
| `meeting_notes` | ✅ | Verbatim client quotes + Elena's interpretations (clearly labeled) |
| `assessment_dimensions` | ✅ | Object with 4 scored dimensions (see below) |
| `assessment_dimensions.design_engagement` | ✅ | Score 1–5 + evidence |
| `assessment_dimensions.budget_realism` | ✅ | Score 1–5 + evidence |
| `assessment_dimensions.scope_clarity` | ✅ | Score 1–5 + evidence |
| `assessment_dimensions.collaborative_style` | ✅ | Score 1–5 + evidence |
| `recommendation` | ✅ | `proceed`, `decline`, or `request_more_information` |
| `rationale` | ✅ | 2–3 sentences citing specific scores and evidence |

**Recommendation rules:**
- `proceed`: average score ≥ 3.5 AND no individual score below 2
- `decline`: budget_realism = 1, OR collaborative_style = 1 with conflict evidence
- `request_more_information`: borderline; one key dimension still unclear

---

### Segment C — Programming (Ana and Sol run in parallel)

#### `area-program.json`

**Written by:** Ana
**Read by:** Tomás, Pablo, Felipe, Andrés, Vera (DG-03 email)

Room-by-room space matrix. Tomás uses this as the base for the SOW. Pablo uses it for schedule duration estimates.

| Field | Required | Description |
|---|---|---|
| `spaces` | ✅ | Array of rooms — each with `name`, `qty`, `size_sqm`, `notes` |
| `total_sqm` | ✅ | Must equal sum of all `spaces[].qty × spaces[].size_sqm` |
| `assumptions` | ✅ | All sizing assumptions stated explicitly — never leave this empty |

#### `cost-basis.json`

**Written by:** Ana
**Read by:** Tomás, Bruno

Preliminary cost estimate. All amounts in MXN unless seed data specifies otherwise.

| Field | Required | Description |
|---|---|---|
| `cost_per_sqm` | ✅ | Market benchmark used (MXN/sqm) |
| `base_construction_cost` | ✅ | `total_sqm × cost_per_sqm` |
| `architecture_fee_pct` | ✅ | Default 12% |
| `architecture_fee` | ✅ | `base_construction_cost × 0.12` |
| `engineering_allowance` | ✅ | `base_construction_cost × 0.03` |
| `contingency_pct` | ✅ | Default 10% |
| `total_estimate` | ✅ | Sum of all above items including contingency |
| `assumptions` | ✅ | Source of cost_per_sqm and any non-standard rates |

#### `site-readiness-report.json`

**Written by:** Sol
**Read by:** Vera (DG-03 trigger check)

Tracks which site documents are required and their receipt status.

| Field | Required | Description |
|---|---|---|
| `required_documents` | ✅ | Array — each item: `name`, `rationale`, `received` (boolean) |
| `request_sent_at` | ✅ | ISO-8601 timestamp when client email was sent |
| `current_status` | ✅ | `documents_requested`, `partial_receipt`, `documents_complete`, `blocked` |
| `blockers` | ✅ | Array of blocker descriptions — empty array `[]` if none |

---

### Segment D — Scope, Budget, Proposal, Legal

#### `scope-of-work.json`

**Written by:** Tomás
**Read by:** Bruno, Renata, Legal, Vera, Pablo, Emilio, Hugo, Tax

The contractual backbone of the project. All downstream documents reference this for payment schedules, phase structure, and project-type clauses.

| Field | Required | Description |
|---|---|---|
| `scope_phases` | ✅ | Array — all phases from the SOW template; each with `phase_number`, `phase_name`, `deliverables` (full list), `duration_weeks` |
| `payment_schedule` | ✅ | Array — all milestones (M1–M5 minimum); each with `milestone`, `name`, `percentage`, `amount`, `currency`, `trigger_event` |
| `responsibilities_matrix` | ✅ | Array — all major deliverables with `deliverable`, `responsible_party`, `reviewed_by` |
| `exclusions` | ✅ | Array — each exclusion as an individual string |
| `revision_assumptions` | ✅ | Object — `phase_1` through `phase_4` each with round count and additional-revision rate |
| `project_type_clauses` | ✅ | Array — all clauses from the matching SOW template verbatim |

**Payment schedule consistency rule:** Amounts must sum to `architecture_fee` from cost-basis.json (within 1% rounding tolerance).

#### `budget.json`

**Written by:** Bruno (Segment D)
**Read by:** Renata, Ofelia, Bruno (Segment G), Controller

Itemized fee budget. Payment schedule must match scope-of-work.json exactly.

| Field | Required | Description |
|---|---|---|
| `project_name` | ✅ | `[client_name] — [project_type] — [location]` |
| `client_name` | ✅ | From state.json |
| `milestone_name` | ✅ | First payment milestone (e.g., `M1 — Contract Signing`) |
| `amount` | ✅ | M1 amount |
| `payment_instructions` | ✅ | Bank name + CLABE (or placeholder `[CLABE — TO BE CONFIGURED IN .env]`) |
| `currency` | ✅ | `MXN` or `USD` — must match scope-of-work.json |
| `total` | ✅ | Sum of all `line_items[].amount` |
| `line_items` | ✅ | Array — one item per scope phase; each with `phase`, `description`, `amount`, `currency` |

**Auto-fail:** Payment schedule milestones in budget.json must match scope-of-work.json in number, names, percentages, and total amount.

#### `proposal.json`

**Written by:** Renata
**Read by:** Legal, Vera, Rosa

Bilingual client-facing proposal document. Both languages are non-negotiable.

| Field | Required | Description |
|---|---|---|
| `scope_summary.es` | ✅ | 2–3 paragraphs in Spanish — professional, warm |
| `scope_summary.en` | ✅ | 2–3 paragraphs in English — native, not translated |
| `budget_detail.es` | ✅ | Fee table + payment schedule in Spanish |
| `budget_detail.en` | ✅ | Fee table + payment schedule in English |
| `budget_detail.total` | ✅ | Must match budget.json total exactly |
| `budget_detail.currency` | ✅ | From budget.json |
| `timeline_phases` | ✅ | Array — one item per phase; `phase`, `duration_weeks`, `key_milestone` |
| `process_narrative.es` | ✅ | 3–4 paragraphs in Spanish — Oficio Taller's process voice |
| `process_narrative.en` | ✅ | 3–4 paragraphs in English — native voice |

**Auto-fail:** Missing `es` or `en` key on any bilingual field, or any placeholder text, is an automatic scoring failure.

#### `legal-review.json`

**Written by:** Legal
**Read by:** Vera (DG-05 gate check)

IP and compliance review of the proposal before it goes to the architect.

| Field | Required | Description |
|---|---|---|
| `reviewed_by` | ✅ | Always `"Legal"` |
| `reviewed_at` | ✅ | ISO-8601 timestamp |
| `ip_rights_status` | ✅ | `clear`, `requires_clarification`, or `flagged` |
| `compliance_flags` | ✅ | Array — each flag: `flag`, `clause_reference`, `proposed_resolution`, `severity` (`blocking`\|`advisory`) |
| `approval_status` | ✅ | `approved`, `approved_with_advisory`, or `requires_revision` |

**Routing rule:** `requires_revision` blocks DG-05 — Vera will not send the architect review email.

#### `client-communication.json`

**Written by:** Rosa
**Read by:** Celia (DG-06 context)

Draft proposal delivery email. Must remain `"draft"` until Marcela approves at DG-06.

| Field | Required | Description |
|---|---|---|
| `channel` | ✅ | Always `"email"` |
| `message_body.es` | ✅ | Draft message in Spanish |
| `message_body.en` | conditional | English version if client communication has been bilingual |
| `project_reference` | ✅ | project_id |
| `status` | ✅ | Must be `"draft"` — **never `"sent"` before DG-06 approval** |

**Auto-fail:** `status: "sent"` before DG-06 approval bypasses Marcela review.

---

### Segment E — Activation & Scheduling

#### `project-schedule.json`

**Written by:** Pablo
**Read by:** Vera (construction dispatch), Hugo (executive plans), Controller (invoice due dates)

Full project timeline with ISO-8601 dates and Asana milestone subtasks.

| Field | Required | Description |
|---|---|---|
| `phases` | ✅ | Array — each phase: `phase_number`, `phase_name`, `start_date`, `end_date`, `duration_weeks`, `deliverables`, `milestone` |
| `milestone_dates` | ✅ | Object — keyed M1–M5 (or more); all ISO-8601 dates |
| `dependencies` | ✅ | Object — each phase keyed to its prerequisite phase |

---

### Segment F — Concept Design

#### `concept-review.json`

**Written by:** Andrés
**Read by:** Felipe

Post-presentation record of concept deliverables and assessment. Must be written after the presentation, not as a pre-presentation checklist.

| Field | Required | Description |
|---|---|---|
| `deliverables_checklist` | ✅ | Object — all 5 keys required: `3d_model`, `renders`, `material_direction`, `color_direction`, `space_arrangement`; each with `status` and `notes` |
| `presentation_date` | ✅ | ISO-8601 date the concept was presented |
| `presentation_milestone` | ✅ | Milestone name from scope-of-work.json (e.g., `M2 — Concept Approved`) |
| `review_notes` | ✅ | 2–3 sentences written after presentation: assessment vs. approved program, deviations flagged, approval recommendation |

**Auto-fail:** `presentation_date` missing or null; `review_notes` written in future tense (pre-presentation).

---

### Segment F → G — Architectural Design

#### `architectural-design.json`

**Written by:** Felipe
**Read by:** Emilio, Hugo

Verifies that the design set reflects the approved concept and area program.

| Field | Required | Description |
|---|---|---|
| `design_set_status` | ✅ | `in_progress`, `complete`, or `pending_revisions` |
| `concept_reflection_confirmed` | ✅ | Boolean — must be `true` to proceed to DG-08 |
| `area_program_compliance` | ✅ | Object: `compliant` (boolean), `deviations` (array), `notes` (string) |
| `structural_coordination_notes` | ✅ | String — structural engineer coordination status |

---

### Segment G — Engineering & Budget Alignment

#### `engineering-package.json`

**Written by:** Emilio
**Read by:** Hugo (executive plans)

Confirms all engineering disciplines are coordinated and ready for executive plans.

| Field | Required | Description |
|---|---|---|
| `systems_status` | ✅ | Object — always includes `structural`, `electrical`, `lighting`, `water`; conditional systems (`irrigation`, `solar`, `av`) only if in scope |
| `conditional_systems` | ✅ | Array of conditional system keys included (empty array `[]` if none) |
| `all_inputs_confirmed` | ✅ | Boolean — must be `true` to dispatch Bruno |
| `conflicts_resolved` | ✅ | Boolean — must be `true` to dispatch Bruno |

Each system in `systems_status`: `status` (`complete`\|`in_progress`\|`pending`), `engineer`, `notes`.

#### `budget-alignment.json`

**Written by:** Bruno (Segment G)
**Read by:** Ofelia

Compares contractor pricing to client budget. Triggers DG-09.

| Field | Required | Description |
|---|---|---|
| `contractor_pricing_source` | ✅ | How contractor pricing was obtained |
| `contractor_total` | ✅ | Total contractor estimate |
| `client_budget` | ✅ | Original client budget from budget.json |
| `variance_amount` | ✅ | `contractor_total - client_budget` |
| `variance_pct` | ✅ | `(contractor_total - client_budget) / client_budget × 100` |
| `recommendation` | ✅ | `proceed` (≤10%), `value_engineer` (10–25%), `escalate_to_marcela` (>25%) |

---

### Segment H — Executive Plans

#### `executive-plans.json`

**Written by:** Hugo
**Read by:** Paco, Ofelia

Final construction document set. Triggers DG-10.

| Field | Required | Description |
|---|---|---|
| `plan_set_components` | ✅ | Array — minimum 3 items; always includes architectural, structural, MEP; add specialty drawings per scope |
| `engineering_integration_confirmed` | ✅ | Boolean — all systems from engineering-package.json coordinated into plan set |
| `conflicts_resolved` | ✅ | Boolean — no outstanding coordination conflicts |
| `client_signoff_milestone` | ✅ | Milestone name (e.g., `M3 — Construction Documents Delivered`) |

---

### Segment I — Bidding & Permits

#### `bid-comparison.json`

**Written by:** Ofelia
**Read by:** Paco

Contractor bid summary with recommendation. Single-bid rule enforced.

| Field | Required | Description |
|---|---|---|
| `bids` | ✅ | Array — each bid: `contractor`, `total`, `currency`, `line_items`, `timeline`, `notes` |
| `recommendation` | ✅ | Contractor name, or `"escalate_to_marcela"` if single bid |
| `recommendation_rationale` | ✅ | Explanation; if single bid must state: "Only one bid was received." |

#### `permit-status.json`

**Written by:** Paco
**Read by:** Vera (construction unlock trigger)

Tracks permit submission and approval. Triggers construction phase when status reaches `approved`.

| Field | Required | Description |
|---|---|---|
| `submitted_at` | ✅ | ISO-8601 — date permit application was submitted (never null) |
| `jurisdiction` | ✅ | Specific municipality/authority (never a placeholder or null) |
| `status` | ✅ | `submitted`, `pending_corrections`, `approved`, or `rejected` |
| `corrections` | ✅ | Array — each correction: `received_at`, `description`, `resolved`; empty array `[]` if none |
| `approved_at` | ✅ | ISO-8601 when approved; `null` otherwise |

**Auto-fail:** `submitted_at` or `jurisdiction` null or missing. `approved_at` must be after `submitted_at` and before `project-schedule.json` construction start date.

---

### Segment J — Construction & Close

#### `invoice.json`

**Written by:** Controller (overwrites on each milestone)
**Read by:** Controller (running_total), Tax

One file per project — updated at each construction milestone. Each write overwrites the previous version (backup created as `invoice-previous.json` during write, deleted on success).

| Field | Required | Description |
|---|---|---|
| `project_name` | ✅ | `[client_name] — [project_type] — [location]` |
| `client_name` | ✅ | From state.json |
| `milestone_name` | ✅ | Milestone name from scope-of-work.json payment_schedule |
| `amount` | ✅ | This milestone's payment amount |
| `due_date` | ✅ | ISO-8601 payment due date |
| `payment_instructions` | ✅ | Bank name + CLABE (or placeholder) |
| `currency` | ✅ | `MXN` or `USD` — must match scope-of-work.json |
| `running_total` | ✅ | Cumulative total of all invoices for this project |

#### `tax-filing.json`

**Written by:** Tax (Segment J close only)
**Read by:** — (human accountant)

Tax filing record generated at project close.

| Field | Required | Description |
|---|---|---|
| `rfc` | ✅ | Oficio Taller RFC from `OFICIO_RFC` env var (or placeholder) |
| `revenue_amount` | ✅ | From invoice.json `running_total` |
| `tax_jurisdiction` | ✅ | Default `"Mexico — IVA 16%"` unless state.json specifies otherwise |
| `filing_period` | ✅ | `YYYY-MM` — month the project closed |
| `cfdi_reference` | ✅ | CFDI folio number, or placeholder `[CFDI — TO BE GENERATED BY ACCOUNTANT]` |
| `deductibles` | ✅ | Array of deductible items; empty array `[]` if none known |

---

### Decision Records

#### `decision-event.json`

**Written by:** Celia (after every Marcela gate)
**Read by:** — (audit trail only)

Immutable record of every Marcela gate decision. Written at DG-01 through DG-11.

| Field | Required | Description |
|---|---|---|
| `project_id` | ✅ | From state.json |
| `phase` | ✅ | Gate identifier: `DG-01` through `DG-11` |
| `review_item` | ✅ | Document being reviewed (see gate-to-review-item map in celia.md) |
| `reviewed_by` | ✅ | Always `"Marcela"` |
| `decision` | ✅ | `approve`, `reject`, or `pass_to_agent` |
| `comment` | ✅ | Marcela's comment verbatim, or `null` only if no comment text was present |
| `timestamp` | ✅ | ISO-8601 |
| `source_channel` | ✅ | Always `"email"` |
| `next_action` | ✅ | What happens next (from routing table in celia.md) |
| `route_to` | ✅ | Agent name being dispatched |
| `sync_to_asana` | ✅ | Always `true` |

---

## Document Flow by Segment

```
Segment A  Lupe ────────────────────── lead-record.json
                                        state.json (init)
                                        [spam: TC-007-segment-A-spam-confirmed.json → STOP]

  DG-01  Marcela ── Celia ─────────────── decision-event.json

Segment B  Lupe ────────────────────── lead-summary.json

Segment B→C  Elena ─────────────────── discovery-questionnaire.json
                                        client-fit-assessment.json

  DG-02  Marcela ── Celia ─────────────── decision-event.json

Segment C  Ana ─────────────────────── area-program.json
           Ana ─────────────────────── cost-basis.json
           Sol ─────────────────────── site-readiness-report.json
           Vera ────────────────────── [DG-03 trigger when both ready]

  DG-03  Marcela ── Celia ─────────────── decision-event.json

Segment D  Tomás ───────────────────── scope-of-work.json
           Bruno ───────────────────── budget.json
           Renata ──────────────────── proposal.json
           Legal ───────────────────── legal-review.json
           Rosa ────────────────────── client-communication.json

  DG-04  Architect ── Celia ────────── decision-event.json
  DG-05  Architect ── Celia ────────── decision-event.json
  DG-06  Marcela ── Celia ──────────── decision-event.json

Segment E  Vera (activation check)
           Pablo ───────────────────── project-schedule.json

Segment F  Andrés ──────────────────── concept-review.json

  DG-07  Marcela ── Celia ─────────────── decision-event.json

Segment F→G  Felipe ─────────────────── architectural-design.json

  DG-08  Marcela ── Celia ─────────────── decision-event.json

Segment G  Emilio ──────────────────── engineering-package.json
           Bruno ───────────────────── budget-alignment.json

  DG-09  Marcela ── Celia ─────────────── decision-event.json

Segment H  Hugo ────────────────────── executive-plans.json

  DG-10  Marcela ── Celia ─────────────── decision-event.json

Segment I  Ofelia ──────────────────── bid-comparison.json

  DG-11  Marcela ── Celia ─────────────── decision-event.json

           Paco ────────────────────── permit-status.json

Segment J  Vera (construction tracking)
           Controller ─────────────── invoice.json (× N milestones)
           [final milestone]
           Tax ─────────────────────── tax-filing.json
           Controller ─────────────── → marketing pipeline (Valentina)
```

---

## Summary Counts

| Category | Count |
|---|---|
| Templates | 6 (1 JSON + 5 SOW) |
| Per-project documents | 26 |
| State document | 1 (`state.json`) |
| **Total distinct document types** | **33** |
