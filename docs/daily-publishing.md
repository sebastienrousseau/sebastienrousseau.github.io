# Daily publishing runbook

> Last Updated: June 4, 2026

The Sebastien Rousseau web platform publishes one long-form article per day across twenty-eight locales using local Claude Code sessions.
All translation and publishing work happens on your local machine to keep the process simple and secure.

## TL;DR

To publish today's article, drop your draft file into the drafts directory and trigger the publishing command in your terminal.

```bash
mv my-piece.md _drafts/2026-05-20-my-piece.md
# In Claude:
/publish-today
```

The build tool handles the draft move, language page, and commit tasks on your behalf.

## Why this design

We design this local workflow to stop the risk of exposing secret API keys to cloud runners.
The session rules allow you to inspect and approve every edit before the changes land on the disk.

## What the slash command does

The command script drives the publication checklist by executing the following steps.

- Step 1: Locate the daily draft file in the drafts directory.
- Step 2: Run the promotion script to move the draft and generate twenty-seven translation stubs.
- Step 3: Update the homepage grid and article listings to include the new post.
- Step 4: Translate each stub file in-conversation using the standard translation rules.
- Step 5: Run the local build tests and push the signed commit to deploy the updates.

## Header contract for the draft

The build tool expects the draft header block to list the standard page tags.
These tags include the title, details, layout, schema, language, and banner image info.

## Timing

The publishing routine runs on demand when you finish writing your article.
You can push changes at specific UTC hours to align the release of new content with active publishing times.

| You push at (UTC) | Catches |
|-------------------|---------|
| **06:30** | Pre-business London, mid-day Mumbai, mid-afternoon Tokyo, fully warm by NY market open |
| **13:00** | NY pre-market, end-of-business London, evening Singapore |
| **22:00** | LA mid-afternoon, NY evening, Tokyo overnight (catches APAC morning) |

The early morning slot has the most reach because the POP servers are warm before the traffic waves.

## Language rules

The language rules require a clear tone and direct text matching for all blocks.
You must preserve the markdown structure, translate citation texts, keep standard short terms, and update header details.

## Safety rules

Running the command many times is safe and will not overwrite existing pages.
The script checks for language stubs and only makes files for languages that are missing.

## Failure modes + fixes

The table lists common publishing errors, their causes, and how to fix them.

| Symptom | Fix |
|---------|-----|
| No draft found | Drop a draft file with today's date prefix |.
| Parity check fails | Re-run the translation script to regenerate the missing slug mappings |.
| Link check fails | Check the alternate language URLs in the frontmatter blocks |.
| CSP check fails | Verify that all inline script blocks carry the correct hashes |.
| Push fails | Load your signing key into the local ssh agent |.

## What is NOT automated on purpose

We do not automate tasks that need human choice or access to secret keys.
These tasks include editing the main cards and managing the GPG keys.
