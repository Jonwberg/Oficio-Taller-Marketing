---
name: architect-intake
description: Use when architects have new project assets and a campaign needs to be started. Launches Arquitecto to structure a campaign brief from raw project materials. Always the first step in any new campaign cycle.
---

# Architect Intake

Use this skill to begin a new campaign cycle. Arquitecto will guide the intake process and produce a complete campaign brief before anything else in the pipeline runs.

---

## What to have ready before starting

The more complete the intake materials, the stronger every agent downstream will perform. Ideal intake includes:

- Project name and location (city, state, country)
- Year completed
- List of available photo and video asset files (filenames or folder path)
- Architect's own site observation notes — what they noticed about the territory before designing
- The sensory thesis: what it feels like to inhabit the space (in the architect's words)
- Materials used and why those materials were chosen
- Climate and ecological context of the site
- Collaborators: builders, craftspeople, interior specialists, landscape collaborators
- Client story (optional)

If some of this is not ready yet, begin anyway. Arquitecto will ask for what is missing.

---

## Step 1: Invoke Arquitecto

```
@Arquitecto Please begin intake for a new project. I will provide the materials now.
```

Arquitecto will ask questions one at a time until the brief is complete. Answer in whatever language is most natural — Spanish or English, or both.

---

## Step 2: Confirm the brief is complete

Arquitecto will confirm:
- The campaign ID (format: `project-name-YYYY-MM-DD`)
- The location of the saved brief: `campaigns/pending/<campaign-id>/brief.json`
- Any fields left intentionally blank

Review the brief if you want to verify it before the campaign runs.

---

## Step 3: Launch the campaign pipeline

When Arquitecto confirms the brief is ready:

```
/run-campaign <campaign-id>
```

Replace `<campaign-id>` with the ID Arquitecto generated.

---

## Notes

- Do not launch `/run-campaign` until Arquitecto has confirmed the brief is complete and saved
- The sensory thesis is the most important field — if it is vague or missing, ask the architects to provide it before proceeding
- Asset files do not need to be in a specific folder yet; Arquitecto records their descriptions and Ileana will reference them during the visual planning step
