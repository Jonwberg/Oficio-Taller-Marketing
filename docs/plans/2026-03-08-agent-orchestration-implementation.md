# Oficio Taller Marketing Agent Orchestration — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a fully autonomous, pod-based multi-agent marketing system as a Claude Code plugin that runs campaign cycles from architect intake through CEO approval to platform publishing, with quarterly iteration loops.

**Architecture:** Ten named Claude Code agents organized into four pods (Resonancia, Materia, Canal, Pulso), orchestrated by a CMO agent (Valentina) and gated by a CEO WhatsApp approval flow. Campaign state lives in a file-based folder system (pending → approved → published). Playwright handles all browser-based publishing (Cargo website, WhatsApp Web, Instagram, YouTube where APIs are unavailable).

**Tech Stack:** Claude Code plugin system (agent + skill markdown files), Python 3.12 + Playwright for browser automation, HTML for approval pages, JSON for metrics and campaign state, Git for version control.

---

## Prerequisites

Before starting:
- Python 3.12 installed
- Node.js 18+ installed (for Playwright)
- Claude Code CLI installed and authenticated
- Working directory: `C:\Users\Jon Berg\Projects\oficio-taller-marketing`

---

### Task 1: Project Scaffolding & Git Init

**Files:**
- Create: `plugin.json`
- Create: `.gitignore`
- Create: `README.md`
- Create: directory tree (see steps)

**Step 1: Create full directory structure**

```bash
cd "C:\Users\Jon Berg\Projects\oficio-taller-marketing"
mkdir -p .claude/agents
mkdir -p .claude/skills
mkdir -p campaigns/pending
mkdir -p campaigns/approved
mkdir -p campaigns/published
mkdir -p intake/templates
mkdir -p metrics/quarterly
mkdir -p publisher/scripts
mkdir -p approval/pages
mkdir -p docs/brand
```

**Step 2: Initialize git**

```bash
git init
git config user.email "oficio@oficiotaller.com"
git config user.name "Oficio Taller"
```

**Step 3: Create `.gitignore`**

```
__pycache__/
*.pyc
.env
node_modules/
playwright-browsers/
approval/pages/*.html
campaigns/published/*/assets/
*.log
```

**Step 4: Create `plugin.json`**

```json
{
  "name": "oficio-taller-marketing",
  "version": "1.0.0",
  "description": "Autonomous marketing agent system for Oficio Taller",
  "agents": [
    ".claude/agents/arquitecto.md",
    ".claude/agents/valentina.md",
    ".claude/agents/lucia.md",
    ".claude/agents/marco.md",
    ".claude/agents/sofia.md",
    ".claude/agents/diego.md",
    ".claude/agents/ileana.md",
    ".claude/agents/canal.md",
    ".claude/agents/rafael.md",
    ".claude/agents/carmen.md"
  ],
  "skills": [
    ".claude/skills/run-campaign.md",
    ".claude/skills/architect-intake.md",
    ".claude/skills/quarterly-review.md",
    ".claude/skills/approve-campaign.md"
  ]
}
```

**Step 5: Create brand voice reference doc**

Create `docs/brand/voice.md`:

```markdown
# Oficio Taller — Brand Voice Reference

## Tone
Quiet, precise, sensory. Never promotional, never loud.
Write as if describing something you are standing inside of.

## What we say
- Territory, climate, material, light, shadow, threshold, atmosphere
- Inhabitation, craft, collaboration, belonging, locality
- The bond between built space and landscape

## What we never say
- Luxury, premium, exclusive, world-class, iconic
- Amazing, beautiful, stunning (these are lazy)
- "We are proud to present..." or any PR voice

## Bilingual rules
- Spanish is primary. English follows.
- Translate meaning, not words. Keep the sensory precision.
- Instagram: ES caption, line break, "—", EN caption
- YouTube: ES title, ES description first, EN description below "—"
- Website: Both languages visible, ES first

## Project naming
Always use the project's given name, never describe it generically.
Wrong: "a beach house in Baja"
Right: "Casa Atlas — Cerritos, Baja California Sur"
```

**Step 6: Commit**

```bash
git add .
git commit -m "feat: scaffold project structure and plugin manifest"
```

---

### Task 2: Intake System — Arquitecto Agent

**Files:**
- Create: `.claude/agents/arquitecto.md`
- Create: `intake/templates/project-intake.json`
- Create: `intake/templates/campaign-brief.json`

**Step 1: Create intake template**

Create `intake/templates/project-intake.json`:

```json
{
  "project_name": "",
  "location": "",
  "year": "",
  "type": "residential",
  "architects": [],
  "collaborators": [],
  "sensory_thesis": "",
  "climate_context": "",
  "materials_used": [],
  "emotional_intent": "",
  "site_observations": "",
  "client_story": "",
  "assets": {
    "photos": [],
    "video_files": [],
    "process_images": []
  },
  "target_platforms": ["instagram", "youtube", "website"],
  "priority": 1
}
```

**Step 2: Create campaign brief output template**

Create `intake/templates/campaign-brief.json`:

```json
{
  "campaign_id": "",
  "created_at": "",
  "status": "pending",
  "project": {},
  "resonancia_brief": null,
  "materia_strategy": null,
  "materia_copy": null,
  "materia_visual_plan": null,
  "approval_package_url": null,
  "ceo_decision": null,
  "ceo_notes": null,
  "published_at": null,
  "metrics": null
}
```

**Step 3: Create Arquitecto agent**

Create `.claude/agents/arquitecto.md`:

```markdown
---
name: Arquitecto
description: Use when an architect has provided project assets and notes and a new campaign brief needs to be structured. Trigger with /architect-intake or when raw project materials are provided.
color: brown
---

You are Arquitecto, the intake agent for Oficio Taller's marketing system.

Your single job: receive raw project materials from the architects and structure them into a clean campaign brief that Valentina and the pods can work from.

## What you receive
- Project name, location, year
- Photos and video asset list
- Architect's site observations, material notes, sensory intent
- Client story context
- Collaborator list

## What you produce
A completed campaign brief saved to `campaigns/pending/<campaign-id>/brief.json`.

## Your process

1. Ask the architect to fill in or confirm each field from `intake/templates/project-intake.json`
2. Generate a unique campaign_id: `<project-name-slug>-<YYYY-MM-DD>`
3. Create folder: `campaigns/pending/<campaign-id>/`
4. Save completed brief as `campaigns/pending/<campaign-id>/brief.json`
5. Copy assets list into `campaigns/pending/<campaign-id>/assets.json`
6. Notify: "Brief ready for Valentina. Campaign ID: <id>"

## Non-negotiables
- Never invent sensory details the architect did not provide
- Ask if unclear. Do not assume.
- The sensory_thesis must come from the architect's own words, not your synthesis
```

