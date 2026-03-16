# Oficio Taller — Full Agent System Design
**Date:** 2026-03-14
**Revised:** 2026-03-15 — expanded from architectural operating manual
**Status:** Draft — pending user review
**Scope:** Complete autonomous agent operating system covering project delivery (full lifecycle), administration, marketing, and performance monitoring — integrated via Asana

---

## 1. System Overview

Oficio Taller operates as a studio of architecture led by Marcela González Veloz. The business has three intersecting operational streams: delivering architectural projects, marketing the studio's work, and managing administration and finance. Today these streams operate without a shared coordination layer and require significant manual orchestration from Marcela.

This system replaces that manual layer with 35 autonomous AI agents organized into four pods, all coordinated through a single Asana workspace. The file-based marketing pipeline already in production remains unchanged — Asana is added as the coordination and visibility layer, not a replacement for existing state management.

**Design principles:**
- Each agent has one job and one clear handoff
- Humans review through **WhatsApp** (primary) and **email** (secondary) — never through the Asana UI
- Every human decision has three possible outcomes: **Approve / Reject / Pass to Agent**
- All human decisions are captured as normalized events and synced into Asana automatically by Celia (Decision Capture)
- Agents operate from unified project state — not isolated messages
- Project state advances only when prerequisites are satisfied
- Content and campaign files live on disk (JSON); task coordination lives in Asana
- **No project activates without:** signed scope, required site documents, and 40% deposit
- **No executive plans begin until** budget alignment is confirmed after engineering
- The system is built to receive human team members later without architectural changes
- Every gap in the current flow is resolved before the relevant phase ships

---

## 2. Agent Roster — 35 Agents, 4 Pods

### Pod: Entrega — Project Delivery (16 agents)

#### Pre-Activation: Lead through Activation

| Agent | Responsibility |
|---|---|
| **Lupe** | Inbound intelligence — monitors all channels (Instagram, Gmail, WhatsApp, website, YouTube, professional contacts), runs initial legitimacy screen (spam/phishing filter), classifies inbound as project inquiry / speaking invite / collaboration / press / spam, creates Asana lead task for every non-spam inbound |
| **Elena** | Discovery & fit — sends initial questionnaire to approved leads, captures structured lead response, schedules and documents first-meeting notes, prepares client-fit assessment summary for Marcela's review gate |
| **Ana** | Pre-scope analyst — once fit is confirmed: builds room-by-room area program matrix, calculates programmed square meters, produces area spreadsheet; then derives preliminary cost logic (sq m basis + assumptions) as input for Tomás |
| **Sol** | Site intelligence — runs in parallel with area program: requests and tracks required site documentation (topographic map, hydrologic assessment), monitors site readiness, flags blockers to Vera |
| **Tomás** | Scope generator — consumes Ana's area program + cost basis + Sol's site confirmation + project type to produce detailed SOW: deliverables by phase, collaborator requirements, timeline structure, payment schedule, exclusions, responsibilities matrix |
| **Bruno** | Cost estimator — prices Tomás's architect-approved scope into itemized budget; later (post-engineering) performs budget alignment analysis between contractor pricing and client budget, recommends proceed or redesign |
| **Renata** | Proposal writer — assembles client-facing proposal: SOW + detailed budget + timeline + Oficio Taller process narrative. Bilingual (ES primary, EN secondary) |
| **Rosa** | Client communications — owns all outbound client contact throughout the project: confirmations, status updates, revision acknowledgements, milestone notifications, proposal delivery. Drafts all messages; Marcela approves before send. On proposal approval: triggers Legal (contract) and CFO. On hard rejection: triggers Vera (close project) and Controller/Legal (cost notification). On revision: routes to Bruno/Tomás/Legal based on `feedback_type`. |
| **Pablo** | Scheduler — builds project timeline and full milestone map in Asana at activation; updates schedule through all design and construction phases as phases close |
| **Vera** | Project tracker — monitors all active projects across all 20 phases, flags delays, updates Asana task statuses, issues weekly digest, manages activation gate (confirms contract + site docs + deposit before releasing Phase 11), triggers downstream agents at milestones and at project completion |

#### Post-Activation: Design through Construction

