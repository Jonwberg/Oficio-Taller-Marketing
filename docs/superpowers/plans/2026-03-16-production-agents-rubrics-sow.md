# Production Agents — Rubrics & SOW Templates Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create the 4 missing rubrics (`budget.md`, `project-schedule.md`, `permit-status.md`, `vera-site-status.md`) and 5 SOW templates that the test framework and Tomás need before any agent can be built or tested.

**Architecture:** Pure content files — no code, no TDD. Each rubric follows the established format in `tests/rubrics/`. Each SOW template follows the 20-item checklist from `tests/rubrics/scope-of-work.md`. Validation steps use `grep` to confirm required sections are present.

**Tech Stack:** Markdown only.

---

## File Structure

```
tests/rubrics/
  budget.md                           ← New: Bruno Segment D rubric
  project-schedule.md                 ← New: Pablo rubric
  permit-status.md                    ← New: Paco rubric
  vera-site-status.md                 ← New: Vera Segment C rubric (Asana-only)

docs/templates/sow/
  sow-standalone-residential.md       ← New: base residential template
  sow-residential-in-development.md   ← New: HOA/covenant variant
  sow-commercial-hotel.md             ← New: hospitality variant
  sow-commercial-health-center.md     ← New: medical variant
  sow-public-civic.md                 ← New: public/government variant
```

---

## Chunk 1: Missing Rubrics

### Task 1: budget.md — Bruno's Segment D deliverable rubric

**Files:**
- Create: `tests/rubrics/budget.md`

- [ ] **Step 1: Create the rubric file**

```markdown
# Rubric: Budget
**Agent:** Bruno
**Deliverable:** Itemized project budget with payment schedule (Segment D, feeds directly into Renata's proposal — no separate gate)

## Schema (Execution Agent validates — pass/fail)
Required fields: project_name, client_name, milestone_name, amount, payment_instructions, currency, line_items

Note: `line_items` must be an array. `milestone_name` labels the first payment milestone; all milestones are covered across `line_items` entries.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; line_items array covers every SOW phase; all 5 payment milestones present with name, percentage, trigger event, and MXN amount
3: All required fields present but one payment milestone missing trigger event or one phase missing from line_items
1: Any required field missing, or fewer than 3 payment milestones, or line_items absent

**Accuracy (1–5)**
5: Total of all milestone amounts equals total_estimate from cost-basis.json within 2% (contingency adjustment acceptable); each line_item amount is correctly calculated
3: Total within 5% of cost_basis total_estimate; minor rounding differences in line items
1: Total differs from cost_basis total_estimate by more than 5% without documented justification

**Clarity (1–5)**
5: Client can understand what they are paying for at each milestone; payment_instructions are specific (bank name, CLABE/SWIFT, reference format); currency is explicit (MXN or USD)
3: Milestones labeled but payment_instructions missing one detail; client would need one follow-up question
1: Payment_instructions absent or generic; client cannot pay without additional information

**State Sync (1–5)**
5: Asana task updated to budget_complete; linked to scope-of-work task; budget passed to Renata without delay
3: State updated but not linked to scope-of-work task
1: No Asana update

**Timing (1–5)**
5: Budget produced after Vera confirms architect SOW approval (DG-04); not before; passed to Renata immediately
3: Minor delay after DG-04 but budget exists before Renata begins proposal
1: Budget produced before DG-04 confirmation or not produced before Renata fires

**Decision Readiness**
N/A — No Marcela gate on Bruno's Segment D budget (proceeds directly to Renata per scope boundary). Average score calculated over 5 dimensions.

## Auto-Fail Conditions
- line_items absent or empty array
- payment_instructions absent
- Total budget not reconciled with cost_basis total_estimate (difference > 5% with no documented justification)
- Budget produced before architect SOW approval (DG-04) confirmed
```

- [ ] **Step 2: Validate required sections present**

```bash
grep -q "Required fields:" tests/rubrics/budget.md && echo "PASS: schema section" || echo "FAIL: schema section"
grep -q "Auto-Fail" tests/rubrics/budget.md && echo "PASS: auto-fail section" || echo "FAIL: auto-fail section"
grep -q "line_items" tests/rubrics/budget.md && echo "PASS: line_items present" || echo "FAIL: line_items present"
grep -q "payment_instructions" tests/rubrics/budget.md && echo "PASS: payment_instructions present" || echo "FAIL"
```

Expected: all 4 PASS

---

### Task 2: project-schedule.md — Pablo's deliverable rubric

**Files:**
- Create: `tests/rubrics/project-schedule.md`

- [ ] **Step 1: Create the rubric file**

```markdown
# Rubric: Project Schedule
**Agent:** Pablo
**Deliverable:** Full project timeline with Asana milestone tasks (Segment E, no Marcela gate — activated after contract + deposit confirmed)

## Schema (Execution Agent validates — pass/fail)
Required fields: phases (array), milestone_dates, dependencies

Note: `phases` must be an array of objects. `milestone_dates` maps milestone names to target dates. `dependencies` maps each phase to its predecessor.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: phases array includes every SOW scope_phase; milestone_dates covers all payment trigger milestones; dependencies graph is complete; Asana subtasks created for each phase
3: All phases present but one dependency missing or one Asana subtask not created
1: Any SOW scope_phase absent from schedule, or milestone_dates missing, or dependencies absent

**Accuracy (1–5)**
5: Timeline is realistic for project type and program size (typical residential: 8–14 months; hotel: 16–24 months; health center: 18–26 months); dates are ISO-8601 format; no dependency inversions
3: Timeline realistic but one phase duration seems off; all dates present
1: Timeline clearly unrealistic (e.g., 2-week construction phase for residential) or dependency inversions present

**Clarity (1–5)**
5: Client receives a clear project flow; each phase has a named milestone and target date; critical path is visible
3: Schedule comprehensible but critical path not explicitly marked
1: Schedule is a list of dates without phase names or dependencies

**State Sync (1–5)**
5: Asana milestone tasks created as subtasks with due dates; project_state updated to active_in_progress
3: Asana subtasks created but due dates missing; state update partial
1: No Asana subtasks created

**Timing (1–5)**
5: Schedule produced only after all three activation conditions confirmed by Vera (contract_signed + site_docs_complete + deposit_confirmed all true)
3: One activation condition not yet confirmed but schedule produced without causing downstream issues
1: Schedule produced before activation conditions met

**Decision Readiness**
N/A — No Marcela gate; Pablo fires after activation confirmed. Average score calculated over 5 dimensions.

## Auto-Fail Conditions
- phases array empty or missing
- milestone_dates absent
- Schedule produced before contract_signed + site_docs_complete + deposit_confirmed all true
- Asana subtasks not created
```

- [ ] **Step 2: Validate required sections present**

```bash
grep -q "Required fields:" tests/rubrics/project-schedule.md && echo "PASS: schema" || echo "FAIL"
grep -q "Auto-Fail" tests/rubrics/project-schedule.md && echo "PASS: auto-fail" || echo "FAIL"
grep -q "activation conditions" tests/rubrics/project-schedule.md && echo "PASS: activation check" || echo "FAIL"
```

Expected: all 3 PASS

---

### Task 3: permit-status.md — Paco's deliverable rubric

**Files:**
- Create: `tests/rubrics/permit-status.md`

- [ ] **Step 1: Create the rubric file**

```markdown
# Rubric: Permit Status
**Agent:** Paco
**Deliverable:** Permit submission and tracking record (Segment I, no Marcela gate — Paco fires after contractor selected at DG-11)

## Schema (Execution Agent validates — pass/fail)
Required fields: submitted_at, jurisdiction, status, corrections (array), approved_at

Note: `corrections` is an array (empty array `[]` is valid when status is not "corrections_required"). `approved_at` may be null if permit not yet approved.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All required fields present; jurisdiction names the specific authority (e.g., "Municipio de San Pedro Garza García — Desarrollo Urbano"); status is one of: submitted, under_review, corrections_required, approved; corrections array populated with specific items when status is corrections_required
3: All fields present but jurisdiction is generic (city name only); or corrections array empty when status is corrections_required
1: Any required field absent; or approved_at present while status is not approved

**Accuracy (1–5)**
5: Jurisdiction matches project location from state.json client_address or project context; submitted_at is after contractor selection confirmed (DG-11); correction items match actual permit reviewer feedback
3: Jurisdiction correct but authority name slightly wrong; submitted_at timing plausible
1: Wrong jurisdiction; submitted_at predates contractor selection

**Clarity (1–5)**
5: Vera can trigger construction phase start immediately from this document when status is approved; correction items are specific enough for action
3: Status clear but corrections lack specifics; Vera needs one follow-up to act
1: Status ambiguous; Vera cannot determine whether to unlock construction

**State Sync (1–5)**
5: Asana permit task updated at each status change: submitted → under_review → corrections_required / approved; construction phase unlocked in Asana when approved
3: Asana updated at submission and approval but not at intermediate steps
1: No Asana update

**Timing (1–5)**
5: Submission initiated promptly after DG-11 contractor selection; status updates reflected within reasonable processing window
3: Minor delay in submission initiation but within acceptable range
1: Permit submitted before contractor selection or not submitted at all

**Decision Readiness**
N/A — No Marcela gate; Paco → Vera (auto-unlock) on approval. Average score over 5 dimensions.

## Auto-Fail Conditions
- jurisdiction absent or entirely generic ("Mexico")
- submitted_at absent
- corrections array absent (even empty array required when no corrections)
- approved_at populated while status is not "approved"
- Permit submitted before DG-11 contractor selection confirmed
```

