---
name: approve-campaign
description: Use after the CEO has approved a campaign. Confirms the approval, moves the campaign to approved/, dispatches Canal to publish in sequence, and closes the campaign into published/ when all posts are live.
---

# Approve and Publish Campaign

Executes the publish phase after CEO approval is confirmed.

**Usage:**
```
/approve-campaign <campaign-id>
```

---

## Step 1: Confirm CEO approval

```bash
cat campaigns/pending/<campaign-id>/ceo-decision.json
```

The `decision` field must be `"approved"`. If it is anything else, do not proceed.

---

## Step 2: Move campaign to approved

```bash
mv "campaigns/pending/<campaign-id>" "campaigns/approved/<campaign-id>"
```

Verify the move:
```bash
ls campaigns/approved/<campaign-id>/
```

You should see: `brief.json`, `copy.json`, `strategy.json`, `visual-plan.json`, `approval-package.json`, `ceo-decision.json`, `assets.json`

---

## Step 3: Dispatch Canal

```
@Canal The CEO has approved campaign <campaign-id>.
All files are in campaigns/approved/<campaign-id>/.
Please review the strategy.json post sequence and begin publishing in order.
Check depends_on_sequence for each post before publishing.
Update publish-log.json after each post goes live.
```

---

## Step 4: Canal publishes each post

Canal will work through the sequence. For each post, depending on platform:

**Website (Cargo):**
```bash
python publisher/scripts/publish-cargo.py <campaign-id> <sequence-number>
```

**Instagram** (until API credentials are configured):
Canal will output the exact copy, assets, and framing instructions. Post manually, then confirm the live URL to Canal.

**YouTube** (until API credentials are configured):
Canal will output the exact title, description, and thumbnail instructions. Upload manually, then confirm the live URL to Canal.

---

## Step 5: Confirm all posts are live

When Canal reports all sequences are published, verify the publish log:

```bash
cat campaigns/approved/<campaign-id>/publish-log.json
```

Check that:
- Every sequence from `strategy.json` has a corresponding entry in `posts_published`
- Each entry has a `url` (not empty)
- `status` is `"published"` for all entries

---

## Step 6: Close the campaign

```bash
python publisher/scripts/move-to-published.py <campaign-id>
```

This records the completion timestamp and moves the campaign to `campaigns/published/`.

---

## Step 7: Notify Rafael

```
@Rafael Campaign <campaign-id> is complete and in campaigns/published/.
Please add it to your tracking list for the next quarterly Pulso report.
The published URLs are in campaigns/published/<campaign-id>/publish-log.json.
```

---

## If a post fails to publish

If Canal reports a platform error (image rejected, API failure, caption too long):

1. Do not workaround or modify the content
2. Note the exact error
3. Notify Valentina:

```
@Valentina Canal encountered an error publishing sequence <N> of campaign <campaign-id>.
Error: [exact error message]
Please advise on how to proceed.
```

Valentina will determine whether a revision is needed or if the error can be resolved technically.

---

## Notes

- Never skip the CEO confirmation check in Step 1
- Publish sequences in the exact order Canal follows from `strategy.json`
- If a publish date is in the future, Canal will note it and pause — do not force early publication
- Instagram and YouTube API credentials can be added to `publisher/.instagram-credentials.json` and `publisher/.youtube-credentials.json` respectively to enable automated posting when ready
