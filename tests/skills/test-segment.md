---
name: test-segment
description: Run a single segment test (A–J) against a test case. Usage: /test-segment [segment] [TC-ID]. Example: /test-segment D TC-001
allowed-tools: Agent, Read, Write, Bash, Glob
---

# /test-segment [segment] [TC-ID]

Run a single-segment QA test against a real test case.

## Parse Arguments

Extract `segment` (letter A–J) and `tc_id` (e.g. TC-001) from the command arguments.

If either argument is missing, respond:
> Usage: /test-segment [A–J] [TC-ID]
> Example: /test-segment D TC-001

## Pre-flight checks

1. Verify `tests/data/[tc_id]-seed.json` exists. If not: report "Seed data not found for [tc_id]" and stop.
2. Verify `tests/cases/[tc_id]-*.md` exists. If not: report "Test case definition not found for [tc_id]" and stop.
3. Verify the segment letter is valid (A–J). If not: report "Invalid segment. Use A–J." and stop.

## Generate run_id

```
run_id = [YYYY-MM-DD]-[tc_id]-segment-[letter]
```
Example: `2026-03-15-TC-001-segment-D`

## Create results directory

```bash
mkdir -p tests/results/[run_id]
```

## Dispatch Execution Agent

Use the Agent tool to dispatch the test-execution agent:
- subagent_type: test-execution
- Provide: run_id, tc_id, segment

The Execution Agent dispatches the Decision Gate Agent (subagent_type: test-decision-gate) internally for each deliverable in the segment. Scorecards are written by the Decision Gate Agent before the Execution Agent writes execution-complete.json.

## Wait for completion and check for failures

After the Execution Agent returns, check for results in this order:

1. Check whether `tests/results/[run_id]/[segment]-schema-fail.json` exists.
   - If it exists: read the file to extract `missing` fields. Report: "Schema validation failed for segment [letter]. Missing fields: [list]. No scorecard was produced." Stop — do not print a summary.

2. Check whether `tests/results/[run_id]/[segment]-execution-complete.json` exists.
   - If it exists: proceed to print summary.
   - If neither file exists: report "Execution agent did not produce a result for segment [letter]. The production agent may have failed to respond." Stop.

## Print focused summary

Read all scorecard JSON files from `tests/results/[run_id]/`. Print a compact summary:

```
/test-segment [segment] [tc_id] — [run_id]

Segment [letter] results:
  Agent: [name]    Deliverable: [type]    Score: [avg]/5.0    [PASS/FAIL]
  ...

Routing (Celia/Vera): [OK / FAILED at gate DG-XX]

Overall: [PASS / FAIL]
```

Do not dispatch the Gap Analysis Agent for single-segment runs.
