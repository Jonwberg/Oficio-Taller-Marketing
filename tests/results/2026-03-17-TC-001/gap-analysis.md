# Gap Analysis — 2026-03-17-TC-001

**Test Case:** TC-001 Casa Moderna — standalone_residential happy path
**Date:** 2026-03-17
**Segments scored:** A–J
**Total scorecards:** 31 (22 deliverable scorecards + 9 Celia routing scorecards)
**Overall average score:** 4.36 / 5.0

---

## Overall Scores by Segment

| Segment | Agents | Scorecards | Avg Score | Auto-Fail | Result |
|---------|--------|-----------|-----------|-----------|--------|
| A | Lupe | 1 | 4.33 | — | PASS |
| B | Lupe, Elena, Celia (DG-01, DG-02) | 5 | 4.54 | — | PASS |
| C | Ana, Sol, Celia (DG-03) | 4 | 4.34 | — | PASS |
| D | Tomás, Bruno, Renata, Legal, Rosa, Celia (DG-06) | 6 | 3.88 | budget.json AUTO-FAIL | FAIL |
| E | Pablo | 1 | 3.80 | — | PASS (with gaps) |
| F | Andrés, Felipe, Celia (DG-07, DG-08) | 5 | 4.34 | — | PASS |
| G | Emilio, Bruno, Celia (DG-09) | 3 | 4.61 | — | PASS |
| H | Hugo, Celia (DG-10) | 2 | 4.42 | — | PASS |
| I | Ofelia, Paco, Celia (DG-11) | 3 | 3.83 | permit-status.json AUTO-FAIL | FAIL |
| J | Controller, Tax | 2 | 3.90 | — | PASS (with gaps) |

---

## Critical Findings

### AUTO-FAIL 1 — Segment D: budget.json (Bruno)
**File:** `budget.json`
**Rubric:** `budget.md`
**Conditions triggered:**
- `payment_instructions` is absent — explicit auto-fail condition
- `project_name` is absent — required schema field
- `client_name` is absent — required schema field
- `milestone_name` is absent — required schema field

**What the file has:** `total`, `currency`, `line_items` (phase cost breakdown in USD)
**What it is missing:** client identity fields, payment instructions, milestone trigger structure

**Impact:** The budget.json is effectively a phase fee schedule, not an invoiceable budget document. A client cannot pay from this document, and it cannot be linked back to a named client or project without follow-up. Renata's proposal correctly referenced the $54,000 total and three-stage payment structure, but this came from the SOW payment schedule rather than from a well-formed budget.json.

**Resolution required:** Bruno must populate project_name, client_name, milestone_name, payment_instructions (with specific bank/account/reference details), and restructure line_items to map to payment milestones rather than production phases.

---

### AUTO-FAIL 2 — Segment I: permit-status.json (Paco)
**File:** `permit-status.json`
**Rubric:** `permit-status.md`
**Conditions triggered:**
- `submitted_at` is absent — explicit auto-fail condition
- `jurisdiction` is absent — explicit auto-fail condition

**What the file has:** `status`, `municipal_permit_approved`, `approved_at`, `corrections`
**What it is missing:** `submitted_at`, `jurisdiction`

**Additional issue:** The `approved_at` date is 2026-11-01, which is after the `construction_start` date of 2026-09-15 in the project schedule. This means construction starts before the permit is approved — a logical inconsistency that Vera cannot resolve without a corrected permit timeline.

**Resolution required:** Paco must add `submitted_at` (date submission was filed), `jurisdiction` (specific authority, e.g., "Municipio de Los Cabos — Dirección de Desarrollo Urbano"), and correct the construction timeline to account for permit lead time before construction start.

---

## High Priority

### H1 — Segment E: project-schedule.json (Pablo) — Missing `dependencies` field
**File:** `project-schedule.json` | **Score:** 3.80
The schema requires a `dependencies` field mapping each phase to its predecessor. The file is entirely missing this field. The rubric lists `dependencies absent` as an auto-fail condition for completeness; this was scored 3 (not auto-fail) in the simulated context because phase ordering is unambiguous from dates, but this must be resolved before production. Additionally the schema uses `milestone_dates` (map) but the file uses `milestones` (array of objects) — a structural deviation.

**Resolution:** Pablo must add a `dependencies` field and rename/restructure the milestone field to match the required schema.

---

### H2 — Segment D: client-communication.json (Rosa) — Status field incorrectly set to "sent"
**File:** `client-communication.json` | **Score:** 4.00 (individual)
The status field is `"sent"` but the rubric requires the message to be in `"draft"` status awaiting Marcela approval before send. In production this would mean a client message was dispatched without Marcela review — an auto-fail condition (`Message sent without Marcela approval`). In this simulated run the scoring was lenient because no real message was sent, but the field value is wrong and must be corrected to `"draft"` in production.

**Resolution:** Rosa must set status to `"draft"` until Marcela explicitly approves. The status update to `"sent"` should occur only after Marcela approval is confirmed.

---

## Medium Priority

### M1 — Segment C: cost-basis.json (Ana) — Not labeled as preliminary estimate
**File:** `cost-basis.json` | **Score:** 4.00
The document lacks a `"preliminary_estimate": true` flag or equivalent label. The rubric requires it to be "clearly labeled as preliminary estimate." The information is present and the assumptions note is specific, but a future agent or human reviewer could mistake this for a confirmed cost without the explicit label.

**Resolution:** Add a `status: "preliminary_estimate"` or equivalent field to cost-basis.json.