- [ ] **Step 2: Validate required sections present**

```bash
grep -q "Required fields:" tests/rubrics/permit-status.md && echo "PASS: schema" || echo "FAIL"
grep -q "Auto-Fail" tests/rubrics/permit-status.md && echo "PASS: auto-fail" || echo "FAIL"
grep -q "corrections" tests/rubrics/permit-status.md && echo "PASS: corrections field" || echo "FAIL"
```

Expected: all 3 PASS

---

### Task 4: vera-site-status.md — Vera Segment C evaluation rubric

**Files:**
- Create: `tests/rubrics/vera-site-status.md`

- [ ] **Step 1: Create the rubric file**

```markdown
# Rubric: Vera Site Status Update
**Agent:** Vera
**Deliverable:** Asana site readiness status update (Segment C — no JSON client deliverable)

## Special Handling
Vera does not write a scored JSON deliverable. Her Segment C evaluation is based on her raw text output describing the Asana update she performed. The Decision Gate Agent scores Vera's stated actions against this rubric.

The test-execution agent passes Vera's complete raw output text as the `deliverable` field. The Decision Gate Agent reads this text and scores whether Vera correctly identified and applied the right Asana update.

## Schema (Execution Agent validates — pass/fail)
No JSON schema validation for this segment. Test-execution agent checks that Vera produced any non-empty text output describing her Asana actions. If output is empty, flag as schema_fail.

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Asana Field Accuracy (1–5)**
5: Vera's output explicitly states: (a) which Asana task was updated (site_readiness task_id from state.json), (b) which field was set (site_readiness_status), (c) what value was set (matching Sol's current_status from site-readiness-report.json), and (d) what the blockers are if any
3: Vera updated the correct task and field but did not surface blockers explicitly
1: Vera updated wrong task or wrong field, or did not identify any Asana action

**Source Fidelity (1–5)**
5: Vera's status value matches Sol's site-readiness-report.json current_status exactly (not paraphrased); blockers listed match Sol's blockers array
3: Status value semantically correct but not verbatim from Sol's report; blockers partially surfaced
1: Vera's stated status contradicts Sol's report

**Clarity (1–5)**
5: Any human reading Vera's output can immediately confirm what was updated in Asana and why
3: Update described but reasoning not connected to Sol's report
1: Vera's output does not describe a clear Asana action

**State Sync (1–5)**
5: Vera explicitly states state.json was not modified (Sol's completion flag is set by Sol, not Vera) AND that she did not dispatch any downstream agent
3: Vera updated correct Asana field but did not confirm she did not modify state.json
1: Vera attempted to set state.json flags (Sol's responsibility) or attempted to dispatch Tomás directly

**Timing (1–5)**
5: Vera's update fires after Sol's site-readiness-report.json exists and before DG-03 review request is sent
3: Minor timing gap but Vera updated before DG-03
1: Vera fired before Sol's report exists or after DG-03 already sent

## Auto-Fail Conditions
- Vera's output is empty or contains no Asana update description
- Vera dispatched Tomás or any downstream agent (Vera's scope in Segment C is Asana update only — chain continuation is not Vera's role here)
- Vera set state.json site_data_complete flag (Sol sets this, not Vera)
- Vera reported a site status that contradicts Sol's site-readiness-report.json
```

- [ ] **Step 2: Validate required sections present**

```bash
grep -q "Special Handling" tests/rubrics/vera-site-status.md && echo "PASS: special handling" || echo "FAIL"
grep -q "Auto-Fail" tests/rubrics/vera-site-status.md && echo "PASS: auto-fail" || echo "FAIL"
grep -q "state.json" tests/rubrics/vera-site-status.md && echo "PASS: state boundary" || echo "FAIL"
```

Expected: all 3 PASS

---

### Task 5: Commit rubrics

- [ ] **Step 1: Commit the 4 rubric files**

```bash
git add tests/rubrics/budget.md tests/rubrics/project-schedule.md tests/rubrics/permit-status.md tests/rubrics/vera-site-status.md
git commit -m "feat: add missing rubrics — budget, project-schedule, permit-status, vera-site-status"
```

Expected: commit succeeds, 4 files added

---

## Chunk 2: SOW Templates

### Task 6: sow-standalone-residential.md

**Files:**
- Create: `docs/templates/sow/sow-standalone-residential.md`

> Note: `docs/templates/sow/` does not exist yet. Create it.

- [ ] **Step 1: Create directory and template file**

```bash
mkdir -p docs/templates/sow
```

Then create `docs/templates/sow/sow-standalone-residential.md`:

