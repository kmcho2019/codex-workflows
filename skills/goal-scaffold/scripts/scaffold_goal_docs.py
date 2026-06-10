#!/usr/bin/env python3
"""Create feature goal planning documents under docs/feature_history."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def main() -> None:
    args = _parse_args()
    repo_root = args.repo_root.resolve()
    assert repo_root.is_dir(), repo_root
    summary = args.summary or ""
    if args.summary_file is not None:
        assert args.summary_file.is_file(), args.summary_file
        summary = args.summary_file.read_text().strip()
    assert summary.strip(), "Pass --summary or --summary-file"

    slug = args.slug or _slug(args.feature_name)
    assert slug, args.feature_name
    timestamp = datetime.now(ZoneInfo("Asia/Seoul")).strftime("%Y%m%d_%H%M%S_KST")
    root = repo_root / "docs" / "feature_history" / f"{timestamp}_{slug}"
    if root.exists() and not args.force:
        raise SystemExit(f"exists: {root}")
    root.mkdir(parents=True, exist_ok=args.force)

    files = {
        f"{slug}_plan.md": _plan(args.feature_name, slug, summary),
        f"{slug}_implementation_todo.md": _todo(
            args.feature_name, slug, args.todo_line_limit
        ),
        f"{slug}_implementation_history.md": _history(args.feature_name, slug),
        "goal_template.md": _goal_template(args.feature_name, slug),
        f"{slug}_adversarial_prompt.md": _adversarial(args.feature_name, slug),
        f"{slug}_subagent_validation_report.md": _subagent_report(
            args.feature_name
        ),
    }
    for name, text in files.items():
        path = root / name
        if path.exists() and not args.force:
            raise SystemExit(f"exists: {path}")
        path.write_text(text)
    print(root)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--feature-name", required=True)
    parser.add_argument("--slug")
    parser.add_argument("--summary")
    parser.add_argument("--summary-file", type=Path)
    parser.add_argument("--todo-line-limit", type=int, default=120)
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def _slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return re.sub(r"_+", "_", slug)[:64].strip("_")


def _plan(feature: str, slug: str, summary: str) -> str:
    return f"""# {feature} Plan

Feature slug: `{slug}`

## Outcome

{summary}

## Source Of Truth

- Living checklist: `{slug}_implementation_todo.md`
- Implementation history: `{slug}_implementation_history.md`
- Goal template: `goal_template.md`
- Adversarial rubric: `{slug}_adversarial_prompt.md`
- Sub-agent report: `{slug}_subagent_validation_report.md`

## Requirements

- TODO: state the user-visible capability or research artifact.
- TODO: state the required interfaces, commands, reports, or outputs.
- TODO: state the quantitative gates and qualitative gates.
- TODO: state what must not regress.

## Boundaries

- TODO: list allowed files, repos, tools, data, GPUs, and output directories.
- TODO: list out-of-scope work and claims that must not be made.

## Implementation Plan

1. TODO: gather baseline evidence.
2. TODO: implement the smallest useful change.
3. TODO: add or update focused tests.
4. TODO: update usage docs and reproducibility notes.
5. TODO: run validation commands and record evidence.
6. TODO: request adversarial validation and resolve any FAIL findings.

## Completion Gates

- [ ] TODO: quantitative gate.
- [ ] TODO: correctness or regression test gate.
- [ ] TODO: documentation gate.
- [ ] TODO: reproducibility or artifact hash gate.
- [ ] `ruff`/`ty`/tests pass, adjusted for this repo's normal commands.
- [ ] Adversarial sub-agent returns PASS and writes the validation report.

## Risks And Blockers

- TODO: list likely blockers.
- TODO: list what evidence would prove each blocker is resolved.
"""


def _todo(feature: str, slug: str, line_limit: int) -> str:
    return f"""# {feature} TODO

Line limit: {line_limit} lines. Keep this checklist concise. Move details to
`{slug}_implementation_history.md`.

Central plan: `{slug}_plan.md`.
Adversarial rubric: `{slug}_adversarial_prompt.md`.

