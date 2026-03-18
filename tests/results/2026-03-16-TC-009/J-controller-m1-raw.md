# Controller — Milestone 1: Contract Signed
**run_id:** 2026-03-16-TC-009
**agent:** Controller
**milestone_number:** 1
**milestone_name:** Contract Signed
**final_milestone:** false
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**timestamp:** 2026-03-16

---

## Step 1: Read context

Read `state.json`:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- client_name: Familia Reyes-Montoya
- project_type: standalone_residential
- tasks.invoice: null

Read `scope-of-work.json` payment_schedule:
- M1 — Contract Signing: $36,000 USD (40%) — trigger: Signed SOW + first payment received
- M2 — Concept Design Approved: $27,000 USD (30%)
- M3 — Executive Plans Approved: $27,000 USD (30%)

Read `project-schedule.json` milestone_dates:
- M1_contract_signing: 2026-03-16
- M2_concept_approved: 2026-04-17
- M3_executive_plans_approved: 2026-09-04

Milestone in context: milestone_name = "Contract Signed", milestone_number = 1
SOW match: M1 — Contract Signing — $36,000 USD
Due date: M1_contract_signing = 2026-03-16

---

## Step 2: Calculate running_total

No previous `invoice.json` exists for this project.

running_total = $36,000 USD (first invoice; no prior invoices)

---

## Step 3: Pre-write check — backup

Check: does `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json` exist?
→ NO — no previous invoice.json exists for this project.
→ No backup needed. Proceeding to write.

---

## Step 4: Write invoice.json

Writing to: `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json`

```json
{
  "project_name": "Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México",
  "client_name": "Familia Reyes-Montoya",
  "milestone_name": "M1 — Contract Signed",
  "amount": 36000,
  "due_date": "2026-03-16",
  "payment_instructions": "Bank transfer to Oficio Taller. Bank: [BANK_NAME]. CLABE: [CLABE — TO BE CONFIGURED IN .env]. Reference: PRJ-2026-0316-familia-reyes-montoya-M1.",
  "currency": "USD",
  "running_total": 36000
}
```

**WRITE: SUCCESS**

---

## Step 5: Post-write — delete backup

Check: does `projects/PRJ-2026-0316-familia-reyes-montoya/invoice-previous.json` exist?
→ NO — no backup existed. Nothing to delete.

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
  --body "Invoice generated: M1 — Contract Signed. Amount: 36000 USD. Running total: 36000. Due: 2026-03-16."
```

**LOG: ASANA_UNAVAILABLE** — continuing.

---

## Step 7: Check final_milestone

final_milestone: false → Do NOT dispatch Tax or marketing. Stop here.

---

## Schema Validation

| Field | Value | Status |
|-------|-------|--------|
| project_name | Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México | PASS |
| client_name | Familia Reyes-Montoya | PASS |
| milestone_name | M1 — Contract Signed | PASS |
| amount | 36000 | PASS |
| due_date | 2026-03-16 | PASS |
| payment_instructions | Present with CLABE placeholder | PASS |
| currency | USD | PASS |
| running_total | 36000 | PASS |
| CLABE present | [CLABE — TO BE CONFIGURED IN .env] | PASS (placeholder) |
| All 8 required fields | Complete | PASS |
| Backup behavior | No prior invoice — no backup needed | PASS |
| final_milestone dispatch | Not triggered (false) | PASS |
