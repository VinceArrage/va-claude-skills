# Conventions checklist

Shared fast-scan checklist used by the `sev` (writing) and `ellie` (reviewing)
skills, so the standard Sev writes to and the standard Ellie reviews against
are the same document by construction.

**The repo's own rules outrank this file.** Each project's `CLAUDE.md`,
`CONTRIBUTING`, and tool configuration (linter, formatter, type-checker,
analyzers, `.editorconfig`) are the authority; this checklist fills the gaps
they leave and covers what tools can't see. Where they disagree, the repo
wins — and a reviewer says so rather than silently picking one.

## Ground rule — new code is clean, old code is left alone

New or modified lines meet the repo's configured rules and this checklist.
"It matches the rest of the file" is a reason to mirror *structure* (which
helpers to call, error-handling shape, naming scheme, file layout), never a
reason to repeat something the repo's tooling or this checklist calls wrong.
Do not restyle untouched code around a change — that's scope creep and noisy
diffs.

Each language section below adds to the general one; read both.

---

## General (every language)

### Lens 1 — Mechanical

- Formatter output is clean: the repo's formatter would make no changes to the
  touched lines (`ruff format`/`black`, `prettier`, `dotnet format`).
- Linter and type-checker pass on changed files with zero new warnings.
- No commented-out code, debug prints, stray `TODO`s without an issue number,
  or leftover scratch files.
- Names say what the thing is; no single-letter names outside tight loops and
  lambdas; no misleading names left after a refactor.

### Lens 2 — Structural

- **Parameterized queries** — values never string-built into SQL, shell
  commands, or file paths.
- **Errors are handled or propagated, never swallowed** — no bare
  `except:`/`catch {}` that hides failure; catch the narrowest type you can
  handle.
- **Resources are released** on every path (`with`, `using`/`await using`,
  `try/finally`).
- **Secrets stay out of code and logs**; config comes from the project's
  existing mechanism (env vars, settings files), not new hard-coded values.
- **Layering respected** — new code lives where its neighbours live; no
  reaching across layers the project keeps apart (UI ↔ data access, etc.).
- **Public contracts are deliberate** — a changed function signature, API
  route, CLI flag, config key, or exported type has its callers updated and,
  for anything external, a compatibility note.
- **Tests follow the repo's practice** — a bug fix in a tested codebase comes
  with a regression test that fails without the fix.

### Lens 3 — Idiomatic

- Reuse over reinvention: existing helpers are used instead of near-copies.
- Functions do one thing; deep nesting is flattened with early returns.
- Comments explain *why*, not *what*; no comment restates the code, and none
  name the issue number (that's what `git blame` is for).
- Log and error messages name the condition and the record involved.
- Match the comment density, naming, and idiom of the surrounding code.

---

## Python

- **Mechanical:** PEP 8 as enforced by the repo's `ruff`/`flake8`/`black`
  config; imports grouped stdlib → third-party → local, no unused imports, no
  wildcard imports.
- **Structural:**
  - Type hints on new public functions where the repo uses them; `mypy`/
    `pyright` clean if configured.
  - No mutable default arguments (`def f(x=[])`).
  - `pathlib` over string path-joining in new code; `subprocess` with an
    argument list, never `shell=True` with interpolated input.
  - Exceptions: `raise ... from err` when re-raising; no `except Exception:
    pass`.
  - Dependencies declared where the project declares them (`pyproject.toml`,
    `requirements*.txt`), lockfile updated if one exists.
- **Idiomatic:** comprehensions over manual append-loops when clearer;
  f-strings for formatting (but `logging` calls use `%s` args, not
  f-strings); `dataclass`/`NamedTuple` over ad-hoc dicts for structured
  records; context managers for anything that opens.

## TypeScript / JavaScript

- **Mechanical:** `eslint` and `prettier` clean per the repo's config; no
  unused imports or variables; consistent module style (ESM vs CommonJS) with
  the rest of the project.
- **Structural:**
  - TypeScript: no new `any`, no non-null `!` assertions or `as` casts that
    paper over a real type gap; `strict` settings respected.
  - Every promise is awaited or deliberately handled — no floating promises;
    `async` functions don't swallow rejections.
  - `===`/`!==`, never `==` (except the deliberate `== null` idiom if the repo
    allows it).
  - React (if used): hooks follow the rules of hooks, effect dependency arrays
    are complete, lists have stable keys, no state derived by copying props.
  - User input is never passed to `innerHTML`/`dangerouslySetInnerHTML`,
    `eval`, or a shell without sanitizing.
  - `package.json` and the lockfile change together.
- **Idiomatic:** `const` by default, `let` only when reassigned, never `var`;
  optional chaining and nullish coalescing over hand-rolled guards;
  early-return over nested conditionals.

## .NET / C#

- **Mechanical:** `dotnet format` clean; analyzers configured in
  `.editorconfig`/`Directory.Build.props` produce no new warnings; file-scoped
  namespaces and `using` placement match the project.
- **Structural:**
  - Nullable reference types respected where `<Nullable>enable</Nullable>` is
    on — no `!` suppressions covering a real null path.
  - `async` all the way: no `.Result`/`.Wait()` on tasks, no `async void`
    except event handlers; `CancellationToken` passed through where the
    callers have one.
  - `IDisposable`/`IAsyncDisposable` wrapped in `using`.
  - EF Core / ADO.NET: parameterized queries, no N+1 loops over lazy loads.
  - Dependencies registered and resolved through the project's DI container,
    not `new`-ed up inside services.
- **Idiomatic:** pattern matching and `switch` expressions where they read
  better; `record` for immutable data; LINQ when it's clearer than a loop (and
  a loop when it isn't); `nameof` instead of string literals for member names.

## Other languages

No section yet: use the general lenses plus the repo's own tooling and the
language's mainstream style guide. When a language recurs across projects,
add a section here.
