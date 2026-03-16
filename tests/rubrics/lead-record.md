# Rubric: Lead Record
**Agent:** Lupe
**Deliverable:** Asana lead task created on inbound message receipt

## Schema (Execution Agent validates — pass/fail)
Required fields: source_channel, category, received_at, summary, status

## Quality Dimensions (Decision Gate Agent scores 1–5)

**Completeness (1–5)**
5: All custom fields populated, raw message stored verbatim in task body
3: All fields present but raw message summarized not preserved verbatim
1: Any required field missing

**Accuracy (1–5)**
5: source_channel exactly matches inbound platform; category correctly classified
3: source_channel correct, category could be argued either way
1: Wrong platform identified or wrong category

**Clarity (1–5)**
5: Summary in task body is immediately scannable — project type, location, client name visible
3: Summary present but requires reading to understand context
1: Summary is absent or a raw paste with no structure

**State Sync (1–5)**
5: Asana task created with status = "new", correct section, correct project tag
3: Task created but in wrong section or missing tag
1: No Asana task created

**Timing (1–5)**
5: Task created within expected window after inbound message receipt
3: Minor delay but task exists
1: Task missing or significantly delayed

**Decision Readiness (1–5)**
5: Lead record provides sufficient structured data for Marcela's review (all required fields populated, quality signal clear)
3: Most fields present but one supporting field missing or unclear
1: Core qualifying fields absent — Marcela cannot make an informed decision

## Auto-Fail Conditions
- No Asana task created
- received_at field missing
- status field absent
- Legitimate lead classified as spam (false positive) — Critical failure