```markdown
# Scope of Work Template — Standalone Residential
**Project type:** `standalone_residential`
**Use for:** Private residential projects on individually owned lots — houses, villas, residences not subject to HOA governance.

---

## Phase Structure

### Phase 1 — Conceptual Design (Diseño Conceptual)
**Deliverables:**
- Parti diagram and design narrative (1–2 pages)
- Preliminary floor plan sketches (1:200 scale minimum)
- Site placement / orientation concept
- 3D conceptual massing model
- Material and color direction board (preliminary)
- Space arrangement diagram showing all programmed spaces

**Collaborators required:** None at this phase. Structural and systems engineers join Phase 2.

**Revision assumptions:** 2 rounds of client revision included. Each additional round billed at MXN 8,000/day.

**Milestone trigger:** Phase 1 complete when client provides written approval of conceptual direction.

---

### Phase 2 — Architectural Design (Proyecto Arquitectónico)
**Deliverables:**
- Floor plans all levels (1:100 scale)
- Elevations all four facades (1:100)
- Building sections minimum 2 (1:100)
- Roof plan
- Site plan with property boundaries, setbacks, access, parking
- Interior design criteria document
- Window and door schedule
- Preliminary structural coordination sketch (Oficio Taller coordinates with structural engineer)

**Collaborators required:**
- Structural engineer (Oficio Taller coordinates; client contract is separate)
- Electrical engineer (Oficio Taller coordinates)
- Plumbing / hydraulic engineer (Oficio Taller coordinates)

**Revision assumptions:** 2 rounds of client revision included. Each additional round billed at MXN 10,000/day.

**Milestone trigger:** Phase 2 complete when client provides written approval of architectural design.

---

### Phase 3 — Engineering Coordination (Coordinación de Ingeniería)
**Deliverables:**
- Structural engineering drawings integrated with architectural set
- Electrical single-line diagram and panel schedules
- Lighting layout plan with fixture specifications
- Plumbing and hydraulic layout
- Landscape architecture: excluded by default (client responsibility for independent landscape architect). If requested as an added service, add to Phase 2 deliverables and this phase.
- Irrigation plan: included by default for residential; explicitly excluded if client opts out
- Solar systems: rough layout included if in scope; client decision required by end of Phase 2
- Foundation plan and details

**Collaborators required:**
- Structural engineer (contract between client and engineer; Oficio Taller coordinates)
- Electrical / MEP engineers (same structure)

**Revision assumptions:** 1 round of structural coordination revision included. Changes driven by client program additions are billed additionally.

---

### Phase 4 — Executive Plans (Planos Ejecutivos)
**Deliverables:**
- Fully coordinated construction drawing set (architectural + structural + MEP)
- Detail sheets: wall sections, stairs, roof details, openings
- Finish schedule (all surfaces, all rooms)
- Door and window schedule with specifications
- Built-in furniture drawings (kitchen, closets, built-in shelving)
- Technical specifications document

**Collaborators required:** All engineers from Phase 3 must deliver coordinated final drawings.

**Revision assumptions:** 1 round of coordination revision included. Client changes after executive plan approval require a change order.

---

### Phase 5 — Contractor Bidding (Licitación)
**Deliverables:**
- Bid package preparation (executive plans + spec document sent to minimum 2 contractors)
- Bid comparison matrix (contractor name, total, key line items, timeline, notes)
- Recommendation with rationale

**Standard requirement:** Minimum 2 bids required. If only 1 contractor responds, matter is escalated to client for decision before proceeding.

**Local contractor cost validation:** Bid prices are reviewed against current local construction cost benchmarks (MXN per sqm for project type and quality level). Significant deviations above or below benchmark are flagged with explanation before recommending a contractor.

---

### Phase 6 — Permitting (Trámites)
**Deliverables:**
- Building permit application package (architectural plans + structural calculations + forms)
- Submission to municipal authority (Municipio)
- Tracking and correction management until permit issued

**Jurisdiction:** Determined by project location (Municipio de [city]).

---

### Phase 7 — Construction Administration (Supervisión Arquitectónica)
**Status:** Optional — included only if client adds supervision scope.
**Deliverables (if included):**
- Weekly site visit reports
- Material and finish approval sign-offs
- RFI (Request for Information) responses to contractor
- Construction milestone confirmation for invoice triggers

---

## Payment Schedule

| Milestone | Name | Percentage | Amount (TBD) | Trigger Event |
|---|---|---|---|---|
| M1 | Contract Signing | 30% | — | Signed SOW + first payment received |
| M2 | Concept Design Approved | 20% | — | Client written approval of Phase 1 |
| M3 | Construction Documents Delivered | 25% | — | Executive plans package delivered to client |
| M4 | Building Permit Obtained | 15% | — | Permit document delivered to client |
| M5 | Construction Administration Final | 10% | — | Final site visit report delivered (if supervision in scope) |

Note: If supervision is not in scope, M5 triggers at construction start instead.

Amounts are calculated by Bruno using `cost-basis.json` total_estimate × percentages above.
Payment currency: MXN unless otherwise agreed in writing.
Payment method: Bank transfer to Oficio Taller CLABE account (provided in invoice).

---

## Typical Timeline

| Phase | Typical Duration |
|---|---|
| Phase 1 — Conceptual Design | 3–5 weeks |
| Phase 2 — Architectural Design | 6–8 weeks |
| Phase 3 — Engineering Coordination | 4–6 weeks |
| Phase 4 — Executive Plans | 4–6 weeks |
| Phase 5 — Contractor Bidding | 3–4 weeks |
| Phase 6 — Permitting | 4–16 weeks (authority processing time varies) |
| Phase 7 — Construction Administration | Duration of construction (residential: 10–18 months typical) |
| **Total design phases (excl. permitting + construction)** | 20–29 weeks |

Note: Durations are typical estimates. Actual timeline is set by Pablo in `project-schedule.json` based on project size, complexity, and confirmed contractor start date.

---

## Responsibilities Matrix

| Deliverable | Responsible Party | Reviewed by |
|---|---|---|
| Conceptual design | Oficio Taller | Client |
| Architectural drawings | Oficio Taller | Client |
| Structural calculations | Structural engineer | Oficio Taller coordinates |
| MEP engineering | MEP engineers | Oficio Taller coordinates |
| Executive plans set | Oficio Taller | Client + engineers |
| Bid package | Oficio Taller | Client selects contractor |
| Permit application | Oficio Taller | Municipal authority |
| Construction | Contractor | Oficio Taller (if supervision in scope) |
| Payment milestone sign-off | Client | Oficio Taller invoices |

---

## Standard Exclusions

The following are explicitly **not included** in this scope:
1. Structural, electrical, plumbing, and civil engineering fees (client contracts engineers directly; Oficio Taller coordinates only)
2. Permit fees, municipal taxes, or government charges
3. Contractor selection or construction contracts (Oficio Taller recommends; client decides)
4. Furniture, art, décor, or movable equipment not shown in built-in furniture drawings
5. Topographic survey (required — client responsibility to provide)
6. Hydrologic or soil study (if required by municipality — client responsibility)
7. Legal review of property title or easements
8. Construction cost guarantees (estimates are preliminary; final cost determined by contractor bids)

---

## Project-Type Clauses

```json
{
  "project_type_clauses": [
    {
      "clause": "residential_standard",
      "title": "Standard Residential Scope",
      "text": "This project is a private standalone residential building on an individually owned lot. All design decisions are made exclusively between the client and Oficio Taller unless otherwise noted. No HOA, covenant, or third-party design review applies unless disclosed by the client before contract signing."
    },
    {
      "clause": "client_changes",
      "title": "Client-Initiated Program Changes",
      "text": "Changes to the approved program requested by the client after a phase milestone has been approved will be scoped and billed as a change order. Oficio Taller will not absorb rework costs from client-initiated changes."
    },
    {
      "clause": "site_conditions",
      "title": "Site Condition Discovery",
      "text": "Design is based on information provided by the client and publicly available municipal records. If site conditions discovered during construction (soil, utilities, encroachments) require design changes, these will be scoped as a change order."
    },
    {
      "clause": "esignature",
      "title": "Electronic Signature",
      "text": "This document is valid when signed electronically by the client and an authorized Oficio Taller representative. Electronic signatures carry the same legal weight as physical signatures under Mexican federal law (NOM-151-SCFI)."
    }
  ]
}
```

---

## Tomás Instructions

When producing `scope-of-work.json` from this template:
1. Read `area-program.json` to determine actual program size and spaces
2. Read `cost-basis.json` to populate payment milestone amounts (M1–M5 × percentages)
3. Set `project_type_clauses` from the JSON block above verbatim
4. Adjust phase deliverables to reflect actual project scope (e.g., if irrigation is not in scope, mark as excluded)
5. Set `revision_assumptions` per phase as specified above
6. Do NOT include supervision (Phase 7) unless state.json or seed data explicitly includes it
```

- [ ] **Step 2: Validate all 20 checklist items from scope-of-work rubric are covered**

```bash
f=docs/templates/sow/sow-standalone-residential.md
grep -q "Conceptual" $f && echo "PASS: item 1 conceptual" || echo "FAIL: item 1"
grep -q "Executive" $f && echo "PASS: item 3 executive plans" || echo "FAIL: item 3"
grep -q "supervision" $f && echo "PASS: item 4 supervision" || echo "FAIL: item 4"
grep -q "Landscape" $f && echo "PASS: item 5 landscape" || echo "FAIL: item 5"
grep -q "Structural engineer" $f && echo "PASS: item 6 structural" || echo "FAIL: item 6"
grep -q "Electrical" $f && echo "PASS: item 7 electrical" || echo "FAIL: item 7"
grep -q "Lighting" $f && echo "PASS: item 8 lighting" || echo "FAIL: item 8"
grep -q "Plumbing\|hydraulic\|water" $f && echo "PASS: item 9 water" || echo "FAIL: item 9"
grep -qi "irrigation" $f && echo "PASS: item 10 irrigation" || echo "FAIL: item 10"
grep -qi "solar" $f && echo "PASS: item 11 solar" || echo "FAIL: item 11"
grep -q "cost validation\|benchmarks" $f && echo "PASS: item 12 cost validation" || echo "FAIL: item 12"
grep -q "Payment Schedule" $f && echo "PASS: item 13 payment" || echo "FAIL: item 13"
grep -q "Responsibilities" $f && echo "PASS: item 15 responsibilities" || echo "FAIL: item 15"
grep -q "Exclusions" $f && echo "PASS: item 16 exclusions" || echo "FAIL: item 16"
grep -q "Revision assumptions" $f && echo "PASS: item 17 revision" || echo "FAIL: item 17"
grep -q "Typical Timeline\|Timeline" $f && echo "PASS: item 18 timeline" || echo "FAIL: item 18"
grep -q "project_type_clauses" $f && echo "PASS: item 19 type clauses" || echo "FAIL: item 19"
grep -q "esignature" $f && echo "PASS: item 20 esignature" || echo "FAIL: item 20"
```

Expected: all 19 PASS (item 14 — deliverables listed by phase — verified by presence of Phase 1–7 sections)

---

### Task 7: sow-residential-in-development.md

**Files:**
- Create: `docs/templates/sow/sow-residential-in-development.md`

- [ ] **Step 1: Create template file**

This template extends sow-standalone-residential.md with HOA coordination and covenant review clauses. Copy all sections and apply the following differences:

