# TC-005 — Biblioteca Municipal

**Type:** public_civic
**Complexity:** Civic — public procurement rules
**Seed data:** `tests/data/TC-005-seed.json`

## Scenario
Municipality of Los Cabos commissioning a 2,000sqm public library via
official public works procurement process. Budget approved at government
level. Compliance with obra pública guidelines required.

## Key Verification Points
- Tomás applies `public_civic` template with civic procurement and public bidding clauses
- Client is institutional — fit assessment adjusts for organizational decision-making (not individual)
- Permit process expected to be longer (public project)
- Segment I (bid comparison): Ofelia must collect a minimum of two formal bids per obra pública procurement rules (`procurement_type: "obra_publica"` in seed); single-bid outcome must be flagged as a Marcela decision gate rather than accepted as standard result

## Expected Final State
closed
