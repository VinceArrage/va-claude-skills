# The humanize gate — outward-facing text

Anything this loop produces that **another person will read** gets a humanizing
pass before the developer sees it: part of producing the artifact, never offered
afterwards. It goes out under their name, and a draft that still reads as
generated is not finished work.

## Covered

- GitHub issue comments and issue text
- PR titles, PR bodies, PR review comments
- Release notes, changelog entries, and README or docs prose written for readers
- Emails and chat messages the developer will send
- Learning docs written for others to read
- The Issue / Cause / Fix block at the head of a brief (`issue-cause-fix.md`)

## Not covered

- Code, identifiers, log strings, file paths, SQL, config
- Internal working notes: ledgers, briefs (minus their Issue / Cause / Fix
  head), task folders, decision logs
- Text the developer wrote and asked you to keep verbatim, and quoted material
  from issues, users, or logs
- Your ordinary replies to the developer in chat

## Who is speaking

The developer, in the first person singular. Everything the loop writes goes
out under their name, and they did the work: "I reviewed the logs", "I've
pushed the fix", "I couldn't reproduce this locally". Never "we" for their
own actions.

The exception is text that speaks for the project rather than for one person:
release notes and changelog entries, which describe the software ("Fixed a
crash when the config file is empty"), not the author.

| Audience | Voice |
|---|---|
| Release notes, changelog, README prose | the project — describe the software, no pronoun needed |
| Everything else — issue comments, PR bodies and review comments, messages, Dev Review comments to an author | **I** |

"We" inside an artifact is allowed only when it is literally true and says
who: a decision two named people made. It is never the default.

## How to run it

**Dispatch a subagent that loads the `va-humanizer` skill and returns the
finished text.** It is large; never load it inline. Follow the standing
model tiers — outward-facing prose is judgment work, so it runs on the session
model. Name the artifact's register **and its voice** (I, or the project's)
in the dispatch prompt, so the pass preserves the first and corrects the
second — a stray "we" in an issue comment is the humanizer's to catch.

**Batch what is ready together.** One dispatch carries every artifact that is
finished at the same moment — at closeout, the PR body and the closing issue
comment go as one pass, not two. Dispatch per moment, not per artifact.

Then show the developer **the finished version only**. Not the draft, not the
humanizer's findings, not a before-and-after. They asked for the artifact.

**Keep the register the artifact calls for.** Humanizing release notes must
not make them casual or strip their technical precision. Humanizing removes
the tells, not the substance.

**A dispatched pass satisfies the gate.** It does not re-trigger it — text that
came back from the humanizer is finished, and running it again is waste.

## If you cannot dispatch

Say so in one line, then do the pass yourself against the tells in
`skills/va-humanizer/SKILL.md`: em dashes, negative parallelisms, significance
inflation, rule-of-three padding, tacked-on -ing clauses, vague attribution.
