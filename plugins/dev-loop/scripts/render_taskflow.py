import io, html

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "task-flow.html")

# ---------------------------------------------------------------- layout model
LANES = ["Developer", "Sigmund", "Sev", "Ellie", "Skills & docs"]
COLS  = ["Ready", "1 · Intake", "2 · Planning", "3 · Execution", "4 · Verification", "5 · Delivery", "6 · Closeout", "Done"]

# kind: stop = developer gate (you act) · auto = auto-pass gate · hat = Sev hat-swap
#       disp = clean-room dispatch · skill = skill/doc/tool call · state = start/end
# new=True would tag a node with a release badge; none are tagged right now
STEPS = [
 # (col, lane, lines, kind, new)
 (0, 0, ["/sigmund #42", "plus any context you attach"], "state", False),
 (1, 1, ["Read dev profile", "task folder + ledger.md", "(ledger-template.md) · INDEX row"], "sig", False),
 (1, 4, ["gh issue view → issue.md", "pulled once; the run reads this"], "skill", False),
 (1, 1, ["Readiness check", "(readiness-check.md)"], "sig", False),
 (1, 1, ["G-READINESS", "auto-pass: HIGH + corrective", "LOW, NOT_A_BUG, or additive → stop"], "auto", False),
 (1, 1, ["DoD pinned · effort forecast", "You-Are-Here block"], "sig", False),
 (1, 0, ["STOP · Intake", "confirm understanding, DoD,", "any extra gates you want"], "stop", False),
 (2, 2, ["Sev hat · Phase 1 context", "learnings, CLAUDE.md, repo configs,", "end-to-end code trace"], "hat", False),
 (2, 2, ["Phase 2 · brief.md", "opens with Issue / Cause / Fix,", "approach, risk, verification plan"], "hat", False),
 (2, 4, ["va-humanizer (dispatch)", "the Issue / Cause / Fix block"], "skill", False),
 (2, 0, ["STOP · G-APPROACH", "read the three beats, then the brief;", "nothing is coded until you approve"], "stop", False),
 (2, 4, ["adversarial cases", "(Sonnet dispatch, risk-gated)", "from Issue/Cause/Fix + risk", "surface; not Sev's plan; S / A"], "skill", False),
 (3, 2, ["Phase 3 · implement to convention", "(conventions-checklist.md)"], "hat", False),
 (3, 4, ["the repo's own build,", "test, and lint commands"], "skill", False),
 (3, 1, ["G-COMMIT / G-PUSH", "auto under confidence-check.md,", "otherwise ask per action"], "auto", False),
 (4, 2, ["Stage the walk sheet", "start the app, seed the data"], "hat", False),
 (4, 0, ["STOP · G-UI walk", "you drive the app against the sheet;", "results recorded in the ledger"], "stop", False),
 (4, 3, ["Ellie (dispatch, clean-room)", "diff + issue.md + brief.md,", "+ walk results → coverage"], "disp", False),
 (4, 1, ["Triage", "valid → Sev fixes → re-verify;", "Review outcomes row per round"], "sig", False),
 (5, 4, ["va-pr-draft → va-humanizer"], "skill", False),
 (5, 0, ["STOP · G-PR-OPEN", "the PR opens on your say-so"], "stop", False),
 (5, 1, ["Wake-ups", "CI + Copilot comments → Sev triage,", "until the PR is clean"], "sig", False),
 (5, 4, ["issue closing comment", "→ va-humanizer"], "skill", False),
 (5, 0, ["STOP · delivery package", "G-MERGE click · G-ISSUE ok;", "metrics written"], "stop", False),
 (6, 1, ["DoD check", "task_metrics.py --write · index", "INDEX regenerated → Done"], "sig", False),
 (6, 4, ["va-share-learning", "learnings captured"], "skill", False),
 (7, 0, ["Done", "merged, closed, recorded"], "state", False),
]

LOOPS = [  # (from step idx, to step idx, label)  — drawn as dashed return arrows
 (18, 12, "findings → fixes → re-verify"),
 (21, 12, "CI / Copilot valid → fix → re-check"),
]

