---
name: test-full-run
description: Run a full end-to-end test for one test case across all 10 segments. Usage: /test-full-run [TC-ID]. Example: /test-full-run TC-001
allowed-tools: Agent, Read, Write, Bash, Glob
---

# /test-full-run [TC-ID]

Run a complete QA test across all 10 segments (A–J) for one test case, then produce a gap analysis report.

## Parse Argument

Extract `tc_id` from the command argument.

If missing, respond:
> Usage: /test-full-run [TC-ID]
> Example: /test-full-run TC-001
> Available: TC-001, TC-002, TC-003, TC-004, TC-005, TC-006, TC-007, TC-008

## Pre-flight checks

1. Verify `tests/data/[tc_id]-seed.json` exists.
2. Verify `tests/cases/[tc_id]-*.md` exists.
3. Verify all 20 rubric files exist in `tests/rubrics/`.

If any check fails, stop and report what is missing.

## Generate run_id

```
run_id = [YYYY-MM-DD]-[tc_id]
```
Example: `2026-03-15-TC-001`

## Create results directory

```bash
mkdir -p tests/results/[run_id]
```

## Execute segments sequentially

For TC-007 (bad lead), run Segment A only. Stop after Lupe's discard is confirmed.

For all other TC-IDs, run segments A through J in order. Each segment depends on the previous:

1. Dispatch test-execution agent: segment=A
2. Wait for segment-A-execution-complete.json
3. Dispatch test-execution agent: segment=B
4. Wait for segment-B-execution-complete.json
5. Continue through segment=J

If any segment writes a schema-fail.json: stop execution at that segment (do not continue downstream segments). Then proceed to dispatch the Gap Analysis Agent — it will include the schema failure in its Critical Findings report.

## Dispatch Gap Analysis Agent

After all segments complete (or after TC-007 single-segment run), dispatch:
- subagent_type: test-gap-analysis
- Provide: run_id, tc_id

Wait for gap analysis to complete. Completion is confirmed when `tests/results/[run_id]/run-summary.md` exists. For TC-007 runs, `gap-analysis.md` is intentionally not produced — the run-summary.md alone is sufficient.

## Print pass/fail summary

Read `tests/results/[run_id]/run-summary.md` and print it in full.

Then add:
```
Full results: tests/results/[run_id]/
Gap analysis: tests/results/[run_id]/gap-analysis.md
```