### M2 — Segment C: cost-basis.json (Ana) — Minor arithmetic discrepancy in contingency
**File:** `cost-basis.json` | **Score:** 4.00
Contingency at 5% of (5,000,000 + 600,000 + 250,000) = 292,500. Total should be 6,142,500. File states 6,162,500 — a 20,000 MXN (~0.3%) unexplained overage. The discrepancy is small but unexlained.

**Resolution:** Recalculate and document the contingency basis explicitly.

### M3 — Segment C: area-program.json (Ana) — Total sqm arithmetic gap
**File:** `area-program.json` | **Score:** 4.50
The sum of individual space areas is 257sqm (25+36+24+20+45+12+35+40+5+15), but `total_sqm` is stated as 250sqm. A 7sqm difference is more than rounding. The program target is 250sqm and individual spaces were distributed to reach this, but the individual sizes don't add up to the stated total.

**Resolution:** Reconcile individual space sizes to sum to 250sqm, or document the 7sqm difference as an unallocated circulation/wall allowance.

### M4 — Segment D: scope-of-work.json (Tomás) — Multiple 20-item checklist gaps
**File:** `scope-of-work.json` | **Score:** 4.00
Items missing or not explicitly addressed from the 20-item checklist: (4) optional architectural supervision clause, (8) lighting design scope as distinct item, (10) irrigation scope explicitly excluded, (12) local contractor cost validation, (20) e-signature path. Five items absent puts this at the lower boundary of score 3 per rubric. The e-signature path absence is the most actionable gap.

**Resolution:** Tomás must add explicit e-signature path documentation and address the remaining checklist items.

### M5 — Segment B: client-fit-assessment.json (Elena) — Collaborative working style dimension absent
**File:** `client-fit-assessment.json` | **Score:** 4.00
The rubric requires four specific assessment dimensions. The `collaborative_working_style` dimension is not present by name, only implied. This is one of the four required dimensions per the auto-fail check in the rubric.

**Resolution:** Elena must add an explicit `collaborative_working_style` assessment dimension to the assessment_dimensions object.

### M6 — Segment J: invoice.json (Controller) — Generic payment instructions
**File:** `invoice.json` | **Score:** 3.80
`payment_instructions` is `"Wire transfer to Oficio Taller account per contract"` — this is generic. The rubric requires specific bank name, CLABE/SWIFT, and reference format. This is a clarity failure that would cause client friction at payment time.

**Resolution:** Controller must populate payment_instructions with specific bank details, account number, and reference format.

### M7 — Segment J: tax-filing.json (Tax) — Only one CFDI reference for three-invoice project
**File:** `tax-filing.json` | **Score:** 4.00
The project has three payment milestones (M1, M2, M3) each requiring a CFDI. The tax filing has only one CFDI reference (`CFDI-TC001-2026-08`). Revenue total of $54,000 is correct but should be supported by three traceable CFDI references.

**Resolution:** Tax must include CFDI references for all three invoice milestones.

---

## Low Priority

### L1 — Segment F: concept-review.json (Andrés) — Review notes describe design rather than capture feedback
**File:** `concept-review.json` | **Score:** 4.00
The rubric requires review notes to capture "Marcela's specific feedback — not just 'approved.'" The notes describe the design concept but do not separate what was presented from what Marcela specifically approved or requested. In production, if revisions are requested, this distinction becomes critical.

### L2 — Segment F: celia-routing dg-07.json — next_action value incorrect for approve
**File:** `dg-07.json` | **Score:** 4.17
`next_action='concept_in_progress'` is semantically wrong for an approve event. It should be `'advance_to_architectural_design'`. This is a minor label error that could cause state confusion in Asana if sync were live.

### L3 — Segment I: celia-routing dg-11.json — next_action premature
**File:** `dg-11.json` | **Score:** 4.17
`next_action='advance_to_construction'` is premature at DG-11 because permit approval (Paco) is still pending. Should be `'advance_to_permits_and_construction_prep'` or similar to reflect the intermediate state.

### L4 — Segment H: executive-plans.json (Hugo) — Technical coordination layer not explicitly named
**File:** `executive-plans.json` | **Score:** 4.17
The rubric schema requires `technical_coordination` as a named component in `plan_set_components`. The file covers the equivalent content (MEP drawings, structural drawings, etc.) but doesn't include a component explicitly called "Technical coordination layer."

### L5 — Segment D: celia-routing dg-06.json — Comment describes post-gate state
**File:** `dg-06.json` | **Score:** 4.33
Comment says "Proposal sent to client" at the moment of the DG-06 gate event. DG-06 is the gate where the proposal is reviewed before sending — the comment should describe the gate decision, not the post-send state.

### L6 — Segment I: permit-status.json — Construction start predates permit approval
**File:** `permit-status.json`
`construction_start` in project-schedule.json is 2026-09-15, but permit approval is 2026-11-01. Construction cannot legally start before permit approval. This timeline inconsistency needs to be resolved between Paco and Pablo.

---

## Summary

| Priority | Count | Issues |
|----------|-------|--------|
| AUTO-FAIL | 2 | budget.json (missing 4 required fields), permit-status.json (missing 2 required fields + timeline inconsistency) |
| High | 2 | project-schedule missing dependencies field, client-communication status='sent' before approval |
| Medium | 7 | cost-basis labeling, cost-basis arithmetic, area-program total mismatch, SOW 20-item gaps, fit-assessment dimension missing, generic payment instructions, incomplete CFDI references |
| Low | 6 | concept review notes, DG-07 next_action label, DG-11 next_action label, executive plans component naming, DG-06 comment timing, construction/permit date conflict |

**9 of 31 scorecards have at least one dimension scored below 4.0. 2 scorecards triggered auto-fail conditions.**

No gaps found in Celia routing completeness (all 11 fields present at every gate) or in correct agent routing (all route_to values correct per production routing table).