```markdown
# Scope of Work Template — Residential in Development
**Project type:** `residential_in_development`
**Use for:** Private residential projects within a gated community, fraccionamiento, or any development governed by an HOA, covenant, or developer design guidelines.

---

## Key Differences from Standalone Residential

This template is identical to `sow-standalone-residential.md` with the following additions and modifications:

1. **Phase 1 addition:** Design concept submission to HOA/development design review committee required before client milestone approval
2. **Phase 2 addition:** HOA/covenant compliance review of floor plans and elevations; developer setback and height limit verification added to deliverables
3. **Additional deliverable (Phase 2):** HOA design review submission package (cover letter + required plan formats per HOA rules)
4. **Additional deliverable (Phase 2):** Covenant compliance checklist (Oficio Taller confirms design against all development covenants)

---

## Phase Structure

### Phase 1 — Conceptual Design (same as standalone residential)
**Additional deliverable:** Preliminary concept submitted to HOA design review committee for early feedback.
All other deliverables identical to standalone residential template.

### Phase 2 — Architectural Design
**Additional deliverables:**
- HOA design review submission package (floor plans + elevations in format required by development)
- Covenant compliance checklist confirming: setbacks, maximum height, facade materials, parking count, prohibited uses, landscaping requirements
- Written HOA approval document (obtained by Oficio Taller on behalf of client)

**Important:** Municipal permit application cannot proceed until HOA written approval is received.

### Phase 3 — Engineering Coordination
Identical to standalone residential.

### Phase 4 — Executive Plans
**Addition:** Final HOA-compliant drawing set must bear HOA approval stamp or reference number.

### Phase 5 — Contractor Bidding
**Addition:** Contractors must be pre-approved by development (if development maintains a contractor list, confirm with client before bidding phase).

### Phase 6 — Permitting
**Addition:** Some developments require the developer's internal authorization before municipal permit application. Oficio Taller will verify this requirement with client during Phase 2.

### Phase 7 — Construction Administration (optional — same as standalone)

---

## Landscape, Irrigation, Solar Scope

- **Landscape architecture:** Same as standalone residential — excluded by default; included only if client requests as an additional service.
- **Irrigation:** Included by default for residential; explicitly excluded if client opts out.
- **Solar systems:** Explicitly excluded unless client confirms interest before Phase 2 completion.

## Local Contractor Cost Validation

Included in Phase 5 (identical to standalone residential): bid prices reviewed against local benchmarks before recommendation.

## Revision Assumptions

- Phase 1 — Conceptual Design: 2 rounds included. Each additional round: MXN 8,000/day.
- Phase 2 — Architectural Design (including HOA compliance): 2 rounds included. HOA-driven revisions beyond 2 rounds billed as change orders (MXN 10,000/day).
- Phase 3 — Engineering Coordination: 1 round included.
- Phase 4 — Executive Plans: 1 round included. Client-initiated changes after Phase 4 approval require a change order.

## Typical Timeline

| Phase | Typical Duration |
|---|---|
| Phase 1 — Conceptual Design + HOA early review | 4–6 weeks |
| Phase 2 — Architectural Design + HOA submission | 8–12 weeks |
| Phase 3 — Engineering Coordination | 4–6 weeks |
| Phase 4 — Executive Plans | 4–6 weeks |
| Phase 5 — Contractor Bidding | 3–4 weeks |
| Phase 6 — Permitting | 4–16 weeks |
| **Total design phases (excl. permitting + construction)** | 23–34 weeks |

Note: HOA review adds 2–4 weeks vs. standalone residential.

## Payment Schedule

| Milestone | Name | Percentage | Amount (TBD) | Trigger Event |
|---|---|---|---|---|
| M1 | Contract Signing | 30% | — | Signed SOW + first payment received |
| M2 | Concept Design Approved | 20% | — | Client written approval of Phase 1 (and HOA early feedback received) |
| M3 | Construction Documents Delivered | 25% | — | Executive plans package + HOA-approved drawing set delivered |
| M4 | Building Permit Obtained | 15% | — | Municipal permit document delivered to client |
| M5 | Construction Administration Final | 10% | — | Final site visit report delivered (if supervision in scope); otherwise triggers at construction start |

Note: If HOA review process causes delays, milestone dates adjust accordingly. Payment triggers are based on deliverable completion, not calendar date.

---

## Responsibilities Matrix
Same as standalone residential, with additions:

| Deliverable | Responsible Party | Reviewed by |
|---|---|---|
| HOA design review submission | Oficio Taller | HOA design committee |
| Covenant compliance checklist | Oficio Taller | Client |
| HOA approval document | Oficio Taller (pursues) | HOA / Client |
| Developer contractor pre-approval | Client | — |

---

## Standard Exclusions
Same as standalone residential, with additions:
9. HOA fees, development assessment fees, or design review committee fees
10. Legal challenges to HOA decisions or covenant disputes (refer to attorney)
11. Design changes required by HOA feedback beyond 2 revision rounds (billed as change orders)

---

## Project-Type Clauses

```json
{
  "project_type_clauses": [
    {
      "clause": "hoa_coordination",
      "title": "HOA Design Review Coordination",
      "text": "This project is subject to design review by a homeowners association (HOA) or development covenant authority. Oficio Taller will prepare and submit the design review package and coordinate responses. Review timelines set by the HOA are outside Oficio Taller's control and do not constitute a project delay attributable to Oficio Taller."
    },
    {
      "clause": "covenant_review",
      "title": "Covenant Compliance",
      "text": "Oficio Taller will review the project design against all applicable development covenants and restrictions disclosed by the client. The client is responsible for disclosing all covenants, deed restrictions, and development design guidelines applicable to the property. Covenants discovered after design approval may require paid revision rounds."
    },
    {
      "clause": "client_changes",
      "title": "Client-Initiated Program Changes",
      "text": "Changes to the approved program requested by the client after a phase milestone has been approved will be scoped and billed as a change order."
    },
    {
      "clause": "esignature",
      "title": "Electronic Signature",
      "text": "This document is valid when signed electronically under Mexican federal law (NOM-151-SCFI)."
    }
  ]
}
```

---

## Tomás Instructions
Same as standalone residential. Additional step:
- Set `project_type_clauses` to include `hoa_coordination` and `covenant_review` clauses verbatim
- Note in `revision_assumptions` that HOA-driven revisions are billed beyond the 2 included rounds
```

- [ ] **Step 2: Validate required sections present**

```bash
f=docs/templates/sow/sow-residential-in-development.md
grep -q "project_type_clauses" $f && echo "PASS: type clauses" || echo "FAIL"
grep -q "hoa_coordination" $f && echo "PASS: HOA clause" || echo "FAIL"
grep -q "covenant_review" $f && echo "PASS: covenant clause" || echo "FAIL"
grep -q "Payment Schedule" $f && echo "PASS: payment schedule (full table)" || echo "FAIL"
grep -q "Exclusions" $f && echo "PASS: exclusions" || echo "FAIL"
grep -qi "landscape" $f && echo "PASS: landscape scope" || echo "FAIL"
grep -qi "irrigation" $f && echo "PASS: irrigation" || echo "FAIL"
grep -qi "solar" $f && echo "PASS: solar" || echo "FAIL"
grep -q "Revision Assumptions" $f && echo "PASS: revision assumptions" || echo "FAIL"
grep -q "Typical Timeline" $f && echo "PASS: timeline" || echo "FAIL"
grep -q "cost validation\|benchmarks" $f && echo "PASS: cost validation" || echo "FAIL"
```

Expected: all 11 PASS

---

### Task 8: sow-commercial-hotel.md

**Files:**
- Create: `docs/templates/sow/sow-commercial-hotel.md`

- [ ] **Step 1: Create template file**

