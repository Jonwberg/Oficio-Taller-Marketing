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
