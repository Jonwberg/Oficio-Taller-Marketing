# Oficio Taller — Marketing Agent Orchestration Design
**Date:** 2026-03-08
**Status:** Approved
**Goal:** 3–5 residential architectural + interior design projects per year, $150K annual income

---

## 1. System Overview

A pod-based multi-agent system built as Claude Code skills, mirroring the firm's existing marketing mission stack. Each agent has a single responsibility and defined handoff protocol. The CMO agent (Valentina) orchestrates all pods. The CEO approves campaigns via WhatsApp link before any content is published. The system is iterative: outcomes feed back into strategy every 90 days.

**Tech stack:** Claude Code skills + pure Claude API. Browser automation via Playwright for Cargo (website) and platform posting where direct APIs are unavailable. Python agent layer to be built in a subsequent phase.

---

## 2. Agent Roster

### Orchestration Layer
| Agent | Name | Responsibility |
|---|---|---|
| Intake Agent | **Arquitecto** | Receives architect intake (photos, video, project briefs, site notes) → structures a campaign brief |
| CMO Agent | **Valentina** | Orchestrates all pods, enforces brand voice, assembles CEO approval package, routes rejections |

### Trust Pod — *Resonancia*
| Agent | Name | Responsibility |
|---|---|---|
| Audience Intelligence | **Lucía** | Maps sentiment, value-language, audience segments from past engagement + intake context |
| Brief Writer | **Marco** | Converts Lucía's analysis into a creative brief for Materia |

### Creative Pod — *Materia*
| Agent | Name | Responsibility |
|---|---|---|
| Content Strategist | **Sofía** | Campaign strategy, platform calendar, message architecture, post sequence |
| Copywriter | **Diego** | Bilingual captions (ES+EN), website copy, YouTube descriptions, Reels scripts |
| Visual Director | **Ileana** | Asset selection, visual sequencing, framing direction notes |

### Publisher
| Agent | Name | Responsibility |
|---|---|---|
| Publisher | **Canal** | Posts approved content to Cargo (Playwright), Instagram, YouTube |

### Iteration Pod — *Pulso*
| Agent | Name | Responsibility |
|---|---|---|
| Metrics Analyst | **Rafael** | Tracks inquiry volume/quality, engagement signals per platform |
| Learning Loop | **Carmen** | Synthesizes Rafael's data → actionable brief back to Resonancia |

### CEO Gate (Human)
| Actor | Name | Responsibility |
|---|---|---|
| Human checkpoint | **CEO** | Reviews approval package via WhatsApp link. Approves or rejects with notes |

---

## 3. Full Campaign Pipeline

```
[ARCHITECT INTAKE]
Photos + video + project brief + site notes
        ↓
    Arquitecto
Structures: project name, location, materials,
sensory thesis, intended emotion, collaborators
        ↓
    Valentina (CMO)
Opens campaign cycle, sets platform targets,
passes brief to Resonancia
        ↓
━━━━━━━━ RESONANCIA POD ━━━━━━━━
    Lucía → Audience analysis
    (past engagement + intake context)
        ↓
    Marco → Creative brief
    (value language, message angle, tone direction)
        ↓
━━━━━━━━ MATERIA POD ━━━━━━━━
    Sofía → Campaign strategy
    (platforms, cadence, post types, sequence)
        ↓
    Diego → Bilingual copy
    (captions ES+EN, website text, YT description, script)
        ↓
    Ileana → Visual plan
    (which assets, sequence, framing notes)
        ↓
    Valentina → Brand review
    Assembles approval package → generates hosted HTML page
        ↓
━━━━━━━━ CEO GATE ━━━━━━━━
    WhatsApp (Playwright on WhatsApp Web) → CEO review link
    CEO: Approve / Reject with notes
        ↓ (approved)
━━━━━━━━ CANAL ━━━━━━━━
    Publishes to:
    • Cargo website (Playwright)
    • Instagram (API or Playwright)
    • YouTube (description + metadata via API or Playwright)
        ↓
━━━━━━━━ PULSO POD ━━━━━━━━
    Rafael → Metrics collection
    (engagement, inquiry volume, inquiry quality)
        ↓
    Carmen → Learning brief
    Feeds back to Valentina → Lucía
    (closes loop for next campaign cycle)
```