```markdown
# Scope of Work Template — Commercial: Hotel
**Project type:** `commercial_hotel`
**Use for:** Hospitality projects — hotels, boutique hotels, apart-hotels, resort components. Subject to hotel brand standards (if branded) and hospitality-specific compliance requirements.

---

## Phase Structure

### Phase 1 — Conceptual Design
**Deliverables:**
- Hotel concept narrative: positioning, guest experience vision, programmatic breakdown (rooms by category, F&B, spa, meeting, back-of-house)
- Schematic floor plans (1:200) showing room distribution per level
- Massing model and site orientation
- Preliminary room key count and category mix
- Conceptual material direction aligned with brand positioning

**Brand standards note:** If project is a branded hotel (franchise or management agreement), brand design guidelines are provided by client. Oficio Taller integrates brand standards from Phase 1. Brand review submission is part of Phase 2.

### Phase 2 — Architectural Design
**Deliverables:**
- Floor plans all levels (1:100) — guestrooms, corridors, BOH, F&B, spa, meeting rooms
- Elevations all facades (1:100)
- Typical guestroom layout + bathroom layout (detailed, 1:50)
- Lobby and public area layout with finish zones
- F&B kitchen layout concept (coordinated with kitchen consultant if applicable)
- Brand standards compliance matrix (if branded)
- Brand design review submission package (if branded)
- Accessibility compliance plan (hospitality-specific requirements: guest room accessible category, accessible routes, signage)

**Collaborators required:**
- Structural engineer (Oficio Taller coordinates)
- MEP engineers: electrical, lighting, plumbing/hydraulic, HVAC
- Kitchen consultant (if full-service F&B — client contracts; Oficio Taller coordinates)
- AV/tech consultant (for meeting rooms / entertainment systems — client contracts)

### Phase 3 — Engineering Coordination
**Deliverables:**
- Structural system (likely concrete frame for multi-story hotel)
- Electrical: guest room outlet layout, panel schedule, emergency/backup power design
- Lighting: decorative + functional per zone (lobby, guestroom, F&B, exterior); lighting narrative by zone
- HVAC: central system vs. split unit strategy (hotel efficiency requirement)
- Plumbing/hydraulic: guestroom bathroom layouts, pool/spa systems if applicable
- Fire protection coordination (fire sprinkler, fire alarm — specialized contractor by client)
- Low-voltage / AV rough-in (coordinated with AV consultant)
- Irrigation plan (if grounds/landscape in scope)

**Additional systems for hotel vs. residential:**
- HVAC is always required (not conditional)
- AV/sound system rough-in always required for hotel public areas
- Fire suppression coordination always required

**Landscape, Irrigation, Solar scope for hotel:**
- Landscape architecture: included if grounds/exterior areas are in scope; coordinate with landscape architect. If grounds not in hotel scope, explicitly excluded.
- Irrigation: included if landscaped grounds are in scope; explicitly excluded if no grounds component.
- Solar systems: explicitly excluded by default for hotel. If owner requests sustainability certification (LEED/EDGE), solar feasibility study added as separate line item.

**Revision assumptions:**
- Phase 1 — Conceptual Design: 2 rounds included. Brand review revisions: up to 2 rounds included; additional rounds are change orders.
- Phase 2 — Architectural Design: 2 rounds included. Brand review-driven revisions beyond 2 rounds: billed as change orders (MXN 12,000/day).
- Phase 3 — Engineering Coordination: 1 round included.
- Phase 4 — Executive Plans: 1 round included; brand compliance final review included.

**Local contractor cost validation:** Bid prices reviewed against local hospitality construction benchmarks (cost per sqm for hotel category: economy/midscale/upscale/luxury). Included in Phase 5.

### Phase 4 — Executive Plans
**Deliverables:**
- Fully coordinated construction drawing set
- Guestroom interior drawings (all room categories)
- BOH kitchen construction drawings (if full-service F&B)
- Pool/spa drawings (if in scope)
- Signage system specification
- FF&E specification document (furniture, fixtures, equipment — selection; procurement by client)
- Brand standards final compliance confirmation document (if branded)

### Phase 5 — Contractor Bidding
Same as residential. Note: Hotel projects typically use a general contractor with specialty subcontractors (MEP, FF&E, AV).

### Phase 6 — Permitting
**Additional requirements for hotel:**
- COFEPRIS or municipal health authority review (if F&B serving public)
- Tourism ministry registration (Secretaría de Turismo — SECTUR) — client responsibility; Oficio Taller provides plans in required format
- Hotel operating license application support (plans only; client manages process)
- Fire department review (fire exit, egress, sprinkler) — Oficio Taller provides plans; specialized inspector coordinates

### Phase 7 — Construction Administration (optional — same structure as residential)

> **Optional architectural supervision clause:** Construction administration for hotels is recommended but optional. If excluded, an explicit supervision exclusion clause is included in the SOW stating that construction conformance is the contractor's and client's responsibility. Oficio Taller is available for periodic consultation visits billed at day rate.

---

## Typical Timeline

| Phase | Typical Duration |
|---|---|
| Phase 1 — Conceptual Design | 4–6 weeks |
| Phase 2 — Architectural Design + Brand Review | 8–14 weeks |
| Phase 3 — Engineering Coordination | 6–8 weeks |
| Phase 4 — Executive Plans | 6–8 weeks |
| Phase 5 — Contractor Bidding | 4–6 weeks |
| Phase 6 — Permitting | 8–20 weeks (hospitality permitting multi-authority) |
| **Total design phases (excl. permitting + construction)** | 28–42 weeks |

---

## Payment Schedule

| Milestone | Name | Percentage | Amount (TBD) | Trigger Event |
|---|---|---|---|---|
| M1 | Contract Signing | 25% | — | Signed SOW |
| M2 | Concept Design Approved | 15% | — | Client + brand written approval of Phase 1 |
| M3 | Architectural Design Approved | 20% | — | Client + brand written approval of Phase 2 |
| M4 | Construction Documents Delivered | 25% | — | Executive plans package delivered |
| M5 | Permits Obtained | 15% | — | Building permit document delivered |

Note: Hotel projects have larger Phase 2/4 amounts due to greater complexity.

---

## Responsibilities Matrix

| Deliverable | Responsible Party | Reviewed by |
|---|---|---|
| Conceptual / architectural design | Oficio Taller | Client + brand (if branded) |
| Brand standards compliance | Oficio Taller | Brand design team |
| Structural engineering | Structural engineer | Oficio Taller coordinates |
| MEP engineering | MEP engineers | Oficio Taller coordinates |
| Kitchen layout | Kitchen consultant | Oficio Taller + client |
| FF&E specification | Oficio Taller (specs only) | Client (selects + procures) |
| SECTUR registration | Client | — |
| Fire department review | Oficio Taller (plans) | Fire department |

---

## Standard Exclusions
1–8: Same as standalone residential, plus:
9. Hotel brand franchise fees or royalties
10. FF&E procurement (Oficio Taller specifies; client procures)
11. Kitchen equipment procurement
12. Hotel operating license fees
13. SECTUR registration fees
14. COFEPRIS permit fees for F&B
15. AV equipment and installation (Oficio Taller coordinates rough-in only)

---

## Project-Type Clauses

```json
{
  "project_type_clauses": [
    {
      "clause": "hospitality_compliance",
      "title": "Hospitality Regulatory Compliance",
      "text": "Hotel projects in Mexico are subject to regulations from SECTUR, municipal development authorities, and where food service is included, COFEPRIS. Oficio Taller will prepare construction drawings in formats required by these authorities. Application submissions, fees, and follow-up with government agencies are the client's responsibility unless explicitly included as an add-on service."
    },
    {
      "clause": "brand_standards_coordination",
      "title": "Brand Standards Coordination",
      "text": "If this hotel operates under a brand franchise or management agreement, the client is responsible for providing Oficio Taller with the current brand design standards manual and FF&E specifications before Phase 1 begins. Design revisions required by brand design review feedback beyond 2 rounds will be billed as change orders."
    },
    {
      "clause": "ffe_scope_boundary",
      "title": "FF&E Scope Boundary",
      "text": "Oficio Taller's scope includes specification of furniture, fixtures, and equipment. Procurement, purchasing, delivery, and installation coordination of FF&E is the client's responsibility. Oficio Taller is available for FF&E procurement management as an additional service."
    },
    {
      "clause": "esignature",
      "title": "Electronic Signature",
      "text": "This document is valid when signed electronically under Mexican federal law (NOM-151-SCFI)."
    }
  ]
}
```

---

## Tomás Instructions
- Set `project_type_clauses` to include `hospitality_compliance`, `brand_standards_coordination`, `ffe_scope_boundary` verbatim
- Adjust payment schedule to hotel percentages (25/15/20/25/15) — not residential defaults
- Check if project is branded hotel (state.json or seed data) — include brand standards deliverables if yes
- HVAC and AV are always required systems for hotels — do not mark as conditional
```

- [ ] **Step 2: Validate**

```bash
f=docs/templates/sow/sow-commercial-hotel.md
grep -q "project_type_clauses" $f && echo "PASS: type clauses" || echo "FAIL"
grep -q "hospitality_compliance" $f && echo "PASS: compliance clause" || echo "FAIL"
grep -q "brand_standards_coordination" $f && echo "PASS: brand clause" || echo "FAIL"
grep -q "Payment Schedule" $f && echo "PASS: payment" || echo "FAIL"
grep -q "Exclusions" $f && echo "PASS: exclusions" || echo "FAIL"
grep -qi "landscape" $f && echo "PASS: landscape" || echo "FAIL"
grep -qi "solar" $f && echo "PASS: solar" || echo "FAIL"
grep -q "Revision assumptions\|Revision Assumptions" $f && echo "PASS: revision assumptions" || echo "FAIL"
grep -q "Typical Timeline" $f && echo "PASS: timeline" || echo "FAIL"
grep -q "cost validation\|benchmarks" $f && echo "PASS: cost validation" || echo "FAIL"
grep -q "supervision clause\|optional_supervision" $f && echo "PASS: supervision clause" || echo "FAIL"
```

Expected: all 11 PASS

---

### Task 9: sow-commercial-health-center.md

**Files:**
- Create: `docs/templates/sow/sow-commercial-health-center.md`

- [ ] **Step 1: Create template file**

