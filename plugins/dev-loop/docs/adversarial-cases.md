# Adversarial cases — test-first, by someone who didn't write the fix

The author of a fix writes its verification plan (Sev, Phase 2). Cases written
by the person who wrote the fix test the fix's assumptions, which is the same
conflict of interest that makes the code review clean-room. This pass applies
the same independence to *behavior*: after the approach is approved and
before implementation, one dispatched agent writes the cases Sev didn't, from
the brief's risk surface, without seeing Sev's plan.

It is a protocol, not a persona: one Sonnet dispatch, no new gate, no new
skill. Provenance: a base-control probe once refuted two review findings
that code reading had produced. Testing beat reviewing; this makes that a
step instead of a rescue.

## When it runs

Sigmund dispatches it after G-APPROACH passes when the fix is **corrective**
*and* the brief's Risk & regression surface is non-trivial: more than one
caller of a changed function, a contract or schema exposure, config- or
feature-flag-gated behavior, shared state. Or when the developer names it as a
G-CUSTOM. Otherwise it is skipped with one journal line:
`adversarial cases skipped — <reason>`. No gate row; a gate that always
auto-passes is ceremony.

## The dispatch

Sonnet (case generation from a stated surface is mechanical work). The brief
carries **only**:

- the Issue / Cause / Fix block,
- the brief's **Risk & regression surface** and **Assumptions** sections,
- `issue.md`,
- read access to the repo at the task branch.

**Not** Sev's verification plan — that is the point. The agent returns a table
in the walk-sheet schema (Case ID `A1…` · Steps · Data to stage · Expected
result · Surface item covered) that must include:

- a **base-control case**: how to show the issue on the unpatched base branch
  first, so "green after" means something;
- one case per surface item: each caller, each gated branch, null and empty
  inputs, the ordering the assumptions rely on;
- for anything it believes a local run cannot demonstrate (concurrency across
  processes, production-only data, another OS), a case marked **cannot walk
  here** with what would show it — never silently dropped.

## What Sigmund does with it

Merge into the walk sheet: Sev's cases keep their IDs, adversarial cases keep
`A` IDs, and a provenance column (S / A) says which is which. Cases that
duplicate one of Sev's are dropped in favor of Sev's ID. If an adversarial
case exposes a path the approved approach does not cover, that is a brief
re-gate to the developer — raise it now, before a line is written. Sev stages
the merged sheet in Phase 4 exactly as before; the developer walks it at
G-UI; the results are recorded per case.

Then Ellie closes the loop: her dispatch carries the recorded walk results,
and her report's Coverage section says whether the surface was walked, the
base-control went red, and the fix went green (`review-dispatch.md`).

## Recording

- Journal: `adversarial cases: <n> added, <m> merged with Sev's, <k> cannot
  walk here` or the skip line.
- Delegation log row: the dispatch, model `sonnet`.
- The walk sheet in the brief's Verification plan gains the provenance column.
