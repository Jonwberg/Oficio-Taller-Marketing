# Segment C — Sol — Site Readiness

## Agent: Sol
## Project: PRJ-2026-0317-tc005-biblioteca-municipal
## Triggered by: DG-02 Approve (parallel with Ana)

---

Step 1: Read state.json and lead-summary.json.
- Site: flat municipal land, no hydrology concerns (from seed data)
- Location: Cabo San Lucas, BCS
- Project type: public_civic

Step 2: Determine required documents.
- Always required: Levantamiento Topográfico
- public_civic (commercial/public) requires: Estudio de Mecánica de Suelos
- Government land: Municipal title/authorization required
- No hydrology concerns → no hydrologic assessment required
- No HOA (not residential_in_development)

Step 3: Send document request to client.
GMAIL_UNAVAILABLE: would send site document request to r.salinas@obras-publicas-loscabos.gob.mx

Step 4: Written site-readiness-report.json
- 3 required documents
- current_status: documents_requested
- blockers: []

Step 5: ASANA_UNAVAILABLE: would update site readiness status

Step 6: Set site_data_complete = true
Written state.json

Step 7: Dispatch Vera (mode: site_status_update)