**Rejection path:** CEO notes return to Valentina → routed to relevant pod for revision → new approval package generated → re-sent to CEO.

---

## 4. Platforms & Publishing Method

| Platform | CMS/Method | Notes |
|---|---|---|
| oficiotaller.com | Cargo — Playwright browser automation | No public API; use authenticated Playwright session |
| Instagram | Meta Graph API (preferred) or Playwright | API credentials needed; scope: feed posts + Reels |
| YouTube | YouTube Data API v3 | Credentials needed; scope: video metadata + descriptions |
| CEO approval page | Local HTML file served via simple HTTP or hosted static page | Generated per campaign by Valentina |
| CEO notification | WhatsApp Web via Playwright | Regular WhatsApp number; no Business API required |

---

## 5. Content Language

All content bilingual: **Spanish primary, English secondary.** Diego produces both versions per asset. Platform default:
- Instagram: Spanish caption first, English below separator
- YouTube: Spanish title + description, English subtitle
- Website: Toggle or parallel text per project page

---

## 6. FY27 Campaign Priorities

### Priority 1 — *Habitar* Series (YouTube-first)
Atmospheric project films (2–4 min), one per completed project. La Cueva format proven at 19K views. No voiceover, ambient sound, bilingual title card.
**FY27 goal:** 6 films, grow 482 → 3K+ subscribers.
**Agents:** Sofía + Diego + Ileana → Canal

### Priority 2 — *Territorio* (Instagram weekly)
Weekly sensory posts: material details, light studies, landscape relationships. Not project promotions — atmospheric fragments that build resonance.
**FY27 goal:** 52 posts, saves and DM quality as primary Pulso signals.
**Agents:** Lucía → Marco → Diego + Ileana → Canal

### Priority 3 — *Proceso* Reels
Bi-weekly short Reels (30–60s): site observation, craft decisions, material selection, builder collaboration.
**FY27 goal:** 24 Reels, track which topics generate right-fit comments.
**Agents:** Sofía → Diego + Ileana → Canal

### Priority 4 — Website Project Pages
Full narrative page per project: sensory thesis, climate context, material rationale, photo sequence. Bilingual. 8 projects including backlog.
**FY27 goal:** 8 pages published, website as primary inquiry destination.
**Agents:** Diego + Ileana → Canal (Playwright on Cargo)

### Priority 5 — Quarterly Inquiry Conversion
One direct campaign per quarter targeting right-fit residential clients in BCS, Guerrero, NL, and international markets. CTA: *"Conversemos sobre tu proyecto."*
**FY27 goal:** 4 campaigns, 15–20 qualified inquiries, 3–5 closed projects.
**Agents:** Full pod cycle → CEO gate → Canal

---

## 7. Pulso Quarterly Review

Carmen delivers a learning brief every 90 days to Valentina covering:
- Inquiry volume and quality score
- Top-performing content by saves/shares/comments
- Content themes that generated misaligned attention (to suppress)
- Recommended pivot for next quarter

Feeds back into Lucía → Marco → Sofía for the next campaign cycle.

---

## 8. Success Metrics

| Metric | Target | Measured By |
|---|---|---|
| Qualified inquiries/year | 15–20 | Rafael |
| Inquiry-to-consultation rate | >25% | Rafael |
| Closed residential projects | 3–5 | CEO + Rafael |
| Annual revenue | $150K USD | CEO |
| YouTube subscribers | 482 → 3K+ | Rafael |
| Instagram saves/post (avg) | Baseline → 2× | Rafael |
| CEO approval turnaround | <48h | Valentina |

---

## 9. Constraints & Open Items

- Cargo API: none available — all website posting via Playwright authenticated session
- Instagram API credentials: pending setup
- YouTube Data API credentials: pending setup
- WhatsApp: regular number, Playwright on WhatsApp Web (fragile; upgrade to Business API if needed)
- Python agent layer: Phase 2, after Claude Code skills validated
- Git not globally configured on this machine — commit manually after setup
