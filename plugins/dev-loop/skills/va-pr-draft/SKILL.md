---
name: va-pr-draft
description: Draft a Pull Request body in a terse, reviewer-focused format for the developer's own GitHub repos. Use whenever the user asks to write, draft, polish, or restructure a PR description for a code change.
---

# PR Draft Skill

> **Dev profile first.** Read `~/.claude/va-profile.md` before anything else; wherever this
> skill says *profile:X*, substitute that file's value. Missing → stop and offer `/va-workflow-setup`.

You are drafting a Pull Request body for the developer named in the dev profile. The reviewer may be the developer themselves, a collaborator, or a future reader scanning history, so write for someone who has not seen the issue or the code.

## Tone and voice

- **Professional, direct.** Match the user's own tone — not formal, not casual.
- **Terse over verbose.** Cut anything that doesn't earn its place. No filler sentences ("This PR aims to…", "In conclusion…", etc.). No marketing language.
- **Reviewer-first.** Every section should answer a question a reviewer would otherwise have to ask.
- **First person singular where a person speaks.** "I couldn't reproduce this on Windows", "I verified against the staging build" — never "we". Most sections are impersonal; where one isn't, it's the developer.
- **No emojis** except the lightweight `✓` / `✗` used in comparison tables.

## Required section order

Use this exact order. Omit a section only if it has no content; never reorder.

1. `## Summary` — What the change does and why, in plain language. Describe prior behaviour and what happens now, and **explicitly state what is NOT affected** in the last sentence.
2. `## Root Cause` — For fixes: 2–4 sentences or a short comparison table identifying the module/function that owned the bug. If the bug couldn't be reproduced, say so and explain why. Omit for features.
3. `## Changes` — Bulleted list. Each bullet starts with `path/to/file :: function_name()` followed by ` - ` (a plain hyphen, not an em dash) and a one-line description of the change and its purpose.
4. `## Files with Changes for Review` — Compact list of changed files with one-line scope (e.g. "1 import, 1 helper, 8 line edits").
5. `## Why this is safe` — Only include when the change has non-obvious safety properties (feature-flag gating, backwards compatibility, migration ordering). Numbered list of safety nets.
6. `## Linked Issues` — `Closes #<n>` (so merging closes the issue) or `Refs #<n>` when the PR only partly addresses it. List each on its own line.
7. `## Test Plan` — Reference the approach brief's Verification plan (or an attached test plan file) by name. Then a checkbox list — one box per test case, prefixed with the case ID (A1, B2, etc.) when the plan uses them. Use `[x]` for executed/passed, `[ ]` for not-run, and annotate skipped cases with a brief reason in italics.
8. `## Development Checklist` — Use the verbatim template in **Development Checklist template** below.

## Title convention

`<Verb-first, specific summary> (#<n>)`

- Verb-first, present tense ("Fix recurring duplicates in the importer", "Add retry to the upload client"). Not "Fixes for…" or "Adjustments to…".
- Keep under ~72 chars. If the repo uses conventional commits (`fix:`, `feat:` — check `git log`), follow that instead.

## Label recommendation

Suggest labels at the top of the response (above the PR body), chosen from the repo's existing label set (`gh label list`): a type label (`bug`, `enhancement`, `docs`, …) and, if the repo uses one, a size or review-effort label. Never invent labels the repo doesn't have.

## Formatting rules

