---
name: va-share-learning
description: >-
  Capture a just-resolved gotcha so it is recalled instantly next time. Use whenever
  an annoying problem gets diagnosed and fixed — build quirks, environment surprises,
  runtime behavior, tooling traps. Trigger on "/va-share-learning", "write that up",
  "capture that gotcha", "so I don't hit this again", or proactively offer it after
  any painful debugging detour resolves.
---

# va-share-learning — gotcha capture

> **Dev profile first.** Read `~/.claude/va-profile.md` before anything else; wherever this
> skill says *profile:X*, substitute that file's value. Missing → stop and offer `/va-workflow-setup`.

1. **Draft the learning** from the conversation: `YYYY-MM-DD-short-slug.md` with four
   sections — Symptom (what it looked like) · Root cause · Resolution (exact commands/
   edits) · Applies to (repo/area/tool). One screen max; terse beats complete.
2. **Classify it.** Specific to one repo or machine (local paths, local config) → save to
   that repo's `.claude/docs/learnings/` (or `*profile:Workspace root*\.claude\docs\learnings\`
   when it spans repos) and stop. Useful across projects → also step 3.
3. **Land it in the plugin.** Write the file into the plugin clone's
   `*profile:Workspace root*\va-claude-skills\plugins\dev-loop\docs\learnings\` and add its
   one-line catalog entry to that directory's `README.md`. Commit it on a `learning/<slug>`
   branch and, with permission, open a PR against your own repo; merging it is what makes
   every project's Sev and Ellie see it.
4. Never include credentials, tokens, or machine-identifying values in the learning.
