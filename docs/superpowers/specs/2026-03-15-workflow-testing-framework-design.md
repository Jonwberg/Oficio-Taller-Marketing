# Oficio Taller — Workflow Testing Framework Design
**Date:** 2026-03-15
**Status:** Draft — pending user review
**Scope:** Post-build QA system for validating all 35 production agents across the full 20-phase project delivery pipeline. Tests that real agent outputs meet quality standards at every phase and that Celia routes all decisions correctly through the full 47-state project model.

**Source of truth for production system:** `docs/superpowers/specs/2026-03-14-oficio-taller-agent-system-design.md`

---

## 1. Purpose

This framework tests **built agent code and processes** to verify:
1. Each production agent produces correctly structured, high-quality outputs
2. Every Marcela decision gate correctly passes through Celia with the right routing, field updates, and 11-field decision payload
3. Both architect email gates (SOW Review, Proposal Approval) are correctly managed by Vera including 24h/48h escalation paths
4. All 47 Asana project states transition correctly and in the right sequence
5. Edge cases (budget mismatch, bad leads, site complications) are handled gracefully

This is not a design simulation. It runs against real agent code.

---

## 2. Architecture

### What the original 5-agent design becomes

The Process Mapper and Test Case Builder are **static files** — written once, updated when the operating model changes. They do not run on every test.

Three runtime agents do the actual work:

```
/test-segment B          /test-full-run TC-001
      ↓                          ↓
  Execution Agent    ←────────────────────────
      │  dispatches real production agents
      │  (Lupe, Elena, Ana, Sol, Tomás, Celia, etc.)
      │  with test seed data via Agent tool
      │  validates output schema
      │  captures each output to disk
      ↓
  Decision Gate Agent
      │  reads actual agent output
      │  scores content quality against per-deliverable rubric
      │  simulates Marcela's decision (or architect email reply for DG-04/DG-05)
      │  for Marcela gates: dispatches simulated decision to Celia,
      │    verifies routing, field updates, 11-field payload
      │  for architect gates: simulates email reply through Vera,
      │    verifies Vera routing and 24h/48h escalation paths
      │  writes scorecard JSON
      ↓
  Gap Analysis Agent
      │  runs after full test completes
      │  reads all scorecards from this run
      │  compares against previous run for same TC-ID
      │  identifies regressions and improvements
      ↓
  tests/results/2026-03-15-TC-001/
      ├── segment-A-scorecard.json
      ├── segment-B-scorecard.json
      ├── ... (one per segment)
      ├── run-summary.md
      └── gap-analysis.md
```

### Key architectural decisions

- **Claude-native only.** All agents dispatched via the Agent tool. No Python test harness.
- **Celia is a first-class test subject.** Every Marcela decision gate test has two parts: (1) evaluate deliverable quality, (2) send simulated decision to Celia and verify correct routing, Asana field updates, and complete 11-field decision payload.
- **Vera owns architect gates.** DG-04 (SOW Architect Review) and DG-05 (Proposal Architect Review) are routed through Vera's email flow, not Celia. The Decision Gate Agent tests Vera's email assembly, architect reply handling, and 24h/48h escalation paths separately.
- **Decision Gate Agent evaluates real content.** It reads actual outputs and scores them before deciding. It does not rubber-stamp based on persona signals alone.
- **File-based result logging.** Each test run writes to `tests/results/[DATE]-[TC-ID]/`. Results persist across sessions for comparison.
- **Scorecard `phase` field vocabulary:** Use segment letter (A–J) as the canonical value for the `phase` field in all scorecard JSON files. This ensures consistent run-to-run comparison by the Gap Analysis Agent.
- **Pass to Agent simulation:** On every full run, the Decision Gate Agent simulates a "Pass to Agent" decision at DG-07 (Concept Design) — this gate is designated as the fixed Pass to Agent test point. This is deterministic and regression-comparable across runs.
- **Option C extension path.** `/test-unit [agent-name]` and `/test-regression [TC-ID]` skills can be added later without restructuring. Unit test files slot into `tests/cases/units/` and a registry at `tests/registry.json`.

---

## 3. File Structure

