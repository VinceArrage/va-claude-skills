# va-claude-skills

A personal Claude Code plugin marketplace. It ships one plugin, **`dev-loop`**: a GitHub
issue to merged-PR dev loop. Sev implements, Ellie reviews, Sigmund orchestrates across
sessions, plus PR drafting, a humanize pass for anything a person will read, and a shared
base of gotchas. It takes an issue through approach, code, build and test, review, PR, and
closeout, with the gates you want kept. Stack-agnostic: Python, TypeScript/JavaScript, and
.NET/C# have checklist sections, and the repo's own rules always win.

## Install

**Terminal:** run `claude`, then:

```
/plugin marketplace add <your-github-user>/va-claude-skills
/plugin install dev-loop@va-claude-skills
```

**Claude Desktop:** Customize → Plugins → Add Marketplace →
`<your-github-user>/va-claude-skills` → install `dev-loop` (user scope).
`/plugin` isn't typeable in the Desktop chat, so use this path there instead.

The two surfaces do **not** share plugin installs, so install on the surface you use, or both.
Terminal `/reload-plugins` may report "0 skills" here; skills still resolve in sessions, and
reinstalling on your surface fixes it if they don't.

Then run `/va-workflow-setup`, an interactive wizard that verifies your `git`, `gh`, and
Python and writes your dev profile. Nothing else works until it does.

## Read this next

**[The manual](plugins/dev-loop/docs/MANUAL.md)** covers two pages: the six-stage loop, the
gates that stop it, and the full cast of skills on page 1; prereqs and your first task on
page 2. Start there. [task-flow.html](plugins/dev-loop/docs/task-flow.html) draws the whole
pipeline as a diagram (regenerate it with `python plugins/dev-loop/scripts/render_taskflow.py`).

## Contributing

Hit a gotcha worth keeping? `/va-share-learning` drafts it and files it under
`plugins/dev-loop/docs/learnings/`. Skill fixes and better trigger phrasing are welcome too.

**Naming a new skill.** The three agent personas keep bare names — `sev`, `ellie`,
`sigmund`. Everything else takes the `va-` prefix and is then named for the job it does:
`va-pr-draft`, `va-humanizer`, `va-workflow-setup`, `va-share-learning`. Name the work, not
the plumbing. A skill's directory name and its frontmatter `name:` must match, or it won't
load.