# Dev Review track
DR = [
 ("Ready", ["someone else's PR exists", "on one of your repos"], "state", False),
 ("Sigmund", ["Review intake", "Issue / Cause / Fix from", "the diff and the issue;", "beat 3: is the author's fix right?"], "sig", False),
 ("Skills", ["Sonnet gatherer (optional)", "diff walk summary;", "judgment stays Sigmund's"], "skill", False),
 ("Ellie", ["Ellie (dispatch, clean-room)", "+ coverage: do the author's", "claimed cases cover the surface?"], "disp", False),
 ("Developer", ["STOP · G-COMMENTS", "findings go to the author as PR", "review comments you approve"], "stop", False),
 ("Skills", ["build + test locally", "(gh pr checkout)"], "skill", False),
 ("Developer", ["STOP · G-MERGE"], "stop", False),
 ("Skills", ["G-NOTIFY · va-humanizer", "thank the author;", "close out the PR / issue"], "skill", False),
 ("Sigmund", ["Closeout", "review DoD · metrics · INDEX Done"], "sig", False),
]

# ---------------------------------------------------------------- geometry
COL_W, LANE_LABEL_W, NODE_W = 226, 118, 200
LINE_H, PAD_Y, GAP = 15, 9, 10
HEAD_H = 34

def node_h(lines): return PAD_Y*2 + LINE_H*len(lines)

# per (col, lane) stack
from collections import defaultdict
stack = defaultdict(list)
for i, (c, l, lines, kind, new) in enumerate(STEPS):
    stack[(c, l)].append(i)

lane_h = {}
for l in range(len(LANES)):
    best = 0
    for c in range(len(COLS)):
        ids = stack.get((c, l), [])
        h = sum(node_h(STEPS[i][2]) for i in ids) + GAP*(len(ids)+1)
        best = max(best, h)
    lane_h[l] = max(best, 52)

lane_y = {}
y = HEAD_H
for l in range(len(LANES)):
    lane_y[l] = y; y += lane_h[l]
TOTAL_H = y + 8
TOTAL_W = LANE_LABEL_W + COL_W*len(COLS) + 8

pos = {}
for (c, l), ids in stack.items():
    used = sum(node_h(STEPS[i][2]) for i in ids) + GAP*(len(ids)-1)
    y0 = lane_y[l] + (lane_h[l] - used)/2
    x0 = LANE_LABEL_W + c*COL_W + (COL_W - NODE_W)/2
    for i in ids:
        h = node_h(STEPS[i][2]); pos[i] = (x0, y0, NODE_W, h); y0 += h + GAP

def esc(s): return html.escape(s, quote=False)

def node_svg(x, y, w, h, lines, kind, new, num=None):
    cls = "n " + kind + (" new" if new else "")
    out = [f'<g class="{cls}"><rect x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" rx="7"/>']
    ty = y + PAD_Y + LINE_H - 4
    for k, ln in enumerate(lines):
        out.append(f'<text x="{x+w/2:.0f}" y="{ty + k*LINE_H:.0f}" class="{"t0" if k==0 else "t"}">{esc(ln)}</text>')
    if num is not None:
        out.append(f'<circle cx="{x+12:.0f}" cy="{y+12:.0f}" r="9" class="num"/><text x="{x+12:.0f}" y="{y+15.5:.0f}" class="numt">{num}</text>')
    if new:
        out.append(f'<text x="{x+w-4:.0f}" y="{y+11:.0f}" class="badge">0.6.0</text>')
    out.append('</g>')
    return "\n".join(out)

def arrow(a, b, dashed=False, label=None):
    ax, ay, aw, ah = pos[a]; bx, by, bw, bh = pos[b]
    ca, cb = STEPS[a][0], STEPS[b][0]
    if ca == cb:
        # same column: vertical
        if by > ay:  # downward
            p = f"M{ax+aw/2:.0f},{ay+ah:.0f} L{bx+bw/2:.0f},{by:.0f}"
        else:
            p = f"M{ax+aw/2:.0f},{ay:.0f} L{bx+bw/2:.0f},{by+bh:.0f}"
    else:
        sx, sy = ax+aw, ay+ah/2; ex, ey = bx, by+bh/2
        mx = (sx+ex)/2
        p = f"M{sx:.0f},{sy:.0f} C{mx:.0f},{sy:.0f} {mx:.0f},{ey:.0f} {ex:.0f},{ey:.0f}"
    cls = "ar dashed" if dashed else "ar"
    s = f'<path d="{p}" class="{cls}" marker-end="url(#ah)"/>'
    if label:
        ax2 = (ax+aw/2 + bx+bw/2)/2; ay2 = min(ay, by) - 6
        s += f'<text x="{ax2:.0f}" y="{ay2:.0f}" class="lbl">{esc(label)}</text>'
    return s

