# Financial Model & Dashboard Design
**Date:** 2026-03-20
**Project:** Oficio Taller — Studio Financial Model

---

## Goal

Build a two-file financial modeling system for Oficio Taller: a JSON data file that models estimated project fees across the studio's 34-project portfolio, and an interactive HTML dashboard that visualizes historical revenue, active pipeline value, projected cash flow, and key financial KPIs — all derived from fee formulas, not actual accounting records.

## Context

- **Studio:** Oficio Taller (Marcela González Veloz) — architecture firm, Monterrey/CDMX
- **Portfolio:** 34 projects (21 built, 13 in-process), 91% residential
- **Revenue model:** Architecture fee = m² × construction cost/m² × 12%
- **Payment schedule:** 30% advance / 20% at conceptual / 20% at anteproyecto / 30% at ejecutivo
- **Currency:** MXN throughout
- **Data basis:** All numbers are estimates derived from fee formulas. No actual accounting data is used.
- **Existing pattern:** `data/project-timelines.json` → `docs/plans/timeline-dashboard.html` (this design follows the same pattern)

---

## Architecture

Two files with clear separation of concerns:

```
data/financial-model.json          ← data layer (numbers, assumptions)
docs/plans/financial-dashboard.html ← presentation layer (charts, tabs)
```

The dashboard fetches `financial-model.json` via the local HTTP server (already running at `127.0.0.1:8787`). All rendering is client-side JavaScript + SVG — no external dependencies.

---

## Data Layer — `data/financial-model.json`

### Fee Tiers

Four tiers used to assign estimated fees to projects:

| Tier | Typical m² | Fee range (MXN) | Default fee (MXN) |
|---|---|---|---|
| small_residential | 150–200 | 350K–600K | 475K |
| mid_residential | 250–400 | 650K–1.2M | 925K |
| large_residential | 400m²+ | 1.2M–2.5M | 1.85M |
| commercial | varies | 1.5M–3.5M | 2.5M |

Tier midpoints are the defaults. Any project can override with a specific `estimated_fee_mxn` value.

### Project Records

One entry per project (34 total). Two status values only: `built` or `in_process`. Every project is one or the other.

Each record contains:

```json
{
  "id": "string",
  "name": "string",
  "tier": "small_residential | mid_residential | large_residential | commercial",
  "estimated_fee_mxn": 925000,
  "status": "built | in_process",
  "fy27": true,
  "scope_year": 2022,
  "delivery_year": 2023,
  "current_phase": "scope_signed | conceptual | anteproyecto | ejecutivo | complete",
  "milestones": [
    { "id": "M1", "label": "Advance",      "pct": 30, "amount_mxn": 277500, "trigger": "scope_signed",  "estimated_date": "2022-03", "status": "collected | projected" },
    { "id": "M2", "label": "Conceptual",   "pct": 20, "amount_mxn": 185000, "trigger": "conceptual",    "estimated_date": "2022-06", "status": "collected | projected" },
    { "id": "M3", "label": "Anteproyecto", "pct": 20, "amount_mxn": 185000, "trigger": "anteproyecto",  "estimated_date": "2022-09", "status": "collected | projected" },
    { "id": "M4", "label": "Ejecutivo",    "pct": 30, "amount_mxn": 277500, "trigger": "ejecutivo",     "estimated_date": "2023-01", "status": "collected | projected" }
  ]
}
```

**`fy27`:** Boolean. True = this project is a priority for the FY27 marketing campaign (the 11 flagged projects). Used to filter and highlight across all tabs.

**`current_phase`:** The most advanced phase reached. Milestone status assignment rule: milestones whose `trigger` ≤ `current_phase` (in sequence: scope_signed → conceptual → anteproyecto → ejecutivo → complete) = `collected`. Remaining milestones = `projected`.

**`estimated_date`:** Format `"YYYY-MM"`. Null dates = milestone excluded from cash flow chart.

**Built projects:** `current_phase` = `complete`. All 4 milestones `collected`. `delivery_year` is set.

**In-process projects:** `current_phase` reflects latest phase reached. `delivery_year` = null until delivered.

### Assumptions Block

```json
{
  "assumptions": {
    "architecture_fee_pct": 12,
    "construction_cost_per_sqm_mxn": {
      "residential_low": 15000,
      "residential_mid": 20000,
      "residential_high": 28000,
      "commercial": 22000
    },
    "payment_schedule_pct": [30, 20, 20, 30],
    "phase_duration_weeks": {
      "estudios_previos": 3,
      "conceptual_anteproyecto": 10,
      "ejecutivo": 12
    },
    "tier_defaults": {
      "small_residential":  { "sqm_range": "150–200", "fee_min": 350000,  "fee_max": 600000,  "fee_default": 475000  },
      "mid_residential":    { "sqm_range": "250–400", "fee_min": 650000,  "fee_max": 1200000, "fee_default": 925000  },
      "large_residential":  { "sqm_range": "400+",    "fee_min": 1200000, "fee_max": 2500000, "fee_default": 1850000 },
      "commercial":         { "sqm_range": "varies",  "fee_min": 1500000, "fee_max": 3500000, "fee_default": 2500000 }
    },
    "data_disclaimer": "All figures are estimates derived from fee formulas. These are not accounting records."
  }
}
```