| Agent | Responsibility |
|---|---|
| **Andrés** | Concept design ops — manages concept design phase: coordinates architect brief and area program into concept deliverables checklist (3D model, renders, material direction, spatial intent), manages concept review gate, routes approval or revision |
| **Felipe** | Architectural design ops — manages detailed architectural design phase after concept approval: tracks design set production, manages architectural design review gate, confirms design is ready for engineering coordination |
| **Emilio** | Engineering coordination — manages structural and systems engineering phase: sends project to structural engineers, coordinates parallel systems (electrical, lighting, water, irrigation, solar, AV), tracks inputs from all engineering consultants, confirms engineering package is complete |
| **Hugo** | Executive plans — manages Fase Ejecutiva production after budget alignment: coordinates detailed plan book (cross sections, full plan set, technical coordination), manages final approval gate, confirms client sign-off before bidding |
| **Ofelia** | Tender & bidding — requests bids from multiple contractors, assembles comparison matrix, supports contractor selection decision, routes recommendation to Marcela for approval |
| **Paco** | Permitting — manages permit submission after contractor selection: assembles permit package, submits to relevant jurisdiction, tracks permit status, logs correction cycles, notifies Vera when permit is approved |

### Pod: Admin (8 agents)

| Agent | Responsibility |
|---|---|
| **Celia** | Decision capture — bridges all human decisions from WhatsApp and email into Asana. Consumes Approve/Reject/Pass-to-Agent responses from any review gate, produces normalized decision events, updates Asana task fields, moves tasks to next stage, assigns next agent, logs reviewer comment. Cross-pod infrastructure. |
| **Legal** | Shared across pods — reviews proposal clauses before client delivery, prepares contracts post-approval, handles IP and usage rights for marketing, flags compliance issues |
| **CFO** | Budget oversight — reviews and approves Bruno's payment schedule, monitors project financials, receives budget confirm task on campaign approvals |
| **Controller** | Invoicing — issues invoices automatically at each milestone per Bruno's payment schedule, manages accounts receivable, produces financial reports |
| **FP&A** | Forecasting — quarterly variance analysis and planning, reports to CFO |
| **Finance Ops** | Day-to-day transactions, payments, reconciliation, and deposit tracking (40% activation deposit confirmation to Vera) |
| **Tax** | Tax obligations, quarterly and year-end filings, compliance |
| **COO** | Operations oversight — resolves cross-team blockers escalated by Vera or Alma, monitors process health across all pods |

### Pod: Marketing (10 agents)

| Agent | Responsibility |
|---|---|
| **Arquitecto** | Campaign intake — receives project materials from architects, structures brief.json, opens Asana campaign project |
| **Lucía** | Audience intelligence — maps which segment a project speaks to, defines value language and emotional hook |
| **Marco** | Creative brief writer — translates Lucía's analysis into actionable direction for Materia pod |
| **Sofía** | Content strategist — campaign calendar, platform sequence, post types, publish dates |
| **Diego** | Bilingual copywriter — all captions, website text, YouTube descriptions. Spanish first, always |
| **Ileana** | Visual director — asset selection, sequencing, framing notes |
| **Valentina** | CMO orchestrator — brand review, assembles CEO approval package, routes rejections |
| **Canal** | Publisher — posts approved content to Cargo, Instagram, YouTube in sequence order |
| **Rafael** | Metrics analyst — tracks engagement quality, inquiry volume and scoring, platform performance |
| **Carmen** | Learning loop — produces two types of feedback: (1) per-campaign brief to Lucía after every publish cycle (engagement and tone quality signals); (2) quarterly strategic synthesis to Lucía and Valentina, incorporating Alma's performance data. Both operate independently. |

### Pod: Performance (1 agent)

| Agent | Responsibility |
|---|---|
| **Alma** | Cross-pod performance monitor — logs every task completion timestamp and rejection event across all 34 other agents, produces monthly performance digest per agent (on-time rate, rejection rate, avg completion time), flags active underperformance to COO in real time, escalates systemic issues to Marcela |

---

## 3. Asana Workspace Structure

**One workspace. Four project types.**

### Dynamic projects — one per client engagement

```
📁 [Project name] — Entrega
  Sections:
  ├── Lead & Screening
  ├── Marcela Review
  ├── Discovery & Questionnaire
  ├── First Meeting & Fit
  ├── Area Program
  ├── Site Documentation (parallel)
  ├── Cost Basis
  ├── Cost Basis Review (Marcela gate — Phase 7)
  ├── Scope & SOW
  ├── Proposal & Architect Review
  ├── Contract & Legal
  ├── Activation Gate (deposit + site docs + signature)
  ├── Conceptual Design
  ├── Architectural Design
  ├── Engineering (structural + systems)
  ├── Budget Alignment
  ├── Executive Plans
  ├── Final Approval
  ├── Bidding & Contractor Selection
  ├── Permitting
  ├── Construction
  └── Supervision (optional) & Completion
```

### Dynamic projects — one per marketing campaign

```
📁 [Campaign name] — Marketing
  Sections:
  ├── Resonancia (Lucía → Marco)
  ├── Materia (Sofía → Diego → Ileana)
  ├── CMO Review (Valentina)
  ├── CEO Gate
  └── Publishing (Canal → Rafael → Carmen)
```