def loop(a, b, label, k=0):
    ax, ay, aw, ah = pos[a]; bx, by, bw, bh = pos[b]
    # route: from top of a, up over the lanes to the top of b (b is left of a)
    sx, sy = ax+aw/2, ay; ex, ey = bx+bw/2, by
    top = min(sy, ey) - 24 - 18*k
    p = f"M{sx:.0f},{sy:.0f} C{sx:.0f},{top:.0f} {ex:.0f},{top:.0f} {ex:.0f},{ey:.0f}"
    return (f'<path d="{p}" class="ar loop" marker-end="url(#ahl)"/>'
            f'<text x="{(sx+ex)/2:.0f}" y="{top+4:.0f}" class="lbl loopl">{esc(label)}</text>')

svg = [f'<svg width="{TOTAL_W:.0f}" height="{TOTAL_H:.0f}" viewBox="0 0 {TOTAL_W:.0f} {TOTAL_H:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Task flow from Ready to Done">']
svg.append('''<defs>
<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahp"/></marker>
<marker id="ahl" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahpl"/></marker>
</defs>''')
# lanes
for l, name in enumerate(LANES):
    svg.append(f'<rect x="0" y="{lane_y[l]:.0f}" width="{TOTAL_W:.0f}" height="{lane_h[l]:.0f}" class="lane {"alt" if l%2 else ""}"/>')
    svg.append(f'<text x="12" y="{lane_y[l]+lane_h[l]/2+5:.0f}" class="lanel">{esc(name)}</text>')
# columns
for c, name in enumerate(COLS):
    x = LANE_LABEL_W + c*COL_W
    svg.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{TOTAL_H:.0f}" class="colline"/>')
    svg.append(f'<text x="{x+COL_W/2:.0f}" y="22" class="colh">{esc(name)}</text>')
# loops first (behind), then arrows, then nodes
for k, (a, b, lab) in enumerate(LOOPS): svg.append(loop(a, b, lab, k))
for i in range(len(STEPS)-1):
    svg.append(arrow(i, i+1, dashed=(STEPS[i+1][3]=="disp")))
for i, (c, l, lines, kind, new) in enumerate(STEPS):
    x, y0, w, h = pos[i]
    svg.append(node_svg(x, y0, w, h, lines, kind, new, num=i+1 if kind!="state" else None))
svg.append('</svg>')
MAIN_SVG = "\n".join(svg)

# ---- Dev Review track: horizontal chain, lane colour by owner
DR_W = 212; DR_GAP = 20; DR_X0 = 8
dr_h = max(node_h(l) for _, l, _, _ in DR) + 40
dr_svg = [f'<svg width="{DR_X0*2 + len(DR)*(DR_W+DR_GAP):.0f}" height="{dr_h+14:.0f}" viewBox="0 0 {DR_X0*2 + len(DR)*(DR_W+DR_GAP):.0f} {dr_h+14:.0f}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Dev Review track">']
dr_svg.append('<defs><marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahp"/></marker></defs>')
kindmap = {"Developer":"stop","Sigmund":"sig","Sev":"hat","Ellie":"disp","Skills":"skill"}
for i, (owner, lines, kind, new) in enumerate(DR):
    x = DR_X0 + i*(DR_W+DR_GAP); h = node_h(lines); y0 = 30 + (dr_h-30-h)/2
    dr_svg.append(f'<text x="{x+DR_W/2:.0f}" y="18" class="owner">{esc(owner)}</text>')
    dr_svg.append(node_svg(x, y0, DR_W, h, lines, kind, new, num=None if kind=="state" else i))
    if i < len(DR)-1:
        nh = node_h(DR[i+1][1]); ny = 30 + (dr_h-30-nh)/2
        dr_svg.append(f'<path d="M{x+DR_W:.0f},{y0+h/2:.0f} L{x+DR_W+DR_GAP:.0f},{ny+nh/2:.0f}" class="ar {"dashed" if DR[i+1][2]=="disp" else ""}" marker-end="url(#ah2)"/>')
dr_svg.append('</svg>')
DR_SVG = "\n".join(dr_svg)