## Current Status

- [ ] Confirm scope, branch, and output directory.
- [ ] Fill in the plan's concrete gates and boundaries.
- [ ] Establish baseline evidence.
- [ ] Implement the first highest-risk workstream.
- [ ] Add focused tests.
- [ ] Update usage and contributor docs.
- [ ] Run validation commands.
- [ ] Record final evidence in history.
- [ ] Run adversarial validation.

## Completion Gates

- [ ] Outcome in `{slug}_plan.md` is satisfied.
- [ ] Quantitative gates are met without reward hacking.
- [ ] Correctness and regression tests pass.
- [ ] Documentation explains how to use and reproduce the feature.
- [ ] `{slug}_subagent_validation_report.md` records adversarial PASS.

## Open Follow-Ups

- [ ] TODO: non-blocking follow-up.
"""


def _history(feature: str, slug: str) -> str:
    return f"""# {feature} Implementation History

Unbounded journal for `{slug}`. Record notable decisions, commands, outputs,
experiments, failed attempts, blockers, commits, and validation evidence.

## Session Start

- TODO: record branch, HEAD, dirty state, feature directory, and initial goal.
"""


def _goal_template(feature: str, slug: str) -> str:
    return f"""# Goal Template

Use this as a draft for `/goal` after reviewing the local plan. Keep the
activated goal under 4000 characters when possible.

```text
/goal Complete {feature} as specified in {slug}_plan.md, verified by the
living checklist in {slug}_implementation_todo.md, the evidence recorded in
{slug}_implementation_history.md, passing the stated quantitative gates,
correctness checks, documentation requirements, and adversarial validation.

Work only within the boundaries listed in {slug}_plan.md. Use local repo
commands and artifacts as the verification surface. Keep the TODO concise and
update the history with notable decisions, commands, failures, and evidence.

Between iterations, choose the next action that removes the highest-risk
blocker or most uncertain validation gap. Do not claim success from a metric
alone if the implementation diverges from the original intent.

Completion requires the adversarial validator prompt in
{slug}_adversarial_prompt.md to return PASS and write
{slug}_subagent_validation_report.md. If blocked for three concrete attempts,
stop with the attempted paths, evidence gathered, blocker, and exact input or
resource needed to continue.
```
"""


def _adversarial(feature: str, slug: str) -> str:
    return f"""# {feature} Adversarial Validation Prompt

You are an adversarial validation sub-agent. Decide whether `{feature}` is
actually complete according to `{slug}_plan.md`.

Read:

- `{slug}_plan.md`
- `{slug}_implementation_todo.md`
- `{slug}_implementation_history.md`
- relevant code, tests, docs, artifacts, and git commits

Write your report to `{slug}_subagent_validation_report.md`.

Return `PASS` only if the implementation satisfies the original intent and the
evidence is reproducible. Otherwise return `FAIL`.

Check:

- quantitative gates and command evidence;
- reward hacking, cherry-picking, data leakage, or metric gaming;
- skipped hard cases or claims broader than the evidence;
- tests for important behavior and regressions;
- docs that explain usage, reproduction, and limitations;
- simple, skimmable code with narrow states and clear types;
- asserts for required data instead of silent defaults;
- useful docstrings/type hints where they help maintenance;
- commit quality: atomic changes, signed-off commits, clear messages;
- unresolved blockers and what would unlock progress.

Report format:

```markdown
# {feature} Sub-Agent Validation Report

## Verdict

PASS or FAIL

## Evidence Checked

## Findings

## Missing Or Weak Evidence

## Reward-Hacking Or Intent Risks

## Required Fixes Before PASS
```
"""


def _subagent_report(feature: str) -> str:
    return f"""# {feature} Sub-Agent Validation Report

## Verdict

PENDING

## Evidence Checked

## Findings

## Missing Or Weak Evidence

## Reward-Hacking Or Intent Risks

## Required Fixes Before PASS
"""


if __name__ == "__main__":
    main()
