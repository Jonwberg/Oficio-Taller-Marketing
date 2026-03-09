---
name: quarterly-review
description: Run the quarterly Pulso iteration cycle. Dispatches Rafael to generate the metrics report, then Carmen to synthesize the learning brief, then feeds insights back into Valentina and Lucía for the next campaign cycle. Run at the end of each quarter.
---

# Quarterly Review Cycle

Closes the learning loop. Measures what happened, synthesizes what it means, and updates the next quarter's campaign approach.

**Usage:**
```
/quarterly-review <YYYY-QN>
```

Examples: `/quarterly-review 2026-Q2`, `/quarterly-review 2027-Q1`

**Run at the end of:** March (Q1), June (Q2), September (Q3), December (Q4)

---

## Before you start — gather raw platform data

Rafael needs real data. Export the following manually before running this skill:

### Instagram
1. Open Instagram app → Profile → Professional Dashboard → Insights
2. Set date range to the full quarter
3. Export or screenshot: reach, saves, shares per post, follower count start/end
4. Save to: `metrics/raw/<YYYY-QN>/instagram-insights.json` or `.csv`

### YouTube
1. Open YouTube Studio → Analytics
2. Set date range to the full quarter
3. Export: views, watch time %, subscriber count start/end, top videos
4. Save to: `metrics/raw/<YYYY-QN>/youtube-analytics.csv`

### Website (Cargo / Google Analytics)
1. Export session data, page views by project, contact form submissions
2. Save to: `metrics/raw/<YYYY-QN>/website-analytics.json`

### Inquiries
Compile a list of all inquiries received in the quarter with:
- Source (Instagram, YouTube, website, referral, other)
- First message or summary (2–3 sentences)
- Outcome (no response, consultation booked, project started, closed)

Save to: `metrics/raw/<YYYY-QN>/inquiries.json`

```json
[
  {
    "received_at": "2026-04-15",
    "source": "instagram",
    "summary": "Couple building residential home in Todos Santos, BCS. Referenced Jardín Mar. Asked about process and timeline.",
    "outcome": "consultation_booked",
    "quality_score": null
  }
]
```

---

## Step 1: Create the raw data directory

```bash
mkdir -p metrics/raw/<YYYY-QN>
```

Place all exported data files here before proceeding.

---

## Step 2: Dispatch Rafael — Metrics Report

```
@Rafael Please generate the quarterly metrics report for <YYYY-QN>.
Raw platform data is in metrics/raw/<YYYY-QN>/.
Published campaigns from this quarter are in campaigns/published/.
Previous quarter report (for comparison) is in metrics/quarterly/ — use the most recent file.
Use the template at metrics/quarterly/template.json.
Score every inquiry in metrics/raw/<YYYY-QN>/inquiries.json using the 1–3 quality scale.
Save your completed report to metrics/quarterly/<YYYY-QN>.json.
Flag high-engagement-zero-inquiry combinations explicitly.
```

**Wait for:** `metrics/quarterly/<YYYY-QN>.json`

---

## Step 3: Dispatch Carmen — Learning Brief

```
@Carmen Rafael's metrics report for <YYYY-QN> is saved at metrics/quarterly/<YYYY-QN>.json.
The creative briefs from this quarter's campaigns are in campaigns/published/*/creative-brief.json.
The published copy is in campaigns/published/*/copy.json.
The current audience segments are in docs/brand/audience-segments.md.
Synthesize the learning brief and save it to metrics/quarterly/<YYYY-QN>-learning-brief.json.
Include the FY27 progress check — we need 3–5 projects and $150K revenue annually.
```

**Wait for:** `metrics/quarterly/<YYYY-QN>-learning-brief.json`

---

## Step 4: Integrate learnings into Valentina

```
@Valentina Carmen's learning brief for <YYYY-QN> is at metrics/quarterly/<YYYY-QN>-learning-brief.json.
Please read the message_for_valentina field and the recommended_pivots section.
Integrate these learnings into your approach for the next campaign cycle.
Confirm which recommendations you are adopting and flag any you disagree with for discussion.
```

---

## Step 5: Update Lucía's intelligence baseline

```
@Lucía Carmen's learning brief for <YYYY-QN> is at metrics/quarterly/<YYYY-QN>-learning-brief.json.
Please read the message_for_lucia, audience_segment_update, and value_language_update fields.
If Carmen recommends additions or removals to the value language bank or audience segment definitions,
apply those updates to docs/brand/audience-segments.md.
Confirm what you changed and why.
```

**Wait for:** Updated `docs/brand/audience-segments.md` (if changes were recommended)

---

## Step 6: Copy latest report for easy reference

```bash
cp metrics/quarterly/<YYYY-QN>.json metrics/quarterly/latest.json
```

This ensures Lucía always has a `latest.json` to reference when analyzing future campaigns.

---

## Step 7: Commit all quarterly data

```bash
git add metrics/
git add docs/brand/audience-segments.md
git commit -m "data: quarterly review <YYYY-QN> complete"
```

---

## Step 8: FY27 progress check

Read Carmen's `fy27_progress` section from the learning brief:

```bash
python -c "
import json
brief = json.load(open('metrics/quarterly/<YYYY-QN>-learning-brief.json'))
p = brief['fy27_progress']
print(f'Qualified inquiries YTD: {p[\"qualified_inquiries_ytd\"]}')
print(f'Consultations booked YTD: {p[\"consultations_booked_ytd\"]}')
print(f'Projects closed YTD: {p[\"projects_closed_ytd\"]}')
print(f'Revenue YTD: \${p[\"revenue_ytd\"]:,}')
print(f'On track: {p[\"on_track_for_goal\"]}')
print(f'Gap analysis: {p[\"gap_analysis\"]}')
"
```

**If on track:** Continue with the next quarter's campaign priorities.

**If behind pace:** Escalate to a Priority 5 conversion campaign immediately:
```
@Valentina FY27 progress is behind pace per Carmen's Q<N> report.
Please open a Priority 5 conversion campaign cycle immediately.
Run /architect-intake to gather the strongest available project for the conversion campaign.
```

---

## Quarterly review calendar

| Quarter | Period | Review runs | Campaigns that quarter |
|---|---|---|---|
| Q1 | Apr–Jun 2026 | End of June 2026 | Habitar launch, Territorio weekly |
| Q2 | Jul–Sep 2026 | End of Sep 2026 | 2 more Habitar films, Proceso Reels, Q2 conversion |
| Q3 | Oct–Dec 2026 | End of Dec 2026 | 2 more Habitar films, Q3 conversion |
| Q4 | Jan–Mar 2027 | End of Mar 2027 | Annual review, FY28 planning |

---

## Notes

- Do not skip the raw data export step — Rafael cannot estimate platform numbers
- Carmen's recommendations are inputs, not mandates — Valentina confirms what she adopts
- The `latest.json` copy in Step 6 is important — Lucía reads it at the start of every new campaign
- If the FY27 goal is at risk, do not wait for the next cycle — trigger a conversion campaign immediately