```
tests/
├── cases/                              # Static — test case definitions
│   ├── TC-001-casa-moderna.md
│   ├── TC-002-casa-vista.md
│   ├── TC-003-wellness-retreat.md
│   ├── TC-004-centro-salud.md
│   ├── TC-005-biblioteca-municipal.md
│   ├── TC-006-edge-budget-mismatch.md
│   ├── TC-007-edge-bad-lead.md
│   └── TC-008-edge-site-complications.md
│
├── data/                               # Static — seed data per scenario
│   ├── TC-001-seed.json
│   ├── TC-002-seed.json
│   ├── TC-003-seed.json
│   ├── TC-004-seed.json
│   ├── TC-005-seed.json
│   ├── TC-006-seed.json
│   ├── TC-007-seed.json
│   └── TC-008-seed.json
│
├── rubrics/                            # Static — quality criteria per deliverable
│   ├── lead-record.md
│   ├── lead-summary.md
│   ├── discovery-questionnaire.md
│   ├── client-fit-assessment.md
│   ├── area-program.md
│   ├── cost-basis.md
│   ├── site-readiness-report.md
│   ├── scope-of-work.md
│   ├── legal-review.md
│   ├── proposal.md
│   ├── client-communication.md
│   ├── concept-review.md
│   ├── architectural-design.md
│   ├── engineering-package.md
│   ├── budget-alignment.md
│   ├── executive-plans.md
│   ├── bid-comparison.md
│   ├── controller-invoice.md
│   ├── tax-filing.md
│   └── celia-decision-routing.md
│
├── agents/                             # Runtime — 3 test agents
│   ├── execution-agent.md
│   ├── decision-gate-agent.md
│   └── gap-analysis-agent.md
│
├── skills/                             # Entry points
│   ├── test-segment.md                 # /test-segment [A-J] [TC-ID]
│   └── test-full-run.md                # /test-full-run [TC-ID]
│
└── results/                            # Generated — one folder per run
    └── [DATE]-[TC-ID]/
        ├── segment-A-lead-intake-scorecard.json
        ├── segment-B-discovery-scorecard.json
        ├── segment-C-area-program-scorecard.json
        ├── segment-D-scope-contract-scorecard.json
        ├── segment-E-activation-scorecard.json
        ├── segment-F-design-scorecard.json
        ├── segment-G-engineering-scorecard.json
        ├── segment-H-executive-plans-scorecard.json
        ├── segment-I-bidding-permitting-scorecard.json
        ├── segment-J-construction-scorecard.json
        ├── run-summary.md
        └── gap-analysis.md
```

---

## 4. Test Scenarios

| ID | Name | Type | Complexity | Budget Range |
|---|---|---|---|---|
| TC-001 | Casa Moderna | Standalone Residential | Standard | $300K–$500K USD |
| TC-002 | Casa Vista | Residential in Development | HOA Restricted | $400K–$700K USD |
| TC-003 | Wellness Retreat | Commercial — Hotel | High | $2M–$5M USD |
| TC-004 | Centro de Salud | Commercial — Health Center | Specialized | $1M–$3M USD |
| TC-005 | Biblioteca Municipal | Public / Institutional | Civic | $800K–$2M USD |
| TC-006 | Edge Case — Budget Mismatch | Residential | Redesign Required | $200K (constrained) |
| TC-007 | Edge Case — Bad Lead | N/A | Spam/Rejection | N/A |
| TC-008 | Edge Case — Site Complications | Commercial | Hydrology Issues | $1.5M–$4M USD |

---

## 5. Process Segments

| Segment | Phases | Production Agents Tested |
|---|---|---|
| A | 1–2 | Lupe |
| B | 3–4 | Lupe → Celia → Elena → Celia |
| C | 5–7 | Ana + Sol (parallel) → Vera (site status update) → Celia → Marcela gate (DG-03) |
| D | 8–9 | Tomás → Vera (architect SOW gate DG-04) → Bruno → Renata → Legal → Vera (architect approval gate DG-05) → Rosa |
| E | 10 | Vera (activation gate) → Pablo |
| F | 11–12 | Andrés → Celia → Felipe → Celia |
| G | 13–14 | Emilio → Bruno → Celia |
| H | 15–16 | Hugo → Celia |
| I | 17–18 | Ofelia → Celia → Paco |
| J | 19–20 | Vera (construction tracking + optional supervision + project close) → Controller (final invoice) → Tax (project revenue filing) |

**Note on Segment C site data:** Sol's site readiness output is validated as a Vera-managed status update — not a Marcela/Celia decision gate. The Execution Agent validates Sol's output schema and Vera's Asana field update (`site_data_pending` → `site_data_complete`). There is no Celia routing event for site data readiness.

---

## 6. Runtime Agents

### 6.1 Execution Agent

**Single responsibility:** Dispatch real production agents with test seed data, capture outputs, validate output schema, write to disk.

**Protocol per phase:**
1. Load test case and seed data for the TC-ID
2. Dispatch the production agent (e.g. Lupe) via Agent tool with seed data as input
3. Capture the output artifact (lead record, area program, SOW, etc.)
4. Validate schema: required fields present, correct format, no empty required sections
5. Write raw output to `tests/results/[run]/[segment]-raw-output/`
6. Flag schema failures immediately — do not continue to Decision Gate Agent if schema fails
7. Pass validated output to Decision Gate Agent

