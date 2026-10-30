import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from task_metrics import (
    BEGIN, END, SESSION_RE,
    parse_ledger, sum_usage, find_transcript, render_block, update_ledger_text,
    run_task, main, compute,
)

# Ledger in the current (0.4.0) template shape: Pipeline state carries a
# single When column, the Decision log holds pending decisions as rows with
# a blank Decision, and neither table is parsed by the script — only the
# session lines and the Delegation log are.
LEDGER = """# myapp-999 — Test task

## Pipeline state

| Gate | Status | When | By |
|---|---|---|---|
| G-READINESS | done | 2026-08-04 08:05 | dev |
| G-APPROACH | done | 2026-08-04 08:40 | dev |
| G-ISSUE | pending | | |

## Decision log

| # | Gate | When | Question | Decided by | Decision |
|---|------|------|----------|------------|----------|
| 1 | G-APPROACH | 2026-08-04 09:30 | Approve brief? | dev | Approved |
| 2 | G-UI | 2026-08-04 11:00 | Walk the UI? | | |

## Metrics

- session: aaaaaaaa-1111-2222-3333-444444444444
- session: bbbbbbbb-1111-2222-3333-444444444444 · stage: Execution (resumed after compaction)

<!-- metrics:begin -->
old content
<!-- metrics:end -->
"""


def test_parse_ledger_sessions_dedupe_annotated_lines():
    parsed = parse_ledger(LEDGER)
    assert parsed["sessions"] == [
        "aaaaaaaa-1111-2222-3333-444444444444",
        "bbbbbbbb-1111-2222-3333-444444444444",
    ]
    # stage annotation captured where present, absent key where not
    assert parsed["session_stages"] == {
        "bbbbbbbb-1111-2222-3333-444444444444": "Execution",
    }


def test_session_re_matches_trailing_annotation():
    text = "- session: cccccccc-1111-2222-3333-444444444444 (resumed after compaction)"
    assert SESSION_RE.findall(text) == ["cccccccc-1111-2222-3333-444444444444"]


def test_parse_ledger_stage_annotation_first_wins():
    sid = "dddddddd-1111-2222-3333-444444444444"
    text = (f"- session: {sid} · stage: Planning\n"
            f"- session: {sid} · stage: Execution\n")
    parsed = parse_ledger(text)
    assert parsed["session_stages"][sid] == "Planning"


def test_non_delegation_tables_contribute_nothing():
    # Pipeline state, Decision log, and Review outcomes rows are data-shaped
    # (timestamps, int-leading cells) but the script must ignore them — only
    # the Delegation log is parsed, and only via its Model column. A
    # pre-0.3.0 Delegation log (no Model column) also contributes nothing:
    # the "What" cell must not be misread as a model name.
    text = """# myapp-1002 — Section-scoping regression

## Pipeline state

| Gate | Status | When | By |
|---|---|---|---|
| G-APPROACH | done | 2026-08-04 08:30 | dev |

## Decision log

| # | Gate | When | Question | Decided by | Decision |
|---|------|------|----------|------------|----------|
| 1 | G-APPROACH | 2026-08-04 09:30 | Approve brief? | dev | Approved |

## Review outcomes

| Round | Reviewer | Raised | Valid (applied) | Invalid (pushed back) | Worst valid severity |
|---|---|---|---|---|---|
| 1 | Ellie | 2026-08-04 10:00 | 3 | 1 | Should-fix |

## Delegation log

| Date | To | What | Outcome |
|------|----|------|---------|
| 2026-08-04 | Sev | Implement step 3 | Done |
"""
    parsed = parse_ledger(text)
    assert parsed["dispatch_models"] == {}
    assert parsed["sessions"] == []


def test_delegation_log_model_column_counting():
    text = """# myapp-1003 — Model column

## Delegation log

| Date | To | Model | What | Outcome |
|------|----|-------|------|---------|
| 2026-08-08 | Sev | opus | Implement step 3 | Done |
| 2026-08-08 | explorer | sonnet | Fan-out over callers | Done |
| 2026-08-08 | Ellie | opus | Clean-room review | 2 findings |
| 2026-08-08 | task_metrics.py | | Closeout metrics | Written |
"""
    parsed = parse_ledger(text)
    # blank Model cell rolls up as "—"; separator row is not a data row
    assert parsed["dispatch_models"] == {"opus": 2, "sonnet": 1, "—": 1}


