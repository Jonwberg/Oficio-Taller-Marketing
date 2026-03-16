# Production Agents — Full Pipeline Design
**Date:** 2026-03-16
**Status:** Approved
**Scope:** 20 production agents covering pipeline segments A–J (lead intake through project close), infrastructure layer, SOW templates, and Marcela gate resume flow

---

## 1. Overview

Build the 20 production agents that power the Oficio Taller project delivery pipeline. These agents are tested by the existing workflow testing framework (`/test-segment`, `/test-full-run`). Once built, the full pipeline runs from inbound lead to project close with Marcela reviewing and deciding at 11 human gates via email.

**Design principles:**
- Each agent has one job and one clear deliverable
- Agents chain autonomously within a phase; Marcela gates pause the chain
- Asana tracks task state; `projects/[project_id]/` tracks content
- No agent hits an API directly — all external calls go through helper scripts
- Gmail receives Marcela's decisions (WhatsApp sending is a later upgrade — scope decision, see Section 11)

---

## 2. Scope Boundary

The full system design specifies 35 agents across 4 pods. This build covers **20 agents** from the Entrega pod only. The 15 agents not in scope for this build are:

| Deferred agent | Responsibility in full system | Interim handling |
|---|---|---|
| CFO | Approves Bruno's payment schedule | Bruno produces budget; Marcela's DG-03 approval covers cost basis. Payment schedule proceeds to Renata without separate CFO gate. |
| Finance Ops | Confirms 40% deposit received | Manual: Marcela confirms deposit via email reply to Vera's activation gate check. |
| COO | Escalation path for blockers | Manual: Vera escalates to Marcela directly on no-viable-bids. |
| FP&A | Quarterly forecasting | Deferred. |
| All 10 Marketing agents | Campaign pipeline | Already built and operational. |
| Alma | Performance monitoring | Deferred. |

---

## 3. Infrastructure Layer

Three Python modules in `entrega/`. Agents call these via the Bash tool — no agent hits an API directly.

### `entrega/asana_client.py`

Wraps all Asana API operations agents need. Reads `ASANA_PAT` from environment.

```python
# Functions exposed:
asana.create_project(name, team, sections, custom_fields)
asana.create_task(project_id, section, name, fields, tag)
asana.complete_task(task_id, comment)
asana.move_task(task_id, new_section)
asana.update_field(task_id, field_name, value)
asana.add_comment(task_id, agent_name, body)
asana.get_task(task_id)
asana.create_dependency(task_id, depends_on_id)
asana.create_subtask(parent_id, name, fields)
```

### `entrega/gmail_client.py`

All email operations for both Marcela gate flow and client-facing communications. Reads `GMAIL_CREDENTIALS_PATH` from environment.

```python
# Marcela gate flow:
gmail.send_review_request(to, subject, body) -> thread_id
gmail.read_latest_reply(thread_id) -> message_text | None
gmail.send_reminder(thread_id, to, body)       # reply on same thread at 24h
gmail.send_escalation(thread_id, to, body)     # reply on same thread at 48h

# Client-facing email (Elena questionnaire, Rosa proposal, Sol doc requests):
gmail.send_client_email(to, subject, body) -> thread_id
gmail.read_client_reply(thread_id) -> message_text | None
```

### `entrega/setup.py`

One-time scaffold script. Run once before any agents fire. Creates:
- Permanent Asana projects: Leads, Finanzas, Legal, Impuestos, Handoffs, Decisiones
- All custom field schemas (Entrega fields, Lead fields, Decision fields, Admin fields)
- Team structure

> Note: Operaciones and Performance Asana projects are deferred until COO and Alma are built.

### Environment variables required

```
ASANA_PAT=...
GMAIL_CREDENTIALS_PATH=...
MARCELA_EMAIL=...
ARCHITECT_EMAIL=...
```

---

## 4. Agent Architecture Pattern

### File location

All 20 delivery agents live in `.claude/agents/entrega/[name].md`. Grouped separately from marketing agents.

### YAML frontmatter

```yaml
---
name: [AgentName]
description: [Trigger description — when to invoke this agent]
color: [unique color]
tools: Bash, Read, Write, Glob
---
```

### System prompt structure

