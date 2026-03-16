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
- Gmail receives Marcela's decisions (WhatsApp sending is a later upgrade)

---

## 2. Infrastructure Layer

Three Python modules in `entrega/`. Agents call these via the Bash tool.

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
```

### `entrega/gmail_client.py`

Two operations for review gate email flow. Reads `GMAIL_CREDENTIALS_PATH` from environment.

```python
gmail.send_review_request(to, subject, body) -> thread_id
gmail.read_latest_reply(thread_id) -> message_text | None
```

### `entrega/setup.py`

One-time scaffold script. Run once before any agents fire. Creates:
- Permanent Asana projects: Leads, Finanzas, Legal, Impuestos, Operaciones, Performance, Handoffs, Decisiones
- All custom field schemas (Entrega fields, Lead fields, Decision fields, Admin fields)
- Team structure

### Environment variables required

```
ASANA_PAT=...
GMAIL_CREDENTIALS_PATH=...
MARCELA_EMAIL=...
ARCHITECT_EMAIL=...
```

---

## 3. Agent Architecture Pattern

### File location

All 20 delivery agents live in `.claude/agents/entrega/[name].md`. Grouped separately from marketing agents (`arquitecto.md`, `lucia.md`, etc.).

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
3. **What to produce** — output file path + JSON schema
4. **Step-by-step protocol** — numbered steps
5. **Asana update** — which fields to update, which task to complete
6. **Chain instruction** — dispatch next agent (autonomous) or trigger gate (pause)

### Autonomous chaining

At the end of its protocol, an agent that chains automatically dispatches the next agent via the `Agent` tool. Example: after Tomás writes `scope-of-work.json`, he dispatches Vera to send the architect SOW email (DG-04).

### Marcela gate pause

At a gate, the agent:
1. Calls `python entrega/gmail_client.py send_review_request ...` with formatted email
2. Updates `state.json`: `"project_state": "awaiting_decision"`, `"awaiting_gate": "DG-XX"`, `"review_thread_id": "[thread_id]"`
3. Updates Asana task field `decision_status` to `awaiting`
4. Completes its Asana task and stops

---

## 4. Project File Structure

### `projects/[project_id]/state.json`

Every agent reads this first. Holds current project state and all Asana task IDs.

```json
{
  "project_id": "PRJ-2026-001",
  "project_state": "awaiting_decision",
  "awaiting_gate": "DG-01",
  "review_thread_id": "gmail_thread_id_here",
  "asana_project_id": "...",
  "client_name": "",
  "project_type": "standalone_residential",
  "architect_email_thread_id": null,
  "tasks": {
    "lead_intake": "asana_task_id",
    "discovery": "asana_task_id",
    "area_program": "asana_task_id"
  }
}
```

### Full deliverable set per project

```
projects/[project_id]/
  state.json
  lead-record.json
  lead-summary.json
  discovery-questionnaire.json
  fit-assessment.json
  area-program.json
  cost-basis.json
  site-readiness.json
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
```

---

## 5. SOW Templates

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
- Standard exclusions
- Payment milestone skeleton (percentages, trigger events)
- Revision assumptions

Tomás reads the matching template + `area-program.json` + `cost-basis.json` to produce a project-specific `scope-of-work.json`.

---

## 6. The 20 Agents

### Agent roster

| Agent | File | Segment | Deliverable |
|---|---|---|---|
| Lupe | `entrega/lupe.md` | A, B | `lead-record.json`, `lead-summary.json` |
| Celia | `entrega/celia.md` | All gates | `decision-event.json` |
| Elena | `entrega/elena.md` | B | `discovery-questionnaire.json`, `fit-assessment.json` |
| Ana | `entrega/ana.md` | C | `area-program.json`, `cost-basis.json` |
| Sol | `entrega/sol.md` | C | `site-readiness.json` |
| Vera | `entrega/vera.md` | C, D, E, J | `site-status.json`, `architect-email.json`, `activation-status.json` |
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

### Agent summaries

**Lupe** — Monitors inbound channels, runs legitimacy screen, classifies inquiry type (project / speaking / collaboration / press / spam), creates Asana lead task. On non-spam: writes `lead-record.json`, sends lead summary to Marcela for DG-01. Segment A. At Segment B re-invocation: writes `lead-summary.json` with full context for Elena.

**Celia** — Parses Marcela's email reply (Approve / Reject / Pass to Agent + optional comment), produces normalized `decision-event.json` with all 11 required fields, updates Asana decision fields, routes to correct next agent. Cross-pod infrastructure invoked at every Marcela gate by `/resume-project`.

**Elena** — After DG-01 approval: sends discovery questionnaire to lead, captures response, schedules and documents first meeting, prepares client fit assessment. Writes `discovery-questionnaire.json` and `fit-assessment.json`. Triggers DG-02 (fit decision gate).

**Ana** — After DG-02 approval: builds room-by-room area program matrix (sq m per space, total programmed sq m, assumptions). Derives preliminary cost basis (cost per sq m, total estimate, architecture fee, engineering allowance, contingency). Writes `area-program.json` and `cost-basis.json`. Triggers DG-03 (cost basis review).

**Sol** — Runs in parallel with Ana after DG-02: requests required site documentation (topographic map, hydrologic assessment), tracks receipt status, flags blockers. Writes `site-readiness.json`. When complete, updates Vera.

**Vera** — Multi-phase tracker. At Segment C: monitors site readiness, updates `site-status.json`. At Segment D: assembles and sends SOW architect notification (DG-04) and proposal architect notification (DG-05) via Gmail, monitors for architect reply with 24h/48h escalation logic. At Segment E: confirms activation gate (contract signed + site docs complete + 40% deposit) before Pablo fires. At Segment J: tracks construction milestones, triggers Controller at each milestone, closes project at completion.

**Tomás** — After DG-03 approval: reads area program + cost basis + project type, selects matching SOW template from `docs/templates/sow/`, generates project-specific scope of work with deliverables by phase, payment schedule, collaborator requirements, exclusions, responsibilities matrix. Writes `scope-of-work.json`. Dispatches Vera (architect SOW email DG-04).

**Bruno** — Two modes. Segment D: after architect approves SOW, prices scope into itemized budget + payment milestone schedule. Writes `budget.json`. Segment G: after Emilio completes engineering, requests contractor pricing, compares against client budget, recommends proceed or redesign. Writes `budget-alignment.json`. Triggers DG-09.

**Renata** — After CFO approves budget: assembles client-facing proposal (SOW summary + detailed budget + timeline + Oficio Taller process narrative). Bilingual (ES primary, EN secondary). Writes `proposal.json`. Dispatches Legal for clause review.

**Legal** — Shared across pods. Reviews proposal clauses before client delivery. Flags compliance issues, IP rights, contract terms. Writes `legal-review.json` with `approval_status`. Dispatches Vera (architect proposal approval email DG-05).

**Rosa** — After architect approves proposal: sends proposal to client via email. Monitors client response. On approval: triggers Legal (contract) + CFO. On revision: classifies `feedback_type` (budget / scope / copy / legal) and routes to correct agent. On hard rejection: triggers Vera (close project). Writes `client-communication.json` at each send. Triggers DG-06.

**Pablo** — After activation gate clears: builds full project timeline and Asana milestone task map. Writes `project-schedule.json` with phase durations, milestone dates, dependencies. Updates schedule as phases close.

**Andrés** — Manages concept design phase: coordinates concept deliverables brief (3D model, renders, material direction, spatial intent) with architect. Tracks production. Writes `concept-review.json` with deliverables checklist and review notes. Triggers DG-07.

**Felipe** — After concept approval (DG-07): manages architectural design set development. Confirms design set is ready for engineering coordination. Writes `architectural-design.json`. Triggers DG-08.

**Emilio** — After architectural design approval (DG-08): coordinates structural and systems engineering (electrical, lighting, water, irrigation, solar, AV). Tracks all consultant inputs. Confirms complete engineering package. Writes `engineering-package.json`. Dispatches Bruno (budget alignment).

**Hugo** — After budget alignment approval (DG-09): coordinates Fase Ejecutiva production (cross sections, full plan set, technical coordination). Confirms client sign-off milestone. Writes `executive-plans.json`. Triggers DG-10.

**Ofelia** — After executive plans approval (DG-10): requests bids from multiple contractors, assembles comparison matrix. Writes `bid-comparison.json` with bids array, recommendation, rationale. Triggers DG-11 (contractor selection).

**Paco** — After contractor selected (DG-11): assembles permit package, submits to jurisdiction, tracks status, manages correction cycles. Writes `permit-status.json`. Notifies Vera when permit approved (unlocks construction phase).

**Controller** — Invoked by Vera at each payment milestone. Issues invoice per Bruno's payment schedule. Writes `invoice.json` with milestone name, amount, due date, running total. Also produces final invoice at project close.

**Tax** — Invoked at project close. Produces tax filing for project revenue. Writes `tax-filing.json` with RFC, revenue amount, jurisdiction, filing period, CFDI reference, deductibles.

---

## 7. Marcela Gates & Resume Flow

### Gate map

| Gate | Phase | Approves → | Rejects → |
|---|---|---|---|
| DG-01 | Lead review | Elena | Archive lead |
| DG-02 | Fit decision | Ana + Sol (parallel) | Rosa (polite decline) |
| DG-03 | Cost basis review | Tomás | Ana (revise) |
| DG-04 | SOW architect review (Vera) | Bruno | Tomás (revise) |
| DG-05 | Proposal architect approval (Vera) | Rosa (send to client) | Renata/Tomás/Bruno per `feedback_type` |
| DG-06 | Client proposal response | Legal + CFO | Rosa (revision loop, max 3) |
| DG-07 | Concept review | Felipe | Andrés (revise) |
| DG-08 | Architectural design | Emilio | Felipe (revise) |
| DG-09 | Budget alignment | Hugo | Felipe or Emilio per `feedback_type` |
| DG-10 | Executive plans | Ofelia | Hugo (revise, routes to Felipe or Emilio per feedback) |
| DG-11 | Contractor selection | Paco | Ofelia (re-bid) |

DG-04 and DG-05 are architect email gates — Vera manages, uses `architect_email_thread_id` in `state.json`.

### `/resume-project [project_id]` skill

Handles all Marcela gate continuations:

1. Read `projects/[project_id]/state.json` — find `awaiting_gate` and `review_thread_id`
2. Call `python entrega/gmail_client.py read_latest_reply [thread_id]`
3. If no reply: report "No reply yet for [gate] on [project_id]" and stop
4. Dispatch Celia with the reply text and gate context
5. Celia writes `decision-event.json`, updates `state.json` and Asana
6. Skill dispatches correct next agent based on `decision` field

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

## 8. plugin.json Updates

Add all 20 agents to `plugin.json`:

```json
"agents": [
  ... (existing 10 marketing agents + 3 test agents),
  ".claude/agents/entrega/lupe.md",
  ".claude/agents/entrega/celia.md",
  ".claude/agents/entrega/elena.md",
  ".claude/agents/entrega/ana.md",
  ".claude/agents/entrega/sol.md",
  ".claude/agents/entrega/vera.md",
  ".claude/agents/entrega/tomas.md",
  ".claude/agents/entrega/bruno.md",
  ".claude/agents/entrega/renata.md",
  ".claude/agents/entrega/legal.md",
  ".claude/agents/entrega/rosa.md",
  ".claude/agents/entrega/pablo.md",
  ".claude/agents/entrega/andres.md",
  ".claude/agents/entrega/felipe.md",
  ".claude/agents/entrega/emilio.md",
  ".claude/agents/entrega/hugo.md",
  ".claude/agents/entrega/ofelia.md",
  ".claude/agents/entrega/paco.md",
  ".claude/agents/entrega/controller.md",
  ".claude/agents/entrega/tax.md"
]
```

Add one new skill:

```json
".claude/skills/resume-project.md"
```

---

## 9. Build Sequence

Build in this order so each group is testable before the next:

1. **Infrastructure** — `asana_client.py`, `gmail_client.py`, `setup.py`, `projects/` directory structure
2. **SOW templates** — 5 markdown files from existing Drive documents
3. **Segment A** — Lupe + Celia (core agents, simplest segment, TC-007 testable immediately)
4. **Segment B** — Elena
5. **Segment C** — Ana, Sol, Vera (partial)
6. **Segment D** — Tomás, Bruno, Renata, Legal, Rosa, Vera (architect gates)
7. **Segment E** — Pablo, Vera (activation gate)
8. **Segments F–H** — Andrés, Felipe, Emilio, Hugo
9. **Segments I–J** — Ofelia, Paco, Controller, Tax
10. **`/resume-project` skill** — wires all gates
11. **`plugin.json` update** — register all agents and skill

---

## 10. Open Items (Pre-Build)

- [ ] Asana Personal Access Token — needed for `setup.py` and all Asana calls
- [ ] Gmail API credentials — needed for `gmail_client.py`
- [ ] Marcela's email address — review request recipient
- [ ] Architect email address(es) — DG-04 / DG-05 recipients
- [ ] Access to existing SOW documents in Google Drive — needed for template creation
- [ ] Payment milestone percentages — Bruno's default template (e.g. 30% signing / 30% design / 40% delivery)
- [ ] Spam classification criteria — explicit definition for Lupe's discard rules