### Permanent projects — one per admin function

```
📁 Leads          — all inbound from Lupe, permanent record
📁 Finanzas       — CFO · Controller · FP&A · Finance Ops
📁 Legal          — all legal review tasks across all pods
📁 Impuestos      — Tax obligations and filings
📁 Operaciones    — COO oversight and escalations
📁 Performance    — Alma's reports, active flags, resolved flags
```

### Permanent project — cross-team coordination

```
📁 Handoffs       — auto-created tasks at pipeline transition events
📁 Decisiones     — Celia's normalized decision log, one task per human decision
```

### Agent identity in Asana

One service account handles all API calls. Agents identify via:
- Task **tags** = agent name (Elena, Tomás, Bruno, etc.)
- Task **comments** signed with agent name: `— Rosa / Mensaje listo para revisión de Marcela`
- Human checkpoints assigned to real user accounts (Marcela, architects)

When human team members join, real Asana seats are added alongside agents cleanly — no architectural change required.

---

## 4. Data Model

### Project state model — 47 states

```text
lead_received
lead_screened
lead_summary_sent_to_marcela
followup_sent
awaiting_lead_response
lead_qualified
meeting_scheduled
discovery_completed
client_fit_approved
client_fit_rejected
area_program_in_progress
area_program_confirmed
site_data_pending
site_data_complete
cost_basis_ready
scope_in_preparation
scope_sent_for_architect_review
architect_review_no_response
architect_review_escalated
scope_under_revision
scope_signed
contract_pending
contract_signed
deposit_pending
project_activated
concept_in_progress
concept_ready_for_review
concept_approved
concept_rejected
architectural_design_in_progress
architectural_design_approved
structural_engineering_in_progress
systems_engineering_in_progress
budget_alignment_pending
budget_aligned
budget_misaligned
executive_plans_in_progress
executive_plans_approved
bidding_in_progress
contractor_selected
permit_submitted
permit_corrections
permit_approved
construction_started
supervision_active
project_on_hold
closed
```

### Custom fields per task type

**Entrega tasks:**
```
project_id, client_name, project_type, budget_range,
site_location, current_phase, project_state,
review_status, decision_status, assigned_agent,
human_reviewer, area_sqm, deposit_status,
budget_alignment_status, permit_status,
supervision_status, missing_documents,
client_fit_status, architect_assigned, due_date, revision_count,
feedback_type (budget | scope | copy | legal | other)
```