**Step 4: Test Arquitecto manually**

Invoke in Claude Code:
```
@Arquitecto I have a new project: Casa Surfhouse, Pescadero, BCS, 2024. Materials: concrete, wood, mesh. The site is a surf break. Sensory intent: the sound of waves entering the space.
```

Expected: Arquitecto asks follow-up questions and creates `campaigns/pending/casa-surfhouse-2026-03-08/brief.json`

**Step 5: Commit**

```bash
git add .
git commit -m "feat: add Arquitecto intake agent and templates"
```

---

### Task 3: CMO Orchestrator — Valentina Agent

**Files:**
- Create: `.claude/agents/valentina.md`
- Create: `docs/brand/campaign-checklist.md`

**Step 1: Create Valentina agent**

Create `.claude/agents/valentina.md`:

```markdown
---
name: Valentina
description: Use when a campaign brief is ready and needs to move through the full pod pipeline. Valentina is the CMO orchestrator — invoke her after Arquitecto completes a brief. She coordinates Resonancia, Materia, and the CEO approval gate.
color: purple
---

You are Valentina, CMO of Oficio Taller's marketing system.

You are the narrative steward and brand gatekeeper. You do not create content — you orchestrate, review, and approve it. You are the final check before anything goes to the CEO.

## Your responsibilities
1. Receive completed brief from Arquitecto
2. Dispatch Resonancia Pod (Lucía, then Marco)
3. Dispatch Materia Pod (Sofía, then Diego, then Ileana) with Marco's brief
4. Review all Materia outputs against brand voice (`docs/brand/voice.md`)
5. Assemble the CEO approval package
6. Trigger the approval page generator and WhatsApp notification
7. On CEO approval: dispatch Canal to publish
8. On CEO rejection: route notes back to the correct pod and restart

## Brand review checklist
Before assembling the CEO package, verify:
- [ ] No luxury/premium language anywhere
- [ ] Sensory details match architect's actual words
- [ ] Project name used correctly (never generic description)
- [ ] Both ES and EN versions present for all copy
- [ ] Visual plan references real assets (not invented shots)
- [ ] CTA is present only in Priority 5 campaigns, absent in atmospheric posts

## What you output
An approval package saved to `campaigns/pending/<campaign-id>/approval-package.json` containing:
- Campaign summary (1 paragraph, Valentina's voice)
- All copy from Diego (ES + EN per platform)
- Visual plan from Ileana
- Platform calendar from Sofía
- Your brand review verdict with any notes

## Routing logic
- If brand review fails → return to Diego or Ileana with specific notes
- If CEO rejects → read CEO notes, identify which pod to re-engage, restart from that pod
- If CEO approves → dispatch Canal with the approved package

## Non-negotiables
- You cannot approve content that uses luxury/promotional language
- You cannot approve content where sensory details were invented
- Every campaign must have both ES and EN copy before going to CEO
```

**Step 2: Create campaign checklist doc**

Create `docs/brand/campaign-checklist.md`:

```markdown
# Campaign Quality Checklist

Used by Valentina before every CEO submission.

## Voice
- [ ] No "luxury", "premium", "exclusive", "iconic", "stunning", "amazing"
- [ ] Sensory details traceable to architect's intake notes
- [ ] Tone: quiet, precise, present-tense when possible

## Completeness
- [ ] Spanish copy complete for all planned posts
- [ ] English copy complete for all planned posts
- [ ] Visual plan references only assets that exist in assets.json
- [ ] Platform calendar has specific dates, not "week 1"

## Brand fit
- [ ] Project name used correctly in all copy
- [ ] Collaborators credited where relevant
- [ ] No superlatives used for project description

## CEO package
- [ ] Approval page HTML generated
- [ ] All assets accessible via approval page link
- [ ] WhatsApp message draft prepared
```

**Step 3: Commit**

```bash
git add .
git commit -m "feat: add Valentina CMO agent and campaign checklist"
```

---

### Task 4: Resonancia Pod — Lucía + Marco

**Files:**
- Create: `.claude/agents/lucia.md`
- Create: `.claude/agents/marco.md`
- Create: `docs/brand/audience-segments.md`

**Step 1: Create audience segments reference**

Create `docs/brand/audience-segments.md`:

```markdown
# Oficio Taller — Audience Segments

## Segment 1: The Place-Seeker
Values: belonging, nature, authenticity, slowness
Language they use: "connection to the land", "waking up to", "the way light hits", "it feels like it grew there"
Where they are: Instagram saves, YouTube full watches, direct inquiry
Red flags: asks about finishes before asking about the site

## Segment 2: The Second-Home Builder
Values: quality craft, investment, prestige (secondary), uniqueness
Language: "something that isn't just another house", "I want it to feel Mexican but not kitschy"
Where they are: Instagram DMs, referrals
Red flags: mentions square footage in first message

## Segment 3: The Design-Aligned Client
Values: materiality, process, the story of how it was made
Language: "I love how you used the local stone", "the collaboration with the craftspeople"
Where they are: YouTube comments, long caption engagement
Green flags: saves multiple posts before reaching out

## Misaligned signals (suppress content that attracts these)
- Pure luxury tourism content
- Celebrity/influencer engagement
- Generic "inspo" saves with no follow-through
```

**Step 2: Create Lucía agent**

Create `.claude/agents/lucia.md`:

```markdown
---
name: Lucía
description: Audience intelligence agent in the Resonancia Pod. Invoke after Valentina passes a campaign brief. Lucía analyzes which audience segment the project speaks to and what value-language to use.
color: teal
---

You are Lucía, audience intelligence analyst for Oficio Taller's Resonancia Pod.

You listen before anyone speaks. Your job is to understand which people will genuinely resonate with this project — and what language they use when they talk about the things they care about.

## What you receive
- Campaign brief from `campaigns/pending/<campaign-id>/brief.json`
- Audience segment reference: `docs/brand/audience-segments.md`
- Metrics from most recent Pulso report (if available): `metrics/quarterly/latest.json`

## What you produce
Save to `campaigns/pending/<campaign-id>/lucia-analysis.json`:
```json
{
  "primary_segment": "",
  "secondary_segment": "",
  "value_language": [],
  "emotional_hook": "",
  "topics_to_emphasize": [],
  "topics_to_avoid": [],
  "engagement_hypothesis": "",
  "notes_for_marco": ""
}
```

## Your process
1. Read the project brief. What is the dominant sensory or material story?
2. Match it to the most aligned audience segment(s)
3. Identify 5-8 value-language phrases that segment uses naturally
4. Define the emotional hook: what feeling should someone have 3 seconds into the post?
5. Note what to avoid based on misaligned signals
6. Write a one-paragraph briefing note for Marco

## Non-negotiables
- Do not optimize for maximum reach — optimize for right-fit resonance
- If the project has no clear segment match, say so. Do not force a fit.
```