Every agent follows this section order:
1. **Role statement** — who the agent is, one job
2. **What to read before starting** — `state.json`, input deliverables, Asana context
3. **What to produce** — output file path + JSON schema (fields must match rubric Required fields exactly)
4. **Step-by-step protocol** — numbered steps
5. **Asana update** — which fields to update, which task to complete
6. **Chain instruction** — dispatch next agent (autonomous) or trigger gate (pause)

> Schema authority: For each deliverable, the required JSON fields are defined by the corresponding rubric in `tests/rubrics/`. Agent prompts must reference these fields explicitly. See Section 7 for the deliverable→rubric filename mapping.

### Autonomous chaining

At the end of its protocol, an agent that chains automatically dispatches the next agent via the `Agent` tool. Example: after Tomás writes `scope-of-work.json`, he dispatches Vera to send the architect SOW email (DG-04).

**Parallel dispatch after DG-02:** Celia dispatches both Ana and Sol simultaneously using two Agent tool calls. Both write to `projects/[project_id]/` independently. Tomás checks `state.json` for `area_program_complete: true` AND `site_data_complete: true` before proceeding. Sol signals completion by setting `state.json → site_data_complete: true` (does NOT dispatch Vera or Tomás directly).

### Marcela gate pause

At a gate, the agent:
1. Calls `python entrega/gmail_client.py send_review_request ...` with formatted email → captures `thread_id`
2. Updates `state.json`: `project_state: "awaiting_decision"`, `awaiting_gate: "DG-XX"`, `review_thread_id: "[thread_id]"`
3. Updates Asana task field `decision_status` to `awaiting`
4. Completes its Asana task and stops

### Pass to Agent at gates

