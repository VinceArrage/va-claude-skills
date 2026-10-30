# Issue / Cause / Fix — the post-investigation summary

Shared by **Sev** and **Sigmund**. This is the short statement the developer
reads to understand a task without reading the whole brief: *what is wrong,
why it is wrong, and what we should do about it.* It is written for the owner
deciding at the gate and for any dev who has not skimmed the ticket or the
code — high value, briefly, with no context assumed.

It runs **after** exploration: the readiness check (`readiness-check.md`) is the
hypothesis before any code is traced; this block is the answer once the mechanism
is known.

## When it fires

| Situation | When | Written by |
|---|---|---|
| Normal task | Head of `brief.md`, and it opens the approach gate in chat | Sev |
| Dev Review | Before Ellie is dispatched, from the PR diff and the issue | Sigmund |

It leads; never bury it under Goal and Acceptance Criteria.

## The three beats

**Issue** — what actually goes wrong, in terms the developer or the client
would observe. One or two sentences. This is the *confirmed* issue, not the
reporter's version of it; if exploration corrected the issue, this is where the
corrected version appears.

**Cause** — the mechanism, explained the way you would across a desk: plain
words, no assumed context. Name the specific thing — the branch not taken, the
value arriving padded, the caller that skips the guard — and end with the
`file:line` cite as a pointer for whoever wants to look, not as the
explanation itself. A cause you cannot cite is a cause you have not found
yet.

**Best fix** — what you recommend and why it beats the alternative you
considered. One or two sentences, naming the tradeoff rather than hiding it.
"Best" is a claim; if a smaller or safer fix was rejected, say what for.

Six sentences is a good ceiling for all three. Depth belongs in the brief;
this block is what gets read.

## Register — explain, don't prove

Internal jargon stays in the brief below. The block renders understanding the
agents already hold and changes nothing else about the run. Readers other than
the author see it, so it goes through the humanize pass (`humanize-gate.md`),
the one part of a brief that does.

## When the cause is not known

Say so. Write `Cause: not established` followed by what you ruled out and what
it would take to find it — a log capture, a local repro, a question for the
reporter.

A confident-sounding wrong cause costs more than an honest unknown, because it
is about to be approved.

## When the task is additive

An enhancement has no root cause — nothing is broken. Replace the Cause beat
with **why today's behavior falls short**: the limitation, the missing option,
the assumption the current design makes that the request breaks. Keep the other
two beats as they are.

(If a Bug-typed ticket turns out additive here, the readiness check's hard stop
applies and the task goes back to the developer as a product question.)

## When it contradicts intake

If these three beats disagree with the readiness restatement recorded at
intake, add one line saying so: **Changed from intake:** what you thought then,
what it turned out to be.

A divergence means the ticket was misleading, which the developer should know
before closing it.

## Dev Review variant

In Dev Review the author has already chosen a fix, so the third beat changes
shape: state **the author's fix and whether it is the right one**. Agreeing is
a fine answer — say so plainly and move to the review. Disagreeing is a finding
that belongs to the developer, not to Ellie's convention pass, and it goes to
them before the review dispatches rather than after.

## Recording

Goes at the top of `brief.md` (normal task) or in the ledger's Intake section
(Dev Review), and is presented in chat as-is. The block's shape is the ledger
template's `### Issue / Cause / Fix` section.
