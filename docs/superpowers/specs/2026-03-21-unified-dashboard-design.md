# Unified Studio Dashboard — Design Spec
**Date:** 2026-03-21

---

## Goal

Replace eight standalone HTML dashboards with a single unified application shell (`docs/plans/index.html`) that presents all views through a persistent sidebar navigation and iframe content area — without modifying any existing dashboard files.

## Architecture

```
docs/plans/index.html          ← new unified app shell (single file, ~150 lines)
docs/plans/*.html              ← existing dashboards, unchanged, loaded via iframe
```

The shell fetches nothing, has no build step, and requires only the existing HTTP server at port 8787.

## Navigation Structure

Left sidebar, three groups:

**SYSTEM**
- Pipeline Flowchart → `pipeline-flowchart.html`
- Agent Flow Chart → `agent-flow-chart.html`
- Agent System Flow → `agent-system-flow.html`
- Data Layer Architecture → `data-layer.html`

**PROJECTS**
- Project History → `project-history.html`
- Timeline Dashboard → `timeline-dashboard.html`
- Project Timeline → `tc-009-project-timeline.html`

**FINANCE**
- Financial Model → `financial-dashboard.html`

## Shell Layout

```
┌─────────────────────────────────────────────────┐
│ TOP BAR: "Oficio Taller Studio" | current view  │
├──────────┬──────────────────────────────────────┤
│ SIDEBAR  │                                      │
│          │         IFRAME (content)             │
│ SYSTEM   │         width: 100%                  │
│  ○ view  │         height: 100%                 │
│  ○ view  │         border: none                 │
│          │                                      │
│ PROJECTS │                                      │
│  ○ view  │                                      │
│          │                                      │
│ FINANCE  │                                      │
│  ○ view  │                                      │
└──────────┴──────────────────────────────────────┘
```

- Sidebar width: 200px, fixed
- Content area: fills remaining viewport (calc(100vw - 200px) × calc(100vh - 40px))
- Top bar height: 40px
- No scrollbars on the shell itself — scroll happens inside the iframe

## Routing

Hash-based routing. Explicit hash → file map:

| Hash | File | Label |
|---|---|---|
| `#pipeline` | `pipeline-flowchart.html` | Pipeline Flowchart |
| `#agent-flow` | `agent-flow-chart.html` | Agent Flow Chart |
| `#agent-system` | `agent-system-flow.html` | Agent System Flow |
| `#data-layer` | `data-layer.html` | Data Layer |
| `#history` | `project-history.html` | Project History |
| `#timeline` | `timeline-dashboard.html` | Timeline Dashboard |
| `#project-timeline` | `tc-009-project-timeline.html` | Project Timeline |
| `#financial` | `financial-dashboard.html` | Financial Model |

**Default:** `#pipeline` (Pipeline Flowchart) when hash is empty or invalid.

**Active state rules:**
- Exactly one nav item is active at a time
- Match is exact: `window.location.hash === '#pipeline'`
- Invalid or missing hash → activate `#pipeline`

Each nav item click:
1. Sets `window.location.hash`
2. Updates iframe `src` to the mapped file (relative path, same directory)
3. Removes `.active` from all nav items, adds to clicked item
4. Updates top bar breadcrumb text to the nav item's Label

## Layout Dimensions

- Top bar: exactly `40px` height, `100vw` width, `position: fixed`, `top: 0`, `left: 0`
- Sidebar: exactly `200px` width, `position: fixed`, `top: 40px`, `left: 0`, `height: calc(100vh - 40px)`, `overflow-y: auto`
- iframe: `position: fixed`, `top: 40px`, `left: 200px`, `width: calc(100vw - 200px)`, `height: calc(100vh - 40px)`, `border: none`
- `body` and `html`: `overflow: hidden`, `margin: 0`, `padding: 0`
- Sidebar has `1px right border` (`#1f1f1f`) — does NOT affect iframe left position (use `left: 200px` regardless)
- Breadcrumb in top bar = the Label from the route map above

## Visual Style

Matches existing dashboards exactly:
- Background: `#0a0a0a`
- Sidebar background: `#080808`
- Border color: `#1f1f1f`
- Font: `'JetBrains Mono', 'Fira Mono', monospace`
- Active item: green left border `#4ade80`, text `#f5f5f5`
- Inactive item: text `#555`, hover `#888`
- Group labels: `#333`, uppercase, 9px, letter-spacing

## Files

| File | Action |
|---|---|
| `docs/plans/index.html` | CREATE — unified app shell |
| All other `docs/plans/*.html` | NO CHANGE |
