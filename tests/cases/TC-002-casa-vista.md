# TC-002 — Casa Vista

**Type:** residential_in_development
**Complexity:** Standard with HOA restrictions
**Seed data:** `tests/data/TC-002-seed.json`

## Scenario
Patricia Reyes — referral contact — wants a 337sqm home in a private
residential development in San José del Cabo. The development has strict
covenants: contemporary style only, natural stone/stucco facade, 7m height
limit.

## Key Verification Points
- Tomás applies `residential_in_development` template (Segment D)
- SOW includes HOA coordination clause and covenant review clause
- hoa_details from seed data referenced in scope
- Area program respects height limit implications for massing

## Expected Flow
- **Segment A:** Lupe qualifies lead, Celia routes to Elena (DG-01 approve), Elena sends intro email
- **Segment B:** Elena sends discovery questionnaire, Ana conducts discovery call, Sol completes site readiness (no hydrology concerns)
- **Segment C:** Ana produces area program (337sqm, residential_in_development), Ana produces cost basis, Tomás produces SOW with HOA coordination clause
- **Segment D:** Legal review (Alejandra), Proposal generation (Bruno), client communication (communication logged)
- **Segment E:** Concept design (Andrés), Celia routes DG-07 to Felipe (approve)
- **Segment F:** Architectural design (Felipe), engineering (Emilio), budget alignment (Bruno)
- **Segment G:** Executive plans (Hugo), contractor bid comparison (Ofelia — multiple bids)
- **Segment H:** Construction oversight or close (Vera), controller invoice (Controller), tax filing (Tax)
- **Segments I–J:** Standard completion

## Expected Final State
closed
