# Superpowers routing — which technique skill for which moment

The `superpowers:*` skills (separate plugin) supply *technique*: how to brainstorm a
design, debug systematically, write tests first, verify before claiming done. The
dev-loop supplies *structure*: stages, gates, the ledger, who may act. Sigmund picks the
technique that fits the moment; the technique never replaces a stage or a gate.

## Precedence (read first)

1. **Dev-loop gates always win.** No superpowers skill can waive, skip, or satisfy
   G-READINESS, G-APPROACH, G-UI, G-PR-OPEN, G-MERGE, or G-ISSUE. If a skill's own steps
   say "get approval", "merge", or "open the PR", that happens at the dev-loop gate, in
   the dev-loop way (`va-pr-draft`, the developer's click).
2. **Artifacts land where the loop says.** Specs, plans, and findings from a superpowers
   skill go into `brief.md` (design and plan), `reviews\` (review reports), or the ledger
   journal, not into new files scattered in the repo. A skill that wants to commit
   something commits under the confidence check (`../../docs/confidence-check.md`).
3. **Reviews stay Ellie's.** The clean-room dispatch (`../../docs/review-dispatch.md`) is
   the review. Do not run `superpowers:requesting-code-review` in addition or instead.
4. **Not installed? Carry on.** Before routing, check the skill is actually available
   (it appears in the skills list). If not, do the step the built-in way and journal
   `superpowers not available — <skill> skipped` once per task. Never fail a stage over it.
5. **Hat-swap, not dispatch,** for technique skills that talk to the developer
   (brainstorming) or change code (TDD, plans). Pure information gathering
   (`dispatching-parallel-agents`) dispatches on Sonnet per the usual tiers. Ellie, once
   dispatched, loads no superpowers skills: she is read-only and clean-room.
6. **One line in the ledger.** Each time you invoke one, add `superpowers:<name> · <why>`
   to the session journal. That is how a later retro sees what shaped the run.

## The routing table

| Moment | Condition | Use |
|---|---|---|
| Intake → Planning (Sev Phase 1–2) | **Additive** task: a feature, a behavior change, anything with open design questions | `superpowers:brainstorming`. Its questions and design become the brief's Approach and Alternatives; its output is `brief.md`, approved at G-APPROACH |
| Planning (Phase 1) | **Corrective** task, a bug, a failing test, unexpected behavior | `superpowers:systematic-debugging` before the brief's Cause beat is written. The Cause stays "not established" until it finds one |
| Planning, after G-APPROACH | Approved brief has several dependent steps | `superpowers:writing-plans`; the plan is appended to `brief.md` under *Implementation plan*. Skip for a change that fits in one sitting |
| Start of Execution | Work should be isolated from the developer's current checkout, or tasks run in parallel | `superpowers:using-git-worktrees` |
| Execution (Phase 3) | The repo has a test suite or the change is testable | `superpowers:test-driven-development` |
| Execution | An approved plan with steps to carry out | Small or tightly coupled: `superpowers:executing-plans` inline. Large with independent tasks: `superpowers:subagent-driven-development` (dispatches follow Sigmund's model tiers: Sonnet floor, session model for anything that judges or writes production code) |
| Planning or Execution | Two or more independent investigations or fixes with no shared state | `superpowers:dispatching-parallel-agents` |
| Verification, before the G-UI handover and again before Delivery | Always | `superpowers:verification-before-completion`: run the build, tests, and lint and show the output before saying anything passes |
| Verification, triage loop | Ellie's findings come back | `superpowers:receiving-code-review` for Sev applying them: verify each finding against the code, push back on wrong ones, never comply blindly |
| After G-MERGE | A worktree or task branch is left to clean up | `superpowers:finishing-a-development-branch`, **cleanup only**. Never to merge or open the PR; those are G-MERGE and G-PR-OPEN |
| Any task that edits a skill or this plugin | The repo under change contains `SKILL.md` files | `superpowers:writing-skills` |
| Developer says a superpowers run went badly | Asked explicitly | `superpowers:diagnosing-superpowers` |

`superpowers:using-superpowers` governs session start and needs no routing.

## Choosing between neighbours

- **brainstorming vs. writing-plans:** brainstorming decides *what and why* (before
  G-APPROACH); writing-plans decides *the order of the work* (after it). Never write a plan
  for an approach the developer hasn't approved.
- **TDD vs. a task with no tests:** if the repo has no test suite, don't invent one for a
  small fix; follow the brief's Tests line (propose tests only where they earn their keep).
- **executing-plans vs. subagent-driven-development:** default to inline. Move to
  subagent-driven only when the steps are independent and large enough that keeping them
  out of this context is worth the dispatch cost.
- **verification-before-completion vs. G-UI:** verification covers what the agent can
  prove (build, tests, lint, logs). G-UI is the developer's own walk and is never
  self-certified.

## Dev Review mode

Reviewing someone else's PR uses almost none of this: Ellie reviews, Sigmund triages. Use
`systematic-debugging` only if a finding turns on why something fails, and
`verification-before-completion` before telling the author the build and tests pass. On
"take over", the authoring rows above apply from Planning onward.
