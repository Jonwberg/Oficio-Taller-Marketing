---
name: log-inquiry
description: Log and score an incoming client inquiry. Use when a new message arrives via Instagram DM, WhatsApp, or the Cargo contact form. Produces a structured inquiry.json and updates leads/log.json.
---

You are logging and scoring an incoming inquiry for Oficio Taller.

## Step 1 — Extract information from the message

Ask the user to paste the raw inquiry message if they haven't already. Then extract:

- `contact_name` — first name or full name if given
- `contact_phone` — if provided
- `contact_email` — if provided
- `source` — which channel sent this (instagram_dm / whatsapp / cargo_contact_form / referral / other)
- `project_type` — residential / commercial / interior / unknown
- `project_location` — city/region if mentioned
- `project_description` — what they want to build or design
- `budget_mentioned` — any number or range they mentioned, or "not mentioned"
- `timeline_mentioned` — when they want to start or finish, or "not mentioned"

If any field is unclear from the message, note it as empty — do not guess.

## Step 2 — Score the inquiry

Apply Rafael's scoring rubric:

**Score 3 — Right-fit (proceed to consultation)**
- Residential project in BCS, Guerrero, NL, or international
- References a specific project, the studio's work, or the feeling of a space
- Mentions inhabitation, craft, a site, or quality of life
- Budget language suggests they understand design fees
- Timeline is deliberate (not urgent/rushed)

**Score 2 — Possible (ask clarifying questions before deciding)**
- Interest is genuine but project type, location, or budget is unclear
- Could be right-fit with more information
- No red flags but no strong signals either

**Score 1 — Misaligned (decline gracefully)**
- Commercial, retail, or hospitality project outside the studio's focus
- Budget language focused on cheapest option or comparison shopping
- Urgency that conflicts with the studio's pace
- Looking for contractor, not architect/designer

Write a one-sentence `score_reason` explaining why.

## Step 3 — Generate the inquiry file

Generate a `lead_id` using the format: `<first-name-lowercase>-<YYYY-MM-DD>` (e.g., `carlos-2026-03-15`)

Produce the complete `inquiry.json` by filling the template at `leads/template/inquiry.json`.

Set:
- `status`: `scored`
- `follow_up_owner`: the person responsible for responding (default: CEO)
- `follow_up_due`: today + 24 hours for score 3, today + 48 hours for score 2

## Step 4 — Save and update the log

1. Create folder `leads/<lead_id>/`
2. Save the filled `inquiry.json` there
3. Append a summary entry to `leads/log.json`:

```json
{
  "lead_id": "<lead_id>",
  "date": "<date_received>",
  "name": "<contact_name>",
  "source": "<source>",
  "score": <score>,
  "status": "scored",
  "follow_up_due": "<date>"
}
```

## Step 5 — Recommend next action

- **Score 3:** Draft a response message for the user to send — warm, unhurried, in Oficio Taller's voice. Invite them to a call: *"Nos gustaría conocer más sobre tu proyecto. ¿Tienes tiempo para una llamada esta semana?"*
- **Score 2:** Draft 2–3 clarifying questions to understand the project better before deciding.
- **Score 1:** Draft a graceful decline that respects the person and leaves the door open: acknowledge their project, explain the studio's focus, and wish them well.

All response drafts: Spanish first, English below if the inquiry was in English.
