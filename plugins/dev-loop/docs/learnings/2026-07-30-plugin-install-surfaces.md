# Claude Code terminal and Desktop app do NOT share plugin installs

**Symptom:** Installed the dev-loop plugin from a terminal `claude` session
(`/plugin marketplace add` + `/plugin install`), but the skills never appeared in
Claude Desktop sessions — even after a full Desktop restart. Typing `/plugin` in the
Desktop chat returns "/plugin isn't available in this environment," so there's no
obvious way forward from inside Desktop.

**Root cause:** The two surfaces keep separate plugin registrations. A terminal-side
install registers the marketplace and plugin for terminal sessions only; Desktop has
its own install flow and doesn't read the terminal's plugin state (and vice versa).

**Resolution:** Install on the surface you actually use — or both:
- Terminal: run `claude`, then `/plugin marketplace add <your-github-user>/va-claude-skills`
  and `/plugin install dev-loop@va-claude-skills`.
- Claude Desktop: Customize → Plugins → Add Marketplace →
  `<your-github-user>/va-claude-skills` → install `dev-loop` (user scope).

Related quirk: terminal-side `/reload-plugins` may report "0 skills" for this plugin;
the skills still resolve in sessions. If they don't, reinstall on the surface you're using.

**Applies to:** plugin installation on any dev machine; first discovered during the
2026-07-30 onboarding dry-run.
