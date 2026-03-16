# Rubric: Area Program
**Agent:** Ana
**Deliverable:** Room-by-room area matrix (Segment C)

## Schema (Execution Agent validates — pass/fail)
Required fields: spaces (array with name, qty, size_sqm per entry), total_sqm, assumptions

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: Every space from seed data program has name, quantity, and size in sqm; special features that are programmed spaces (pool, rooftop) included with size
3: All spaces present but one or two missing size values
1: Total sqm missing, or any programmed space has no size

**Accuracy (1–5)**
5: Total programmed sqm correctly calculated and matches sum of all spaces
3: Total present but off by minor rounding
1: Total missing or significantly wrong

**Clarity (1–5)**
5: Matrix is readable as standalone document; no conversation context needed
3: Matrix understandable but requires some context
1: Matrix not readable without back-reference to client conversation

**State Sync (1–5)**
5: Asana state updated to area_program_in_progress then area_program_confirmed
3: State partially updated
1: No Asana update

**Timing (1–5)**
5: Area program delivered within expected window after fit approval
3: Minor delay
1: Not delivered or excessive delay

**Decision Readiness (1–5)**
5: Assumptions documented where client input was incomplete; Marcela can review with full context
3: Assumptions partially documented
1: No assumptions section; Marcela cannot evaluate validity of program

## Auto-Fail Conditions
- total_sqm missing
- Any programmed space has no size value
- No assumptions section