**The Execution Agent does not judge content quality.** It only checks structure and completeness. Quality evaluation is the Decision Gate Agent's job.

**Agent dispatching pattern:**
```
Dispatch: Lupe
Input: seed data from TC-001-seed.json (inbound Instagram message)
Capture: lead-record.json + lead-summary.md
Validate schema: source_channel, category, received_at, summary, status all present
Pass to: Decision Gate Agent
```

---

### 6.2 Decision Gate Agent

**Single responsibility:** Read actual agent output, score content quality, simulate a human decision, test Celia's routing (Marcela gates) or Vera's email routing (architect gates).

#### Marcela gates protocol (DG-01, DG-02, DG-03, DG-06 through DG-12)

1. Read the actual content of the deliverable
2. Load the matching rubric from `tests/rubrics/`
3. Score each quality dimension 1–5 with written justification per score
4. Calculate average score
5. If average ≥ 3.0 and no auto-fail triggered: simulate Approve
6. If average < 3.0 or auto-fail triggered: simulate Reject with specific revision notes
7. **At DG-07 (Concept Design) on every full run:** simulate Pass to Agent instead of Approve or Reject — this is the designated fixed test point for Pass to Agent routing. For Pass to Agent at DG-07: Celia retains `concept_in_progress` as the `project_state` (no state change) and only updates `assigned_agent` to the next handling agent. This is the expected state outcome to verify against.
8. Send simulated decision to Celia using the production decision payload schema (all 11 fields required)
9. Verify Celia:
   - Routes to the correct next agent
   - Updates the correct Asana fields: `decision_status`, `project_state`, `assigned_agent`
   - Logs reviewer comment verbatim
   - Payload contains all 11 required fields: `project_id`, `phase`, `review_item`, `reviewed_by`, `decision`, `comment`, `timestamp`, `source_channel`, `next_action`, `route_to`, `sync_to_asana`
   - **Note on field naming:** The production spec's YAML payload schema uses `route_to`. The production spec's Asana custom field list uses `routed_to` — this is a known inconsistency in the source document. Test against the YAML payload schema (11 fields with `route_to`). The production spec's Asana custom field list should be reconciled with the YAML schema before build.
10. Write scorecard JSON

#### Architect email gates protocol (DG-04 SOW Review, DG-05 Proposal Approval)

These gates are managed by Vera, not Celia. The Decision Gate Agent:

1. Evaluates Vera's email assembly: is the email package complete (correct deliverable attached, correct reply instructions, project context included)?
2. Simulates architect email reply using `architect_response` field from seed data (values: `approve` / `flag` / `no_response_24h` / `no_response_48h`)
3. Passes simulated reply to Vera and verifies:
   - `approve` → Vera routes to Bruno (DG-04) or Rosa (DG-05)
   - `flag` → Vera routes feedback to Tomás (DG-04) or to Renata/Tomás/Bruno per `feedback_type` (DG-05)
   - `no_response_24h` → Vera sends reminder
   - `no_response_48h` → Vera escalates to Marcela
4. Confirms Asana task updated and next agent assigned correctly
5. Writes scorecard — this gate does not test Celia routing

#### Scorecard JSON schema

```json
{
  "run_id": "2026-03-15-TC-001",
  "segment": "A",
  "phase": "A",
  "agent_tested": "Lupe",
  "deliverable": "lead-summary",
  "gate": "DG-01",
  "scores": {
    "completeness": 5,
    "accuracy": 4,
    "clarity": 5,
    "state_sync": 5,
    "timing": 4,
    "decision_readiness": 5
  },
  "average_score": 4.67,
  "auto_fail": false,
  "decision_simulated": "approve",
  "decision_commentary": "Lead summary complete, source identified, legitimacy assessment has clear reasoning. Marcela can decide immediately.",
  "celia_routing_correct": true,
  "celia_routing_notes": "Routed to Elena correctly. decision_status updated to approved. Comment preserved. All 11 payload fields present.",
  "passed": true
}
```

**Note:** The `phase` field uses the segment letter (A–J) as its canonical value. This is the controlled vocabulary for all scorecard files. Gap Analysis Agent uses this field to group and compare scorecards across runs.

**This agent must fail tests.** A Decision Gate Agent that always approves is not testing anything.

---

### 6.3 Gap Analysis Agent

**Single responsibility:** After a full test run, synthesize all scorecards and produce actionable findings.

**Protocol:**
1. Read all scorecard JSONs from the current run
2. If a prior run exists for the same TC-ID, load it for comparison
3. Group by `phase` field (segment letter) for consistent comparison
4. Identify phases with average score below 3.0
5. Identify which quality dimensions failed most often across all phases
6. Identify which production agents produced the weakest outputs
7. Identify any Celia routing failures
8. Identify any auto-fail triggers
9. Identify any Vera email gate failures (incorrect routing, missed escalation)
10. If prior run exists: flag regressions (scores that dropped) and improvements (scores that rose)
11. Write `run-summary.md` — scores at a glance, pass/fail per segment
12. Write `gap-analysis.md` — detailed findings, prioritized by severity, with specific improvement recommendations

