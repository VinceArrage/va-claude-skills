# dev-loop manual

## Page 1: The loop

This plugin is a personal dev loop for GitHub projects: **Sev** implements, **Ellie**
reviews, **Sigmund** runs the show, and a small bench of `va-` skills covers PR bodies,
the humanize pass, onboarding, and learnings. Sigmund is the front door at every task
size: you talk to him, he wears the Sev hat for the engineering and dispatches Ellie for
review, and everything a run produces lands in one folder. The mechanical work happens
without you. Every consequential decision still stops at you. Dispatched agents run on a
chosen model tier (Sonnet floor, session model for judgment) and say which as they spawn.

### Start here: hand Sigmund the issue

`/sigmund` plus the issue number (`#42`) is enough. The more context you attach, the
better: linked issues, prior fixes, a stack trace. No issue yet? Describe the task in chat
and Sigmund offers to open one, since the issue is what the PR closes at the end.

Before anything else, Sigmund proves he understands the issue. He restates it in his own
words, covering reported behavior, expected behavior, how it's produced, and the suspected
area, and classifies the fix as **corrective** (restores intended behavior) or
**additive** (introduces new behavior). Three things stop him right there: low confidence
in his own understanding (he asks you targeted questions instead of burning a loop), an
issue whose premise looks wrong, or a **bug-labelled issue whose fix turns out to be
additive**. That last one is an enhancement wearing a bug label, and it goes back to you
as a product question. The classification is re-checked in the approach brief too,
because the sneaky case only surfaces after exploration.

Then the effort forecast. He scopes the task cheaply (likely files, repos touched, public
API or schema exposure, risk surface) and tells you what it will cost *you*: which stops
he'll need you at and roughly how long each takes. Want more stops? Name them at intake
("show me the diff before Ellie", "check with me before touching X") and they're recorded
in the ledger and enforced like any other gate.

### The pipeline

Six stages, each with exit criteria Sigmund enforces. The full stage machine and gate
registry live in the sigmund skill's `references/pipeline.md`; this is the shape:

1. **Intake.** Task folder and ledger created, the issue pulled once into a local
   `issue.md` snapshot the rest of the run reads from (the live issue is re-read only
   when you ask, or right before writing to it), readiness check passed, Definition of
   Done pinned, effort forecast given.
2. **Planning.** Sev hat: context from the issue, git history, learnings, the repo's own
   `CLAUDE.md` and tooling config; approach brief written to the task folder. The brief
   **opens with three beats: what the issue is, what causes it, and the best fix**, cited
   to `file:line`, so you can grasp the whole task before reading any detail. **Your
   gate: nothing gets coded until you approve the brief.** For a bug whose mechanism he
   can't explain, he says so plainly instead of guessing: the cause line reads "not
   established" and names what he ruled out. Once you approve, on a fix with a real
   regression surface, one cheap dispatched agent writes adversarial test cases from the
   brief's risk surface without seeing Sev's plan, and they join the walk sheet you'll
   drive.
3. **Execution.** Implement to the repo's conventions and the shared checklist (the same
   one Ellie reviews against), building, testing, and linting early and often with the
   repo's own commands. Commits and pushes run **silently** here when the task-branch
   check passes; see "Silent commits" below.
4. **Verification.** Sev starts the app and stages each test case while **you drive the
   checks**. When behavior is verified, Ellie's clean-room review dispatches
   automatically. She sees the diff, issue, brief, and your recorded walk results, and
   nothing of the dev session; her report says whether the walk covered the risk
   surface. The triage loop (valid findings applied, wrong ones argued, outcomes
   recorded) repeats until she has no notes.
5. **Delivery.** Two stops instead of a drip. First: the PR body is drafted unprompted,
   with `Closes #42`, and **opens on your say-so**. CI results and Copilot's comments
   then get triaged at each wake-up without you asking. Second: one delivery package that
   bundles **your merge click** and the pre-drafted closing comment for the issue.
6. **Closeout.** Definition of Done checked, learnings captured, metrics computed, INDEX
   regenerated.