At every Marcela gate, "Pass to Agent" is a valid third outcome. Behavior per gate:
- **DG-01:** Pass to Agent → Elena handles outreach autonomously (same as Approve but without Marcela's explicit endorsement)
- **DG-02:** Pass to Agent → Elena continues to coordinate fit assessment with minimal oversight
- **DG-03:** Pass to Agent → Tomás begins SOW immediately (same as Approve)
- **DG-07:** Pass to Agent → Andrés continues concept phase autonomously; `project_state` remains `concept_in_progress` (does NOT advance)
- **All other gates:** Pass to Agent → same routing as Approve unless Celia's decision payload specifies otherwise

---

## 5. Project File Structure

### `projects/[project_id]/state.json`

Every agent reads this first. Complete schema:

```json
{
  "project_id": "PRJ-2026-001",
  "project_state": "awaiting_decision",
  "awaiting_gate": "DG-01",
  "review_thread_id": "gmail_thread_id_here",
  "architect_email_thread_id": null,
  "asana_project_id": "...",
  "client_name": "",
  "client_email": "",
  "project_type": "standalone_residential",
  "area_program_complete": false,
  "site_data_complete": false,
  "revision_count": 0,
  "feedback_type": null,
  "contract_signed": false,
  "site_docs_complete": false,
  "deposit_confirmed": false,
  "tasks": {
    "lead_intake": "asana_task_id",
    "lead_review_gate": "asana_task_id",
    "discovery": "asana_task_id",
    "fit_gate": "asana_task_id",
    "area_program": "asana_task_id",
    "site_readiness": "asana_task_id",
    "cost_basis_gate": "asana_task_id",
    "scope_of_work": "asana_task_id",
    "sow_architect_gate": "asana_task_id",
    "budget": "asana_task_id",
    "proposal": "asana_task_id",
    "legal_review": "asana_task_id",
    "proposal_architect_gate": "asana_task_id",
    "client_proposal": "asana_task_id",
    "activation_gate": "asana_task_id",
    "schedule": "asana_task_id",
    "concept": "asana_task_id",
    "concept_gate": "asana_task_id",
    "architectural_design": "asana_task_id",
    "design_gate": "asana_task_id",
    "engineering": "asana_task_id",
    "budget_alignment": "asana_task_id",
    "budget_alignment_gate": "asana_task_id",
    "executive_plans": "asana_task_id",
    "final_approval_gate": "asana_task_id",
    "bidding": "asana_task_id",
    "contractor_selection_gate": "asana_task_id",
    "permitting": "asana_task_id",
    "construction": "asana_task_id",
    "invoice": "asana_task_id",
    "tax_filing": "asana_task_id"
  }
}
```

**Key state fields:**
- `area_program_complete` + `site_data_complete` — both must be `true` before Tomás begins (parallel track coordination)
- `revision_count` — Rosa increments on each client revision; max 3 before Marcela escalation
- `feedback_type` — set by rejection decision; used by Celia for routing at DG-05, DG-09, DG-10
- `contract_signed` + `site_docs_complete` + `deposit_confirmed` — all three must be `true` before Pablo fires

### Full deliverable set per project

```
projects/[project_id]/
  state.json
  lead-record.json
  lead-summary.json
  discovery-questionnaire.json
  client-fit-assessment.json       ← matches rubric filename
  area-program.json
  cost-basis.json
  site-readiness-report.json       ← matches rubric filename
  scope-of-work.json
  budget.json
  proposal.json
  legal-review.json
  client-communication.json
  project-schedule.json
  concept-review.json
  architectural-design.json
  engineering-package.json
  budget-alignment.json
  executive-plans.json
  bid-comparison.json
  permit-status.json
  invoice.json
  tax-filing.json
  decision-event.json              ← Celia writes at each gate
```

---

## 6. Deliverable → Rubric Filename Mapping

Implementers must use the rubric's Required fields as the authoritative JSON schema for each deliverable.

| Deliverable file | Rubric file | Required fields (from rubric) |
|---|---|---|
| `lead-record.json` | `lead-record.md` | source_channel, category, received_at, summary, status |
| `lead-summary.json` | `lead-summary.md` | project_name, source_channel, raw_message, initial_assessment, recommended_action |
| `discovery-questionnaire.json` | `discovery-questionnaire.md` | sent_to, sent_at, project_type_question, budget_question, timeline_question, location_question, special_requirements_question, design_style_question, site_ownership_question |
| `client-fit-assessment.json` | `client-fit-assessment.md` | meeting_notes, assessment_dimensions, recommendation, rationale |
| `area-program.json` | `area-program.md` | spaces (array), total_sqm, assumptions |
| `cost-basis.json` | `cost-basis.md` | cost_per_sqm, base_construction_cost, architecture_fee_pct, architecture_fee, engineering_allowance, contingency_pct, total_estimate, assumptions |
| `site-readiness-report.json` | `site-readiness-report.md` | required_documents, request_sent_at, current_status, blockers |
| `scope-of-work.json` | `scope-of-work.md` | scope_phases, payment_schedule, responsibilities_matrix, exclusions, revision_assumptions, project_type_clauses |
| `budget.json` | *(rubric TBD — see open items)* | project_name, client_name, milestone_name, amount, payment_instructions, currency, line_items |
| `proposal.json` | `proposal.md` | scope_summary, budget_detail, timeline_phases, process_narrative (ES + EN) |
| `legal-review.json` | `legal-review.md` | reviewed_by, reviewed_at, ip_rights_status, compliance_flags, approval_status |
| `client-communication.json` | `client-communication.md` | channel, message_body, project_reference, status |
| `project-schedule.json` | *(rubric TBD — see open items)* | phases (array), milestone_dates, dependencies |
| `concept-review.json` | `concept-review.md` | deliverables_checklist (includes: 3d_model, renders, material_direction, color_direction, space_arrangement), presentation_milestone, review_notes |
| `architectural-design.json` | `architectural-design.md` | design_set_status, concept_reflection_confirmed, area_program_compliance, structural_coordination_notes |
| `engineering-package.json` | `engineering-package.md` | systems_status (object with required: structural, electrical, lighting, water; conditional: irrigation, solar, av — only include if in scope), conditional_systems, all_inputs_confirmed, conflicts_resolved |
| `budget-alignment.json` | `budget-alignment.md` | contractor_pricing_source, contractor_total, client_budget, variance_amount, variance_pct, recommendation |
| `executive-plans.json` | `executive-plans.md` | plan_set_components (array, min 3 items), engineering_integration_confirmed, conflicts_resolved, client_signoff_milestone |
| `bid-comparison.json` | `bid-comparison.md` | bids (array with contractor, total, line_items, timeline, notes), recommendation, recommendation_rationale |
| `permit-status.json` | *(rubric TBD — see open items)* | submitted_at, jurisdiction, status, corrections (array), approved_at |
| `invoice.json` | `controller-invoice.md` | project_name, client_name, milestone_name, amount, due_date, payment_instructions, currency, running_total |
| `tax-filing.json` | `tax-filing.md` | rfc, revenue_amount, tax_jurisdiction, filing_period, cfdi_reference, deductibles |
| `decision-event.json` | `celia-decision-routing.md` | project_id, phase, review_item, reviewed_by, decision, comment, timestamp, source_channel, next_action, route_to, sync_to_asana |

**Note on `concept-review.json`:** `deliverables_checklist` uses `space_arrangement` (not "spatial intent") and includes `color_direction`. Both are required by the rubric.

**Note on `engineering-package.json`:** `systems_status` must include `structural`, `electrical`, `lighting`, `water` as always-required keys. `irrigation`, `solar`, `av` are conditional — only include if the project scope includes them. The `av` key covers both sound and AV systems (per system design). This prevents false failures on projects where these systems are not in scope.

---

## 7. SOW Templates

Five markdown templates, one per project type. Created from existing Oficio Taller SOW documents in Google Drive.

```
docs/templates/sow/
  sow-standalone-residential.md
  sow-residential-in-development.md
  sow-commercial-hotel.md
  sow-commercial-health-center.md
  sow-public-civic.md
```

Each template defines:
- Phase structure (which phases apply to this project type)
- Standard deliverables per phase
- Collaborator requirements (structural engineer, systems engineers, etc.)
- `project_type_clauses` — project-type-specific contract terms (required by scope-of-work rubric)
- Standard exclusions
- Payment milestone skeleton (percentages, trigger events)
- Revision assumptions

Tomás reads the matching template + `area-program.json` + `cost-basis.json` to produce a project-specific `scope-of-work.json`.

---

## 8. The 20 Agents

### Agent roster

| Agent | File | Segment | Deliverable |
|---|---|---|---|
| Lupe | `entrega/lupe.md` | A, B | `lead-record.json`, `lead-summary.json` |
| Celia | `entrega/celia.md` | All gates | `decision-event.json` |
| Elena | `entrega/elena.md` | B | `discovery-questionnaire.json`, `client-fit-assessment.json` |
| Ana | `entrega/ana.md` | C | `area-program.json`, `cost-basis.json` |
| Sol | `entrega/sol.md` | C | `site-readiness-report.json` |
| Vera | `entrega/vera.md` | C, D, E, J | `site-status-update` (Asana only), architect emails (Gmail), activation confirmation |
| Tomás | `entrega/tomas.md` | D | `scope-of-work.json` |
| Bruno | `entrega/bruno.md` | D, G | `budget.json`, `budget-alignment.json` |
| Renata | `entrega/renata.md` | D | `proposal.json` |
| Legal | `entrega/legal.md` | D | `legal-review.json` |
| Rosa | `entrega/rosa.md` | D | `client-communication.json` |
| Pablo | `entrega/pablo.md` | E | `project-schedule.json` |
| Andrés | `entrega/andres.md` | F | `concept-review.json` |
| Felipe | `entrega/felipe.md` | F | `architectural-design.json` |
| Emilio | `entrega/emilio.md` | G | `engineering-package.json` |
| Hugo | `entrega/hugo.md` | H | `executive-plans.json` |
| Ofelia | `entrega/ofelia.md` | I | `bid-comparison.json` |
| Paco | `entrega/paco.md` | I | `permit-status.json` |
| Controller | `entrega/controller.md` | J | `invoice.json` |
| Tax | `entrega/tax.md` | J | `tax-filing.json` |

> **Vera's deliverables:** Vera does not write scored JSON deliverables — she updates Asana task state and sends/monitors Gmail threads. Her test segment (C) scores are evaluated on Asana field accuracy and email send correctness rather than a JSON file.

### Agent summaries

**Lupe** — Monitors inbound channels, runs legitimacy screen, classifies inquiry type (project / speaking / collaboration / press / spam), creates Asana lead task. On non-spam: writes `lead-record.json`, sends DG-01 review request to Marcela via Gmail. Segment A. At Segment B: re-reads the approved lead, writes `lead-summary.json` with full context for Elena.

**Celia** — Parses Marcela's email reply (Approve / Reject / Pass to Agent + optional comment), produces normalized `decision-event.json` with all 11 required fields (`project_id, phase, review_item, reviewed_by, decision, comment, timestamp, source_channel, next_action, route_to, sync_to_asana`), updates Asana decision fields, updates `state.json`, routes to correct next agent. Cross-pod infrastructure invoked at every Marcela gate by `/resume-project`. Field is `route_to` (not `routed_to`).

**Elena** — After DG-01 approval: sends discovery questionnaire to lead via `gmail.send_client_email`, captures response via `gmail.read_client_reply`, schedules and documents first meeting, prepares client fit assessment. Writes `discovery-questionnaire.json` (9 required fields) and `client-fit-assessment.json`. Triggers DG-02 review request to Marcela.

**Ana** — After DG-02 approval: Celia dispatches Ana and Sol in parallel. Ana builds room-by-room area program matrix and preliminary cost basis. Writes `area-program.json` and `cost-basis.json`. Sets `state.json → area_program_complete: true`. Triggers DG-03 only if `site_data_complete` is also true; otherwise waits.

**Sol** — After DG-02 approval (parallel with Ana): requests required site documentation (topographic map, hydrologic assessment) via `gmail.send_client_email`, tracks receipt status, flags blockers. Writes `site-readiness-report.json`. Sets `state.json → site_data_complete: true`. Does NOT dispatch any downstream agent directly. Ana's completion check triggers DG-03 when both tracks are done.

**Vera** — Multi-phase tracker with no scored JSON deliverable.
- *Segment C:* Reads Sol's `site-readiness-report.json`, updates Asana site readiness status field.
- *Segment D (DG-04):* After Tomás completes SOW, assembles formatted SOW package and sends architect notification via `gmail.send_review_request` using `ARCHITECT_EMAIL`. Stores `architect_email_thread_id` in `state.json`. Polls for reply via `/resume-project` equivalent. Sends reminder at 24h, escalates to Marcela at 48h via `gmail.send_reminder`/`gmail.send_escalation`. On approval: dispatches Bruno. On flag/rejection: dispatches Tomás with architect feedback.
- *Segment D (DG-05):* After Legal review, assembles full proposal package and sends architect approval notification. Same 24h/48h logic. On approval: dispatches Rosa.
- *Segment E:* Monitors `state.json` for `contract_signed: true`, `site_docs_complete: true`, `deposit_confirmed: true`. When all three true: dispatches Pablo.
- *Segment J:* Tracks construction milestones per Pablo's schedule. Dispatches Controller at each milestone. At project close, dispatches Tax and triggers marketing pipeline.

**Tomás** — After DG-03 approval: reads `area-program.json` + `cost-basis.json` + `project_type` from `state.json`, selects matching SOW template, generates project-specific `scope-of-work.json` including `project_type_clauses`. Dispatches Vera (DG-04 architect SOW notification).

**Bruno** — Two modes.
- *Segment D:* After Vera receives architect SOW approval (DG-04), Vera dispatches Bruno. Bruno prices scope into itemized `budget.json` including `project_name, client_name, milestone_name, amount, payment_instructions, currency, line_items`. No separate CFO gate — budget proceeds directly to Renata (see Section 2 scope boundary).
- *Segment G:* After Emilio completes engineering, writes `budget-alignment.json`. Triggers DG-09 review request to Marcela.

**Renata** — After Bruno completes budget: assembles client-facing `proposal.json` (SOW summary + detailed budget + timeline + Oficio Taller process narrative, ES + EN). Dispatches Legal for clause review.

**Legal** — Reviews proposal clauses. Writes `legal-review.json` with `approval_status`. Dispatches Vera (DG-05 architect proposal notification).

**Rosa** — After architect approves proposal (DG-05): sends proposal to client via `gmail.send_client_email`. Monitors client response. Triggers DG-06. On approval: sets `state.json → contract_signed` path begins via Legal. On revision: reads `feedback_type` from Celia's `decision-event.json`, increments `revision_count` in `state.json`, routes to: Renata (copy), Tomás (scope), Bruno (budget). Max 3 revisions before routing to Marcela. On hard rejection: dispatches Vera (close project). Writes `client-communication.json` at each send.

**Feedback_type routing table (Rosa/Celia):**
| feedback_type | Route to |
|---|---|
| copy | Renata |
| scope | Tomás |
| budget | Bruno |
| legal | Legal |

**Pablo** — After all three activation conditions confirmed (Vera dispatches): builds full project timeline, creates Asana milestone tasks as subtasks via `asana.create_subtask`. Writes `project-schedule.json`. Updates schedule as phases close.

**Andrés** — After concept approval gate cleared: coordinates concept deliverables with architect. Writes `concept-review.json` with `deliverables_checklist` containing: `3d_model`, `renders`, `material_direction`, `color_direction`, `space_arrangement`. Triggers DG-07.

**Felipe** — After DG-07 approval: manages architectural design set development. Writes `architectural-design.json`. Triggers DG-08.

**Emilio** — After DG-08 approval: coordinates structural and all systems engineering. `systems_status` includes always-required systems (`structural`, `electrical`, `lighting`, `water`) plus conditional systems only if in project scope (`irrigation`, `solar`, `av` — where `av` covers both sound and AV). Writes `engineering-package.json`. Dispatches Bruno (budget alignment mode).

**Hugo** — After DG-09 approval: coordinates Fase Ejecutiva. Writes `executive-plans.json` with `plan_set_components` (minimum 3 items). Triggers DG-10.

**Ofelia** — After DG-10 approval: requests bids, assembles `bid-comparison.json`. If only one bid received, flags explicitly in `recommendation_rationale` and escalates to Marcela as a decision (does not auto-select). Triggers DG-11.

**Paco** — After DG-11 contractor selection: manages permit submission and tracking. Writes `permit-status.json`. On permit approval: notifies Vera to unlock construction phase.

**Controller** — Dispatched by Vera at each milestone. Writes `invoice.json` with all 8 required fields including `payment_instructions` and `currency`. Also produces final invoice at project close.

**Tax** — Dispatched by Vera at project close. Writes `tax-filing.json`. Must use Mexican tax jurisdiction (IVA 16%) unless `tax_jurisdiction` in `state.json` explicitly specifies otherwise.

---

## 9. Marcela Gates & Resume Flow

### Gate map

| Gate | Phase | Managed by | Approves → | Rejects → | Pass to Agent → |
|---|---|---|---|---|---|
| DG-01 | Lead review | Lupe | Elena | Archive lead | Elena (autonomous outreach) |
| DG-02 | Fit decision | Elena | Ana + Sol (parallel, Celia dispatches both) | Rosa (polite decline) | Elena continues |
| DG-03 | Cost basis review | Ana | Tomás | Ana (revise) | Tomás (same as Approve) |
| DG-04 | SOW architect review | Vera | Bruno (Vera dispatches) | Tomás (Vera dispatches with feedback) | N/A — architect gates are Approve/Flag only |
| DG-05 | Proposal architect approval | Vera | Rosa | Renata/Tomás/Bruno per `feedback_type` | N/A |
| DG-06 | Client proposal response | Rosa | Legal (contract begins) | Rosa (revision loop, max 3) | Rosa continues |
| DG-07 | Concept review | Andrés | Felipe | Andrés (revise) | Andrés continues; `project_state` stays `concept_in_progress` |
| DG-08 | Architectural design | Felipe | Emilio | Felipe (revise) | Felipe continues |
| DG-09 | Budget alignment | Bruno | Hugo | Felipe or Emilio per `feedback_type` | Hugo (same as Approve) |
| DG-10 | Executive plans | Hugo | Ofelia | Hugo (revise; routes to Felipe or Emilio per `feedback_type`) | Ofelia (same as Approve) |
| DG-11 | Contractor selection | Ofelia | Paco | Ofelia (re-bid) | Ofelia continues |

DG-04 and DG-05 use `architect_email_thread_id` in `state.json`. All other gates use `review_thread_id`.

### `/resume-project [project_id]` skill

Handles all Marcela gate continuations:

1. Read `projects/[project_id]/state.json` — find `awaiting_gate` and `review_thread_id`
2. Call `python entrega/gmail_client.py read_latest_reply [thread_id]`
3. If no reply: report "No reply yet for [gate] on [project_id]" and stop
4. Dispatch Celia with the reply text and gate context
5. Celia writes `decision-event.json`, updates `state.json` and Asana
6. Skill dispatches correct next agent based on `decision` field and gate map above

**Invocation:** `/resume-project` must be run manually after Marcela replies. There is no automatic polling in Phase 1. A future build will add a cron-based poller that runs `/resume-project` for all projects with `project_state: "awaiting_decision"`. For now, Marcela's email reply is the trigger for the operator to run the skill.

### Review request email format

```
Project: [client_name] — [project_type]
Phase: [phase_name]
Gate: [DG-XX]

Summary:
[2–3 sentence summary of what was produced and what decision is needed]

Choose one:
- Approve
- Reject — [optional note]
- Pass to Agent — [optional note]
```

---

## 10. plugin.json Updates

Add all 20 agents to `plugin.json` under `agents`:

```
".claude/agents/entrega/lupe.md"
".claude/agents/entrega/celia.md"
".claude/agents/entrega/elena.md"
".claude/agents/entrega/ana.md"
".claude/agents/entrega/sol.md"
".claude/agents/entrega/vera.md"
".claude/agents/entrega/tomas.md"
".claude/agents/entrega/bruno.md"
".claude/agents/entrega/renata.md"
".claude/agents/entrega/legal.md"
".claude/agents/entrega/rosa.md"
".claude/agents/entrega/pablo.md"
".claude/agents/entrega/andres.md"
".claude/agents/entrega/felipe.md"
".claude/agents/entrega/emilio.md"
".claude/agents/entrega/hugo.md"
".claude/agents/entrega/ofelia.md"
".claude/agents/entrega/paco.md"
".claude/agents/entrega/controller.md"
".claude/agents/entrega/tax.md"
```

Add one new skill: `".claude/skills/resume-project.md"`

---

## 11. Scope Decision: WhatsApp

The full system design specifies WhatsApp as Marcela's primary decision channel (via Business API). This build uses **Gmail only** as the decision channel — both for sending review requests and reading replies. WhatsApp sending via Playwright (existing `send-whatsapp.py` pattern) will be added in a future build once the pipeline is proven on Gmail. This is a deliberate scope reduction, not an oversight.

---

## 12. Build Sequence

Build in this order so each group is testable before the next:

1. **Infrastructure** — `asana_client.py`, `gmail_client.py`, `setup.py`, `projects/` directory, `.env` template
2. **SOW templates** — 5 markdown files from existing Drive documents
3. **Missing rubrics** — `budget.md`, `project-schedule.md`, `permit-status.md` (see open items)
4. **Segment A** — Lupe + Celia
5. **Segment B** — Elena
6. **Segment C** — Ana, Sol, Vera (partial — site readiness + Asana tracking)
7. **Segment D** — Tomás, Bruno, Renata, Legal, Rosa, Vera (architect email gates)
8. **Segment E** — Pablo, Vera (activation gate)
9. **Segments F–H** — Andrés, Felipe, Emilio, Hugo
10. **Segments I–J** — Ofelia, Paco, Controller, Tax
11. **`/resume-project` skill** — wires all Marcela gates
12. **`plugin.json` update** — register all 20 agents and `/resume-project` skill

---

## 13. Open Items (Pre-Build)

**Credentials (required before any agents can run):**
- [ ] Asana Personal Access Token
- [ ] Gmail API credentials (`credentials.json` + OAuth setup)
- [ ] Marcela's email address
- [ ] Architect email address(es) for DG-04/DG-05

**Content (required before specific agents can be built):**
- [ ] Access to existing SOW documents in Google Drive — Tomás's 5 templates
- [ ] Discovery questionnaire templates by project type (5 needed, one per project type) — Elena
- [ ] Payment milestone percentages — Bruno's default template (e.g. 30% signing / 30% design / 40% delivery)
- [ ] Spam classification criteria — explicit definition for Lupe's discard rules

**Missing rubrics (required before test framework can score these agents):**
- [ ] `tests/rubrics/budget.md` — Bruno Segment D deliverable
- [ ] `tests/rubrics/project-schedule.md` — Pablo deliverable
- [ ] `tests/rubrics/permit-status.md` — Paco deliverable
- [ ] `tests/rubrics/vera-site-status.md` — Vera Segment C Asana update validation

**Deferred to future build:**
- [ ] WhatsApp sending for review requests (Playwright pattern already exists)
- [ ] Automatic `/resume-project` poller (cron-based)
- [ ] CFO, Finance Ops, COO, FP&A, Alma agents
- [ ] Asana webhook listener for automatic agent triggering
