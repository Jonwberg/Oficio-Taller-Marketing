# TC-001 — Casa Moderna

**Type:** standalone_residential
**Complexity:** Standard — happy path
**Seed data:** `tests/data/TC-001-seed.json`

## Scenario
Carlos Mendoza contacts via Instagram looking to design a 250sqm modern
residence in Los Cabos on a flat 2,500sqm site. Design-engaged client with
realistic budget ($300K–$500K). No site complications. Supervisor selected.

## Expected Flow
- Segment A: Lupe classifies as project_inquiry, creates lead record
- Segment B: Elena sends questionnaire, schedules meeting, fit approved
- Segment C: Ana produces area program (250sqm), cost basis prepared; Sol requests topo only (flat site)
- Segment D: Tomás generates SOW with standalone_residential template; architect approves both gates
- Segment E: All three prerequisites met simultaneously; Pablo builds timeline
- Segment F: Andrés produces concept package; Marcela approves (DG-07 = Pass to Agent test point)
- Segment G: Emilio completes all systems; Bruno confirms budget aligned
- Segment H: Hugo produces executive plans; Marcela approves
- Segment I: Ofelia collects 2+ bids; contractor selected; Paco submits permit
- Segment J: Construction starts; supervision active; project closes; Controller invoices; Tax files

## Key Verification Points
- standalone_residential SOW template applied (Segment D)
- No hydrologic study requested (flat site, Segment C)
- Pass to Agent simulated at DG-07 — Celia sets concept_in_progress, updates assigned_agent only
- All 11 Celia payload fields present at every Marcela gate
- route_to field (not routed_to) in payload

## Expected Final State
closed

## Edge Conditions
None — this is the baseline happy path used to calibrate rubric scoring.