A small task, end to end, stops for you exactly five times: intake, the approach brief,
the UI walk, the PR open, and the delivery package. The gate registry is longer, but the
rest never stops a small task: readiness passes silently on HIGH, and commits ride the
confidence check. That is the whole interface.

### Extra stops when you want them

The five standing stops are a minimum, and nothing removes a standing gate. Extra gates
you name at intake are recorded in the ledger and enforced like any other gate. When
scoping shows a task is large (multi-repo, API or schema exposure, unclear mechanism),
Sigmund proposes pair cadence himself, with checkpoints at every meaningful step, rather
than running ahead.

**Silent commits:** commit and push run without asking only when *all* of these hold: the
current branch carries the task's issue number as a whole token (`42-fix` matches issue
42, not `421-fix`), it isn't a base branch (`main`, `master`, `develop`, `release*`,
`staging*`, or the repo's observed base), the diff contains only files within the scope of
the brief *as you approved it*, the commit message references the issue, the repo's own
CLAUDE.md doesn't forbid agent commits, and the push targets the same-named branch with no
force push of any kind (`--force`, `--force-with-lease`, `+refspec`, `--delete`). If any
condition fails, it asks, per action. PR creation, merge, and every write to an issue or PR
ask **every** time, and Sigmund cannot waive the approach gate on your behalf.

### Anything a person will read gets humanized

Issue and PR comments, PR bodies, release notes, messages: all of it goes through a
humanizing pass before it reaches you. The pass is not offered afterwards as optional
polish. It is part of producing the artifact, because a draft that still reads as
generated isn't finished work, and this text goes out under your name. Your ledgers,
briefs, and the ordinary back-and-forth in chat are untouched. It speaks as *you* ("I",
not "we") everywhere except release notes, which describe the software. The pass runs in
a dispatched agent, so the cost lands there rather than in the session carrying your
task. It ships with the plugin as `va-humanizer`. If you kept a personal humanizer
skill, retire it: the two trigger on the same phrases and compete.

### One folder per task