CSS = """
  :root { --bg:#ffffff; --ink:#1c2330; --muted:#5b6472; --accent:#1f5f8b; --line:#d9dee5; --card:#f4f6f8; --code-bg:#eef1f4; --gate:#8b3a1f; --sev:#2f7d5b; --ellie:#6a4c93; --moh:#b8742a; --lanealt:#f7f9fb; }
  @media (prefers-color-scheme: dark) { :root { --bg:#14181f; --ink:#dde3ea; --muted:#98a2b0; --accent:#6db3e0; --line:#2c3440; --card:#1b212b; --code-bg:#232b36; --gate:#e0906d; --sev:#6cc39a; --ellie:#b39ddb; --moh:#e0a85a; --lanealt:#181d26; } }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink); font:16px/1.55 "Segoe UI", system-ui, -apple-system, sans-serif; }
  main { max-width:100rem; margin:0 auto; padding:2.5rem 1.5rem 4rem; }
  header.doc { border-bottom:2px solid var(--accent); padding-bottom:1rem; margin-bottom:1.5rem; }
  h1 { font-size:1.7rem; margin:0 0 .25rem; } .sub { color:var(--muted); font-size:.95rem; }
  h2 { font-size:1.25rem; margin:2.25rem 0 .75rem; padding-top:1rem; border-top:1px solid var(--line); color:var(--accent); }
  p, li { margin:.5rem 0; max-width:52rem; }
  code { background:var(--code-bg); padding:.1em .35em; border-radius:4px; font:.875em/1.4 Consolas,"Cascadia Code",monospace; }
  .wrap { overflow-x:auto; border:1px solid var(--line); border-radius:8px; background:var(--bg); }
  svg { display:block; max-width:none; font-family:"Segoe UI",system-ui,sans-serif; }
  .lane { fill:transparent; } .lane.alt { fill:var(--lanealt); }
  .lanel { font-size:12.5px; font-weight:700; fill:var(--muted); }
  .colline { stroke:var(--line); stroke-width:1; } .colh { font-size:13px; font-weight:700; fill:var(--accent); text-anchor:middle; }
  .n rect { fill:var(--card); stroke:var(--line); stroke-width:1.2; }
  .n text { text-anchor:middle; fill:var(--ink); font-size:11px; } .n .t0 { font-weight:700; font-size:11.5px; }
  .n.stop rect { fill:var(--gate); stroke:var(--gate); } .n.stop text { fill:#fff; }
  .n.auto rect { fill:var(--bg); stroke:var(--gate); stroke-width:1.6; stroke-dasharray:4 3; } .n.auto .t0 { fill:var(--gate); }
  .n.sig rect { stroke:var(--accent); stroke-width:1.6; } .n.sig .t0 { fill:var(--accent); }
  .n.hat rect { stroke:var(--sev); stroke-width:1.6; } .n.hat .t0 { fill:var(--sev); }
  .n.disp rect { stroke:var(--ellie); stroke-width:1.6; stroke-dasharray:5 3; } .n.disp .t0 { fill:var(--ellie); }
  .n.skill rect { fill:var(--code-bg); stroke:var(--line); } .n.skill text { font-family:Consolas,"Cascadia Code",monospace; font-size:10.5px; } .n.skill .t0 { font-size:11px; }
  .n.state rect { fill:var(--ink); stroke:var(--ink); } .n.state text { fill:var(--bg); }
  .n.new rect { stroke:var(--moh); } .n.new .t0 { fill:var(--moh); }
  .num { fill:var(--accent); } .numt { fill:#fff; font-size:10px; font-weight:700; text-anchor:middle; }
  .badge { font-size:9px; fill:var(--moh); text-anchor:end; font-weight:700; }
  .ar { fill:none; stroke:var(--muted); stroke-width:1.3; } .ar.dashed { stroke-dasharray:5 3; } .ahp { fill:var(--muted); }
  .ar.loop { stroke:var(--gate); stroke-width:1.2; stroke-dasharray:3 3; } .ahpl { fill:var(--gate); }
  .lbl { font-size:10px; fill:var(--muted); text-anchor:middle; } .loopl { fill:var(--gate); }
  .owner { font-size:11.5px; font-weight:700; fill:var(--muted); text-anchor:middle; }
  .legend { display:flex; flex-wrap:wrap; gap:.6rem 1.4rem; font-size:.9rem; margin:.75rem 0 1rem; color:var(--muted); }
  .legend span::before { content:""; display:inline-block; width:14px; height:14px; border-radius:4px; vertical-align:-2px; margin-right:.4rem; border:1.6px solid var(--line); background:var(--card); }
  .legend .stop::before { background:var(--gate); border-color:var(--gate); }
  .legend .auto::before { background:var(--bg); border:1.6px dashed var(--gate); }
  .legend .sig::before { border-color:var(--accent); } .legend .hat::before { border-color:var(--sev); }
  .legend .disp::before { border:1.6px dashed var(--ellie); } .legend .skill::before { background:var(--code-bg); }
  .legend .new::before { border-color:var(--moh); }
  table { border-collapse:collapse; width:100%; max-width:60rem; margin:1rem 0; font-size:.93rem; }
  th, td { border:1px solid var(--line); padding:.5rem .65rem; text-align:left; vertical-align:top; } th { background:var(--card); }
  .note { background:var(--card); border-left:4px solid var(--accent); padding:.7rem .9rem; border-radius:0 6px 6px 0; margin:1rem 0; max-width:52rem; }
  footer.doc { margin-top:3rem; padding-top:1rem; border-top:1px solid var(--line); color:var(--muted); font-size:.85rem; }
  @media print { .wrap { overflow:visible; border:none; } svg { width:100%; height:auto; } main { max-width:none; padding:0; } }
"""

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>dev-loop: a task from Ready to Done</title>
<style>{CSS}</style>
</head>
<body>
<main>
<header class="doc">
  <h1>A task from Ready to Done</h1>
  <div class="sub">Every agent and skill call in the dev-loop, in order, from a GitHub issue to a merged and closed task.</div>
