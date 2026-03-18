# Controller — Milestone 2: Concept Approved
**run_id:** 2026-03-16-TC-009
**agent:** Controller
**milestone_number:** 2
**milestone_name:** Concept Approved
**final_milestone:** false
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**timestamp:** 2026-03-16
**TC-009 SPECIAL:** M2 write failure simulation — backup/recovery pattern test

---

## Step 1: Read context

Read `state.json`:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- client_name: Familia Reyes-Montoya
- project_type: standalone_residential
- tasks.invoice: null

Read `scope-of-work.json` payment_schedule:
- M2 — Concept Design Approved: $27,000 USD (30%) — trigger: Client written approval of Phase 1 conceptual design

Read `project-schedule.json` milestone_dates:
- M2_concept_approved: 2026-04-17

Milestone in context: milestone_name = "Concept Approved", milestone_number = 2
SOW match: M2 — Concept Design Approved — $27,000 USD
Due date: M2_concept_approved = 2026-04-17

---

## Step 2: Calculate running_total

Previous `invoice.json` exists (from M1 Controller).
Read previous invoice.json:
- running_total: $36,000 USD (M1)

running_total (M2) = $36,000 + $27,000 = **$63,000 USD**

---

## Step 3: Pre-write check — backup

Check: does `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json` exist?
→ YES — M1 invoice.json exists.

**Backing up:** copy invoice.json → invoice-previous.json
`invoice-previous.json` written successfully. Backup complete.

---

## Step 4a: FIRST WRITE ATTEMPT — SIMULATED FAILURE

Attempting to write invoice.json for M2...

**LOG: WRITE_FAILED** — Simulated write failure on M2 first attempt (TC-009 specific test scenario).

Per protocol:
- invoice-previous.json is RETAINED (not deleted)
- WRITE_FAILED logged
- Controller re-dispatched to retry

invoice-previous.json retained: ✓ (contains M1 invoice data as safety backup)

**→ RE-DISPATCH: Controller M2 retry initiated**

---

## Step 4b: RETRY WRITE — SUCCESS

Retry attempt for M2 invoice.json write...

Writing to: `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json`

```json
{
  "project_name": "Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México",
  "client_name": "Familia Reyes-Montoya",
  "milestone_name": "M2 — Concept Approved",
  "amount": 27000,
  "due_date": "2026-04-17",
  "payment_instructions": "Bank transfer to Oficio Taller. Bank: [BANK_NAME]. CLABE: [CLABE — TO BE CONFIGURED IN .env]. Reference: PRJ-2026-0316-familia-reyes-montoya-M2.",
  "currency": "USD",
  "running_total": 63000
}
```

**WRITE: SUCCESS** (retry)

---

## Step 5: Post-write — delete backup

Write succeeded on retry.
Check: does `projects/PRJ-2026-0316-familia-reyes-montoya/invoice-previous.json` exist?
→ YES — deleting invoice-previous.json.

**invoice-previous.json DELETED.** Backup cleanup complete.

---

## Step 6: Update Asana

```bash
python entrega/asana_client.py update_field \
  --task_id null \
  --field project_state \
  --value invoice_sent
```

**LOG: ASANA_UNAVAILABLE** — tasks.invoice is null; continuing.

```bash
python entrega/asana_client.py add_comment \
  --task_id null \
  --agent Controller \
  --body "Invoice generated: M2 — Concept Approved. Amount: 27000 USD. Running total: 63000. Due: 2026-04-17."
```

**LOG: ASANA_UNAVAILABLE** — continuing.

---

## Step 7: Check final_milestone

final_milestone: false → Do NOT dispatch Tax or marketing. Stop here.

---

## Schema Validation (Final Written Invoice)

| Field | Value | Status |
|-------|-------|--------|
| project_name | Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México | PASS |
| client_name | Familia Reyes-Montoya | PASS |
| milestone_name | M2 — Concept Approved | PASS |
| amount | 27000 | PASS |
| due_date | 2026-04-17 | PASS |
| payment_instructions | Present with CLABE placeholder | PASS |
| currency | USD | PASS |
| running_total | 63000 | PASS (36000 + 27000) |
| CLABE present | [CLABE — TO BE CONFIGURED IN .env] | PASS (placeholder) |
| All 8 required fields | Complete | PASS |

## TC-009 Recovery Pattern Validation

| Check | Result | Status |
|-------|--------|--------|
| M2 first write attempt | WRITE_FAILED (simulated) | PASS — failure detected |
| invoice-previous.json retained on failure | YES — backup retained | PASS |
| WRITE_FAILED logged | YES | PASS |
| Re-dispatch triggered | YES — Controller M2 retry | PASS |
| M2 retry write | SUCCESS | PASS |
| invoice-previous.json deleted after successful retry | YES — deleted | PASS |
| running_total on successful write | 63000 (36000 + 27000) | PASS |
