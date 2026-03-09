---
name: run-campaign
description: Run the full campaign pipeline for a brief that Arquitecto has prepared. Dispatches all pods in sequence — Resonancia then Materia — then triggers Valentina's brand review, generates the CEO approval package, and sends the WhatsApp notification. Use after /architect-intake is complete.
---

# Run Campaign Pipeline

Executes the full autonomous campaign cycle: Resonancia → Materia → Valentina review → CEO gate.

**Usage:**
```
/run-campaign <campaign-id>
```

---

## Pre-flight check

Before running, confirm:

```bash
# Brief must exist
cat campaigns/pending/<campaign-id>/brief.json

# sensory_thesis must not be empty
# If it is empty, return to /architect-intake
```

If the brief is incomplete, do not proceed. Return to `@Arquitecto` to complete it.

---

## Phase 1 — Resonancia Pod

Run these agents in order. Wait for each to save its output file before dispatching the next.

### Step 1: Lucía — Audience Analysis

```
@Lucía Please analyze the campaign brief for <campaign-id>.
Read campaigns/pending/<campaign-id>/brief.json and docs/brand/audience-segments.md.
If a recent Pulso report exists at metrics/quarterly/latest.json, read that too.
Save your analysis to campaigns/pending/<campaign-id>/lucia-analysis.json.
```

**Wait for:** `campaigns/pending/<campaign-id>/lucia-analysis.json`

---

### Step 2: Marco — Creative Brief

```
@Marco Lucía's analysis for <campaign-id> is complete.
Read campaigns/pending/<campaign-id>/lucia-analysis.json and campaigns/pending/<campaign-id>/brief.json.
Write the creative brief and save it to campaigns/pending/<campaign-id>/creative-brief.json.
```

**Wait for:** `campaigns/pending/<campaign-id>/creative-brief.json`

---

## Phase 2 — Materia Pod

Run these agents in order. Each depends on the previous one completing.

### Step 3: Sofía — Campaign Strategy

```
@Sofía Marco's creative brief for <campaign-id> is ready.
Read campaigns/pending/<campaign-id>/creative-brief.json and campaigns/pending/<campaign-id>/brief.json.
Design the campaign calendar and save the strategy to campaigns/pending/<campaign-id>/strategy.json.
Use today's date as the campaign launch baseline unless Valentina has specified a different window.
```

**Wait for:** `campaigns/pending/<campaign-id>/strategy.json`

---

### Step 4: Diego — Bilingual Copy

```
@Diego Sofía's strategy for <campaign-id> is complete.
Read campaigns/pending/<campaign-id>/creative-brief.json, campaigns/pending/<campaign-id>/strategy.json,
campaigns/pending/<campaign-id>/brief.json, and docs/brand/voice.md.
Write all bilingual copy for every post in the strategy and save to campaigns/pending/<campaign-id>/copy.json.
```

**Wait for:** `campaigns/pending/<campaign-id>/copy.json`

---

### Step 5: Ileana — Visual Plan

```
@Ileana Diego's copy for <campaign-id> is ready.
Read campaigns/pending/<campaign-id>/assets.json, campaigns/pending/<campaign-id>/strategy.json,
campaigns/pending/<campaign-id>/copy.json, campaigns/pending/<campaign-id>/creative-brief.json,
and campaigns/pending/<campaign-id>/brief.json.
Select and sequence assets for every post and save the visual plan to campaigns/pending/<campaign-id>/visual-plan.json.
Flag any asset gaps directly in the visual-plan.json flags field.
```

**Wait for:** `campaigns/pending/<campaign-id>/visual-plan.json`

---

## Phase 3 — CMO Review and CEO Gate

### Step 6: Valentina — Brand Review and Approval Package

```
@Valentina All Materia outputs for <campaign-id> are complete.
Run a full brand review against docs/brand/campaign-checklist.md and docs/brand/voice.md.
If the review passes, assemble the CEO approval package and save it to campaigns/pending/<campaign-id>/approval-package.json.
If the review fails, route the specific revision notes back to the relevant agent and tell me which agent you are revising with.
```

**If Valentina routes a revision:**
- Wait for the revised output from the agent she named
- Re-invoke Valentina for re-review

**Wait for:** `campaigns/pending/<campaign-id>/approval-package.json` with `valentina_brand_verdict: "approved"`

---

### Step 7: Generate approval page and serve it

Open a terminal in the project directory and run:

```bash
python publisher/scripts/generate-approval-page.py <campaign-id> --serve
```

This will:
- Generate the approval page HTML
- Start a local server at `http://localhost:8765/<campaign-id>.html`
- Open the page in your browser automatically
- Wait for the CEO's decision

Note the URL before proceeding to Step 8.

---

### Step 8: Send WhatsApp notification to CEO

Open a **second terminal** and run:

```bash
python publisher/scripts/send-whatsapp.py <campaign-id> "http://localhost:8765/<campaign-id>.html" --phone=+52XXXXXXXXXX
```

Replace `+52XXXXXXXXXX` with the CEO's WhatsApp number.

To avoid passing the phone number every time, set it once:
```bash
set OFICIO_CEO_PHONE=+52XXXXXXXXXX
python publisher/scripts/send-whatsapp.py <campaign-id> "http://localhost:8765/<campaign-id>.html"
```

---

### Step 9: Wait for CEO decision

The approval server (Step 7) will print the CEO's decision when it arrives and stop automatically.

Check the decision file:
```bash
cat campaigns/pending/<campaign-id>/ceo-decision.json
```

**If approved:** Run `/approve-campaign <campaign-id>`

**If rejected:** Read the CEO's notes, then:
```
@Valentina The CEO has rejected campaign <campaign-id>.
Their notes are in campaigns/pending/<campaign-id>/ceo-decision.json.
Please read the notes, identify which pod needs to revise, and coordinate the revision.
```

Re-run from the revision point when Valentina has routed the corrections.

---

## Typical total run time

| Phase | Expected duration |
|---|---|
| Resonancia (Lucía + Marco) | 5–10 minutes |
| Materia (Sofía + Diego + Ileana) | 15–25 minutes |
| Valentina review | 5–10 minutes |
| CEO review and decision | 1–48 hours |
| **Total to approval** | **~30 min agent time + CEO turnaround** |