- **Markdown tables** for change inventories with file+line+description, root-cause path comparisons, before/after behaviour. Tables outperform bullet paragraphs for review scannability.
- **Fenced code blocks** carry the language tag (` ```python `, ` ```ts `, ` ```csharp `). Keep snippets to ≤20 lines — link to file paths instead of pasting more.
- **File paths use forward slashes** and are relative to the repo root.
- **Function references** use the form `function_name()` with parentheses, and where a file path is also given, separate them with ` :: ` (`importer.py :: dedupe_rows()`).
- **Line numbers** in change tables are valuable — keep them when provided, but warn the user to verify them post-rebase.

## Content rules

1. **State what is NOT changed.** A single sentence at the end of `Summary` preempts the reviewer's biggest question.
2. **Ordering-sensitive edits get inline justification.** If a transformation must happen *after* a lookup (or *before* a serialization step, etc.), say so in the change row.
3. **Gated changes name the gate.** If the change is behind a flag or config value, call out the gate explicitly and explain why the default path is unaffected.
4. **Test plan checkboxes match the attached plan.** When there is a plan, mirror its case IDs exactly — don't renumber. Mark cases not executed with `[ ]` and an italic reason (`*not checked (path unmodified)*`).
5. **No speculative changes.** Do not list "potential future improvements", "could also refactor X", or "considered Y but…". Keep the PR scope tight.
6. **Plain-language Summary, engineering Root Cause.** The first section should be understandable without reading the code (no internal function names). The Root Cause section is where the engineering detail lives.

## Information to gather before drafting

If any of these are missing, ask before writing. Don't fabricate or guess:

1. The issue number (and any related issues or PRs).
2. Branch name and target branch.
3. One-line summary of the change.
4. Before-behavior and after-behavior.
5. List of changed files (paths + functions + line numbers where possible).
6. Anything intentionally not changed that a reviewer might expect to see changed.
7. Test plan — file attachment, or list of executed test cases with pass/fail.
8. Whether the change is gated by a flag/config and how it was exercised.
9. Build, test, and lint result (zero new warnings expected).
10. Approximate diff size, for label selection.

## The humanize gate

A PR body is read by reviewers and often quoted into release notes, so **run the
humanize pass before presenting it** (`../../docs/humanize-gate.md` from this
skill's base directory). Dispatch a subagent that loads the plugin's
`va-humanizer` skill and hand over the finished body only. The anti-patterns
below apply either way — the pass removes what slipped through, it doesn't
excuse drafting the tells in.

## Output format

Always produce **two** artifacts in the initial response:

1. A short header above the code block with: suggested title, suggested labels, and any caveats the user should verify before posting (line numbers, issue state, etc.).
2. A single fenced markdown file block named `pr-<issue number>-body.md` containing the PR body, ready to paste directly into the GitHub "Description" field (or pass to `gh pr create --body-file`).

Do not produce alternate versions, "concise vs. detailed" variants, or commentary inside the code block. Do not open the PR yourself: opening it is a G-PR-OPEN decision that needs the developer's explicit go-ahead.

## Development Checklist template

Use this verbatim. Match the heading structure (H3 subsections under the H2). The boxes default to checked because they reflect the standard hygiene the developer completes before opening a PR. That default is not license to blanket-check, though: uncheck any item that genuinely isn't done for the PR at hand (for example, if the branch hasn't been rebased, or the tests weren't run).

```markdown
## Development Checklist

### Code

- [x] The changes follow the project's coding conventions.
- [x] The branch builds and the test suite passes, with no new warnings.
- [x] Docs and changelog are updated where the change is user-visible.

### Pull Request

- [x] The correct base branch is targeted.
- [x] The Summary accurately reflects the scope and nature of the changes.
- [x] The linked issue is referenced (`Closes #<n>` / `Refs #<n>`).
- [x] The branch has no merge conflicts.
```

## Follow-up step: the issue comment

After the user has reviewed, edited, and signaled the PR body is finalized — typically by pasting back an edited version, or saying "looks good", "ready to push", "I posted it", etc. — offer a short comment for the issue that says the PR is up and what it does. Draft it from the finalized Summary and Root Cause, run it through the humanize gate, and post it only on explicit approval. It is a separate artifact from the PR body.

## Anti-patterns to avoid

- ❌ "This pull request introduces…" / "The purpose of this PR is to…" — start with content, not throat-clearing.
- ❌ Repeating the Summary in the Changes section in different words.
- ❌ Blanket-checking the Development Checklist when items aren't actually done.
- ❌ Markdown headings deeper than `###`.
- ❌ Long prose paragraphs where a table would do.
- ❌ Listing files in three separate sections (Summary, Changes, Files for Review) with the same content — each section has a distinct purpose: Summary = what+why, Changes = where+how, Files for Review = scope-at-a-glance.
- ❌ Including draft commit messages, branch-setup commands, or local build instructions in the PR body.
