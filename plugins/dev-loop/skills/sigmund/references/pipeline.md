# The pipeline — stage machine and gate registry

This is Sigmund's operational spec. Advance stage by stage; a stage exits only
when its exit criteria hold; gates block until their owner acts (or their
auto-pass condition is met). All control flow lives here — none hidden in
delegates.

## Stages

| # | Stage | Actions (automated) | Delegate | Exit criteria |
|---|---|---|---|---|
| 1 | **Intake** | Task folder + ledger created; GitHub issue pulled once with `gh issue view` → `issue.md` snapshot (the run reads this, not the live issue — live pulls only on developer request or read-before-write at G-ISSUE); no issue yet → offer to open one (`gh issue create`, an issue write, so it asks); readiness check (`../../docs/readiness-check.md` from the skill's base dir); DoD pinned; effort forecast stated (see below); INDEX regenerated | — | Verdict HIGH · classification clean · DoD agreed · forecast given |
| 2 | **Planning** | Context build; **Issue / Cause / Fix** summary written and led with (`../../docs/issue-cause-fix.md`); approach brief (incl. verification plan) → `*profile:Tasks dir*\<KEY>\brief.md`; classification re-checked in brief; after G-APPROACH, adversarial cases (`../../docs/adversarial-cases.md`: one Sonnet dispatch, risk-gated, or skipped with the reason journaled) merged into the walk sheet | `sev` (Phases 1–2) | Issue/Cause/Fix stated · **G-APPROACH** passed |
| 3 | **Execution** | Implementation to the repo's conventions; build and test early and often with the repo's own commands; commits/pushes under G-COMMIT/G-PUSH | `sev` (Phase 3) | Clean build · tests pass · zero new lint/compiler warnings |
| 4 | **Verification** | Run the app locally; stage the walk sheet (Sev's cases + adversarial); **G-UI** walk, results recorded per case; auto-dispatch clean-room Ellie with those results (`../../docs/review-dispatch.md`); triage loop until resolved; record review outcomes | `ellie` | Behavior verified · findings resolved |
| 5 | **Delivery** | PR body draft (with `Closes #<n>` so the merge closes the issue); **G-PR-OPEN**; Copilot/CI loop at each wake-up (recorded); then ONE package: **G-MERGE** + **G-ISSUE** closing comment; `task_metrics.py --write` runs here, while the developer is present | `va-pr-draft` | PR merged · issue closed with its summary comment |
| 6 | **Closeout** | DoD check; learnings; `task_metrics.py --write` only if sessions were added since the package; `task_metrics.py index --write` | `sev` (Phase 5) | Ledger closed |

**Delivery batches into exactly two stops:** the PR open (the PR must exist
before Copilot and CI can run on it), then one delivery package — merge click
and the pre-drafted issue closing comment — presented together.

**Two non-progress states**, both written on the ledger's Stage line and neither
a stage: `Blocked — on <whom>` when the task waits on someone who isn't the
developer (an upstream maintainer, a dependency release) — it stays active in
INDEX with the wait visible; `Closed — <reason>` when a task leaves the loop
without merging (bounced at readiness, parked, superseded, abandoned) — INDEX
counts it as done.

## Issue snapshot format (`issue.md`)

Written at intake, refreshed on every live pull — always a whole-file rewrite,
never an append. Pull with
`gh issue view <n> --repo <owner/repo> --json number,title,state,labels,milestone,author,assignees,body,comments`.
Sev, Ellie, and PR drafting read this file instead of the live issue, so keep
the headings exact and never omit a section (write "— none" if the issue has
nothing there):

```markdown
# <owner/repo>#<n> — <Title>

- **Pulled:** YYYY-MM-DD HH:MM
- **Labels:** <list or —> · **State:** open | closed · **Milestone:** <name or —>
- **Author / Assignees:** <logins>

## Description

<verbatim from the issue body>

## Acceptance criteria

<list — or "— none stated">

## Comments

- <YYYY-MM-DD HH:MM> — <author>: <comment; condense only when long, keep decisions verbatim>
```

The **Pulled** timestamp is the load-bearing line: it is how any reader judges
staleness, and what the refresh-on-live-pull rule updates.

## Gate registry

| Gate | Fires at | Owner | Auto-pass |
|---|---|---|---|
| G-READINESS | Intake | Agent self-verdict (developer on any stop) | HIGH + corrective only |
| G-APPROACH | End of Planning | Developer | Never |
| G-UI | Verification test walk | Developer | Never (inherently human); `n/a` when the change has no runnable surface (a library with full test coverage, docs only) — journal why |
| G-COMMIT | Any commit | Developer | **Task-branch confidence check** |
| G-PUSH | Any push | Developer | Confidence check + same-branch; no force, no delete |
| G-PR-OPEN | Delivery | Developer | Never |
| G-MERGE | Delivery | Developer | Never — always the developer's click |
| G-ISSUE | Every issue write (create, comment, label, close) | Developer | Never |
| G-CUSTOM-\<name\> | As named at intake | Developer | As specified |

G-READINESS is a gate, not paperwork: the readiness stops (LOW, NOT_A_BUG,
bug-labelled issue + additive fix) count in the gate tally like any other gate,
not as intake notes.

**A G-CUSTOM auto-pass may only be narrower than the gate it adds.** It can
never grant autonomy the standing registry withholds — a custom row is a way to
stop more often, never less.

**Dev Review has its own gate set** (`dev-review.md`), swapped in at intake;
the standing-gate rules below apply to it unchanged.

**Standing gates are always armed.** "Arming" only ever *adds* gates — nothing
removes one, at any posture.

Record every gate pass in the ledger's Pipeline state table (Status, When, By)
**before** presenting the next thing to the developer. Status takes one of five
values: `pending`, `passed`, `auto-passed`, `n/a`, `waived`.

## Task-branch confidence check (G-COMMIT / G-PUSH auto-pass)

The six conditions live in **`../../docs/confidence-check.md`** (from the
skill's base dir) — the single authority Sigmund and Sev both follow, along
with the auto-pass journal-line format and the always-ask list (`stash`,
branch switch, `reset`, branch/remote-branch delete). Any condition failing
or unverifiable → explicit per-action permission, exactly as before.

## Effort forecast (intake)

Scope cheaply at intake (likely files, repos touched, public API/schema
exposure, risk surface) — not to label the task, but to tell the developer
what it will cost *them*: which stops they'll be needed at and roughly how
long each takes. Deliver it in the intake You-Are-Here block — e.g. "You:
approach sign-off (~5 min), the UI walk (~15 min), the merge click. Est. 2
sessions." — and record it in the ledger's Intake section.

Extra stops are always available: G-CUSTOM gates the developer names at
intake add Pipeline-state rows and are enforced like any other gate. When
scoping surfaces risk, propose them yourself ("want to see the diff before
the Ellie dispatch?"). For a genuinely large task — multi-repo, API/schema
exposure, mechanism unclear after recon — propose pair posture rather than
running ahead.