**Step 3: Create Marco agent**

Create `.claude/agents/marco.md`:

```markdown
---
name: Marco
description: Creative brief writer in the Resonancia Pod. Invoke after Lucía completes her analysis. Marco converts Lucía's intelligence into an actionable creative brief for the Materia Pod.
color: teal
---

You are Marco, creative brief writer for Oficio Taller's Resonancia Pod.

You translate intelligence into direction. Lucía tells you who and what resonates — you tell Materia exactly how to use that.

## What you receive
- Lucía's analysis: `campaigns/pending/<campaign-id>/lucia-analysis.json`
- Original campaign brief: `campaigns/pending/<campaign-id>/brief.json`

## What you produce
Save to `campaigns/pending/<campaign-id>/creative-brief.json`:
```json
{
  "campaign_id": "",
  "platform_priorities": ["instagram", "youtube", "website"],
  "message_angle": "",
  "tone_direction": "",
  "value_language_to_use": [],
  "opening_line_direction": "",
  "what_to_show": "",
  "what_not_to_show": "",
  "cta_present": false,
  "cta_text": null,
  "brief_for_sofia": "",
  "brief_for_diego": "",
  "brief_for_ileana": ""
}
```

## Your process
1. Read Lucía's analysis fully
2. Identify the single clearest message angle (one sentence)
3. Write specific direction for each of Sofía, Diego, and Ileana
4. Set cta_present to true only for Priority 5 campaigns

## Non-negotiables
- One message angle per campaign. No "and also..."
- Direction for each Materia agent must be specific enough to act on without follow-up questions
```

**Step 4: Commit**

```bash
git add .
git commit -m "feat: add Resonancia Pod agents (Lucía, Marco) and audience segments"
```

---

### Task 5: Materia Pod — Sofía, Diego, Ileana

**Files:**
- Create: `.claude/agents/sofia.md`
- Create: `.claude/agents/diego.md`
- Create: `.claude/agents/ileana.md`

**Step 1: Create Sofía agent**

Create `.claude/agents/sofia.md`:

```markdown
---
name: Sofía
description: Content strategist in the Materia Pod. Invoke after Marco completes the creative brief. Sofía designs the campaign calendar: which platforms, what post types, in what sequence.
color: orange
---

You are Sofía, content strategist for Oficio Taller's Materia Pod.

You decide the shape of the campaign: where it lives, in what order, at what cadence.

## What you receive
- Creative brief: `campaigns/pending/<campaign-id>/creative-brief.json`
- Campaign brief: `campaigns/pending/<campaign-id>/brief.json`

## What you produce
Save to `campaigns/pending/<campaign-id>/strategy.json`:
```json
{
  "campaign_id": "",
  "platforms": [],
  "post_sequence": [
    {
      "sequence": 1,
      "platform": "",
      "post_type": "",
      "publish_date": "",
      "asset_reference": "",
      "copy_reference": "",
      "notes": ""
    }
  ],
  "anchor_content": "",
  "total_posts": 0,
  "cadence_notes": ""
}
```

## Post types available
- instagram_feed: single image or carousel, caption
- instagram_reel: short video, caption
- youtube_film: full project film (2-4 min)
- youtube_short: 60s cut
- website_project_page: full narrative page on Cargo
- website_journal_post: shorter written reflection

## FY27 priority cadence
- Habitar films: anchor first, other platforms reference it
- Territorio posts: weekly, never promotional
- Proceso Reels: bi-weekly
- Website pages: published within 2 weeks of YouTube film
- Conversion campaigns: all platforms same week

## Non-negotiables
- Every campaign needs a YouTube or website anchor before Instagram posts go out
- Do not schedule posts within 48h of each other on the same platform
- Specific dates only, no "TBD"
```

**Step 2: Create Diego agent**

Create `.claude/agents/diego.md`:

```markdown
---
name: Diego
description: Bilingual copywriter in the Materia Pod. Invoke after Sofía completes the strategy. Diego writes all copy: Instagram captions, YouTube descriptions, website text, Reels scripts — in both Spanish and English.
color: orange
---

You are Diego, bilingual copywriter for Oficio Taller's Materia Pod.

You write the words. Every word must earn its place. This is not marketing copy — it is precise sensory description with intention.

## What you receive
- Creative brief: `campaigns/pending/<campaign-id>/creative-brief.json`
- Strategy: `campaigns/pending/<campaign-id>/strategy.json`
- Brand voice reference: `docs/brand/voice.md`
- Architect's intake (for sensory details): `campaigns/pending/<campaign-id>/brief.json`

## What you produce
Save to `campaigns/pending/<campaign-id>/copy.json`:
```json
{
  "campaign_id": "",
  "posts": [
    {
      "sequence": 1,
      "platform": "",
      "post_type": "",
      "copy_es": "",
      "copy_en": "",
      "hashtags_es": [],
      "hashtags_en": [],
      "youtube_title_es": null,
      "youtube_title_en": null
    }
  ]
}
```

## Writing rules
- Spanish is primary. Write Spanish first, then translate with precision.
- Opening line must land in under 8 words. Make it sensory, not descriptive.
- No "Estamos emocionados de compartir..." / "We are excited to share..."
- Instagram: 3-5 lines ES, separator "—", 3-5 lines EN, hashtags on new line
- YouTube description: ES full description, blank line, "—", EN full description
- Website: long form allowed, but every paragraph must carry weight
- Hashtags: 8-12, mix of Spanish and English, architecture + place-specific

## Non-negotiables
- Every sensory detail must trace back to the architect's intake notes
- Do not invent atmosphere. Describe what is actually there.
- Never use the word "unique", "stunning", "luxury", "premium"
```

**Step 3: Create Ileana agent**

Create `.claude/agents/ileana.md`:

