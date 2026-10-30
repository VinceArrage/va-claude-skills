# Dev Review mode — reviewing someone else's PR

The task handed over is not yours to *build* — it's someone else's finished
work (a contributor, a collaborator, a dependency bot), with a PR already open
on one of the developer's repos, handed to you as the **reviewer of record**.
It has its own gates, its own DoD, and its own Stage grammar rather than a
bent version of the authoring pipeline.

**What's different from a normal task:**

- **You are not the author.** Fixes route back to the *external author* (PR
  review comments), **not** to Sev, until the developer says "take over"
  (below).
- **You enter at Verification.** Intake collapses to review-intake: readiness
  on the linked issue (or the PR description when there is none), confirm the
  engagement is a review, and the **Issue / Cause / Fix** summary you write
  yourself from the diff and the issue. No Planning, no Execution, no Sev
  `brief.md`.
- **The task key is the PR:** `<repo>-pr<n>`.
- **The gate table is the review set** (below), swapped in at intake in place
  of the authoring rows, so nothing sits "pending" that will never fire.

## Stage line and INDEX

Write the Stage line as `Dev Review · <step>`, where step is one of: `intake`,
`review out`, `comments sent`, `awaiting author`, `merge`, `notify`, `done`.
The two non-progress values (`Blocked — on <whom>`, `Closed — <reason>`) apply
as everywhere. INDEX shows the step verbatim.

## The gate set (replaces the authoring rows at intake)

| Gate | Fires at | Owner | Auto-pass |
|---|---|---|---|
| G-REVIEW-INTAKE | Issue / Cause / Fix stated, engagement confirmed | Agent (developer on a design objection) | When beat three agrees with the author |
| G-COMMENTS | Findings drafted for the author | Developer (approves the text; it is a PR write) | Never |
| G-MERGE | The PR | Developer's click | Never |
| G-NOTIFY | Closing comment to the author | Developer (PR/issue write) | Never |

## The track

1. **Issue / Cause / Fix** (`../../docs/issue-cause-fix.md`, from the skill's
   base dir): what was wrong, why, and — since the author has already chosen a
   fix — whether that fix is the right one. For the diff walk you may dispatch
   a Sonnet gatherer and write the beats from its summary; the judgment stays
   yours, and read the actual hunks yourself whenever a finding turns on them.
   Agreeing with the author is a fine answer. Disagreeing is a **design**
   objection for the developer and the author now, not for Ellie's convention
   pass later: raise it here, because it can moot the review.
2. **Clean-room review** — auto-dispatch Ellie on the PR diff exactly as
   always (the author's "no review needed" is never a waiver), with the
   author's stated test cases so her Coverage section can say whether they
   cover the surface. Arbitrate.
3. **Comments to the author (G-COMMENTS)** — valid findings go to the author
   as PR review comments, humanized, approved by the developer. If the
   developer waves the review through, record that and skip. Re-review only
   when the author pushes new commits; the Stage line sits at `awaiting author`
   in between.
4. **Build and test locally** — check out the PR (`gh pr checkout <n>`) and
   run the repo's build and tests. Green CI and the author's "works for me" are
   corroboration, not a substitute.
5. **G-MERGE** — the developer's click.
6. **Notify (G-NOTIFY)** — thank the author and close out on the PR (and the
   linked issue, if the merge didn't close it), humanized.

## Takeover

When the developer says "take over", the task changes hands, not folders.
Record the decision in the Decision log, set the Stage line to `Execution` with
a `taken over from <author> <date>` qualifier, add the authoring gates that now
apply (G-APPROACH for the revision brief, G-UI, G-PR-OPEN if a new PR is
needed) beneath the review rows, and mark G-COMMENTS `n/a — taken over`. Sev
enters at Planning for the revision with the review findings as his input; the
rest is the normal pipeline. The same ledger keeps the whole story.

**Dev Review DoD (tailor at intake):** Issue / Cause / Fix stated · clean-room
review resolved (or waved by the developer) · build and tests verified locally
· PR merged · author notified · ledger closed.

Everything else — single-writer ledger, decision batching, the humanize gate
on every comment — is unchanged.