```markdown
# Scope of Work Template — Commercial: Health Center
**Project type:** `commercial_health_center`
**Use for:** Medical and health facilities — clinics, outpatient centers, diagnostic imaging centers, wellness centers, dental clinics, medical offices. Requires COFEPRIS compliance and specialized medical systems coordination.

---

## Phase Structure

### Phase 1 — Conceptual Design
**Deliverables:**
- Medical facility program narrative: services offered, patient flow diagram, room types and quantities (consulting rooms, procedure rooms, waiting, reception, support)
- Schematic floor plans (1:200) showing clinical zone vs. public zone separation
- Accessibility compliance concept (mandatory for health facilities: IMSS/ISSSTE standards or international equivalent)
- COFEPRIS zone classification scheme (clean zones, semi-restricted, restricted — for surgical/procedure centers)
- Material direction: clinical-grade finishes identified

### Phase 2 — Architectural Design
**Deliverables:**
- Floor plans all areas (1:100) with clinical zone classifications marked
- Patient flow and staff flow diagrams on plans
- Elevations
- Accessible route plan (ramps, door widths, accessible bathrooms per NOM-030-SSA3 or equivalent)
- Waiting room, consultation room, and procedure room layouts (1:50 detail)
- Medical equipment rough coordination plan (equipment list provided by client; Oficio Taller coordinates spatial requirements)
- COFEPRIS preliminary compliance review package

**Collaborators required:**
- Structural engineer (Oficio Taller coordinates)
- MEP engineers: electrical (medical-grade power — dedicated circuits, UPS), plumbing/hydraulic (medical gas rough-in if applicable), HVAC (clinical-grade ventilation, HEPA filtration if applicable)
- Medical equipment consultant (client contracts if specialized — e.g., imaging, OR equipment)

### Phase 3 — Engineering Coordination
**Deliverables:**
- Structural drawings
- Electrical: medical-grade panel layout, dedicated clinical circuits, emergency power for critical areas
- Lighting: clinical-grade lighting in exam/procedure rooms; task lighting specifications
- Plumbing: medical hand-washing stations per clinical standards, sterilization room plumbing if applicable
- Medical gas rough-in drawings (if project includes O2, N2O, vacuum — requires medical gas specialist)
- HVAC: clinical-grade air handling (pressure differentials for restricted zones if applicable)
- Waterproofing specifications for wet clinical areas

**Note on medical gas:** If project includes medical gases (O2, vacuum, N2O), a certified medical gas consultant is required. This consultant must be contracted directly by the client. Oficio Taller integrates rough-in drawings into the set.

**Landscape, Irrigation, Solar scope for health center:**
- Landscape architecture: excluded by default for clinical facilities. If accessible exterior grounds are in scope (courtyards, accessible paths), include with explicit scope statement.
- Irrigation: explicitly excluded unless landscaped exterior grounds are in scope.
- Solar systems: explicitly excluded unless owner targets sustainability certification. If included, add as optional Phase 3 deliverable.

**Revision assumptions:**
- Phase 1 — Conceptual Design + COFEPRIS zone scheme: 2 rounds included.
- Phase 2 — Architectural Design + COFEPRIS package: 2 rounds included. COFEPRIS-driven revisions beyond 2 rounds: billed as change orders (MXN 10,000/day).
- Phase 3 — Engineering Coordination: 1 round included.
- Phase 4 — Executive Plans (COFEPRIS-ready set): 1 round included.

**Local contractor cost validation:** Bid prices reviewed against local benchmarks for clinical construction (cost per sqm for medical facility type). Included in Phase 5.

### Phase 4 — Executive Plans
**Deliverables:**
- Fully coordinated construction drawing set
- Clinical room detail drawings (exam rooms, procedure rooms, sterilization)
- Medical equipment coordination drawings (equipment spaces, clearances, utility connections)
- COFEPRIS-ready drawing set (formatted for health authority review)
- Signage system for clinical wayfinding
- Specification: clinical-grade flooring, wall finish systems, casework

### Phase 5 — Contractor Bidding
Same as residential template. Note: Medical facility construction typically requires contractors with health facility experience.

### Phase 6 — Permitting
**Additional requirements for health facilities:**
- COFEPRIS permit application (Comisión Federal para la Protección contra Riesgos Sanitarios) — Oficio Taller prepares drawings in COFEPRIS format; client manages submission and follow-up
- Municipal building permit (standard)
- Civil protection review (evacuation routes, fire safety)
- For imaging centers: CNSNS radiation safety review (Nuclear Safety Commission) — client responsibility; Oficio Taller provides shielding drawings

### Phase 7 — Construction Administration (optional)

> **Optional architectural supervision clause:** Construction administration for health facilities is recommended. If excluded, the SOW explicitly states that clinical finish conformance (coved base, seamless floors, antimicrobial surfaces) is the contractor's responsibility per specifications. Oficio Taller is available for periodic visits billed at day rate.

---

## Typical Timeline

| Phase | Typical Duration |
|---|---|
| Phase 1 — Conceptual Design + COFEPRIS zone scheme | 4–6 weeks |
| Phase 2 — Architectural Design + COFEPRIS package | 8–12 weeks |
| Phase 3 — Engineering Coordination (clinical-grade) | 6–8 weeks |
| Phase 4 — Executive Plans (COFEPRIS-ready) | 5–7 weeks |
| Phase 5 — Contractor Bidding | 4–5 weeks |
| Phase 6 — Permitting (COFEPRIS + municipal) | 8–24 weeks |
| **Total design phases (excl. permitting + construction)** | 27–38 weeks |

---

## Payment Schedule

| Milestone | Name | Percentage | Amount (TBD) | Trigger Event |
|---|---|---|---|---|
| M1 | Contract Signing | 25% | — | Signed SOW |
| M2 | Concept Design Approved | 15% | — | Client written approval of Phase 1 + COFEPRIS zone scheme accepted |
| M3 | Architectural Design Approved | 20% | — | Client written approval of Phase 2 |
| M4 | Construction Documents Delivered | 25% | — | Executive plans package including COFEPRIS set delivered |
| M5 | COFEPRIS Permit Obtained | 15% | — | COFEPRIS permit document delivered to client |

---

## Responsibilities Matrix

| Deliverable | Responsible Party | Reviewed by |
|---|---|---|
| Architectural + clinical layout | Oficio Taller | Client + COFEPRIS |
| COFEPRIS compliance drawings | Oficio Taller | COFEPRIS |
| Structural engineering | Structural engineer | Oficio Taller coordinates |
| Medical-grade electrical | Electrical engineer | Oficio Taller + client |
| Medical gas rough-in | Medical gas specialist (if applicable) | Oficio Taller integrates |
| Medical equipment coordination | Oficio Taller (spatial only) | Medical equipment consultant |
| COFEPRIS submission | Client | COFEPRIS |
| CNSNS review (if imaging) | Client | CNSNS |

---

## Standard Exclusions
1–8: Same as standalone residential, plus:
9. Medical equipment procurement or installation
10. COFEPRIS and municipal permit fees
11. Medical gas installation (Oficio Taller provides rough-in drawings only; certified installer required)
12. CNSNS radiation safety certification (client responsibility)
13. IT infrastructure and medical records system (Oficio Taller provides data rough-in only)
14. Clinical commissioning / accreditation process

---

## Project-Type Clauses

```json
{
  "project_type_clauses": [
    {
      "clause": "health_authority_compliance",
      "title": "COFEPRIS and Health Authority Compliance",
      "text": "Health facility projects in Mexico require review and approval from COFEPRIS (Comisión Federal para la Protección contra Riesgos Sanitarios). Oficio Taller will prepare construction drawings in the format required by COFEPRIS. The client is responsible for the submission process, all associated fees, and follow-up communications with the authority. Design revisions required by COFEPRIS feedback are included for up to 2 rounds; additional rounds are billed as change orders."
    },
    {
      "clause": "medical_equipment_coordination",
      "title": "Medical Equipment Coordination",
      "text": "Oficio Taller will coordinate the spatial and utility requirements of medical equipment based on the equipment list provided by the client. The client is responsible for providing complete equipment specifications (dimensions, weight, utility requirements) before Phase 2 completion. Equipment not disclosed before Phase 2 approval may require paid change orders to accommodate."
    },
    {
      "clause": "clinical_standards",
      "title": "Clinical Design Standards",
      "text": "The design will comply with applicable Mexican Normas Oficiales (NOM) for health facilities, including accessibility standards. Where international standards are specified by the client (JCI, CAP), Oficio Taller will design to those standards. The client is responsible for confirming which standards apply before Phase 1 begins."
    },
    {
      "clause": "optional_supervision",
      "title": "Optional Architectural Construction Administration",
      "text": "Architectural construction administration (supervision) is an optional service. If not included in this SOW, Oficio Taller is not responsible for monitoring contractor adherence to specifications during construction. The client and contractor bear responsibility for construction conformance. Oficio Taller is available for periodic consultation site visits at a day rate upon request."
    },
    {
      "clause": "esignature",
      "title": "Electronic Signature",
      "text": "This document is valid when signed electronically under Mexican federal law (NOM-151-SCFI)."
    }
  ]
}
```

---

## Tomás Instructions
- Set `project_type_clauses` to include `health_authority_compliance`, `medical_equipment_coordination`, `clinical_standards`, `optional_supervision` verbatim
- Use health center payment schedule (25/15/20/25/15)
- Medical-grade electrical and clinical HVAC are always required — do not mark as conditional
- Note: M5 payment trigger is COFEPRIS permit (not municipal building permit)
```

