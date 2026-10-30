# <KEY> — <Title>

- **Issue:** https://github.com/<owner>/<repo>/issues/<n>
- **Stage:** Intake | Planning | Execution | Verification | Delivery | Closeout | Done — <one-line qualifier>. Non-progress values: `Blocked — on <whom>` (waiting on someone who isn't the developer) · `Closed — <reason>` (bounced at readiness, parked, superseded, abandoned)
- **Posture:** lead | pair
- **Repos / branches:** <repo> · <branch> (base: <base branch>)

## Artifacts

- **Brief:** `brief.md` · **Issue snapshot:** `issue.md` (pulled <YYYY-MM-DD HH:MM>) · **Reviews:** `reviews\` · **Attachments:** `attachments\`
- **PR:** — · **Issue:** <link above> · **Learnings:** —

## Now / Next

- **Last done:** <YYYY-MM-DD HH:MM — one line>
- **Next action:** <one line>
- **Waiting on:** <who/what, since when — or none>

## Goal & Definition of Done

<One-paragraph goal in plain language.>

- [ ] Acceptance criteria met (list them or link the issue)
- [ ] Clean build, tests pass (zero new warnings)
- [ ] Clean-room Ellie review passed / findings resolved
- [ ] PR merged (`Closes #<n>`)
- [ ] Issue closed with a summary comment
- [ ] Learnings captured
- [ ] Metrics computed; ledger closed; INDEX updated with totals

## Intake

### Readiness
- Reported: <one line>
- Expected: <one line>
- Produced by: <one line>
- Suspected area: <one line>
- Verdict: HIGH | LOW | NOT_A_BUG
- Fix classification: corrective | additive — <one-line rationale>

### Issue / Cause / Fix
<Filled after exploration — at the approach gate on a normal task, at review
intake on a Dev Review. The readiness block above is the hypothesis; this is
the answer. See ../../docs/issue-cause-fix.md, from the skill's base dir.>
- **Issue:** <the confirmed behavior, not the issue's version>
- **Cause:** <the mechanism, cited file:line> | not established — <what was ruled out>
- **Best fix:** <the recommendation, and why over the alternative>
- **Changed from intake:** <only when it diverges from the readiness restatement>

### Effort forecast
<The stops the developer will be needed at, with rough durations — as
presented in the intake You-Are-Here block. Note any G-CUSTOM gates named.>

## Pipeline state

| Gate | Status | When | By |
|---|---|---|---|
| G-READINESS | pending | | |
| G-APPROACH | pending | | |
| G-UI | pending | | |
| G-PR-OPEN | pending | | |
| G-MERGE | pending | | |
| G-ISSUE | pending | | |

<Dev Review: replace these rows with the review gate set in
references/dev-review.md at intake. Add G-CUSTOM rows named at intake. G-COMMIT/G-PUSH events are journaled, not
tabled — they recur. Status is exactly one of `pending`, `passed`, `auto-passed`,
`n/a`, `waived`; no bold, no prose — the INDEX regeneration parses this column.>

## Decision log

| # | Gate | When | Question | Decided by | Decision |
|---|------|------|----------|------------|----------|

<A row with a Question but no Decision is pending. Gate holds the gate id, or
`—` for a non-gate decision. Timestamps are `YYYY-MM-DD HH:MM`.>

## Review outcomes

| Round | Reviewer | Raised | Valid (applied) | Invalid (pushed back) | Worst valid severity |
|---|---|---|---|---|---|

<Severity scale: Blocker | Should-fix | Nit — apply to Copilot rounds too.>

## Metrics

Sessions (record at every wake-up):

- session: <session-id> · stage: <stage-at-wake-up>

<!-- metrics:begin -->
*(written by `scripts/task_metrics.py --write` at the delivery package; re-run at closeout only if sessions were added)*
<!-- metrics:end -->

## Session journal

- <YYYY-MM-DD HH:MM>: <what moved, one or two lines — including the
  G-COMMIT/G-PUSH auto-pass lines in the format `docs/confidence-check.md` pins>

## Delegation log

| Date | To | Model | What | Outcome |
|------|----|-------|------|---------|

<Model = the model the work actually ran on (`opus`, `sonnet`, `—` for
scripts) — never a tier label.>
