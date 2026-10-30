"""0.6.0 additions: dispatched-agent transcripts, `index`, and `stamp`."""
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from task_metrics import (
    compute, render_block, stamp_session, ledger_summary, regenerate_index,
    find_subagent_transcripts, main, INDEX_BANNER, SESSIONS_HEADER,
)


def _jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")


def _usage(inp, out, ts="2026-09-01T09:00:00Z"):
    return {"timestamp": ts, "message": {"usage": {
        "input_tokens": inp, "output_tokens": out,
        "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}}}


SID = "aaaaaaaa-1111-2222-3333-444444444444"


def _task(tmp_path, ledger):
    d = tmp_path / "myapp-1"
    d.mkdir()
    (d / "ledger.md").write_text(ledger, encoding="utf-8")
    return d


def test_dispatched_agents_are_counted_and_split(tmp_path):
    root = tmp_path / "projects"
    proj = root / "C--work-x"
    _jsonl(proj / f"{SID}.jsonl", [_usage(100, 50)])
    _jsonl(proj / SID / "subagents" / "agent-a.jsonl", [_usage(10, 200)])
    _jsonl(proj / SID / "subagents" / "agent-b.jsonl", [_usage(10, 300)])
    task = _task(tmp_path, f"# myapp-1 — t\n\n## Metrics\n\n- session: {SID} · stage: Execution\n")

    assert len(find_subagent_transcripts(SID, root)) == 2
    m = compute(task, root)
    assert m["totals"]["output"] == 550            # parent + both agents
    assert m["dispatched"] == {"agents": 2, "input": 20, "output": 500,
                               "cache_read": 0, "cache_create": 0}
    assert m["sessions"][0]["sub_agents"] == 2
    assert m["by_stage"]["Execution"]["output"] == 550   # agents inherit the parent's stage
    block = render_block(m)
    assert "dispatched 2 (out 500)" in block
    assert "**Dispatched:** 2 agent(s)" in block and "(90% of output)" in block


def test_no_dispatched_agents_keeps_old_shape(tmp_path):
    root = tmp_path / "projects"
    _jsonl(root / "C--work-x" / f"{SID}.jsonl", [_usage(100, 50)])
    task = _task(tmp_path, f"# myapp-1 — t\n\n## Metrics\n\n- session: {SID}\n")
    m = compute(task, root)
    assert m["totals"]["output"] == 50 and m["dispatched"]["agents"] == 0
    assert "Dispatched" not in render_block(m)


def test_stamp_inserts_after_existing_sessions_and_is_idempotent():
    text = ("# myapp-1 — t\n\n## Metrics\n\n" + SESSIONS_HEADER + "\n\n"
            "- session: bbbbbbbb-0000-0000-0000-000000000000 · stage: Intake\n\n"
            "<!-- metrics:begin -->\nx\n<!-- metrics:end -->\n\n## Session journal\n")
    new, changed = stamp_session(text, SID, "Execution")
    assert changed
    lines = new.splitlines()
    i = lines.index("- session: bbbbbbbb-0000-0000-0000-000000000000 · stage: Intake")
    assert lines[i + 1] == f"- session: {SID} · stage: Execution"
    assert new.index("<!-- metrics:begin -->") > new.index(SID)
    again, changed2 = stamp_session(new, SID, "Delivery")
    assert not changed2 and again == new            # first annotation wins


def test_stamp_creates_metrics_section_when_missing():
    new, changed = stamp_session("# myapp-1 — t\n\n## Session journal\n", SID, "Intake")
    assert changed and "## Metrics" in new and f"- session: {SID} · stage: Intake" in new


LEDGER_ACTIVE = """# myapp-2 — A long **bold** title with a [link](http://x) in it

- **Issue:** x
- **Stage:** Verification — Dev Review → **TAKEN OVER 2026-08-31** (dev: "take over"); I author the revision on the PR. Still ungated (docs only — no specialist).
- **Posture:** lead

## Now / Next

- **Last done:** 2026-09-02 14:10 — G-APPROACH passed
- **Next action:** All my PRs raised. **Backport DELIVERED** (#238 merged). main has fix+docs (#57/#59 merged). release has fix (#58 merged) → **downstream repo** bumps its own pointer (not me). Only [myapp-web#1038](https://github.com/x/pull/1038) pending merge = the web client. When it merges → closeout.
- **Waiting on:** reviewer to build/run the failing case locally and report back with the log
"""

LEDGER_DONE = """# myapp-3 — Done task

- **Stage:** **Done** — both lines merged
- **Posture:** lead

## Now / Next

- **Last done:** 2026-08-20 — closed
- **Next action:** —

## Metrics

**Sessions:** 3
**Tokens:** in 1,000 · out 2,500 · cache-read 0 · cache-write 0
"""


def test_index_caps_cells_and_puts_done_last(tmp_path):
    (tmp_path / "myapp-2").mkdir(); (tmp_path / "myapp-2" / "ledger.md").write_text(LEDGER_ACTIVE, encoding="utf-8")
    (tmp_path / "myapp-3").mkdir(); (tmp_path / "myapp-3" / "ledger.md").write_text(LEDGER_DONE, encoding="utf-8")
    (tmp_path / "no-ledger").mkdir()

    r = ledger_summary(tmp_path / "myapp-2" / "ledger.md")
    assert r["title"] == "A long bold title with a link in it"
    assert len(r["stage"]) <= 71 and r["stage"].startswith("Verification — Dev Review")
    assert len(r["next"]) <= 141 and "**" not in r["next"] and "](" not in r["next"]
    assert len(r["waiting"]) <= 61
    assert r["updated"] == "2026-09-02 14:10" and not r["done"]

    d = ledger_summary(tmp_path / "myapp-3" / "ledger.md")
    assert d["done"] and d["totals"] == "out 2,500 · 3 sess"

    text, rows = regenerate_index(tmp_path)
    assert INDEX_BANNER in text and len(rows) == 2
    assert text.index("| myapp-2 |") < text.index("| myapp-3 |")   # active before done
    assert "1 active · 1 done" in text

    assert main(["index", str(tmp_path), "--write"]) == 0
    assert (tmp_path / "INDEX.md").read_text(encoding="utf-8") == text
