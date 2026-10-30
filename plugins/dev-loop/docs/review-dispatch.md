# Clean-room review dispatch (Ellie)

How reviews run. Shared by **Sev** (Phase 4) and **Sigmund** (Verification
stage) — this file is the single authority on the protocol; the skills point
here rather than restating it.

**Reviews always dispatch — never in-session.** An in-session reviewer
inherits the author's context and rationalizations — the exact bias that
softens a review. When implementation completes, dispatch the clean-room
review *without asking* (a standing default of this plugin).

**The dispatch:**

- Spawn a fresh-context subagent instructed to load and follow the `ellie`
  skill and return its findings.
- Brief it with ONLY: the diff or branch, the issue reference plus acceptance
  criteria, and the brief path (`Tasks\<KEY>\brief.md`) — none of the
  author's reasoning or session context. Once the developer has walked the
  sheet, add the walk sheet with its recorded per-case results, so her
  Coverage section has something to check against (`adversarial-cases.md`).
  One instruction goes with the brief path: write the report's §2 root cause
  *before* reading the brief's Issue / Cause / Fix head, then note in §2
  whether the two agree. An independent cause is the one thing the brief must
  not hand her.
- **The brief must restrict side effects.** Ellie reads code and writes her
  report, nothing else: no commits, no pushes, no writes to GitHub (no
  comments, reviews, labels, or closing issues), no deploys, no changes to
  the developer's main checkout. The one extra thing she may do is build and
  run the tests inside a throwaway worktree (`git worktree add`) so the
  developer's working tree is untouched. Say this explicitly: a dispatched
  agent has no developer to ask, so it will take any offer in the skill text
  unless told not to.
- Reviews are judgment work: dispatch on the **session model** (Sonnet is
  the plugin's floor for any dispatch, but reviews don't ride the floor),
  and announce the dispatch as you make it — one line naming who, what, and
  the actual model ("Dispatching Ellie on Opus — clean-room review of the
  diff"). Log the resolved model in the Delegation log.

**Then triage before presenting.** Findings you agree with become fixes;
findings that look wrong get pushed back with reasoning; either way,
re-verify after changes (rebuild, re-run tests, re-check behavior) and record
the outcome in the ledger. Treat it as a gate: the loop (review → triage → fix
→ re-verify) repeats until the findings are resolved. Present the triaged
analysis alongside the report, never the raw report alone.