---

## Presentation Layer — `docs/plans/financial-dashboard.html`

### Header Badges (always visible)

Four summary badges matching the timeline dashboard style:

- **Total portfolio est.** — sum of all 34 project fees
- **Collected est.** — sum of all `collected` milestone amounts
- **Outstanding** — sum of all `projected` milestone amounts
- **FY27 pipeline** — sum of fees for the 11 FY27 ★ projects

### Tab 1 — Revenue History

**Content:** Estimated revenue collected per year (2016–2025) from the 21 built projects.

- Horizontal bar chart: one bar per year, width proportional to revenue. Colored by volume tier (green = strong year, muted = lighter year). Built in SVG/JavaScript, same approach as the Gantt.
- Project table below the chart: columns = Name · Tier · Est. Fee (MXN) · Year Delivered · Confidence

**Data source:** Built projects only. Year axis = `delivery_year` field. Projects with null `delivery_year` are excluded from the chart but appear in the table with year = "—".

### Tab 2 — Pipeline Value

**Content:** The 13 in-process projects and their financial status.

- Summary row at top: Total pipeline value · Estimated collected · Outstanding remaining
- Project cards in 2-column grid. Each card shows:
  - Project name + FY27 badge if applicable
  - Total estimated fee (large, prominent)
  - Progress bar: orange = collected %, grey = outstanding %
  - Breakdown: M1–M4 with amounts and status icons (✓ collected / ◷ projected)

**Sorted:** FY27 projects first, then by outstanding amount descending.

### Tab 3 — Cash Flow

**Content:** Projected payment arrivals by quarter, Q1 2026 → Q4 2027.

- Stacked vertical bar chart. X-axis = 8 quarters (Q1 2026 … Q4 2027). Each bar = sum of `projected` milestone amounts landing in that quarter.
- Quarter assignment: parse `estimated_date` as `"YYYY-MM"` → quarter = `ceil(month / 3)`. Milestones with null `estimated_date` are excluded from the chart.
- Color-coded by project (consistent color per project across the chart).
- Below chart: table listing each projected payment — Quarter · Project · Milestone · Amount (MXN)

**Scope:** Only `projected` milestones with `estimated_date` in 2026 or 2027. `collected` milestones excluded. Milestones with dates before 2026 or after 2027 also excluded.

### Tab 4 — KPIs

**Content:** Six metric cards. Each card: large number · label · one-line context note.

1. **Avg fee per project** — `sum(all estimated_fee_mxn) / 34`. Context: "across 34 projects"
2. **Total studio revenue (est.)** — `sum(amount_mxn where status = "collected")`. Context: "estimated collected 2016–2026"
3. **Active pipeline value** — `sum(amount_mxn where status = "projected")`. Context: "outstanding across 13 active projects"
4. **Peak revenue year** — year (from Tab 1 data) with highest sum of collected milestone amounts. Context: "highest single year est."
5. **Most valuable active project** — in-process project with highest `sum(projected milestone amounts)`. Shows project name + amount. Context: "largest outstanding fee"
6. **FY27 pipeline value** — `sum(estimated_fee_mxn where fy27 = true)`. Context: "11 FY27 priority projects"

Card style matches Phase Benchmarks tab in timeline dashboard.

### Tab 5 — Assumptions

**Content:** Read-only display of the model inputs.

- Tier table: Tier name · m² range · Fee range · Default fee
- Payment schedule: 4 cards (30 / 20 / 20 / 30) with trigger labels
- Architecture fee % and construction cost ranges
- Data disclaimer (prominent): *"All figures are estimates derived from fee formulas, not accounting records. Update `data/financial-model.json` to refine assumptions."*

---

## Visual Style

Consistent with all existing dashboards in this repo:
- Dark background (`#0a0a0a`), monospace font (`JetBrains Mono` / fallback)
- Tab navigation matching `timeline-dashboard.html`
- SVG charts rendered client-side via JavaScript string building
- Phase/milestone colors: collected = green (`#4ade80`), projected = orange (`#f97316`), unknown = grey (`#6b7280`)
- FY27 projects: bold text + ★ marker

---

## Data Confidence

All financial figures carry the same confidence caveat as the timeline dataset:
- Feb 21 2018 and Oct 4 2021 = Drive migration events; pre-2019 project start dates are low-confidence
- Phase dates for in-process projects estimated from Drive last-modified metadata
- Fee tier assignments are defaults unless overridden in `financial-model.json`

The Assumptions tab makes this explicit with a persistent disclaimer.

---

## Files Created

| File | Description |
|---|---|
| `data/financial-model.json` | Fee tiers, 34 project records, assumption block |
| `docs/plans/financial-dashboard.html` | 5-tab dashboard (History · Pipeline · Cash Flow · KPIs · Assumptions) |

No other files are created or modified. The existing `data/project-timelines.json` is used as a reference for phase dates but is not modified.