```markdown
---
name: Ileana
description: Visual director in the Materia Pod. Invoke after Diego completes the copy. Ileana reviews available assets and produces a visual plan: which photos/videos to use, in what order, with what framing notes.
color: orange
---

You are Ileana, visual director for Oficio Taller's Materia Pod.

You curate the visual sequence. You do not create images — you select and sequence the assets the architects have provided, and write precise framing and edit notes so whoever assembles the post knows exactly what to do.

## What you receive
- Asset list: `campaigns/pending/<campaign-id>/assets.json`
- Strategy: `campaigns/pending/<campaign-id>/strategy.json`
- Copy: `campaigns/pending/<campaign-id>/copy.json`
- Brief (for sensory thesis): `campaigns/pending/<campaign-id>/brief.json`

## What you produce
Save to `campaigns/pending/<campaign-id>/visual-plan.json`:
```json
{
  "campaign_id": "",
  "posts": [
    {
      "sequence": 1,
      "platform": "",
      "post_type": "",
      "selected_assets": [],
      "asset_order": [],
      "framing_notes": "",
      "edit_notes": "",
      "cover_asset": "",
      "alt_text_es": "",
      "alt_text_en": ""
    }
  ]
}
```

## Visual selection rules
- Lead with the most atmospheric asset — not the most "impressive"
- For carousels: shadow/texture/detail first, wide shot second or last
- For Reels: first 2 seconds must contain movement or light change
- For website: sequence follows the sensory narrative of the copy, not chronology
- Never select an asset that contradicts the copy's emotional register

## Non-negotiables
- Only select assets that exist in assets.json — never reference assets not listed
- If no asset matches a post in the strategy, flag it to Valentina rather than guessing
- Write framing notes as if briefing a skilled editor who hasn't seen the project
```

**Step 4: Commit**

```bash
git add .
git commit -m "feat: add Materia Pod agents (Sofía, Diego, Ileana)"
```

---

### Task 6: Pulso Pod — Rafael + Carmen

**Files:**
- Create: `.claude/agents/rafael.md`
- Create: `.claude/agents/carmen.md`
- Create: `metrics/quarterly/template.json`

**Step 1: Create metrics template**

Create `metrics/quarterly/template.json`:

```json
{
  "period": "",
  "generated_at": "",
  "instagram": {
    "avg_saves_per_post": 0,
    "avg_reach_per_post": 0,
    "top_posts": [],
    "inquiry_from_instagram": 0,
    "right_fit_inquiries": 0,
    "misaligned_inquiries": 0
  },
  "youtube": {
    "subscribers_start": 0,
    "subscribers_end": 0,
    "top_videos_by_watch_time": [],
    "referral_inquiries": 0
  },
  "website": {
    "avg_session_duration": 0,
    "project_page_visits": {},
    "contact_form_submissions": 0
  },
  "campaigns_run": 0,
  "total_qualified_inquiries": 0,
  "consultations_booked": 0,
  "projects_closed": 0,
  "revenue": 0,
  "top_performing_themes": [],
  "underperforming_themes": [],
  "misaligned_attention_sources": []
}
```

**Step 2: Create Rafael agent**

Create `.claude/agents/rafael.md`:

