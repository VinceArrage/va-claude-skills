---
name: va-workflow-setup
description: >-
  Onboard the developer onto the dev-loop plugin: interview them, verify git, gh, and
  Python, and write the dev profile at ~/.claude/va-profile.md. Trigger on
  '/va-workflow-setup', 'set me up', 'onboard me onto the dev loop', or whenever another
  dev-loop skill reports the profile is missing.
---

# Onboarding: plugin installed → working environment

This is the one skill in the plugin that runs **without** a dev profile — it is the skill
that writes it. Every other skill (`sigmund`, `sev`, `ellie`, `va-pr-draft`,
`va-share-learning`) reads `~/.claude/va-profile.md` and stops if it's absent, so nothing
else works until this finishes.

Run it as an **interactive wizard**, not a script. Four stages, in order. At the top of
each stage, **check whether it's already done and skip it if so**, and say what you're
skipping and why, so the dev can see the state of their machine rather than just watching
commands scroll.

**Already have a profile?** If `~/.claude/va-profile.md` exists, read it out, ask whether
they want to *update a field*, *re-verify everything*, or *start over*, and jump to the
relevant stage.

**Shell.** Commands below assume **Git Bash on Windows** (`/c/...` paths, forward slashes,
`~` = the Windows user profile); on macOS or Linux they run unchanged. Run them with the
Bash tool.

**Who runs a fence.** Every fence is **agent-run** unless it is preceded by a
**HUMAN-RUN** label. A HUMAN-RUN step reads from a live terminal (a device code, a
password prompt). Your Bash tool has no TTY, so running one yourself doesn't fail, it
**hangs the session**. When you hit one: hand the dev the exact command, say plainly that
you can't run it for them, wait for them to say it's done, then verify with the agent-run
check that follows. Never "try it anyway" first.

**Placeholders.** The angle-bracket tokens in the fences below are values you collect in
Stage 1 (`<workspace-root>`, `<github-user>`). Substitute the real value before running
the command — never paste an angle bracket into a shell.

---

## Stage 1 — Interview

Ask these in one pass, conversationally, and repeat the answers back before moving on.
Don't dump the whole list as a form; ask, react, follow up on the interesting answers.

1. **Name** — how they want skills to address them.
2. **GitHub user** — the account (or org) that owns their repos; used for clone commands
   and for the plugin's own repo.
3. **Workspace root** — the parent directory holding their repo clones (Git Bash form,
   e.g. `/c/src`; the profile records the Windows form). Verify the root exists; if not,
   offer to create it.
4. **Repos present** — list what's actually there, don't assume:
   ```bash
   ls -1 <workspace-root> 2>/dev/null || echo "(workspace root doesn't exist yet)"
   ```
   Ask which repos they plan to use the loop on and offer to clone any that are missing:
   ```bash
   gh repo clone <github-user>/<repo> <workspace-root>/<repo>
   ```
   This is agent-run and silent once `gh` is authorized over HTTPS (Stage 2). If `gh`
   isn't authorized yet, note the gap and come back after Stage 2.
5. **Plans / Reviews / Tasks directories** — where approach briefs (Sev), review reports
   (Ellie), and task ledgers (Sigmund) live. Default them **inside** the workspace root
   (`<workspace-root>\Plans` etc.) so the workspace stays self-contained. First check both
   locations — someone migrating from an older setup may have history *beside* the
   workspace root:
   ```bash
   ls -d <workspace-root>/Plans <workspace-root>/Reviews <workspace-root>/Tasks \
         <workspace-root>/../Plans <workspace-root>/../Reviews <workspace-root>/../Tasks 2>/dev/null
   ```
   If any exist, ask: keep those paths in the profile, or start fresh at the defaults?
   Otherwise create the defaults:
   ```bash
   mkdir -p <workspace-root>/Plans <workspace-root>/Reviews <workspace-root>/Tasks
   ```
6. **Local extras** — anything skills should know: a personal style guide, a nonstandard
   clone layout, languages they use most. Optional; empty is a fine answer.

Hold these answers — Stages 2–3 use them verbatim.

---

## Stage 2 — Prereq check

Four checks. Report each as pass/fail with the actual output; don't paper over a failure.

```bash
claude --version
git --version
gh auth status
python --version
```

- **`claude --version`** — plugins require a late-2025-or-newer build. If it's older,
  upgrading is the fix; nothing downstream will behave until then.
- **`git --version`** — any recent Git; on Windows, Git for Windows also supplies the Git
  Bash shell the commands here assume.
- **`gh auth status`** — must show an authenticated account. Test real access to one of
  their repos, not just login:
  ```bash
  gh repo view <github-user>/<repo> --json name
  ```
  If it fails, the dev has to log in — **HUMAN-RUN**, in their own terminal window.
  `gh auth login` prints a one-time code and then waits on the keyboard, so an
  agent-issued call hangs instead of authenticating. Hand them this and stop:
  ```bash
  gh auth login --hostname github.com --git-protocol https --web
  ```
  When they say they're done, **you** re-run `gh auth status` and the `gh repo view`
  above, and continue only once the repo name prints. Also confirm the token can manage
  issues and PRs (`gh issue list --repo <github-user>/<repo> --limit 1` succeeds).
- **Superpowers plugin** (optional) — Sigmund routes to its technique skills
  (brainstorming, debugging, TDD, verification) when it is installed. Check whether a
  `superpowers:*` skill appears in the available skills list; if not, mention that
  installing it adds those techniques and **continue anyway**. Record the outcome under
  *Local extras*.
- **`python --version`** — Python 3.8+ runs the plugin's `task_metrics.py` script
  (`scripts/task_metrics.py`, invoked by Sigmund at the delivery package). On Windows try
  `py -3 --version` if `python` isn't on PATH. **Soft dependency** — continue anyway if
  missing, but record the gap under *Local extras* so metrics aren't silently absent.

---

## Stage 3 — Write the profile

Read `../../docs/profile-template.md`, fill every field from the interview and from what
Stage 2 actually proved, and write the result to `~/.claude/va-profile.md`:

```bash
mkdir -p ~/.claude
```

Rules for filling it:

- **Keep the field labels exactly as the template has them.** Skills locate values by label
  (*profile:Tasks dir*, *profile:Workspace root*); a renamed label reads as a missing one.
- **No leftover angle brackets.** Every `<...>` in the template is a placeholder to replace.
  If a value genuinely doesn't apply, write `none`.
- Record paths in **Windows form** (the form the dev sees in Explorer and their editor);
  skills translate to `/c/...` when they shell out.
- Put anything odd the stages surfaced into **Local extras**: a missing Python, a
  nonstandard clone layout.

Then **show the finished profile to the dev in full and ask them to confirm it**. It's a
plain markdown file they own — tell them they can edit it any time, and that the labels are
the only part that has to stay put.

---

## Stage 4 — Finish

Confirm out loud what now works — `gh` access, repos in place, profile written — then
close with:

> You're set. Point me at a GitHub issue and say `/sigmund` (or `/sev` for hands-on
> engineering without the orchestrator). The manual is at `../../docs/MANUAL.md`.