**gap-analysis.md format per finding:**
```
### GAP-[ID]: [Short Title]
Segment: [letter] | Phase: [number] | Agent: [name]
Severity: [Low | Medium | High | Critical]
Score: [average]/5.0

Description: [what the output got wrong]
Evidence: [specific content from the output that demonstrates the issue]
Recommended fix: [specific change to agent prompt or process]
Priority: [1 = fix before next run | 2 = fix before production | 3 = nice to have]
```

---

## 7. Entry Point Skills

### `/test-segment [A-J] [TC-ID]`

Runs a single segment against one test case.

**Use when:** You've updated a specific agent's prompt and want to verify that segment without a full run.

**Example:** `/test-segment D TC-001` — runs Segment D (Scope & Contract) for Casa Moderna.

**Sequence:**
1. Load TC-001 seed data
2. Dispatch Execution Agent for Segment D phases only
3. Run Decision Gate Agent on each output in that segment
4. Write scorecards to `tests/results/[DATE]-TC-001-segment-D/`
5. Print focused summary — scores for that segment only, no gap analysis

---

### `/test-full-run [TC-ID]`

Runs all 10 segments end-to-end for one test case.

**Use when:** Significant changes have been made, or before marking a build phase complete.

**Example:** `/test-full-run TC-006` — runs the budget mismatch edge case all the way through.

**Sequence:**
1. Load full scenario seed data
2. Run segments A–J sequentially (each depends on previous state)
3. Decision Gate Agent evaluates every output, tests Celia routing at Marcela gates, and tests Vera routing at architect email gates
4. After all segments complete, dispatch Gap Analysis Agent
5. Write full results to `tests/results/[DATE]-[TC-ID]/`
6. Print pass/fail summary with scores per segment

---

## 8. Quality Rubrics

Each rubric has three layers:
1. **Schema** — required fields checked by Execution Agent (pass/fail)
2. **Quality dimensions** — scored 1–5 by Decision Gate Agent with written justification
3. **Auto-fail conditions** — immediately fail the test regardless of other scores

---

### 8.1 Lead Record (`lead-record.md`) — Lupe → Asana

**Quality dimensions:**
- Asana lead task created with all required custom fields populated: `source_channel`, `category`, `received_at`, `summary`, `status`
- `source_channel` correctly identifies platform (instagram / gmail / whatsapp / website / youtube / professional_contact)
- `category` correctly classifies inbound (project_inquiry / speaking_invite / collaboration / press / spam)
- Raw message stored verbatim in task body
- `status` set to "new" on creation

**Auto-fail:** No Asana task created, `received_at` missing, `status` absent.

---

### 8.2 Lead Summary (`lead-summary.md`) — Lupe → Marcela

**Quality dimensions:**
- Source and channel correctly identified
- Project type classified (residential / commercial / institutional / unknown)
- Raw message preserved verbatim
- Legitimacy assessment explained with reasoning — not just a label
- Summary is actionable: Marcela can decide without asking for more information

**Auto-fail:** Summary is empty, source is missing, or classification is "unknown" without explanation.

---

### 8.3 Discovery Questionnaire (`discovery-questionnaire.md`) — Elena → Lead

**Quality dimensions:**
- Sent within 24h of lead qualification
- Questionnaire is project-type appropriate (residential questions for residential leads, etc.)
- Covers all required topics: project type, approximate size, site location, budget range, desired timeline, special requirements, design style preferences, site ownership status
- Language matches client's communication language (Spanish or English based on inbound message)
- Tone is professional and inviting — not a form, not bureaucratic

**Auto-fail:** Questionnaire sent to wrong contact, project type not addressed, budget question absent.

---

### 8.4 Client Fit Assessment (`client-fit-assessment.md`) — Elena → Marcela