def _write_jsonl(path, records):
    path.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")


def test_sum_usage(tmp_path):
    p = tmp_path / "s.jsonl"
    _write_jsonl(p, [
        {"timestamp": "2026-08-04T09:00:00Z", "type": "user"},
        {"timestamp": "2026-08-04T09:05:00Z", "message": {"usage": {
            "input_tokens": 100, "output_tokens": 50,
            "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 20}}},
        {"not": "a message"},
        {"timestamp": "2026-08-04T10:00:00Z", "message": {"usage": {
            "input_tokens": 10, "output_tokens": 5}}},
    ])
    u = sum_usage(p)
    assert (u["input"], u["output"], u["cache_read"], u["cache_create"]) == (110, 55, 1000, 20)
    assert u["first"] == "2026-08-04T09:00:00Z" and u["last"] == "2026-08-04T10:00:00Z"


def test_find_transcript(tmp_path):
    proj = tmp_path / "C--work-vRepos-x"
    proj.mkdir()
    sid = "aaaaaaaa-1111-2222-3333-444444444444"
    (proj / f"{sid}.jsonl").write_text("", encoding="utf-8")
    assert find_transcript(sid, tmp_path).name == f"{sid}.jsonl"
    assert find_transcript("missing", tmp_path) is None


def test_update_ledger_text_idempotent():
    block = "TOTALS GO HERE"
    once = update_ledger_text(LEDGER, block)
    assert "old content" not in once and "TOTALS GO HERE" in once
    twice = update_ledger_text(once, block)
    assert twice == once


def test_update_ledger_text_appends_section_when_markers_missing():
    text = "# myapp-1 — No markers yet\n\nSome content.\n"
    block = "TOTALS"
    updated = update_ledger_text(text, block)
    assert updated.count(BEGIN) == 1 and updated.count(END) == 1
    assert "## Metrics" in updated
    assert "TOTALS" in updated
    assert "Some content." in updated  # original content preserved

    updated2 = update_ledger_text(updated, "NEW TOTALS")
    assert updated2.count(BEGIN) == 1 and updated2.count(END) == 1
    assert "NEW TOTALS" in updated2 and "TOTALS GO HERE" not in updated2


def _base_metrics(**overrides):
    m = {
        "key": "myapp-999",
        "sessions": [],
        "missing": [],
        "totals": {"input": 100, "output": 50, "cache_read": 10, "cache_create": 5},
        "by_stage": {},
        "dispatch_models": {},
        "first": None, "last": None,
    }
    m.update(overrides)
    return m


def test_render_block_totals_and_wallclock():
    block = render_block(_base_metrics())
    assert "cache-write 5" in block
    assert "**Wall-clock:**" in block
    # gate-wait tracking was removed in 0.4.0 — the block must not mention it
    assert "Gate wait" not in block


def test_render_block_per_session_stage_and_dispatch_lines():
    sessions = [
        {"id": "aaaaaaaa-1111-2222-3333-444444444444", "stage": "Execution",
         "input": 100, "output": 50, "cache_read": 1000, "cache_create": 20,
         "first": None, "last": None},
        {"id": "bbbbbbbb-1111-2222-3333-444444444444", "stage": None,
         "input": 10, "output": 5, "cache_read": 100, "cache_create": 2,
         "first": None, "last": None},
    ]
    by_stage = {
        "Execution": {"input": 100, "output": 50, "cache_read": 1000,
                      "cache_create": 20, "count": 1},
        "unannotated": {"input": 10, "output": 5, "cache_read": 100,
                        "cache_create": 2, "count": 1},
    }
    block = render_block(_base_metrics(
        sessions=sessions, by_stage=by_stage,
        dispatch_models={"sonnet": 3, "opus": 2}))
    assert "- `aaaaaaaa` · Execution · in 100 · out 50 · cache-read 1,000" in block
    assert "- `bbbbbbbb` · — · in 10 · out 5 · cache-read 100" in block
    # pipeline-ordered, unannotated last
    assert ("**By stage:** Execution in 100 · out 50 (1) — "
            "unannotated in 10 · out 5 (1)") in block
    assert "**Dispatches:** 5 — opus 2 · sonnet 3" in block


def test_render_block_omits_stage_and_dispatch_lines_when_absent():
    # all-unannotated sessions (a pre-0.3.0 ledger): no By-stage line, and no
    # Dispatches line without model data
    by_stage = {"unannotated": {"input": 10, "output": 5, "cache_read": 0,
                                "cache_create": 0, "count": 1}}
    block = render_block(_base_metrics(by_stage=by_stage))
    assert "By stage" not in block
    assert "Dispatches" not in block


def test_compute_attaches_stage_and_rolls_up_by_stage(tmp_path):
    task_dir = tmp_path / "myapp-3000"
    task_dir.mkdir()
    sid_a = "aaaaaaaa-1111-2222-3333-444444444444"
    sid_b = "bbbbbbbb-1111-2222-3333-444444444444"
    (task_dir / "ledger.md").write_text(
        "# myapp-3000\n\n## Metrics\n\n"
        f"- session: {sid_a} · stage: Planning\n"
        f"- session: {sid_b}\n",
        encoding="utf-8")
    projects_root = tmp_path / "projects"
    proj = projects_root / "C--work-vRepos-x"
    proj.mkdir(parents=True)
    _write_jsonl(proj / f"{sid_a}.jsonl", [
        {"timestamp": "2026-08-08T09:00:00Z", "message": {"usage": {
            "input_tokens": 100, "output_tokens": 50}}}])
    _write_jsonl(proj / f"{sid_b}.jsonl", [
        {"timestamp": "2026-08-08T10:00:00Z", "message": {"usage": {
            "input_tokens": 10, "output_tokens": 5}}}])

    m = compute(task_dir, projects_root)
    assert m["sessions"][0]["stage"] == "Planning"
    assert m["sessions"][1]["stage"] is None
    assert m["by_stage"]["Planning"] == {
        "input": 100, "output": 50, "cache_read": 0, "cache_create": 0,
        "count": 1}
    assert m["by_stage"]["unannotated"]["input"] == 10
    assert m["by_stage"]["unannotated"]["count"] == 1


LEDGER_DUP = """# myapp-999 — Test task

## Decision log

| # | Gate | When | Question | Decided by | Decision |
|---|------|------|----------|------------|----------|
| 1 | G-APPROACH | 2026-08-04 09:30 | Approve brief? | dev | Approved |

## Metrics

- session: aaaaaaaa-1111-2222-3333-444444444444
- session: aaaaaaaa-1111-2222-3333-444444444444

<!-- metrics:begin -->
old content
<!-- metrics:end -->
"""


def _strip_computed(text):
    return "\n".join(l for l in text.splitlines() if not l.strip().startswith("*Computed "))


def test_run_task_end_to_end_dedupes_and_writes(tmp_path):
    task_dir = tmp_path / "myapp-999"
    task_dir.mkdir()
    (task_dir / "ledger.md").write_text(LEDGER_DUP, encoding="utf-8")

    projects_root = tmp_path / "projects"
    proj = projects_root / "C--work-vRepos-x"
    proj.mkdir(parents=True)
    sid = "aaaaaaaa-1111-2222-3333-444444444444"
    _write_jsonl(proj / f"{sid}.jsonl", [
        {"timestamp": "2026-08-04T09:00:00Z", "message": {"usage": {
            "input_tokens": 100, "output_tokens": 50,
            "cache_read_input_tokens": 1000, "cache_creation_input_tokens": 20}}},
    ])

    m = run_task(task_dir, projects_root, write=True)

    # duplicated "- session:" line counts the session exactly once
    assert len(m["sessions"]) == 1
    assert m["totals"] == {"input": 100, "output": 50, "cache_read": 1000, "cache_create": 20}

    written_once = (task_dir / "ledger.md").read_text(encoding="utf-8")
    assert "<!-- metrics:begin -->" in written_once and "<!-- metrics:end -->" in written_once
    assert "old content" not in written_once
    assert "**Sessions:** 1" in written_once

    run_task(task_dir, projects_root, write=True)
    written_twice = (task_dir / "ledger.md").read_text(encoding="utf-8")
    # strip the `Computed <ts>` stamp so a minute-boundary tick can't flake this
    assert _strip_computed(written_twice) == _strip_computed(written_once)


def test_run_task_appends_metrics_section_when_missing(tmp_path, capsys):
    # No "## Metrics" heading anywhere -> a whole new section goes at EOF.
    task_dir = tmp_path / "myapp-1000"
    task_dir.mkdir()
    (task_dir / "ledger.md").write_text(
        "# myapp-1000 — No markers, no heading\n\nSome narrative text.\n",
        encoding="utf-8")
    projects_root = tmp_path / "projects"
    projects_root.mkdir()

    run_task(task_dir, projects_root, write=True)
    out = capsys.readouterr().out
    assert "appended" in out.lower()
    assert "wrote metrics block" not in out.lower()

    written = (task_dir / "ledger.md").read_text(encoding="utf-8")
    assert BEGIN in written and END in written
    assert written.count("## Metrics") == 1


def test_update_ledger_text_inserts_under_existing_heading_without_duplicating_it():
    # A "## Metrics" heading already exists (e.g. copied from the template)
    # but the marker pair is missing -- insert under it, don't add a second
    # heading at EOF, and don't disturb what's already in that section or
    # what follows it.
    text = (
        "# myapp-1001 — Heading exists, markers missing\n\n"
        "## Metrics\n\n"
        "Sessions (record at every wake-up):\n\n"
        "- session: aaaaaaaa-1111-2222-3333-444444444444\n\n"
        "## Session journal\n\n"
        "- 2026-08-04 09:00: kicked off\n"
    )
    updated = update_ledger_text(text, "TOTALS")

    assert updated.count("## Metrics") == 1
    assert updated.count(BEGIN) == 1 and updated.count(END) == 1
    assert "- session: aaaaaaaa-1111-2222-3333-444444444444" in updated
    assert "TOTALS" in updated
    # the marker block lands inside the Metrics section, before the next heading
    metrics_pos = updated.index("## Metrics")
    journal_pos = updated.index("## Session journal")
    begin_pos = updated.index(BEGIN)
    assert metrics_pos < begin_pos < journal_pos
    # nothing after the Metrics section got reordered or dropped
    assert "- 2026-08-04 09:00: kicked off" in updated
    assert updated.index("- 2026-08-04 09:00: kicked off") > journal_pos

    # applying again with a new block replaces in place, still one heading
    updated2 = update_ledger_text(updated, "NEW TOTALS")
    assert updated2.count("## Metrics") == 1
    assert "NEW TOTALS" in updated2 and "TOTALS" not in updated2.replace("NEW TOTALS", "")


def test_main_all_dedupes_shared_session_across_ledgers(tmp_path, capsys):
    tasks_root = tmp_path / "Tasks"
    (tasks_root / "myapp-A").mkdir(parents=True)
    (tasks_root / "myapp-B").mkdir(parents=True)
    shared = "aaaaaaaa-1111-2222-3333-444444444444"
    only_a = "bbbbbbbb-1111-2222-3333-444444444444"
    only_b = "cccccccc-1111-2222-3333-444444444444"
    (tasks_root / "myapp-A" / "ledger.md").write_text(
        "# myapp-A\n\n## Metrics\n\n"
        f"- session: {shared}\n- session: {only_a}\n\n"
        f"{BEGIN}\nold\n{END}\n", encoding="utf-8")
    (tasks_root / "myapp-B" / "ledger.md").write_text(
        "# myapp-B\n\n## Metrics\n\n"
        f"- session: {shared}\n- session: {only_b}\n\n"
        f"{BEGIN}\nold\n{END}\n", encoding="utf-8")

    projects_root = tmp_path / "projects"
    proj = projects_root / "C--work-vRepos-x"
    proj.mkdir(parents=True)
    _write_jsonl(proj / f"{shared}.jsonl", [
        {"timestamp": "2026-08-04T09:00:00Z", "message": {"usage": {
            "input_tokens": 100, "output_tokens": 10}}},
    ])
    _write_jsonl(proj / f"{only_a}.jsonl", [
        {"timestamp": "2026-08-04T09:00:00Z", "message": {"usage": {
            "input_tokens": 5, "output_tokens": 1}}},
    ])
    _write_jsonl(proj / f"{only_b}.jsonl", [
        {"timestamp": "2026-08-04T09:00:00Z", "message": {"usage": {
            "input_tokens": 7, "output_tokens": 2}}},
    ])

    main(["--all", str(tasks_root), "--projects-root", str(projects_root)])
    out = capsys.readouterr().out

    # shared session's 100/10 counted once, plus only_a (5/1) and only_b (7/2)
    assert "in 112" in out and "out 13" in out
    assert "shared sessions counted once: 1" in out
