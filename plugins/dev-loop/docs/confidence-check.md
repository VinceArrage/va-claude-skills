# Task-branch confidence check (G-COMMIT / G-PUSH auto-pass)

The one rule that lets commits and pushes run without asking. Shared by
**Sev** and **Sigmund** — this file is the single authority; the skills
point here rather than restating the conditions.

ALL six must hold, verified fresh at action time — not remembered:

1. `git branch --show-current` contains the task's issue number **as a whole
   token** — the character after the number must not be a digit. `42-fix`
   matches issue 42; `421-fix` does **not**. A task with no issue is keyed
   by its slug instead, and the branch must contain that slug.
2. The branch is not a base/protected branch: `main`, `master`, `develop`,
   `release*`, `staging*`, or the repo's observed base. Observed
   base = `git symbolic-ref --short refs/remotes/origin/HEAD`; if that command
   fails, this condition is unverifiable → ask.
3. The staged diff contains **only** files within the approved brief's scope —
   no unrelated files swept in. Scope is the brief **as approved at
   G-APPROACH**. Adding a file to the brief afterwards does not extend scope —
   a file outside the approved list fails this condition and takes explicit
   per-action permission, with the brief edit presented alongside it.
4. The commit message references the issue (`#42` in the subject or body)
   when there is one, and follows the repo's commit style.
5. The repo's own `CLAUDE.md` does not forbid agent-created commits (some
   repos say "Never create git commits unless the user explicitly asks").
   A prohibition, or a doc that exists but hasn't been
   read this session, fails this condition → ask. A repo with no `CLAUDE.md`
   passes (nothing forbids), and one read per session is enough — this is
   not a per-commit re-read.
6. *(Push only)* target is `origin` same-named branch; never `--force`,
   `--force-with-lease`, a `+refspec`, or `--delete` — any history-rewriting or
   branch-removing push asks.

Any condition fails or can't be verified → fall back to explicit per-action
permission, exactly as before. PR creation, merges, and issue or PR writes
are never covered by this check — those ask every time.

**Ungated by this check and therefore always ask:** `stash`, branch switch
away from the task branch, `reset`, branch delete, remote-branch delete.

Under Sigmund, log every auto-passed event in the ledger's Session journal,
in this form:

```
<ts> G-COMMIT auto-pass · branch=<observed> · files=<staged list> · brief-approved=<G-APPROACH date> · msg=<subject>
```

Same line for `G-PUSH`, with the target ref recorded too
(`target=origin/<branch>`).
