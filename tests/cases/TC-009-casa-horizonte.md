# TC-009 — Casa Horizonte

**Type:** standalone_residential
**Complexity:** Standard with coastal site conditions and multi-disciplinary collaborators
**Seed data:** `tests/data/TC-009-seed.json`

## Scenario

Familia Reyes-Montoya contacts via Instagram with a 3,000sqm Pacific-facing plot in
Cerritos, BCS — at the scrub-to-sand edge. They want a 320sqm residence organized
around the horizon as a living condition, not a view. Design-engaged client.
Budget $600K–$900K USD. Open to landscape and interior design referrals.

## Site Conditions

Coastal Pacific site. Strong prevailing wind, salt air, native coastal scrub. Flat to
gently sloping. No hydrology concerns. Requires topographic survey, coastal zone
permit, and wind load study before construction can begin.

## Expected Flow

- **Segment A:** Lupe classifies as project_inquiry, creates lead record, routes to Elena
- **Segment B:** Elena sends questionnaire, schedules discovery call, fit approved (design-engaged, realistic budget)
- **Segment C:** Ana produces area program (320sqm, 10 spaces), identifies coastal zone permit as required document; Sol submits site readiness request noting coastal_zone_permit and wind_load_study as required; `site_data_complete: true` set by Sol; `site_docs_complete` set manually by operator when documents received
- **Segment D:** Tomás generates SOW with `standalone_residential` template; payment schedule at 40/30/30; Bruno produces budget within range; Renata writes proposal; Legal reviews; Rosa sends DG-06; Vera sends DG-04 (SOW review) and DG-05 (proposal review)
- **Segment E:** Pablo builds schedule with coastal permit lead time included as a phase dependency; Vera activates after all three prerequisites met
- **Segment F:** Andrés produces concept package with horizon-axis orientation documented; DG-07 dispatched; Felipe produces architectural drawings with wind/salt material notes; DG-08 dispatched
- **Segment G:** Emilio produces engineering package with structural (wind load), electrical, lighting, water, and solar systems; Bruno confirms budget alignment
- **Segment H:** Hugo produces executive plans; DG-10 dispatched
- **Segment I:** Ofelia collects bids (multiple); contractor selected; DG-11 dispatched; Paco submits coastal zone permit application; on approval dispatches Vera
- **Segment J:** Construction tracking; Controller invoices at each milestone; Tax files at project close; marketing pipeline dispatched

## Key Verification Points

- `standalone_residential` SOW template applied (Segment D)
- Sol's site readiness request includes `coastal_zone_permit` and `wind_load_study` in required_documents
- `site_data_complete` set by Sol when report is written; `site_docs_complete` remains null until operator sets manually
- Vera does NOT send DG-03 until both `area_program_complete` AND `site_data_complete` are true AND `awaiting_gate` is null
- Emilio includes `solar` in systems_status (it is in project scope via special_features)
- Paco sets `permit_status` in Asana (not `project_state`) when logging permit progress
- Controller dispatches Tax on final milestone (not Vera)
- All 11 Celia payload fields present at every Marcela gate; `route_to` field (not `routed_to`)

## Edge Conditions

- Coastal permit adds lead time to Segment I — Paco's `permit-status.json` may cycle through `pending_corrections` before `approved`
- If coastal zone permit is delayed past schedule, `corrections` array in `permit-status.json` must be populated (not left empty)
- Wind load study affects structural engineering inputs in Segment G — Emilio should note structural requirements informed by coastal conditions

## Expected Final State

closed