- [ ] **Step 2: Validate**

```bash
f=docs/templates/sow/sow-commercial-health-center.md
grep -q "project_type_clauses" $f && echo "PASS: type clauses" || echo "FAIL"
grep -q "health_authority_compliance" $f && echo "PASS: compliance clause" || echo "FAIL"
grep -q "medical_equipment_coordination" $f && echo "PASS: equipment clause" || echo "FAIL"
grep -q "optional_supervision" $f && echo "PASS: supervision clause" || echo "FAIL"
grep -q "Payment Schedule" $f && echo "PASS: payment" || echo "FAIL"
grep -q "Exclusions" $f && echo "PASS: exclusions" || echo "FAIL"
grep -qi "landscape" $f && echo "PASS: landscape" || echo "FAIL"
grep -qi "irrigation" $f && echo "PASS: irrigation" || echo "FAIL"
grep -qi "solar" $f && echo "PASS: solar" || echo "FAIL"
grep -q "Revision Assumptions\|Revision assumptions" $f && echo "PASS: revision assumptions" || echo "FAIL"
grep -q "Typical Timeline" $f && echo "PASS: timeline" || echo "FAIL"
grep -q "cost validation\|benchmarks" $f && echo "PASS: cost validation" || echo "FAIL"
```

Expected: all 12 PASS

---

### Task 10: sow-public-civic.md

**Files:**
- Create: `docs/templates/sow/sow-public-civic.md`

- [ ] **Step 1: Create template file**

```markdown
# Scope of Work Template — Public / Civic
**Project type:** `public_civic`
**Use for:** Public buildings — government offices, cultural centers, libraries, museums, plazas, civic infrastructure. Subject to public procurement regulations, government approval processes, and public bidding requirements.

---

## Key Distinctions from Private Projects

1. **Client is a government entity or public institution** — contract approval process may involve committee or board approval; contract signing milestone is when contract is formally executed by authorized representative
2. **Contractor bidding is a public process** — licitación pública (public tender) required above value thresholds set by law (Ley de Obras Públicas); Oficio Taller prepares tender documents; client manages the public tender process
3. **Government approval gates** — design may require review and approval by multiple government bodies beyond the standard municipal permit
4. **Public interest review** — community impact, accessibility, environmental assessment may be required

---

## Phase Structure

### Phase 1 — Conceptual Design
**Deliverables:**
- Civic program narrative: public use description, capacity, accessibility requirements, community service goals
- Schematic floor plans (1:200)
- Site plan showing public access, pedestrian flows, parking, relationship to surrounding streets
- Accessibility concept (mandatory for public buildings: universal design standards)
- Sustainability concept (if IMSS/SEP/SEMARNAT requirements apply — confirm with client)
- Concept presentation for internal government stakeholder review

**Government approval note:** Some government clients require concept design approval by a design committee, elected official, or board before Phase 2 begins.

### Phase 2 — Architectural Design
**Deliverables:**
- Floor plans all areas (1:100) with all public vs. staff vs. service zones marked
- Elevations all facades
- Accessibility-compliant design: ramps, accessible routes, accessible bathrooms, accessible parking per NOM standards
- Fire egress plan (evacuation routes per civil protection requirements)
- Sustainability features document (if LEED/VERDE certification target — confirm with client)
- Preliminary government review package (formatted for review authority if applicable)
- Universal design compliance matrix

**Collaborators required:**
- Structural engineer (Oficio Taller coordinates)
- MEP engineers: electrical, lighting, plumbing/hydraulic
- Civil engineer (if site work includes streets, drainage, public infrastructure)

### Phase 3 — Engineering Coordination
**Deliverables:**
- Structural drawings (may require government structural review)
- Electrical: public-scale systems, emergency/exit lighting, exterior lighting
- Lighting: public space lighting — functional + architectural
- Plumbing/hydraulic: public restrooms, facility-appropriate scale
- Civil/site: drainage, paving, accessibility ramps, street connections (if in scope)
- Sustainability systems integration (if in scope)

### Phase 4 — Executive Plans
**Deliverables:**
- Fully coordinated construction drawing set for public tender
- Tender technical specifications document (Especificaciones Técnicas) — required for licitación pública
- Bill of quantities (Catálogo de Conceptos) — line items for public bidding
- Construction timeline specification
- Quality control requirements specification

**Note:** The tender document set is more extensive than private project construction documents. It must be complete enough for any qualified contractor to bid without additional information from Oficio Taller.

### Phase 5 — Contractor Bidding (Licitación Pública)
**Deliverables:**
- Public tender document package (plans + specs + catálogo de conceptos + contract terms template)
- Pre-qualification criteria for contractor evaluation (if invited bid vs. open bid)
- Bid evaluation matrix and recommendation (for client's internal selection process)
- Technical clarification responses to bidder questions during tender period

**Important difference from private bidding:** Oficio Taller prepares the tender documents and evaluates bids technically. The actual public tender process — advertisement, submission, official opening, and contractor award — is managed by the government client per Ley de Obras Públicas.

### Phase 6 — Permitting
**Additional requirements for public projects:**
- Municipal building permit
- Civil protection review and approval (mandatory for public occupancy)
- Environmental impact assessment (if required by project scale or SEMARNAT)
- Government authority design review approval (if applicable to this institution)
- INAH review (if project is near historical monuments or protected zones — client confirms)

### Phase 7 — Construction Administration (often required for public projects)
**Note:** Government clients frequently require construction supervision as part of the professional services contract. Confirm scope inclusion with client.

> **Optional architectural supervision clause:** For public projects, construction administration is strongly recommended and often required by law. If excluded, the SOW states that compliance with construction specifications is the contractor's responsibility per the tender documents. Oficio Taller is available for periodic site visits under a separate consulting agreement.

---

## Landscape, Irrigation, Solar Scope

- **Landscape architecture:** Included if project scope includes exterior public spaces, plazas, or civic grounds. Coordinate with landscape architect. If building-only scope, explicitly excluded.
- **Irrigation:** Included if landscaped public grounds are in scope; explicitly excluded if no exterior grounds component.
- **Solar systems:** Explicitly excluded by default. If government client targets sustainability certification or energy independence requirements, add as Phase 3 optional item with explicit scope statement.

## Revision Assumptions

- Phase 1 — Conceptual Design: 2 rounds included. Government committee review revisions: up to 2 rounds included; additional rounds billed as change orders.
- Phase 2 — Architectural Design: 2 rounds included. Government authority-driven revisions: 2 rounds included; additional rounds billed as change orders (MXN 10,000/day).
- Phase 3 — Engineering Coordination: 1 round included.
- Phase 4 — Executive Plans + Tender Documents: 1 round included; clarification bulletins during tender period included (up to 5 bulletins).

## Local Contractor Cost Validation

Public bidding inherently validates pricing through competition. Pre-bid cost estimate comparison: Oficio Taller prepares a reference budget estimate before tender. After bids are received, bid amounts are compared to reference estimate; deviations > 20% are flagged for client review. Included in Phase 5 tender document preparation.

## Typical Timeline

| Phase | Typical Duration |
|---|---|
| Phase 1 — Conceptual Design + Government Review | 4–8 weeks |
| Phase 2 — Architectural Design + Authority Review | 8–14 weeks |
| Phase 3 — Engineering Coordination | 6–8 weeks |
| Phase 4 — Executive Plans + Tender Documents | 6–10 weeks |
| Phase 5 — Public Tender Process | 6–12 weeks (legally mandated minimum periods) |
| Phase 6 — Permitting (multi-authority) | 8–24 weeks |
| **Total design phases (excl. permitting + construction)** | 30–52 weeks |

Note: Public projects have longer timelines due to mandatory government review and tender periods.

---

## Payment Schedule

| Milestone | Name | Percentage | Amount (TBD) | Trigger Event |
|---|---|---|---|---|
| M1 | Contract Signing | 20% | — | Government contract formally executed |
| M2 | Concept Design Approved | 15% | — | Official written approval by government authority |
| M3 | Architectural Design Approved | 20% | — | Official written approval by government authority |
| M4 | Tender Documents Delivered | 25% | — | Complete tender package delivered to client |
| M5 | Construction Permits Obtained | 20% | — | All required permits and approvals obtained |

Note: Government payment processes are subject to institutional payment timelines. Oficio Taller reserves the right to pause work if invoices are not paid within 45 days of milestone completion (vs. 30 days for private clients).

---

## Responsibilities Matrix

| Deliverable | Responsible Party | Reviewed by |
|---|---|---|
| Architectural design | Oficio Taller | Government client + review authorities |
| Tender documents (plans + specs + catálogo) | Oficio Taller | Government client |
| Public tender process | Government client | Law (Ley de Obras Públicas) |
| Contractor award decision | Government client | — |
| Structural engineering | Structural engineer | Oficio Taller + government reviewer |
| MEP engineering | MEP engineers | Oficio Taller coordinates |
| Environmental assessment | Environmental consultant (if required) | SEMARNAT |
| INAH review (if applicable) | Government client | INAH |

---

## Standard Exclusions
1–8: Same as standalone residential, plus:
9. Public tender management (advertisement, bid receipt, official opening) — government client responsibility
10. Permit and government approval fees
11. Environmental impact study fees (if required — separate consultancy)
12. INAH research or historical documentation (if applicable)
13. Legal advice on public procurement process
14. Construction cost overrun from contractor bid exceeding budget (Oficio Taller provides estimate; final cost set by tender)

---

## Project-Type Clauses

```json
{
  "project_type_clauses": [
    {
      "clause": "civic_procurement",
      "title": "Public Procurement Compliance",
      "text": "This project is subject to Mexican public procurement law (Ley de Obras Públicas y Servicios Relacionados con las Mismas, LOPSRM). Oficio Taller's professional services contract with the government client was awarded through the applicable procurement process. Contractor selection for construction must follow public tender rules administered by the client institution. Oficio Taller prepares tender documents; it does not participate in the contractor selection decision."
    },
    {
      "clause": "public_bidding_compliance",
      "title": "Public Bidding Documents",
      "text": "The construction documents produced by Oficio Taller for this project include a Catálogo de Conceptos (bill of quantities) and Especificaciones Técnicas suitable for public tender. These documents are prepared to allow any qualified contractor to submit a comparable bid. Ambiguities discovered during the tender period will be resolved through official clarification bulletins issued by the government client."
    },
    {
      "clause": "government_approval_timeline",
      "title": "Government Review Timelines",
      "text": "Review and approval timelines set by government authorities (design committees, civil protection, INAH, SEMARNAT) are outside Oficio Taller's control. Delays caused by government review processes do not constitute a delay by Oficio Taller. Payment milestone triggers are based on deliverable completion by Oficio Taller, not on government agency response timelines."
    },
    {
      "clause": "optional_supervision",
      "title": "Optional Architectural Construction Administration",
      "text": "Architectural construction administration is an optional service for this public project. If included, supervision scope, site visit frequency, and reporting format are defined in a separate exhibit to this SOW. If excluded, contractor conformance with tender specifications is governed by the construction contract between the government client and the contractor. Oficio Taller bears no liability for construction quality if supervision is not included."
    },
    {
      "clause": "esignature",
      "title": "Electronic Signature",
      "text": "This document is valid when signed electronically under Mexican federal law (NOM-151-SCFI), where accepted by the government institution. If the institution requires physical signature per their internal policy, Oficio Taller will provide a physical original."
    }
  ]
}
```

---

## Tomás Instructions
- Set `project_type_clauses` to include `civic_procurement`, `public_bidding_compliance`, `government_approval_timeline`, `optional_supervision` verbatim
- Use public civic payment schedule (20/15/20/25/20)
- Add catálogo de conceptos and Especificaciones Técnicas to Phase 4 deliverables in scope_phases
- Note construction supervision is often required — check state.json or seed data; if not specified, include as optional with separate pricing note
```