</header>

<p>Read left to right by stage and top to bottom by who acts. The numbers give the order. Filled dark-red nodes are where the loop stops and waits for you. Nothing else in the diagram needs you at the screen. A small task stops exactly five times: intake, the approach brief, the UI walk, the PR open, and the delivery package.</p>

<div class="legend">
  <span class="stop">Stop: you act</span>
  <span class="auto">Gate that auto-passes (or stops)</span>
  <span class="sig">Sigmund, bookkeeping and sequencing</span>
  <span class="hat">Sev hat-swap, in session</span>
  <span class="disp">Clean-room dispatch, fresh context</span>
  <span class="skill">Skill, doc, or tool call</span>
</div>

<h2>The main pipeline</h2>
<div class="wrap">{MAIN_SVG}</div>
<div class="note">The dashed return arrows are the two loops that run without you. Review findings turn into Sev fixes and a re-verify until Ellie has no notes left. CI results and Copilot comments get triaged at every wake-up until the PR is clean. The adversarial cases are written from the brief's risk surface <em>without</em> sight of Sev's verification plan. Sigmund merges the two into the walk sheet you drive, and Ellie then checks that the walk covered them.</div>

<h2>The Dev Review track</h2>
<p>When the hand-over is someone else's finished PR on one of your repos, the task enters at Verification and the shape changes. Fixes go back to the author rather than to Sev, and the gates are the review set: comments, merge, notify.</p>
<div class="wrap">{DR_SVG}</div>

<h2>Who calls what</h2>
<table>
<tr><th>Called</th><th>By</th><th>When</th></tr>
<tr><td><code>ledger-template.md</code>, <code>issue.md</code> (<code>gh issue view</code>)</td><td>Sigmund</td><td>Intake, once per task</td></tr>
<tr><td><code>readiness-check.md</code></td><td>Sigmund (Sev standalone)</td><td>Intake, before any scoping</td></tr>
<tr><td><code>issue-cause-fix.md</code></td><td>Sev (brief); Sigmund (Dev Review)</td><td>After exploration, before the approach gate</td></tr>
<tr><td><code>va-humanizer</code></td><td>Every drafting skill, via dispatch</td><td>Before any outward-facing text reaches you (<code>humanize-gate.md</code>)</td></tr>
<tr><td><code>adversarial-cases.md</code> (Sonnet dispatch)</td><td>Sigmund, via dispatch</td><td>After the approach gate, on tasks with a regression surface. The cases join the walk sheet with their provenance marked.</td></tr>
<tr><td><code>conventions-checklist.md</code></td><td>Sev writes to it; Ellie reviews against it</td><td>Execution; review</td></tr>
<tr><td><code>confidence-check.md</code></td><td>Sigmund and Sev</td><td>Every commit and push</td></tr>
<tr><td><code>ellie</code> (<code>review-dispatch.md</code>)</td><td>Sigmund, via dispatch</td><td>When implementation completes; again after fixes. With the walk results, for the coverage check</td></tr>
<tr><td><code>va-pr-draft</code></td><td>Sigmund</td><td>Delivery, before the PR-open stop</td></tr>
<tr><td><code>task_metrics.py</code>, <code>va-share-learning</code></td><td>Sigmund</td><td>Closeout</td></tr>
</table>

<footer class="doc">dev-loop · docs/task-flow.html · generated from the pipeline spec; MANUAL.md remains the canonical prose.</footer>
</main>
</body>
</html>
"""
io.open(OUT, "w", encoding="utf-8", newline="\n").write(HTML)
print("wrote", OUT, len(HTML), "bytes;", len(STEPS), "steps;", f"{TOTAL_W:.0f}x{TOTAL_H:.0f}")
