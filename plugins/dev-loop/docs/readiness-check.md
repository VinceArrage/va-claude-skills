# Readiness check — run before any scoping

Shared pre-check for **Sev** and **Sigmund**. It runs after the issue is
fetched and **before** deep exploration or approach design begins. Its job is
to prove the agent understands the issue at hand — and to catch, up front, the
issues that shouldn't enter the loop at all.

## Inputs — cheap recon only

The check is built from the issue and minutes of recon, not a code trace:

- The issue: description, comments, acceptance criteria, labels (`bug`,
  `enhancement`, …).
- `git log --grep=<issue number>` and recent history on obviously-suspect
  files.
- A scan of learnings (`docs/learnings/` in this plugin, plus the repo's
  `.claude/docs/learnings/`).

If you find yourself reading whole modules, you've left the readiness check
and started scoping — stop and record a verdict first.

## 1. Issue restatement (your own words)

Write four lines. Quoting the issue back is not a restatement.

- **Reported:** what the issue says happens.
- **Expected:** what should happen instead.
- **Produced by:** the conditions/steps that trigger it, as best you can tell.
- **Suspected area:** repo(s), module(s), or flow you believe is involved.

## 2. Understanding verdict

- **HIGH** — you can state the issue precisely and name a plausible area.
  Proceed into scoping without stopping.
- **LOW** — you cannot restate the issue with confidence. Stop and ask the
  developer **targeted questions** (name what's missing: repro steps, expected
  behavior, environment) instead of burning an exploration loop on a guess.
- **NOT_A_BUG** — the issue's premise looks wrong (the described behavior is
  the designed behavior, or the report contradicts itself). Stop and surface
  that to the developer before doing anything else.

## 3. Fix classification

Classify the likely fix:

- **corrective** — restores behavior the code already intends (repairs a
  broken mechanism).
- **additive** — introduces behavior that never existed (new feature, new
  option, design change).

The classification is checked **twice**:

1. **At intake** (here) — catches obvious enhancements filed as bugs.
2. **In the approach brief** (Sev Phase 2, mandatory line) — catches the
   sneaky case that only surfaces after exploration: the code does exactly
   what it was designed to do, and the "fix" is really a design change.

**Hard stop rule:** a **bug-labelled issue + additive fix** always stops the
loop. Frame it for the developer as a product question ("this is
an enhancement wearing a bug label — proceed, relabel, or close?"). An
additive fix nobody approved is scope drift. **If the issue has no label or
type to read**, judge from its description; when it reads as a defect report,
apply this rule — the stop is cheap, a silently-unapproved enhancement is not.

## Recording

Embed the `### Readiness` block (its shape is the ledger template's Intake
section) at the top of Sev's context brief, and, under Sigmund, in the ledger.