- [ ] **Step 2: Validate**

```bash
f=docs/templates/sow/sow-public-civic.md
grep -q "project_type_clauses" $f && echo "PASS: type clauses" || echo "FAIL"
grep -q "civic_procurement" $f && echo "PASS: procurement clause" || echo "FAIL"
grep -q "public_bidding_compliance" $f && echo "PASS: bidding clause" || echo "FAIL"
grep -q "optional_supervision" $f && echo "PASS: supervision clause" || echo "FAIL"
grep -q "Payment Schedule" $f && echo "PASS: payment" || echo "FAIL"
grep -q "Exclusions" $f && echo "PASS: exclusions" || echo "FAIL"
grep -q "Responsibilities" $f && echo "PASS: responsibilities" || echo "FAIL"
grep -qi "landscape" $f && echo "PASS: landscape" || echo "FAIL"
grep -qi "irrigation" $f && echo "PASS: irrigation" || echo "FAIL"
grep -qi "solar" $f && echo "PASS: solar" || echo "FAIL"
grep -q "Revision Assumptions\|Revision assumptions" $f && echo "PASS: revision assumptions" || echo "FAIL"
grep -q "Typical Timeline" $f && echo "PASS: timeline" || echo "FAIL"
grep -q "cost validation\|benchmarks\|reference budget" $f && echo "PASS: cost validation" || echo "FAIL"
```

Expected: all 13 PASS

---

### Task 11: Commit all SOW templates + final validation

- [ ] **Step 1: Final cross-template validation — all 5 templates have required sections**

```bash
for f in docs/templates/sow/*.md; do
  echo "--- $f ---"
  grep -q "project_type_clauses" "$f" && echo "PASS: type clauses" || echo "FAIL: type clauses"
  grep -qi "landscape" "$f" && echo "PASS: landscape" || echo "FAIL: landscape"
  grep -qi "irrigation" "$f" && echo "PASS: irrigation" || echo "FAIL: irrigation"
  grep -qi "solar" "$f" && echo "PASS: solar" || echo "FAIL: solar"
  grep -q "Typical Timeline" "$f" && echo "PASS: timeline" || echo "FAIL: timeline"
  grep -q "Revision assumptions\|Revision Assumptions" "$f" && echo "PASS: revision assumptions" || echo "FAIL: revision assumptions"
  grep -q "cost validation\|benchmarks\|reference budget" "$f" && echo "PASS: cost validation" || echo "FAIL: cost validation"
  grep -q "esignature" "$f" && echo "PASS: esignature" || echo "FAIL: esignature"
done
```

Expected: all checks PASS for all 5 templates (40 total PASS lines)

- [ ] **Step 2: Final cross-rubric validation — all 4 rubrics have Auto-Fail section**

```bash
for f in tests/rubrics/budget.md tests/rubrics/project-schedule.md tests/rubrics/permit-status.md tests/rubrics/vera-site-status.md; do
  grep -q "Auto-Fail" "$f" && echo "PASS: $f" || echo "FAIL: $f"
done
```

Expected: all 4 PASS

- [ ] **Step 3: Commit all SOW templates**

```bash
git add docs/templates/sow/
git commit -m "feat: add 5 SOW templates — standalone residential, residential-in-development, commercial hotel, health center, public civic"
```

Expected: commit succeeds, 5 files in docs/templates/sow/

---

## Summary

After completing all tasks, the following files will exist:

**Rubrics (4 new):**
- `tests/rubrics/budget.md` — Bruno Segment D (required fields: project_name, client_name, milestone_name, amount, payment_instructions, currency, line_items)
- `tests/rubrics/project-schedule.md` — Pablo (required fields: phases, milestone_dates, dependencies)
- `tests/rubrics/permit-status.md` — Paco (required fields: submitted_at, jurisdiction, status, corrections, approved_at)
- `tests/rubrics/vera-site-status.md` — Vera Segment C (Asana-only; no JSON schema; scored from raw text output)

**SOW Templates (5 new):**
- `docs/templates/sow/sow-standalone-residential.md` — 5 payment milestones at 30/20/25/15/10%
- `docs/templates/sow/sow-residential-in-development.md` — adds HOA + covenant clauses
- `docs/templates/sow/sow-commercial-hotel.md` — 5 milestones at 25/15/20/25/15%; brand standards + hospitality compliance
- `docs/templates/sow/sow-commercial-health-center.md` — 5 milestones at 25/15/20/25/15%; COFEPRIS compliance; M5 = COFEPRIS permit
- `docs/templates/sow/sow-public-civic.md` — 5 milestones at 20/15/20/25/20%; public procurement + bidding compliance

**Testable after:** `/test-segment C TC-001` (cost basis chain) and `/test-segment D TC-001` (SOW generation by Tomás)