**Project type** (drives Tomás's SOW template):
```
standalone_residential | residential_in_development |
commercial_hotel | commercial_health_center | public_civic
```

**Marketing tasks:**
```
campaign_id, platform, post_sequence, publish_date,
copy_status, visual_status, ceo_decision
```

**Admin tasks:**
```
linked_project_id, amount, currency, due_date,
document_url, requires_signature, approved_by
```

**Lead tasks (Lupe):**
```
source_channel, category, received_at, summary,
status (new / reviewing / responded / qualified / discarded)
```

**Decision tasks (Celia):**
```
project_id, phase, review_item, reviewed_by,
decision (approve / reject / pass_to_agent),
comment, source_channel, timestamp,
next_action, route_to, sync_to_asana
```

**Performance tasks (Alma):**
```
agent_name, metric_type, value, period,
flag_severity (info / warning / critical)
```

---

## 5. Integration Architecture

### Asana API layer

A single Python module `asana_client.py` wraps all Asana API calls. No agent hits the API directly.

```python
# Core functions agents call:
asana.create_project(team, name, sections, custom_fields)
asana.create_task(project, section, name, fields, tag)
asana.complete_task(task_id, comment)
asana.move_task(task_id, new_section)
asana.create_dependency(task_id, depends_on_id)
asana.add_comment(task_id, agent_name, body)
asana.get_task(task_id)
asana.create_subtask(parent_id, name, fields)
asana.update_field(task_id, field_name, value)
```

### Webhook event loop

```
Agent completes work → writes to file system (if content)
       ↓
Calls asana.complete_task() → Asana marks task done
       ↓
Asana fires webhook → local Python listener receives event
       ↓
Listener reads task tag + section → determines next agent
       ↓
Listener calls asana.create_task() for next agent
       ↓
Next agent begins work
```

File system = source of truth for campaign content.
Asana = source of truth for task state and coordination.

### Decision capture flow (Celia)

```
Human receives WhatsApp/email review request
       ↓
Human replies: Approve / Reject / Pass to Agent [+ optional comment]
       ↓
Celia receives message → parses decision
       ↓
Celia creates normalized decision event (YAML schema below)
       ↓
Celia updates Asana: task field → decision value
                     task section → next stage
                     task assignee → next agent
                     comment → reviewer note logged
       ↓
Webhook listener fires → next agent task created
```

### YAML handoff schema

All major agent-to-agent handoffs use structured data:

```yaml
project_id: PRJ-2026-014
from_agent: AnaAgent
to_agent: TomasAgent
current_phase: cost_basis
status: ready_for_scope_generation
required_inputs:
  - area_program_spreadsheet
  - cost_basis_v1
outputs_created:
  - area_estimate_v2.xlsx
  - cost_basis_v1.md
decisions_needed:
  - confirm_project_type
  - confirm_collaborators
blockers: []
next_action: generate_scope
priority: medium
timestamp: 2026-03-15T13:00:00
```

### Decision payload schema

Every human decision creates a normalized event:

```yaml
# Approve example
project_id: PRJ-2026-014
phase: scope_of_work
review_item: scope_v3
reviewed_by: Marcela
decision: approve
comment: Ready to send for signature.
timestamp: 2026-03-15T11:42:00
source_channel: whatsapp
next_action: send_esign_packet
route_to: LegalAgent
sync_to_asana: true

# Reject example
project_id: PRJ-2026-014
phase: budget_alignment
review_item: contractor_cost_review_v2
reviewed_by: Marcela
decision: reject
comment: Cost too high. Simplify facade and reduce pool scope.
timestamp: 2026-03-15T14:10:00
source_channel: whatsapp
next_action: revise_design_for_budget
route_to: FelipeAgent
sync_to_asana: true

# Pass to Agent example
project_id: PRJ-2026-014
phase: lead_followup
review_item: inbound_lead_summary
reviewed_by: Marcela
decision: pass_to_agent
comment: Continue with questionnaire and schedule meeting if response is good.
timestamp: 2026-03-15T09:05:00
source_channel: whatsapp
next_action: execute_followup_workflow
route_to: ElenaAgent
sync_to_asana: true
```

### Architect notification model

Architects interact via Asana email notifications only — no Asana UI required in Phase 1. Two review gates send formatted emails:
1. **SOW Review gate** — Tomás's scope document, Approve / Flag reply
2. **Proposal Approval gate** — full proposal package, Approve / Reject reply

**Vera owns both architect gates.** Vera assembles the formatted email package and creates the architect-facing task. All architect communication is clear and infrequent.

### Human review message format

All WhatsApp/email review requests follow this structure:

```text
Project: Casa Robles
Phase: Scope Review
Summary: Area estimate approved. Scope includes architectural design, engineering coordination, executive plans, and optional supervision.
Choose action:
- Approve
- Reject
- Pass to Agent
Optional note: ...
```

---

## 6. Business Flow & Pipeline

### Full pipeline — 20 phases

```
CHANNELS (Instagram · Gmail · WhatsApp · website · YouTube · professional contacts)
       ↓
═══════════════════════════════════════════
 PHASE 1-2: LEAD INTAKE & SCREENING
═══════════════════════════════════════════
    Lupe — captures inbound, runs legitimacy screen, classifies, creates lead task
       ↓
═══════════════════════════════════════════
 PHASE 3: MARCELA REVIEW GATE*
═══════════════════════════════════════════
  Marcela* — reviews lead summary via WhatsApp
    → Approve: Elena sends questionnaire
    → Reject: lead archived
    → Pass to Agent: Elena handles outreach autonomously
       ↓
═══════════════════════════════════════════
 PHASE 4: DISCOVERY & FIRST MEETING
═══════════════════════════════════════════
    Elena — sends first questionnaire, captures response, schedules meeting,
            documents meeting notes, prepares fit assessment summary
  Marcela* — reviews fit summary via WhatsApp
    → Fit approved: proceed to area program
    → Not a fit: Rosa sends polite decline
       ↓
═══════════════════════════════════════════
 PHASE 5-6: AREA PROGRAM + SITE DOCS (parallel)
═══════════════════════════════════════════
    Ana    — area program matrix (room-by-room, sq m), preliminary cost basis
    Sol    — requests topo map + hydrology study, tracks site data readiness
  [Both tracks must complete before scope generation]
       ↓
═══════════════════════════════════════════
 PHASE 7: COST BASIS REVIEW*
═══════════════════════════════════════════
  Marcela* — reviews area program + preliminary cost via WhatsApp
    → Approve: Tomás begins SOW
    → Reject / revision: Ana revises
       ↓
═══════════════════════════════════════════
 PHASE 8: SCOPE OF WORK
═══════════════════════════════════════════
    Tomás — generates SOW from area program + cost basis + project type template
            (5 templates: standalone residential, residential in development,
             hotel, health center, civic/public)
  Architect SOW Review* — 24-48h email gate (Vera manages)
    → Scope approved: Bruno prices
    → Flagged: Tomás revises
    → No response at 24h: Vera sends reminder; no response at 48h: Vera escalates to Marcela
       ↓
    Bruno — detailed itemized budget + payment milestone schedule
    CFO   — approves payment schedule
       ↓
    Renata — bilingual proposal
    Legal  — contract clause review
    Vera   — assembles final proposal package, sends architect notification
  Architect Approval Gate* — full proposal package review (Vera manages; 24-48h window)
    → Approved: Rosa sends proposal to client
    → Rejected / flagged: Vera routes feedback to Renata (copy) or Tomás (scope) or Bruno (budget)
      Vera sends reminder at 24h with no response; escalates to Marcela at 48h with no response
       ↓
    Rosa — sends proposal to client
  [Client responds]
    → Approved: Legal drafts contract → Pablo begins timeline prep
    → Revision: Rosa routes to Bruno/Tomás/Legal → Renata reassembles
      (max 3 cycles → Marcela steps in)
    → Hard rejection: Rosa classifies terminal → Vera closes Asana project
      → Lead status "discarded" → Controller/Legal notified of any pre-contract costs
       ↓
═══════════════════════════════════════════
 PHASE 9-10: CONTRACT & ACTIVATION
═══════════════════════════════════════════
    Legal — final contract, e-sign packet
  [Activation gate — Vera holds until ALL THREE confirmed:]
    ✓ Contract/scope signed
    ✓ Site documents complete (topo + hydrology via Sol)
    ✓ 40% deposit received (Finance Ops confirms)
       ↓
    Pablo — builds full project timeline + Asana milestone tasks
    Vera  — begins active tracking, project state → project_activated
       ↓
═══════════════════════════════════════════
 PHASE 11: CONCEPTUAL DESIGN
═══════════════════════════════════════════
    Andrés — coordinates concept deliverables brief, tracks production
             (3D model, renders, material direction, spatial intent)
  Marcela* — reviews concept package via WhatsApp (typically in-person meeting)
    → Approve: Felipe begins architectural design
    → Reject/revision: Andrés routes back
       ↓
═══════════════════════════════════════════
 PHASE 12: ARCHITECTURAL DESIGN
═══════════════════════════════════════════
    Felipe — tracks architectural design set development, manages milestone
  Marcela* — reviews architectural design milestone
    → Approve: Emilio begins engineering coordination
    → Reject/revision: Felipe routes back
       ↓
═══════════════════════════════════════════
 PHASE 13: ENGINEERING (structural + systems, parallel)
═══════════════════════════════════════════
    Emilio — sends project to structural engineers, coordinates parallel:
             electrical · lighting · sound/AV · water · irrigation · solar
             Tracks all engineering inputs, confirms package complete
       ↓
═══════════════════════════════════════════
 PHASE 14: BUDGET ALIGNMENT
═══════════════════════════════════════════
    Bruno  — requests contractor pricing, aligns against client budget
  Marcela* — reviews budget alignment via WhatsApp
    → Aligned: Hugo begins executive plans
    → Not aligned: major design revision (back to Felipe or Emilio)
    [Rule: major changes happen here, not during or after executive plans]
       ↓
═══════════════════════════════════════════
 PHASE 15-16: EXECUTIVE PLANS + FINAL APPROVAL
═══════════════════════════════════════════
    Hugo   — coordinates Fase Ejecutiva: cross sections, full plan book,
             technical coordination, final integrated package
  Marcela* — reviews final plan set via WhatsApp
    → Final approval: Ofelia begins bidding
    → Reject/revision: Hugo routes back to Felipe (design correction) or Emilio (engineering issue)
      depending on nature of feedback captured in `feedback_type`
       ↓
═══════════════════════════════════════════
 PHASE 17: BIDDING / TENDER
═══════════════════════════════════════════
    Ofelia — requests bids, assembles contractor comparison
  Marcela* — selects contractor via WhatsApp
    → Contractor selected: Paco begins permitting
    → All bids rejected (cost / quality): Ofelia re-bids with revised scope note from Marcela
    → No viable bids: Vera escalates to Marcela + COO; project enters hold state
       ↓
═══════════════════════════════════════════
 PHASE 18: PERMITTING
═══════════════════════════════════════════
    Paco   — assembles permit package, submits, tracks status,
             manages corrections, notifies Vera when approved
       ↓
═══════════════════════════════════════════
 PHASE 19-20: CONSTRUCTION + SUPERVISION
═══════════════════════════════════════════
    Vera   — monitors construction phase against Pablo's schedule
  [If supervision selected:]
    Vera   — tracks site visit schedule, logs architect field reports,
             design compliance observations, flags deviations
       ↓
  PROJECT COMPLETION
    Vera       — closes project, triggers downstream
    Controller — final invoice per Bruno's payment schedule
    Tax        — project revenue filing
       ↓
  MARKETING TRIGGER (two types — both valid)
    (a) In-process: Marcela manually triggers when architects have materials
    (b) Completion: Vera auto-triggers when project closes
       ↓
  MARKETING PIPELINE
    Arquitecto → Lucía → Marco → Sofía → Diego → Ileana
       → Valentina → CEO Gate* → Canal → Rafael → Carmen
       → (Carmen feeds back to Lucía for next cycle)
       ↓
  QUARTERLY
    FP&A + Tax → CFO quarterly review
    Carmen → learning brief
    Alma  → performance digest → COO
```

---

## 7. Cross-Team Handoff Triggers

| Event | Triggered by | Creates task for |
|---|---|---|
| Inbound message received | Channels | Lupe |
| Lead classified (non-spam) | Lupe | Celia (notify Marcela via WhatsApp) |
| Press inquiry received | Lupe | Valentina |
| Marcela approves lead | Celia (decision capture) | Elena |
| Elena submits fit summary | Elena | Celia (notify Marcela for fit decision) |
| Fit approved | Celia | Ana + Sol (parallel) |
| Fit declined | Celia | Rosa (sends decline message) |
| Area program + cost basis ready | Ana | Celia (notify Marcela for review) |
| Marcela approves area program | Celia | Tomás |
| Site data complete | Sol | Vera (update site readiness status) |
| SOW ready | Tomás | Vera (assembles + sends architect SOW notification) |
| Scope approved by architect | Architect gate (via Vera) | Bruno |
| Budget + payment schedule ready | Bruno | Renata + CFO |
| Proposal ready | Renata | Legal |
| Legal review complete | Legal | Vera (assembles + sends architect approval notification) |
| Proposal approved by architect | Architect gate (via Vera) | Rosa (send to client) |
| Proposal flagged/rejected by architect | Architect gate (via Vera) | Renata / Tomás / Bruno (per feedback) |
| Final plans rejected/revised | Celia | Hugo (routes to Felipe or Emilio per feedback_type) |
| All bids rejected — re-bid | Ofelia | Ofelia (re-bids with revised scope note) |
| No viable bids — hold | Vera | COO + Marcela (escalation) |
| Client approves proposal | Rosa | Legal (contract) + CFO |
| Contract signed | Legal | Vera (activation gate monitor) |
| 40% deposit confirmed | Finance Ops | Vera (activation gate check) |
| All activation conditions met | Vera | Pablo (schedule) + Vera (activate tracking) |
| Concept package ready | Andrés | Celia (notify Marcela for concept review) |
| Concept approved | Celia | Felipe |
| Architectural design milestone ready | Felipe | Celia (notify Marcela) |
| Architectural design approved | Celia | Emilio |
| Engineering package complete | Emilio | Bruno (budget alignment) |
| Budget alignment review ready | Bruno | Celia (notify Marcela) |
| Budget aligned | Celia | Hugo |
| Budget misaligned (redesign) | Celia | Felipe or Emilio |
| Executive plans ready | Hugo | Celia (notify Marcela for final approval) |
| Final plans approved | Celia | Ofelia |
| Contractor selected | Ofelia (presents comparison) + Celia (captures Marcela's decision) | Paco |
| Permit approved | Paco | Vera (unlock construction phase) |
| Milestone reached | Vera | Controller (invoice) |
| Project complete | Vera | Controller (final invoice) + Tax + Arquitecto (marketing trigger) |
| Campaign CEO-approved | CEO gate | CFO (budget confirm) |
| Campaign published | Canal | Rafael |
| Quarter end (cron) | System | FP&A + Tax + Carmen |
| Agent underperforming | Alma | COO (flag) |
| Systemic issue unresolved | COO | Marcela (escalation) |
| Proposal revision requested | Rosa | Tomás / Bruno / Legal (per feedback type) |
| Proposal hard rejected (terminal) | Rosa | Vera (close project) + Controller/Legal (cost notification) |

---

## 8. Operational Rules

1. No project activates without: signed scope/contract + required site documents + 40% deposit
2. No executive plans begin until budget alignment is confirmed after engineering
3. Major budget-driven design changes happen before executive plans — never during or after
4. Every major phase produces a structured summary for human review
5. Every major phase supports Approve / Reject / Pass-to-Agent outcomes
6. Human decisions are captured through WhatsApp or email and synced into Asana by Celia
7. Agents operate from unified project state — not isolated conversations
8. Marcela is the qualification gate, the fit gate, and the key design milestone approver
9. The area program is the foundational pre-scope document — no SOW without it
10. Site readiness work runs in parallel with area program so activation is not delayed

---

## 9. Gap Resolutions

All gaps identified during design have proposed solutions included in the build.

| Gap | Resolution |
|---|---|
| No CRM / lead tracking | Lupe creates one Asana task per inbound in permanent Leads project. Every message has a record and status. |
| No client communication agent | Rosa added to Entrega pod — owns all outbound client contact, Marcela approves before send |
| Proposal revision loop undefined | Rosa classifies client feedback and routes to correct agent. Vera tracks revision count. Max 3 cycles before Marcela steps in. |
| Architect not in scope phase | SOW Review gate between Tomás and Bruno — 24-48h email gate, Vera manages |
| Payment milestones not defined | Bruno owns payment schedule template as part of budget deliverable. CFO approves. Controller uses for automatic invoicing. |
| Architect interface with Asana undefined | Email-only interaction in Phase 1 — formatted notifications with single-action replies. Vera manages volume. |
| Marketing trigger timing undefined | Two formal trigger types: in-process (Marcela manual) and completion (Vera automatic) |
| No qualified lead filter before Elena | Elena handles questionnaire + meeting + fit prep. Marcela gates before fit approval. Unfit leads never enter intake. |
| No area/cost basis before SOW | Ana added — builds area program matrix + preliminary cost basis before Tomás begins SOW |
| Site documentation not tracked | Sol added — parallel track that must complete before activation; Vera holds activation gate |
| Activation prerequisites not enforced | Vera holds activation until contract signed + site docs complete + 40% deposit confirmed by Finance Ops |
| No design phase coverage post-activation | Andrés (concept), Felipe (architectural), Emilio (engineering), Bruno (budget gate), Hugo (executive plans) added |
| No tender / bidding workflow | Ofelia added — manages bid requests, contractor comparison, selection support |
| No permitting tracking | Paco added — manages permit submission, corrections, approval tracking |
| No normalized decision capture | Celia added — all human decisions normalized as structured events and synced to Asana |
| No project type differentiation in SOW | Tomás now branches on 5 project type templates (standalone residential, residential in development, hotel, health center, civic) |

---

## 10. Alma — Performance Monitoring

Alma monitors all 34 other agents. She logs:
- Task completion timestamps vs. expected benchmarks
- Rejection and revision loop events
- Cross-pod delay patterns (e.g. engineering taking longer than plan = Pablo's schedule needs buffer)

**Reports:**
- **Real-time:** flags active underperformance to COO as it occurs
- **Monthly:** full performance digest per agent — on-time rate, rejection rate, average completion time
- **Quarterly:** cross-pod pattern analysis fed into COO and Carmen's learning brief

**Escalation path:** Alma → COO → Marcela (if unresolved)

### Alma → Carmen data contract

At quarter end, Alma writes `metrics/quarterly/<YYYY-QN>-alma-performance.json`:

```json
{
  "period": "2027-Q1",
  "generated_at": "",
  "agents": [
    {
      "name": "Diego",
      "on_time_rate": 0.92,
      "rejection_rate": 0.08,
      "avg_completion_hours": 4.2,
      "revision_loops": 2,
      "flag_severity": "info"
    }
  ],
  "cross_pod_patterns": [
    "Bruno budgets revised after Legal review 3/4 cycles — likely scope-to-budget handoff gap"
  ],
  "systemic_flags": []
}
```

Carmen reads this file as part of her quarterly learning brief synthesis alongside Rafael's marketing metrics.

---

## 11. Build Phasing

### Phase 1 — Foundation: Asana + Pre-Activation Entrega Pipeline

Deliver a working project delivery pipeline from lead to client-delivered proposal.

**Deliverables:**
- Asana workspace created, all teams and permanent projects scaffolded
- `asana_client.py` — full API wrapper
- Webhook listener server — event-driven task triggering
- Celia — decision capture agent (required for all human gates)
- Lupe, Elena, Ana, Sol, Tomás, Bruno, Renata, Rosa built and connected
- Legal agent built (shared, needed for proposal gate)
- Pablo + Vera built (Vera's activation gate logic included)
- Architect SOW Review gate and Architect Approval gate wired via Vera
- Alma built and logging from day one

**Success criteria:** A new client inquiry flows from Lupe through to an architect-approved proposal delivered to the client — fully visible in Asana without human intervention beyond Marcela's qualification/fit/review decisions (all via WhatsApp through Celia). Contract setup and activation are Phase 2 deliverables.

**Phase 1 blockers — must resolve before build:**
- [ ] Architect email addresses (Vera cannot wire SOW Review or Proposal Approval gates)
- [ ] Rosa's approval channel (email reply / WhatsApp / Asana task from Marcela)
- [ ] WhatsApp API access for Marcela's channel and Celia's decision parsing

---

### Phase 2 — Admin Pod + Activation + Contract

Build the financial layer and wire the activation gate.

**Deliverables:**
- CFO, Controller, FP&A, Finance Ops, Tax, COO agents built
- Contract flow (Legal → e-sign → Finance Ops deposit tracking → Vera activation) wired
- Vera's activation gate: all three conditions enforced before Pablo fires
- Bruno's payment schedule feeds Controller's invoicing automatically
- Milestone and completion triggers wired to Admin agents
- COO escalation path from Vera and Alma operational

**Success criteria:** When all activation conditions are met, Pablo auto-fires. When Vera closes a project, Controller invoices automatically. Quarter-end triggers FP&A and Tax.

---

### Phase 3 — Post-Activation Design Pipeline

Build the design-through-construction agent chain.

**Deliverables:**
- Andrés, Felipe, Emilio, Bruno (budget alignment mode), Hugo, Ofelia, Paco agents built
- Vera extended to cover construction tracking and optional supervision phase
- Pablo updated to manage timeline updates through all design phases
- All review gates wired through Celia — 9 Marcela gates (lead review, fit decision, area program / cost basis review, concept review, architectural design review, engineering / budget alignment review, executive plans review, contractor selection) + 2 architect email gates (SOW review, proposal approval) = 11 human review gates total
- Full 38-state project state model active in Asana
- All 5 project type templates active in Tomás

**Success criteria:** A project that has been activated flows through concept → architectural design → engineering → budget alignment → executive plans → bidding → permitting → construction without manual coordination, with Marcela reviewing and deciding at each milestone via WhatsApp.

---

### Phase 4 — Marketing Pipeline Connected

Wire the existing marketing system into Asana and complete the full loop.

**Deliverables:**
- All 10 Marketing agents get Asana task creation/completion calls added
- Campaign projects auto-created in Asana when Arquitecto fires
- CEO approval gate connected to Asana (alongside existing WhatsApp flow)
- Both marketing trigger types wired (in-process + completion via Vera)
- Cross-team handoffs: campaign approved → CFO, project closed → Arquitecto
- Carmen's quarterly brief connected to Alma's performance data
- Full Handoffs and Decisiones projects operational

**Success criteria:** A complete business cycle — client inquiry to published campaign to quarterly metrics — is fully visible and traceable in Asana across all four pods without manual coordination.

---

## 12. Open Items — Require Decision Before Build

**Phase 1 blockers:**
- [ ] **BLOCKER** Architect email addresses — Vera cannot wire SOW Review or Proposal Approval gates without at least one test address
- [ ] **BLOCKER** Rosa's approval channel — cannot be built until Marcela's outbound message approval method is defined (email reply / WhatsApp / Asana task)
- [ ] **BLOCKER** WhatsApp API access — Celia requires WhatsApp Business API or equivalent to parse Marcela's decision replies

**Pre-launch configuration:**
- [ ] Asana workspace name and team structure — confirm before scaffolding
- [ ] Instagram Graph API credentials — Lupe's DM monitoring + Canal's posting
- [ ] Payment milestone percentages — Bruno's default template (e.g. 30% signing / 30% design / 40% delivery)
- [ ] Spam classification criteria — Lupe's discard rules need explicit definition
- [ ] CEO WhatsApp number for marketing approval flow (already in `send-whatsapp.py`)
- [ ] Supervision service: confirm whether optional architectural supervision is in scope for initial build or deferred
- [ ] Lead follow-up questionnaire templates by project type (5 needed, one per template)
- [ ] SOW template framework by project type (5 needed, one per template)

---

## 13. Agent Count Summary

| Pod | Agents | Count |
|---|---|---|
| Entrega | Lupe · Elena · Ana · Sol · Tomás · Bruno · Renata · Rosa · Pablo · Vera · Andrés · Felipe · Emilio · Hugo · Ofelia · Paco | 16 |
| Admin | Celia · Legal · CFO · Controller · FP&A · Finance Ops · Tax · COO | 8 |
| Marketing | Arquitecto · Lucía · Marco · Sofía · Diego · Ileana · Valentina · Canal · Rafael · Carmen | 10 |
| Performance | Alma | 1 |
| **Total** | | **35** |

*(Expanded from 26 to 35 agents in revision 2026-03-15. Added: Ana (pre-scope analyst), Sol (site intelligence), Andrés (concept design ops), Felipe (architectural design ops), Emilio (engineering coordination), Hugo (executive plans), Ofelia (bidding), Paco (permitting), Celia (decision capture). Elena's scope expanded from intake-only to full discovery and fit lifecycle. Vera's scope expanded to include activation gate and construction phase tracking. Build phasing split into 4 phases to accommodate expanded delivery scope.)*
