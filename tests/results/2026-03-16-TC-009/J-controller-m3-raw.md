# Controller — Milestone 3: Executive Plans Approved (FINAL)
**run_id:** 2026-03-16-TC-009
**agent:** Controller
**milestone_number:** 3
**milestone_name:** Executive Plans Approved
**final_milestone:** true
**project_id:** PRJ-2026-0316-familia-reyes-montoya
**timestamp:** 2026-03-16

---

## Step 1: Read context

Read `state.json`:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- client_name: Familia Reyes-Montoya
- project_type: standalone_residential
- tasks.invoice: null
- tasks.construction: null
- tasks.tax_filing: null

Read `scope-of-work.json` payment_schedule:
- M3 — Executive Plans Approved: $27,000 USD (30%) — trigger: Executive plans package approved by client

Read `project-schedule.json` milestone_dates:
- M3_executive_plans_approved: 2026-09-04

Milestone in context: milestone_name = "Executive Plans Approved", milestone_number = 3, final_milestone = true
SOW match: M3 — Executive Plans Approved — $27,000 USD
Due date: M3_executive_plans_approved = 2026-09-04

---

## Step 2: Calculate running_total

Previous `invoice.json` exists (from M2 Controller, successful retry).
Read previous invoice.json:
- running_total: $63,000 USD (M1 + M2 = 36000 + 27000)

running_total (M3) = $63,000 + $27,000 = **$90,000 USD**

Verify against SOW total_architecture_fee_usd: $90,000 USD ✓ — matches exactly.

---

## Step 3: Pre-write check — backup

Check: does `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json` exist?
→ YES — M2 invoice.json exists (from successful M2 retry).

**Backing up:** copy invoice.json → invoice-previous.json
`invoice-previous.json` written successfully. Backup complete.

---

## Step 4: Write invoice.json

Writing to: `projects/PRJ-2026-0316-familia-reyes-montoya/invoice.json`

```json
{
  "project_name": "Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México",
  "client_name": "Familia Reyes-Montoya",
  "milestone_name": "M3 — Executive Plans Approved",
  "amount": 27000,
  "due_date": "2026-09-04",
  "payment_instructions": "Bank transfer to Oficio Taller. Bank: [BANK_NAME]. CLABE: [CLABE — TO BE CONFIGURED IN .env]. Reference: PRJ-2026-0316-familia-reyes-montoya-M3.",
  "currency": "USD",
  "running_total": 90000
}
```

**WRITE: SUCCESS**

---

## Step 5: Post-write — delete backup

Write succeeded.
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
  --body "Invoice generated: M3 — Executive Plans Approved. Amount: 27000 USD. Running total: 90000. Due: 2026-09-04."
```

**LOG: ASANA_UNAVAILABLE** — continuing.

---

## Step 7: Check final_milestone — FINAL MILESTONE ACTIONS

final_milestone: **true** → Execute final milestone protocol.

### 7a: Dispatch Tax agent

Dispatching Tax via Agent tool with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- Instruction: "Project PRJ-2026-0316-familia-reyes-montoya is closing. Generate tax filing for final revenue."

**→ Tax agent dispatched by Controller** (not Vera — per TC-009 spec and agent protocol)

### 7b: Dispatch Marketing pipeline (Valentina)

Dispatching Valentina via Agent tool with:
- project_id: PRJ-2026-0316-familia-reyes-montoya
- client_name: Familia Reyes-Montoya
- project_type: standalone_residential
- Instruction: "Project PRJ-2026-0316-familia-reyes-montoya is complete. Initiate post-project marketing pipeline for Familia Reyes-Montoya."

**→ Marketing pipeline (Valentina) dispatched by Controller**

### 7c: Update state.json

Writing state update:
```json
{
  "project_state": "project_closed"
}
```

state.json updated: `project_state` → `project_closed`

### 7d: Complete construction task in Asana

```bash
python entrega/asana_client.py complete_task \
  --task_id null \
  --comment "Construction complete. Project closed. Tax and marketing pipeline dispatched."
```

**LOG: ASANA_UNAVAILABLE** — tasks.construction is null; continuing.

---

## Schema Validation (Final Invoice — M3)

| Field | Value | Status |
|-------|-------|--------|
| project_name | Familia Reyes-Montoya — standalone_residential — Cerritos, BCS, México | PASS |
| client_name | Familia Reyes-Montoya | PASS |
| milestone_name | M3 — Executive Plans Approved | PASS |
| amount | 27000 | PASS |
| due_date | 2026-09-04 | PASS |
| payment_instructions | Present with CLABE placeholder | PASS |
| currency | USD | PASS |
| running_total | 90000 | PASS |
| CLABE present | [CLABE — TO BE CONFIGURED IN .env] | PASS (placeholder) |
| All 8 required fields | Complete | PASS |

## TC-009 Final Milestone Checks

| Check | Result | Status |
|-------|--------|--------|
| running_total at M3 | 90000 (36000 + 27000 + 27000) | PASS |
| running_total matches total_architecture_fee_usd | 90000 == 90000 | PASS |
| Tax dispatched by Controller (not Vera) | YES — Controller dispatches Tax | PASS |
| Marketing (Valentina) dispatched | YES | PASS |
| project_state set to project_closed | YES | PASS |
| Backup created before write | YES — invoice-previous.json | PASS |
| Backup deleted after successful write | YES | PASS |
