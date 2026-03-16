# TC-008 — Edge: Site Complications

**Type:** commercial_hotel
**Complexity:** Edge case — hydrology blocker at activation gate
**Seed data:** `tests/data/TC-008-seed.json`

## Scenario
David Chen has a 15,000sqm East Cape property with a stream through it.
Sol identifies that a hydrologic study is required (6-week timeline).
The activation gate is blocked until the study arrives.

## Key Verification Points
- Sol requests BOTH topo AND hydrologic study (stream present, Segment C)
- Blocker logged in Asana: activation_delayed_by_hydrology
- Vera holds activation gate — does NOT activate until study received
- site_data_pending state persists until hydrology resolved

## Expected Final State
project_activated (once hydrology study received and activation prerequisites met)

## Edge Conditions
- Site data blocker must be logged explicitly — not silently waited on
- Activation must not proceed until ALL three prerequisites satisfied