Everything a run produces lives in `Tasks\<KEY>\` (`<KEY>` is `<repo>-<issue number>`,
like `myapp-42`): the ledger (the single entry point, with links to everything else at the
top), the approach brief, Ellie's review reports, and any attachments. The ledger reads
top-to-bottom as the story of the task: pipeline state, decisions with timestamps, review
outcomes (findings raised / valid / invalid, per round, Copilot included), token and time
metrics, session journal. When you come back to a task weeks later, ask Sigmund to
**"walk me through myapp-42"** and he replays the run chronologically: what was decided
and by whom, what the reviews caught, what waited on whom, and what it cost. The metrics
script counts the agents a session dispatched alongside the session itself, fills the
ledger's metrics block at the delivery package, and regenerates INDEX.md from the ledgers;
at month-end, `--all` aggregates every closed ledger in one pass.

### Dev Reviews are a first-class track

Reviewing someone else's PR on one of your repos has its own shape: Sigmund enters at
Verification, writes the Issue / Cause / Fix opener from the diff (beat three: is the
author's fix the right one?), dispatches Ellie clean-room, and routes findings back to the
author as review comments you approve. Say "take over" and the task changes hands without
changing folders: Sev picks up the revision in the same ledger. Ellie also works
standalone on any PR when you just want a review.

### Superpowers

If the `superpowers` plugin is installed, Sigmund picks its technique skills for each
moment of the task: brainstorming for features, systematic debugging for bugs, TDD while
coding, verification before anything is called done, worktrees for isolation, and so on.
The mapping and the rules live in the sigmund skill's `references/superpowers.md`. The
loop's gates always win: no superpowers skill can approve the brief, pass the UI walk,
open the PR, or merge for you, and Ellie stays the only reviewer. Each skill used is
noted in the ledger journal, and nothing breaks if the plugin isn't there.

### Stacks

Sev and Ellie are stack-agnostic. They read the repo's own rules first (`CLAUDE.md`,
linter, formatter, and type-checker config), then the shared `docs/conventions-checklist.md`,
which has a general section plus Python, TypeScript/JavaScript, and .NET/C# sections. A
repo's own configuration wins wherever it disagrees with the checklist. Using another
language? Add a section to the checklist the second time it comes up.

### Sessions

Keep a session open while you're mid-stage; end it when you choose, and Sigmund hands you
a two-line pickup prompt. The next wake-up reconciles the ledger against git and the issue
snapshot and runs to the next gate without you having to re-explain anything.

### The full cast

The three agents keep bare names; everything else takes the `va-` prefix and is named for
the job it does.

| Skill | What it's for |
|---|---|
| `sigmund` | Delivery Lead, the front door at every task size: ledgers, gates, sequencing |
| `sev` | Senior engineer: approach briefs and implementation to convention |
| `ellie` | Clean-room reviewer: pre-merge review, your work or someone else's |
| `va-pr-draft` | PR bodies in a reviewer-focused format |
| `va-humanizer` | The humanize pass itself, dispatched by the gate or on request |
| `va-share-learning` | Write up a gotcha and file it in the plugin |
| `va-workflow-setup` | The onboarding wizard; writes your dev profile |

You rarely name most of these. Hand Sigmund the issue and he routes to whichever the work
needs; the ones you reach for directly are `/sev` for hands-on engineering and
`/va-share-learning` when something bites you.

---

## Page 2: Getting started, and staying flexible

### Prereqs

- **Claude Code**, a late-2025 or newer build (older builds have no plugin support).
- **git** and **`gh`**, logged in to the account that owns your repos.
- **Python 3**: the task-metrics script reads your session transcripts to compute tokens
  per task. The wizard checks for it.
- **Your repos cloned under one workspace root.** The wizard scaffolds it and clones
  what's missing.

### Install

The install steps for both surfaces are in the repo README. Terminal and Claude Desktop do
**not** share plugin installs, so install on the surface you use, or both.

### Then `/va-workflow-setup`

An interactive wizard in four stages: interview, prereq checks, writing your dev profile to
`~/.claude/va-profile.md`, and a closing summary of what now works. It skips whatever
already works. One step is marked **HUMAN-RUN** (`gh auth login`) because it reads from a
live terminal the agent doesn't have; the wizard hands you the command and waits. Every
other skill reads that profile and stops if it's missing.

### Your first task

1. Pick a small issue. `/sigmund` and give the number. Read his restatement of the issue
   and his effort forecast; if he's understood it, tell him to run.
2. He'll come back with the approach brief. This is the minute that pays off most: read
   it, ask the hard questions, and approve or push back. Then he runs (implementation,
   builds, commits on the task branch) until the test walk, where you drive the app while
   he watches the logs.
3. Ellie's review dispatches itself; he hands you the triaged analysis, then the PR draft.
   You OK the open and click the merge. By then the ledger, metrics, and learnings are
   already done. Afterwards, try "walk me through it."

Prefer hands-on for your first one? `/sev` plus the issue still works as a direct door to
the engineering without the orchestration: same brief, same gate, same conventions.

### Don't baby the agents

- **Different folder layout?** Say so in your profile (Local extras). Nothing is hardcoded;
  every path comes from that file, and you can edit it by hand any time.
- **Repo you don't have locally?** They read it remotely through `gh` (PR diffs, file
  contents, history) rather than making you clone it.
- **Forecast looks off?** Say so. It's a forecast rather than a contract, and the stops are
  yours to add or wave through either way.
- **Ask the hard scoping questions before you approve the brief.** "Who else calls this?"
  "What happens when it's null?" "Why not the smaller fix?" The gate is the cheapest place
  in the loop to discover the issue is wrong.
- **Push back.** If a finding is wrong or an assumption doesn't fit your setup, say so. The
  agents will engage with your reasoning rather than defend a position.

### Contributing

Solved a gotcha? `/va-share-learning` writes it up and files it in the plugin's
`docs/learnings/`, and every project's Sev and Ellie pick it up on the next plugin update.
Improved a skill? Open a PR.