**Quality dimensions:**
- Covers all four assessment dimensions: design engagement level, budget realism relative to program, scope clarity, and collaborative working style indicators from meeting
- Meeting notes included and attributed (what the client said, not just Elena's interpretation)
- Recommendation is explicit: proceed / decline / request more information — no ambiguity
- Rationale for recommendation is specific ("client expressed preference for lowest cost option, not design quality") not generic ("client seems unfit")
- Any red flags documented with supporting evidence from meeting

**Auto-fail:** No explicit recommendation, assessment missing any of the four required dimensions.

---

### 8.5 Area Program (`area-program.md`) — Ana

**Quality dimensions:**
- Every room/space has: name, quantity, and size in sqm
- Total programmed sqm calculated and stated explicitly
- Special features captured (pool, rooftop, solar, irrigation, etc.) with size if they are programmed spaces
- Assumptions documented where client input was incomplete
- Matrix is readable as a standalone document — no conversation context required

**Auto-fail:** Total sqm missing, any programmed space has no size, no assumptions section.

---

### 8.6 Cost Basis (`cost-basis.md`) — Ana

**Quality dimensions:**
- Cost-per-sqm basis stated with source (local market rate, contractor benchmark, etc.)
- Base construction cost calculated from area program
- Architecture fee percentage and amount stated
- Engineering allowance included
- Contingency percentage applied
- All assumptions listed explicitly
- Total estimate clearly labeled as preliminary

**Auto-fail:** No assumptions section, total missing, architecture fee absent.

---

### 8.7 Site Readiness Report (`site-readiness-report.md`) — Sol → Vera

**Quality dimensions:**
- Required documents identified based on site conditions: topographic map always required; hydrologic assessment required if site has streams, wetlands, or slope risk
- Document request issued to client with clear instructions and deadline
- Asana site readiness status updated correctly: `site_data_pending` on request sent, `site_data_complete` when all documents received
- Blockers logged in Asana if client has not provided documents within expected window
- Summary identifies what was received, what is pending, and whether activation gate is blocked

**Auto-fail:** Topo map not included in requirements, no status update to Asana, blocker not logged when documents overdue.

---

### 8.8 Scope of Work (`scope-of-work.md`) — Tomás

The most critical pre-activation deliverable. All 20 required items must be present:

```
1.  Conceptual design phase defined with deliverables
2.  Architectural design phases defined with deliverables
3.  Executive architectural plans included with deliverables
4.  Optional architectural supervision clause included
5.  Landscape architecture scope stated (or explicitly excluded)
6.  Structural engineering collaboration defined
7.  Electrical engineering scope included
8.  Lighting design scope stated
9.  Water systems scope defined
10. Irrigation scope included (or explicitly excluded)
11. Solar systems scope included (or explicitly excluded)
12. Local contractor cost validation planned
13. Payment schedule with milestone names, percentages, and trigger events
14. Deliverables listed by phase with specifics — not just phase labels
15. Responsibilities matrix assigning every major deliverable to a named party
16. Exclusions documented with specifics (not generic)
17. Revision assumptions stated (how many rounds per phase)
18. Timeline structure clear with phase sequence
19. Project-type-specific clauses included (see below)
20. E-signature path defined
```

**Project-type-specific clause requirements:**
- `standalone_residential`: standard residential clauses
- `residential_in_development`: HOA coordination clause, covenant review clause
- `commercial_hotel`: hospitality compliance clause, brand standards coordination
- `commercial_health_center`: health authority compliance clause, medical equipment coordination
- `public_civic`: civic procurement clause, public bidding compliance

**Quality dimensions:**
- All 20 items present and complete
- Payment schedule has milestone names, percentages, and trigger events
- Exclusions are specific — not generic
- Correct project-type-specific clauses applied
- Responsibilities matrix names real parties (not "client" and "architect" generically)
- Revision assumptions explicit per phase

**Auto-fail:** Payment schedule missing, exclusions section absent, project type template not applied, any of the 20 items missing entirely.

---

### 8.9 Legal Review (`legal-review.md`) — Legal → Vera

**Quality dimensions:**
- All proposal clauses reviewed — confirmation that Legal read the full document
- IP and usage rights section addressed specifically
- Compliance issues flagged with proposed resolution path (not just flagged and left open)
- Project-type-specific compliance considerations verified (health center regulations, civic procurement rules, HOA restrictions)
- Review output is either a clean approval or a specific flag list — no ambiguous "looks okay" responses

**Auto-fail:** IP section not reviewed, approval given with open unresolved flags, no evidence that the full proposal was reviewed.

---

### 8.10 Proposal (`proposal.md`) — Renata

**Quality dimensions:**
- SOW section accurately reflects Tomás's approved scope — no modifications or omissions
- Budget section matches Bruno's itemized estimate exactly
- Timeline phases are consistent with the SOW deliverables structure and project type
- Oficio Taller process narrative present and in brand voice
- Bilingual: Spanish primary, English secondary, both complete
- Document is client-ready: no internal notes, no placeholders, no agent commentary

**Auto-fail:** Language missing (Spanish or English), placeholder text present, budget doesn't match Bruno's figures.

---

### 8.11 Client Communication (`client-communication.md`) — Rosa

**Quality dimensions:**
- Correct channel used (WhatsApp or email per project communication preference)
- Tone matches Oficio Taller brand voice — professional, warm, design-engaged
- Action requested is clear and singular — one clear next step for the client
- Project name and relevant context included
- Message is in draft status awaiting Marcela approval before send
- No confidential internal information included

**Auto-fail:** Message sent without Marcela approval, missing project reference, action unclear.

---

### 8.12 Concept Design Review (`concept-review.md`) — Andrés

**Quality dimensions:**
- Deliverables checklist confirmed complete: 3D model, renders, material direction, color direction, space arrangement
- In-person presentation logged as milestone with date
- Review summary captures Marcela's specific feedback — not just "approved" or "rejected"
- Revision notes (if any) are specific and actionable for the design team — not vague
- Concept package addresses all program requirements from the area program

**Auto-fail:** Any deliverable in the concept checklist unconfirmed, presentation milestone not logged.

---

### 8.13 Architectural Design (`architectural-design.md`) — Felipe

**Quality dimensions:**
- Design set reflects the approved concept — no unexplained departures
- All rooms and spaces from the area program are present in the design
- Structural coordination notes included, flagging any design elements that need structural input
- Material and finish specifications consistent with concept approval
- Design is complete enough to hand off to Emilio for engineering coordination — no open design questions

**Auto-fail:** Rooms from area program missing in design, concept not reflected, no structural coordination notes.

---

### 8.14 Engineering Package (`engineering-package.md`) — Emilio

**Quality dimensions:**
- All required systems present and confirmed: structural, electrical, lighting, water
- Conditional systems addressed: irrigation (if landscaping in scope), solar (if in scope), AV/sound (if in scope)
- All engineering consultant inputs confirmed received — no pending items
- Engineering package explicitly stated as complete and ready for budget alignment
- Any design conflicts identified during engineering coordination documented with proposed resolutions

**Auto-fail:** Any required system absent, pending consultant inputs not resolved before package declared complete.

---

### 8.15 Budget Alignment Analysis (`budget-alignment.md`) — Bruno

**Quality dimensions:**
- Contractor pricing collected from at least one source with source documented
- Comparison between contractor pricing and client budget clearly presented with variance calculated
- Variance labeled as percentage and dollar amount (over/under)
- Recommendation is explicit: proceed or redesign — no ambiguity
- If redesign recommended: specific scope elements identified for reduction with estimated savings per element

**Auto-fail:** No contractor pricing source, no explicit recommendation.

---

### 8.16 Executive Plans (`executive-plans.md`) — Hugo

**Quality dimensions:**
- Plan set includes all required components: cross sections, full plan book, technical coordination layer
- All engineering inputs from Emilio's package are integrated — no missing system drawings
- No unresolved coordination conflicts between architectural and engineering drawings
- Package is self-contained for client review — no references to documents not included
- Final client sign-off confirmation logged as milestone

**Auto-fail:** Missing cross sections, unresolved engineering conflicts, plan set missing any system.

---

### 8.17 Bid Comparison (`bid-comparison.md`) — Ofelia

**Quality dimensions:**
- At least two bids compared (if available — see exception below)
- Comparison matrix includes: contractor name, total bid, key line items, proposed timeline, and notes
- Recommendation includes reasoning beyond lowest price (track record, timeline, scope understanding)
- Recommendation is explicit — one contractor identified with rationale
- If only one bid received: flagged explicitly and routed as Marcela decision with documented context

**Auto-fail:** Single bid treated as final selection without Marcela decision gate, no comparison matrix.

---

### 8.18 Controller Invoice (`controller-invoice.md`) — Controller

**Quality dimensions:**
- Invoice issued at the correct milestone trigger event — not before the milestone is confirmed by Vera
- Invoice amount exactly matches the amount in Bruno's payment schedule for that milestone
- Invoice contains all required fields: project name, client name, milestone description, amount, due date, payment instructions, currency
- Issued promptly after trigger — no unreasonable delay between milestone confirmation and invoice creation
- Running total of invoiced vs. total contract value calculated and included

**Auto-fail:** Invoice amount differs from Bruno's payment schedule, issued before milestone trigger confirmed, payment instructions absent.

---

### 8.19 Tax Filing (`tax-filing.md`) — Tax

**Quality dimensions:**
- Revenue amount matches the cumulative total of Controller's invoiced amounts for the project
- Correct tax jurisdiction applied (Mexico — IVA 16% standard unless project-specific exception applies)
- Filing period correct — quarterly or annual per filing schedule, not early or late
- All required filing documents complete: RFC, CFDI reference, project revenue declaration
- Any deductible project expenses documented with amounts

**Auto-fail:** Revenue amount does not match Controller's invoiced total, jurisdiction missing, RFC absent.

---

### 8.20 Celia Decision Routing (`celia-decision-routing.md`) — all Marcela gates

**Quality dimensions:**
- Decision parsed correctly: Approve / Reject / Pass to Agent
- Correct next agent assigned in Asana
- Correct Asana fields updated: `decision_status`, `project_state`, `assigned_agent`
- Reviewer comment preserved verbatim in decision log
- Decision payload contains all 11 required fields: `project_id`, `phase`, `review_item`, `reviewed_by`, `decision`, `comment`, `timestamp`, `source_channel`, `next_action`, `route_to`, `sync_to_asana`
- Timestamp in ISO-8601 format
- For Pass to Agent at DG-07: `project_state` remains `concept_in_progress`, only `assigned_agent` is updated

**Auto-fail:** Wrong next agent assigned, decision type misclassified, Asana not updated, reviewer comment dropped, any of the 11 required payload fields missing.

**Note on payload field naming:** Test against the YAML payload schema which uses `route_to`. The production spec's Asana custom field list uses `routed_to` — this is a known inconsistency in the source document that must be reconciled before build.

---

## 9. Decision Gates

12 decision gates — using real agent names, correct phase mappings, and split by routing path (Celia vs. Vera).

| Gate | Phase | Deliverable | Reviewer | Routing | Agents Tested |
|---|---|---|---|---|---|
| DG-01 | Phase 2→3 | Lead Summary | Marcela | Celia | Lupe + Celia |
| DG-02 | Phase 4→5 | Client Fit Assessment | Marcela | Celia | Elena + Celia |
| DG-03 | Phase 7 | Area Program + Cost Basis | Marcela | Celia | Ana + Celia |
| DG-04 | Phase 8 | SOW Architect Review | Architect (email) | Vera | Tomás + Vera |
| DG-05 | Phase 8→9 | Proposal Architect Approval | Architect (email) | Vera | Renata + Legal + Vera |
| DG-06 | Phase 9→10 | Activation Prerequisites | Marcela | Celia | Vera + Finance Ops + Legal + Celia |
| DG-07 | Phase 11→12 | Concept Design | Marcela | Celia | Andrés + Celia *(Pass to Agent test point)* |
| DG-08 | Phase 12→13 | Architectural Design | Marcela | Celia | Felipe + Celia |
| DG-09 | Phase 13→14 | Engineering + Budget Alignment | Marcela | Celia | Emilio + Bruno + Celia |
| DG-10 | Phase 15→16 | Executive Plans | Marcela | Celia | Hugo + Celia |
| DG-11 | Phase 17 | Contractor Selection | Marcela | Celia | Ofelia + Celia |
| DG-12 | Phase 18 | Permit Status | Marcela | Celia | Paco + Vera + Celia |

**DG-07 Pass to Agent:** On every full test run, the Decision Gate Agent simulates a "Pass to Agent" decision at DG-07. This tests Celia's routing of this third outcome type. After Pass to Agent is simulated, the test continues by treating the result as an Approve for downstream segment continuity.

---

## 10. Full State Inventory (47 states)

The test framework validates against all 47 production states. Note: the production system's Section 4 header says "38 states" — this is a known error in that document. The canonical count is 47, confirmed by counting the enumerated list in both documents.

```
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

---

## 11. Seed Data Format

All seed data files follow the production naming conventions. The `architect_response` field supports architect email gate simulation.

```json
{
  "test_case_id": "TC-001",
  "scenario": "Casa Moderna",
  "project_type": "standalone_residential",
  "inbound_channel": "instagram",
  "inbound_message": "Hola, estoy buscando un arquitecto para diseñar mi casa en Los Cabos. Tengo un terreno de 2,500m² y quisiera algo moderno con piscina y terraza.",
  "lead_name": "Carlos Mendoza",
  "location": "Los Cabos, Baja California Sur",
  "site_area_sqm": 2500,
  "total_programmed_sqm": 250,
  "program": {
    "bedrooms": { "qty": 3, "avg_size_sqm": 18 },
    "bathrooms": { "qty": 3, "avg_size_sqm": 8 },
    "kitchen": { "qty": 1, "size_sqm": 20 },
    "dining_living": { "qty": 1, "size_sqm": 45 },
    "office": { "qty": 1, "size_sqm": 12 },
    "pool": { "qty": 1, "size_sqm": 35 },
    "patio": { "qty": 1, "size_sqm": 40 },
    "rooftop_terrace": { "qty": 1, "size_sqm": 5 },
    "service_areas": { "qty": 1, "size_sqm": 15 }
  },
  "special_features": ["pool", "rooftop_terrace", "solar"],
  "budget_range_usd": { "min": 300000, "max": 500000 },
  "site_conditions": "flat, no hydrology concerns",
  "client_profile": "design_engaged",
  "expected_outcome": "full_activation",
  "architect_response": "approve",
  "payment_schedule": [
    { "milestone": "contract_signed", "percentage": 40, "amount_usd": 21600 },
    { "milestone": "concept_approved", "percentage": 30, "amount_usd": 16200 },
    { "milestone": "executive_plans_approved", "percentage": 30, "amount_usd": 16200 }
  ],
  "total_architecture_fee_usd": 54000,
  "tax_jurisdiction": "Mexico",
  "currency": "USD",
  "rfc": "TEST-RFC-001"
}
```

**`architect_response` values for architect email gate simulation:**
- `"approve"` — architect approves, Vera routes to next agent
- `"flag"` — architect flags issues, Vera routes feedback for revision
- `"no_response_24h"` — tests Vera's 24h reminder
- `"no_response_48h"` — tests Vera's 48h escalation to Marcela

---

## 12. Corrections from Original Framework

| Issue | Correction Applied |
|---|---|
| References non-existent `architectural_agent_operating_manual.md` | Updated to reference `docs/superpowers/specs/2026-03-14-oficio-taller-agent-system-design.md` |
| State model claimed 46 states | Corrected to 47 states — canonical count from enumerated list in both documents |
| Celia absent from all decision gates | Celia tested at all 10 Marcela gates (DG-01 through DG-12 excluding DG-04/DG-05) |
| Celia rubric said "8 required fields" | Corrected to 11 required fields with full enumeration |
| DG-02 "Follow-up Response" is not a production decision gate | Removed — no Celia event exists for this step. Gates renumbered from 14 to 12. |
| DG-05 "Site Data Readiness" is not a Marcela/Celia gate | Removed from decision gates — Sol's output validated as Vera status update only |
| Old Cost Basis gate was at "Phase 5→6" | Corrected to Phase 7 per production system's named Phase 7 Cost Basis Review gate — now DG-03 |
| Architect email gates had no gate numbers | Numbered as DG-04 (SOW Review, Phase 8) and DG-05 (Proposal Approval, Phase 8→9) |
| Architect gates had no separate protocol | Added architect email gate protocol to Section 6.2 covering Vera routing, flag handling, and 24h/48h escalation |
| Proposal rubric required "Pablo's milestone structure" | Removed — Pablo acts in Phase 10, after the proposal in Phase 8. Replaced with SOW-consistent timeline criterion. |
| Generic agent names throughout | All real names: Lupe, Elena, Ana, Sol, Tomás, Bruno, Renata, Rosa, Vera, Celia, Andrés, Felipe, Emilio, Hugo, Ofelia, Paco |
| SOW rubric referenced "20 checklist items" with no definition | All 20 items now defined inline in Section 8.8 |
| Missing rubrics for 9 deliverables | Rubrics added for: lead-record, discovery-questionnaire, client-fit-assessment, site-readiness-report, legal-review, client-communication, architectural-design, engineering-package, executive-plans |
| No rubric for Felipe or Emilio | `architectural-design.md` and `engineering-package.md` added to rubrics directory and Section 8 |
| Pass to Agent had no enforcement mechanism | Assigned as fixed test point at DG-07 on every full run — deterministic and regression-comparable |
| `phase` scorecard field had no defined vocabulary | Canonical value defined as segment letter (A–J) |
| Controller and Tax in Segment J with no rubrics or seed data | Rubrics added (Sections 8.18, 8.19); financial fields added to seed data format; Segment J updated to include both agents |
| TC-001 seed data program items summed to 245 sqm, not 250 | Added `rooftop_terrace: 5 sqm` to program block — sum now equals 250 sqm |
| Project type naming inconsistency | Standardized to production naming: `standalone_residential`, `residential_in_development`, `commercial_hotel`, `commercial_health_center`, `public_civic` |

---

## 13. Option C Extension Path

When ready to add unit tests and regression tracking:

**Additional files (slot in without restructuring):**
```
tests/
├── cases/units/                    # One file per production agent
│   ├── lupe-unit-tests.md
│   ├── elena-unit-tests.md
│   └── ... (35 total, added one at a time as agents are built)
├── registry.json                   # All test cases with expected pass/fail state
└── skills/
    ├── test-unit.md                # /test-unit [agent-name]
    └── test-regression.md          # /test-regression [TC-ID]
```

**`registry.json` structure:**
```json
{
  "version": "1.0",
  "test_cases": [
    {
      "id": "TC-001",
      "name": "Casa Moderna",
      "type": "integration",
      "segments": ["A","B","C","D","E","F","G","H","I","J"],
      "last_run": "2026-03-15",
      "last_result": "pass",
      "baseline_scores": {}
    }
  ]
}
```

Add unit tests one agent at a time as each production agent is completed.

---

*This document supersedes the testing framework spec submitted for review on 2026-03-15. All phase numbers, state names, agent names, and decision payloads reference `docs/superpowers/specs/2026-03-14-oficio-taller-agent-system-design.md`. The production system's Section 4 header ("38 states") is a known error in that document — the correct count is 47.*