```markdown
---
name: Rafael
description: Metrics analyst in the Pulso Pod. Invoke quarterly or after a campaign cycle completes. Rafael collects and scores engagement and inquiry data across all platforms.
color: red
---

You are Rafael, metrics analyst for Oficio Taller's Pulso Pod.

You measure what matters. Your job is not to celebrate big numbers — it is to distinguish between attention that leads somewhere and attention that leads nowhere.

## What you receive
- Published campaign records: `campaigns/published/*/`
- Manually entered platform data (Instagram Insights, YouTube Studio, website analytics)
- Previous quarterly report for comparison: `metrics/quarterly/`

## What you produce
Save to `metrics/quarterly/<YYYY-QN>.json` using template from `metrics/quarterly/template.json`

## Inquiry quality scoring
Rate each inquiry 1-3:
- 3 = Right-fit: mentions place, atmosphere, material, or site. Budget-appropriate. Residential.
- 2 = Possible: residential intent, some alignment, unclear budget
- 1 = Misaligned: commercial, budget mismatch, attracted by spectacle not substance

## What you measure
- Saves (Instagram) — strongest signal of resonance
- Watch time (YouTube) — engagement depth
- Inquiry volume AND quality score
- Which content themes drove quality inquiries
- Which content themes drove misaligned attention

## Non-negotiables
- Never report raw follower counts as success metrics
- Flag any content that drove high engagement but zero qualified inquiries — this is a warning sign
- Always compare to previous quarter
```

**Step 3: Create Carmen agent**

Create `.claude/agents/carmen.md`:

```markdown
---
name: Carmen
description: Learning loop agent in the Pulso Pod. Invoke after Rafael completes the quarterly metrics report. Carmen synthesizes the data into a strategic brief for Valentina and Lucía.
color: red
---

You are Carmen, learning loop synthesizer for Oficio Taller's Pulso Pod.

You close the loop. Rafael tells you what happened — you tell Valentina and Lucía what it means and what to do differently.

## What you receive
- Rafael's quarterly report: `metrics/quarterly/<YYYY-QN>.json`
- All creative briefs from the quarter: `campaigns/*/creative-brief.json`
- All published copy: `campaigns/published/*/copy.json`

## What you produce
Save to `metrics/quarterly/<YYYY-QN>-learning-brief.json`:
```json
{
  "period": "",
  "executive_summary": "",
  "what_worked": [],
  "what_underperformed": [],
  "content_to_suppress": [],
  "recommended_pivots": [],
  "audience_segment_update": "",
  "value_language_update": [],
  "priority_adjustments": [],
  "message_for_valentina": "",
  "message_for_lucia": ""
}
```

## Your analysis principles
- What drove saves and qualified inquiries? Do more of that.
- What drove reach but no inquiry? Suppress or deprioritize.
- What drove misaligned inquiries? Stop doing that immediately.
- Are the audience segments still accurate? Propose updates if not.

## Non-negotiables
- Do not recommend reaching a broader audience if it means losing brand fit
- Every recommendation must trace back to a specific data point from Rafael's report
- Write Valentina's message as a strategic memo. Write Lucía's as an intelligence update.
```

**Step 4: Commit**

```bash
git add .
git commit -m "feat: add Pulso Pod agents (Rafael, Carmen) and metrics template"
```

---

### Task 7: Approval System — Page Generator + WhatsApp

**Files:**
- Create: `publisher/scripts/generate-approval-page.py`
- Create: `publisher/scripts/send-whatsapp.py`
- Create: `approval/template.html`

**Step 1: Install Python dependencies**

```bash
cd "C:\Users\Jon Berg\Projects\oficio-taller-marketing"
pip install playwright jinja2
python -m playwright install chromium
```

**Step 2: Create approval page HTML template**

Create `approval/template.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Oficio Taller — Aprobación de Campaña {{ campaign_id }}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Georgia', serif; background: #f8f6f2; color: #1a1a1a; max-width: 800px; margin: 0 auto; padding: 2rem; }
    h1 { font-size: 1.4rem; font-weight: normal; margin-bottom: 0.5rem; }
    .meta { color: #666; font-size: 0.9rem; margin-bottom: 2rem; }
    .section { margin-bottom: 2rem; border-top: 1px solid #ddd; padding-top: 1.5rem; }
    .section h2 { font-size: 1rem; font-weight: normal; text-transform: uppercase; letter-spacing: 0.1em; color: #888; margin-bottom: 1rem; }
    .copy-block { background: #fff; padding: 1rem; margin-bottom: 1rem; border-left: 3px solid #c8b89a; }
    .copy-es { font-size: 1rem; line-height: 1.7; }
    .copy-en { font-size: 0.9rem; line-height: 1.7; color: #555; margin-top: 0.75rem; }
    .platform-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #aaa; margin-bottom: 0.5rem; }
    .visual-note { background: #f0ede8; padding: 0.75rem 1rem; font-size: 0.9rem; color: #444; margin-bottom: 0.75rem; }
    .approve-section { background: #1a1a1a; color: #fff; padding: 2rem; text-align: center; margin-top: 2rem; }
    .approve-section p { margin-bottom: 1rem; font-size: 0.95rem; }
    .btn { display: inline-block; padding: 0.75rem 2rem; margin: 0.5rem; font-size: 0.9rem; cursor: pointer; border: none; }
    .btn-approve { background: #c8b89a; color: #1a1a1a; }
    .btn-reject { background: transparent; color: #fff; border: 1px solid #fff; }
    textarea { width: 100%; padding: 0.75rem; margin-top: 1rem; background: #333; color: #fff; border: 1px solid #555; font-family: inherit; font-size: 0.9rem; }
  </style>
</head>
<body>
  <h1>{{ project_name }}</h1>
  <div class="meta">Campaign {{ campaign_id }} · Prepared by Valentina · {{ created_date }}</div>

  <div class="section">
    <h2>Resumen de Campaña</h2>
    <p>{{ campaign_summary }}</p>
  </div>

  <div class="section">
    <h2>Copy por Plataforma</h2>
    {% for post in posts %}
    <div class="copy-block">
      <div class="platform-label">{{ post.platform }} — {{ post.post_type }}</div>
      <div class="copy-es">{{ post.copy_es }}</div>
      <div class="copy-en">{{ post.copy_en }}</div>
    </div>
    {% endfor %}
  </div>

  <div class="section">
    <h2>Plan Visual</h2>
    {% for post in visual_posts %}
    <div class="visual-note">
      <strong>{{ post.platform }}:</strong> {{ post.framing_notes }}
    </div>
    {% endfor %}
  </div>

  <div class="section">
    <h2>Calendario</h2>
    {% for item in schedule %}
    <div class="visual-note">{{ item.publish_date }} — {{ item.platform }} — {{ item.post_type }}</div>
    {% endfor %}
  </div>

  <div class="approve-section">
    <p>¿Apruebas esta campaña para publicación?</p>
    <button class="btn btn-approve" onclick="submitDecision('approved')">✓ Aprobar</button>
    <button class="btn btn-reject" onclick="submitDecision('rejected')">✗ Rechazar con notas</button>
    <div id="notes-area" style="display:none">
      <textarea id="ceo-notes" rows="4" placeholder="Notas para el equipo..."></textarea>
      <button class="btn btn-reject" onclick="submitWithNotes()">Enviar rechazo</button>
    </div>
    <div id="confirmation" style="display:none; margin-top:1rem; color:#c8b89a;"></div>
  </div>

  <script>
    function submitDecision(decision) {
      if (decision === 'rejected') {
        document.getElementById('notes-area').style.display = 'block';
        return;
      }
      writeDecision(decision, '');
    }
    function submitWithNotes() {
      const notes = document.getElementById('ceo-notes').value;
      writeDecision('rejected', notes);
    }
    function writeDecision(decision, notes) {
      const data = { campaign_id: '{{ campaign_id }}', decision, notes, decided_at: new Date().toISOString() };
      fetch('/decision', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) })
        .then(() => {
          document.getElementById('confirmation').style.display = 'block';
          document.getElementById('confirmation').textContent = decision === 'approved' ? '✓ Campaña aprobada.' : '✗ Rechazo registrado. El equipo revisará.';
        });
    }
  </script>
</body>
</html>
```

**Step 3: Create approval page generator script**

Create `publisher/scripts/generate-approval-page.py`:

```python
#!/usr/bin/env python3
"""Generate CEO approval page from campaign package."""

import json
import sys
import http.server
import threading
from pathlib import Path
from datetime import datetime
from jinja2 import Template

CAMPAIGNS_DIR = Path("campaigns/pending")
APPROVAL_DIR = Path("approval/pages")
TEMPLATE_PATH = Path("approval/template.html")

def generate_page(campaign_id: str) -> Path:
    campaign_dir = CAMPAIGNS_DIR / campaign_id

    brief = json.loads((campaign_dir / "brief.json").read_text())
    copy = json.loads((campaign_dir / "copy.json").read_text())
    strategy = json.loads((campaign_dir / "strategy.json").read_text())
    visual = json.loads((campaign_dir / "visual-plan.json").read_text())
    approval_pkg = json.loads((campaign_dir / "approval-package.json").read_text())

    template = Template(TEMPLATE_PATH.read_text())
    html = template.render(
        campaign_id=campaign_id,
        project_name=brief.get("project_name", campaign_id),
        created_date=datetime.now().strftime("%Y-%m-%d"),
        campaign_summary=approval_pkg.get("campaign_summary", ""),
        posts=copy.get("posts", []),
        visual_posts=visual.get("posts", []),
        schedule=strategy.get("post_sequence", []),
    )

    APPROVAL_DIR.mkdir(parents=True, exist_ok=True)
    output_path = APPROVAL_DIR / f"{campaign_id}.html"
    output_path.write_text(html)
    print(f"Approval page generated: {output_path}")
    return output_path


def serve_with_decision_endpoint(campaign_id: str, port: int = 8765):
    """Serve approval page locally and capture CEO decision."""
    page_path = APPROVAL_DIR / f"{campaign_id}.html"
    decision_file = Path(f"campaigns/pending/{campaign_id}/ceo-decision.json")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/" or self.path == f"/{campaign_id}.html":
                self.path = f"/approval/pages/{campaign_id}.html"
            super().do_GET()

        def do_POST(self):
            if self.path == "/decision":
                length = int(self.headers["Content-Length"])
                data = json.loads(self.rfile.read(length))
                decision_file.write_text(json.dumps(data, indent=2))
                self.send_response(200)
                self.end_headers()
                print(f"\nCEO decision received: {data['decision']}")
                if data.get("notes"):
                    print(f"Notes: {data['notes']}")

        def log_message(self, *args):
            pass  # Suppress request logs

    server = http.server.HTTPServer(("localhost", port), Handler)
    url = f"http://localhost:{port}/{campaign_id}.html"
    print(f"\nApproval page live at: {url}")
    print("Waiting for CEO decision... (Ctrl+C to stop)")
    server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate-approval-page.py <campaign-id> [--serve]")
        sys.exit(1)

    campaign_id = sys.argv[1]
    page_path = generate_page(campaign_id)

    if "--serve" in sys.argv:
        serve_with_decision_endpoint(campaign_id)
```

**Step 4: Create WhatsApp sender script**

Create `publisher/scripts/send-whatsapp.py`:

```python
#!/usr/bin/env python3
"""Send CEO approval WhatsApp message via WhatsApp Web automation."""

import sys
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

# CEO WhatsApp number — set this in .env or pass as arg
CEO_PHONE = ""  # e.g., "+521234567890" — set before use

def send_approval_request(campaign_id: str, approval_url: str, ceo_phone: str = CEO_PHONE):
    brief_path = Path(f"campaigns/pending/{campaign_id}/brief.json")
    brief = json.loads(brief_path.read_text()) if brief_path.exists() else {}
    project_name = brief.get("project_name", campaign_id)

    message = (
        f"*Oficio Taller — Aprobación requerida*\n\n"
        f"Proyecto: {project_name}\n"
        f"Campaña: {campaign_id}\n\n"
        f"Valentina ha preparado el paquete de campaña para tu revisión.\n\n"
        f"Revisa y aprueba aquí:\n{approval_url}\n\n"
        f"_Puedes aprobar o rechazar directamente desde el enlace._"
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Open WhatsApp Web
        page.goto("https://web.whatsapp.com")
        print("WhatsApp Web opened. Please scan QR code if prompted.")
        print("Waiting for WhatsApp to load (up to 60 seconds)...")

        # Wait for chat list to appear (indicates logged in)
        page.wait_for_selector('[data-testid="chat-list"]', timeout=60000)
        print("WhatsApp loaded.")

        # Navigate to CEO chat via wa.me link
        page.goto(f"https://web.whatsapp.com/send?phone={ceo_phone.replace('+', '')}&text=")
        page.wait_for_selector('[data-testid="conversation-compose-box-input"]', timeout=15000)

        # Type message
        msg_box = page.locator('[data-testid="conversation-compose-box-input"]')
        msg_box.fill(message)
        time.sleep(1)

        # Send
        page.keyboard.press("Enter")
        time.sleep(2)
        print(f"WhatsApp message sent to CEO ({ceo_phone})")

        browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send-whatsapp.py <campaign-id> <approval-url>")
        sys.exit(1)

    campaign_id = sys.argv[1]
    approval_url = sys.argv[2]
    send_approval_request(campaign_id, approval_url)
```

**Step 5: Test approval page generation**

Create a minimal test campaign to verify the page renders:

```bash
mkdir -p campaigns/pending/test-001
echo '{"project_name":"Casa Test","campaign_summary":"Test campaign."}' > campaigns/pending/test-001/approval-package.json
echo '{"posts":[{"platform":"instagram","post_type":"feed","copy_es":"Texto ES","copy_en":"Text EN"}]}' > campaigns/pending/test-001/copy.json
echo '{"post_sequence":[{"publish_date":"2026-04-01","platform":"instagram","post_type":"feed"}]}' > campaigns/pending/test-001/strategy.json
echo '{"posts":[{"platform":"instagram","framing_notes":"Wide shot, dusk light"}]}' > campaigns/pending/test-001/visual-plan.json
echo '{"project_name":"Casa Test"}' > campaigns/pending/test-001/brief.json

python publisher/scripts/generate-approval-page.py test-001
```

Expected: `approval/pages/test-001.html` created with no errors.

Open the file in a browser and verify it renders the content correctly.

**Step 6: Commit**

```bash
git add .
git commit -m "feat: add approval page generator, WhatsApp sender, and HTML template"
```

---

### Task 8: Canal Publisher Agent + Scripts

**Files:**
- Create: `.claude/agents/canal.md`
- Create: `publisher/scripts/publish-cargo.py`
- Create: `publisher/scripts/move-to-published.py`

**Step 1: Create Canal agent**

Create `.claude/agents/canal.md`:

```markdown
---
name: Canal
description: Publisher agent. Invoke only after CEO has approved a campaign (ceo-decision.json contains "approved"). Canal coordinates publishing approved content to Cargo website, Instagram, and YouTube using the visual plan and copy from the approved campaign package.
color: green
---

You are Canal, the publisher for Oficio Taller's marketing system.

You execute. You do not create or revise. By the time content reaches you, it has been reviewed by Valentina and approved by the CEO. Your job is to get it onto the right platforms, in the right order, at the right time.

## What you receive
- Approved campaign package in `campaigns/approved/<campaign-id>/`
- CEO decision confirmation: `campaigns/approved/<campaign-id>/ceo-decision.json`
- Strategy (for publish dates): `campaigns/approved/<campaign-id>/strategy.json`
- Copy: `campaigns/approved/<campaign-id>/copy.json`
- Visual plan: `campaigns/approved/<campaign-id>/visual-plan.json`

## Publishing order
Always follow Sofía's strategy sequence exactly. Anchor content (YouTube or website) publishes first.

## Platform methods
- **Cargo website**: Run `python publisher/scripts/publish-cargo.py <campaign-id> <sequence>`
- **Instagram**: Manual upload required until API credentials are configured. Canal will output exact copy and asset instructions.
- **YouTube**: Manual upload required until YouTube Data API is configured. Canal will output title, description, and thumbnail instructions.

## What you produce
After each post goes live, update `campaigns/approved/<campaign-id>/publish-log.json`:
```json
{
  "campaign_id": "",
  "posts_published": [
    {
      "sequence": 1,
      "platform": "",
      "published_at": "",
      "url": "",
      "status": "published"
    }
  ]
}
```

When all posts are live, run:
```bash
python publisher/scripts/move-to-published.py <campaign-id>
```

## Non-negotiables
- Never publish without a confirmed ceo-decision.json showing "approved"
- Never modify copy or assets during publishing — publish exactly what was approved
- Log every publish action immediately
```

**Step 2: Create Cargo publisher script**

Create `publisher/scripts/publish-cargo.py`:

```python
#!/usr/bin/env python3
"""
Publish a website project page to Cargo CMS via Playwright browser automation.
Requires an authenticated Cargo session (manual login on first run, session stored).
"""

import json
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

CARGO_URL = "https://cargo.site"
SESSION_FILE = Path("publisher/.cargo-session.json")

def load_campaign(campaign_id: str, sequence: int) -> dict:
    base = Path(f"campaigns/approved/{campaign_id}")
    copy_data = json.loads((base / "copy.json").read_text())
    visual_data = json.loads((base / "visual-plan.json").read_text())
    brief = json.loads((base / "brief.json").read_text())

    # Find the post matching sequence
    post_copy = next((p for p in copy_data["posts"] if p["sequence"] == sequence), None)
    post_visual = next((p for p in visual_data["posts"] if p["sequence"] == sequence), None)

    return {
        "project_name": brief["project_name"],
        "copy_es": post_copy["copy_es"] if post_copy else "",
        "copy_en": post_copy["copy_en"] if post_copy else "",
        "assets": post_visual["selected_assets"] if post_visual else [],
        "platform": post_copy["platform"] if post_copy else "",
    }


def publish_to_cargo(campaign_id: str, sequence: int):
    data = load_campaign(campaign_id, sequence)

    if data["platform"] != "website":
        print(f"Sequence {sequence} is for {data['platform']}, not website. Skipping.")
        return

    print(f"Publishing to Cargo: {data['project_name']}")
    print("NOTE: Cargo has no public API. This script opens Cargo in a browser.")
    print("You will need to manually log in on first run.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # Try to restore session
        context_options = {}
        if SESSION_FILE.exists():
            storage = json.loads(SESSION_FILE.read_text())
            context_options["storage_state"] = storage

        context = browser.new_context(**context_options)
        page = context.new_page()

        page.goto(CARGO_URL)
        print("Cargo opened. Log in if prompted, then press Enter here to continue...")
        input()

        # Save session for next time
        storage = context.storage_state()
        SESSION_FILE.parent.mkdir(exist_ok=True)
        SESSION_FILE.write_text(json.dumps(storage))

        # Display the content for manual entry
        print("\n" + "="*60)
        print("CONTENT TO PUBLISH ON CARGO:")
        print("="*60)
        print(f"\nProject: {data['project_name']}")
        print(f"\n--- SPANISH ---\n{data['copy_es']}")
        print(f"\n--- ENGLISH ---\n{data['copy_en']}")
        print(f"\nAssets to upload: {data['assets']}")
        print("="*60)
        print("\nCreate the project page in Cargo, paste the content above,")
        print("and upload the listed assets. Press Enter when done.")
        input()

        browser.close()
        print(f"Cargo publish complete for {campaign_id} sequence {sequence}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python publish-cargo.py <campaign-id> <sequence-number>")
        sys.exit(1)
    publish_to_cargo(sys.argv[1], int(sys.argv[2]))
```

**Step 3: Create move-to-published script**

Create `publisher/scripts/move-to-published.py`:

```python
#!/usr/bin/env python3
"""Move a completed campaign from approved/ to published/."""

import sys
import shutil
import json
from pathlib import Path
from datetime import datetime

def move_to_published(campaign_id: str):
    src = Path(f"campaigns/approved/{campaign_id}")
    dst = Path(f"campaigns/published/{campaign_id}")

    if not src.exists():
        print(f"Campaign {campaign_id} not found in approved/")
        sys.exit(1)

    # Add published timestamp
    log_path = src / "publish-log.json"
    if log_path.exists():
        log = json.loads(log_path.read_text())
    else:
        log = {"campaign_id": campaign_id, "posts_published": []}

    log["completed_at"] = datetime.now().isoformat()
    log_path.write_text(json.dumps(log, indent=2))

    shutil.move(str(src), str(dst))
    print(f"Campaign {campaign_id} moved to published/")
    print(f"Ready for Pulso Pod metrics tracking.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python move-to-published.py <campaign-id>")
        sys.exit(1)
    move_to_published(sys.argv[1])
```

**Step 4: Commit**

```bash
git add .
git commit -m "feat: add Canal agent and publisher scripts (Cargo, move-to-published)"
```

---

### Task 9: Orchestration Skills

**Files:**
- Create: `.claude/skills/architect-intake.md`
- Create: `.claude/skills/run-campaign.md`
- Create: `.claude/skills/approve-campaign.md`
- Create: `.claude/skills/quarterly-review.md`

**Step 1: Create architect-intake skill**

Create `.claude/skills/architect-intake.md`:

```markdown
---
name: architect-intake
description: Start here when architects have new project assets. Launches Arquitecto to structure a campaign brief.
---

# Architect Intake

Use this skill to begin a new campaign cycle with fresh project materials from the architects.

## What to have ready
- Project name, location, year
- List of available photo and video assets (file paths or descriptions)
- Architect's site observation notes
- Sensory thesis and emotional intent
- Materials used
- Collaborator names

## Process

Invoke Arquitecto:

```
@Arquitecto Please begin intake for a new project. I will provide the materials now.
```

Arquitecto will guide you through structuring the brief and will create the campaign folder at `campaigns/pending/<campaign-id>/`.

When Arquitecto confirms the brief is complete, run the campaign:

```
/run-campaign <campaign-id>
```
```

**Step 2: Create run-campaign skill**

Create `.claude/skills/run-campaign.md`:

```markdown
---
name: run-campaign
description: Run the full campaign pipeline for a brief that Arquitecto has prepared. Dispatches all pods in sequence, generates approval package, and sends CEO notification.
---

# Run Campaign Pipeline

Executes the full Resonancia → Materia → Valentina → CEO gate cycle.

## Usage
```
/run-campaign <campaign-id>
```

## Pipeline steps (execute in order)

### Step 1: Resonancia Pod
```
@Lucía Please analyze the campaign brief at campaigns/pending/<campaign-id>/brief.json and produce your audience analysis.
```
Wait for Lucía to save `lucia-analysis.json`.

```
@Marco Please read Lucía's analysis and the brief for <campaign-id> and produce the creative brief.
```
Wait for Marco to save `creative-brief.json`.

### Step 2: Materia Pod
```
@Sofía Please read the creative brief for <campaign-id> and produce the campaign strategy and calendar.
```
Wait for Sofía to save `strategy.json`.

```
@Diego Please read the creative brief and strategy for <campaign-id> and write all bilingual copy.
```
Wait for Diego to save `copy.json`.

```
@Ileana Please read the assets, strategy, and copy for <campaign-id> and produce the visual plan.
```
Wait for Ileana to save `visual-plan.json`.

### Step 3: CMO Review
```
@Valentina Please review all Materia outputs for <campaign-id> against the brand voice and assemble the CEO approval package.
```
Wait for Valentina to save `approval-package.json`.

### Step 4: Generate approval page and notify CEO
```bash
python publisher/scripts/generate-approval-page.py <campaign-id> --serve
```

In a separate terminal:
```bash
python publisher/scripts/send-whatsapp.py <campaign-id> "http://localhost:8765/<campaign-id>.html"
```

### Step 5: Wait for CEO decision
Monitor `campaigns/pending/<campaign-id>/ceo-decision.json`.

**If approved:** Run `/approve-campaign <campaign-id>`
**If rejected:** Read CEO notes, invoke `/run-campaign <campaign-id>` again after Valentina routes the revision.
```

**Step 3: Create approve-campaign skill**

Create `.claude/skills/approve-campaign.md`:

```markdown
---
name: approve-campaign
description: Execute after CEO approves a campaign. Moves campaign to approved/, dispatches Canal to publish.
---

# Approve and Publish Campaign

Run after confirming CEO approval in `campaigns/pending/<campaign-id>/ceo-decision.json`.

## Usage
```
/approve-campaign <campaign-id>
```

## Steps

### Step 1: Move to approved
```bash
mv campaigns/pending/<campaign-id> campaigns/approved/<campaign-id>
```

### Step 2: Dispatch Canal
```
@Canal The CEO has approved campaign <campaign-id>. Please review the strategy, copy, and visual plan, then begin publishing in sequence order.
```

### Step 3: Monitor publish log
Canal will update `campaigns/approved/<campaign-id>/publish-log.json` after each post.

### Step 4: Move to published when complete
```bash
python publisher/scripts/move-to-published.py <campaign-id>
```

### Step 5: Notify Rafael
```
@Rafael Campaign <campaign-id> is now in campaigns/published/. Please add it to your tracking list for the next quarterly metrics report.
```
```

**Step 4: Create quarterly-review skill**

Create `.claude/skills/quarterly-review.md`:

```markdown
---
name: quarterly-review
description: Run the quarterly Pulso iteration cycle. Dispatches Rafael then Carmen to generate metrics report and learning brief.
---

# Quarterly Review Cycle

Run at the end of each quarter to close the learning loop.

## Usage
```
/quarterly-review <YYYY-QN>
```
Example: `/quarterly-review 2027-Q1`

## Steps

### Step 1: Gather platform data
Before running, manually export:
- Instagram Insights CSV (from Instagram app)
- YouTube Studio analytics export
- Website analytics (from Cargo or Google Analytics)

Save to: `metrics/raw/<YYYY-QN>/`

### Step 2: Dispatch Rafael
```
@Rafael Please generate the quarterly metrics report for <YYYY-QN>. Raw data is in metrics/raw/<YYYY-QN>/. Published campaigns are in campaigns/published/. Save your report to metrics/quarterly/<YYYY-QN>.json.
```

Wait for Rafael to save the report.

### Step 3: Dispatch Carmen
```
@Carmen Rafael's report for <YYYY-QN> is ready. Please synthesize the learning brief and save it to metrics/quarterly/<YYYY-QN>-learning-brief.json.
```

### Step 4: Valentina integration
```
@Valentina Carmen's learning brief for <YYYY-QN> is ready. Please read it and update your campaign approach for the next quarter accordingly.
```

### Step 5: Commit
```bash
git add metrics/
git commit -m "data: quarterly review <YYYY-QN> complete"
```
```

**Step 5: Commit**

```bash
git add .
git commit -m "feat: add orchestration skills (architect-intake, run-campaign, approve-campaign, quarterly-review)"
```

---

### Task 10: FY27 Campaign 1 — Launch *Habitar* Series

**This is the first real campaign run. Use existing projects from the website.**

**Files:**
- Create: `campaigns/pending/casa-atlas-2026-04/brief.json` (manually)
- Run the full pipeline

**Step 1: Prepare Casa Atlas brief**

Based on the website content observed (Atlas — Cerritos, Baja California Sur, 2022):

```
/architect-intake
```

Provide Arquitecto with:
- Project: Casa Atlas
- Location: Cerritos, Baja California Sur, México
- Year: 2022
- Type: Residential architecture + interior
- Sensory thesis: (ask the architects to provide)
- Priority 1: Habitar YouTube film

**Step 2: Run the full pipeline**

```
/run-campaign casa-atlas-2026-04
```

Follow each pod step. Review outputs at each stage.

**Step 3: CEO review**

When Valentina generates the approval package, serve it and send WhatsApp notification.

**Step 4: After CEO approval**

```
/approve-campaign casa-atlas-2026-04
```

**Step 5: Commit campaign record**

```bash
git add campaigns/published/casa-atlas-2026-04/
git commit -m "campaign: Casa Atlas Habitar series published"
```

---

## FY27 Campaign Schedule

| Quarter | Priority | Projects/Campaigns |
|---|---|---|
| Q1 FY27 (Apr–Jun 2026) | Habitar Series launch | Casa Atlas, Casa Surfhouse films |
| Q1 FY27 | Territorio weekly | 13 Instagram posts |
| Q1 FY27 | Website pages | Casa Atlas, Casa Surfhouse pages |
| Q2 FY27 (Jul–Sep 2026) | Habitar Series | 2 more project films |
| Q2 FY27 | Proceso Reels | 6 Reels |
| Q2 FY27 | Quarterly review | Q1 Pulso report |
| Q2 FY27 | Conversion campaign | Q2 inquiry push |
| Q3 FY27 (Oct–Dec 2026) | Habitar Series | 2 more project films |
| Q3 FY27 | Quarterly review | Q2 Pulso report |
| Q4 FY27 (Jan–Mar 2027) | Full review | Annual Pulso report, FY28 planning |

---

## Open Items (Post-Launch)

- [ ] CEO WhatsApp number — add to `publisher/scripts/send-whatsapp.py` before first use
- [ ] Instagram Graph API credentials — needed for automated posting
- [ ] YouTube Data API v3 credentials — needed for automated description updates
- [ ] Cargo session — first Playwright run requires manual login, session persisted after
- [ ] Metrics raw data format — standardize after first quarter of real data
