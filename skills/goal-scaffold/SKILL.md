---
name: goal-scaffold
description: Create reusable feature-goal planning scaffolds for Codex goal sessions. Use when the user wants to turn a feature, investigation, benchmark, refactor, reproduction effort, or other uncertain multi-step task into local Markdown planning docs before manually launching `/goal`; especially when they mention goal_template.md, implementation_todo, implementation_history, adversarial validation prompts, quantitative gates, blockers, or docs/feature_history.
---

# Goal Scaffold

## Workflow

Use this skill to prepare goal-launch docs, not to start `/goal`.

1. Read the user's feature description, blockers, constraints, and validation
   criteria.
2. Inspect local conventions before writing:
   - `GUIDELINES.md` or `AGENTS.md` when present;
   - recent `*_plan.md`, `*_implementation_todo.md`,
     `*_implementation_history.md`, `goal_template.md`, and
     `*_adversarial_prompt.md` examples.
3. Choose a short slug. Use lowercase letters, digits, and underscores.
4. Create docs under:
   `docs/feature_history/<YYYYMMDD_HHMMSS_KST>_<slug>/`.
5. Generate the standard file set with `scripts/scaffold_goal_docs.py`, then
   edit the drafts so they are specific to the user's request.
6. Stop after the docs are ready for user review. Do not activate `/goal`.

## Standard Files

Each scaffold directory must contain:

- `<slug>_plan.md`: consolidated plan, requirements, intent, specs, gates,
  boundaries, risks, and done criteria.
- `<slug>_implementation_todo.md`: concise living checklist with a line limit
  stated at the top. Keep it skimmable and update-oriented.
- `<slug>_implementation_history.md`: unbounded journal for notable decisions,
  runs, experiments, commands, evidence, failures, and commits.
- `goal_template.md`: copy/paste `/goal` text, preferably under 4000
  characters, linking to the plan for full details.
- `<slug>_adversarial_prompt.md`: prompt for an independent sub-agent to judge
  whether the goal is actually achieved.
- `<slug>_subagent_validation_report.md`: placeholder output file the
  sub-agent should write.

## Goal Template Requirements

Write `goal_template.md` as a compact contract:

- Outcome: what must be true at the end.
- Verification surface: commands, benchmarks, reports, artifacts, hashes, or
  source evidence that prove it.
- Constraints: what must not regress.
- Boundaries: files, tools, repos, data, GPUs, outputs, and ignored artifacts
  Codex may use.
- Iteration policy: how Codex chooses the next action after each attempt.
- Blocked stop condition: when Codex should stop and what evidence/input would
  unlock progress.

The template should point to `<slug>_plan.md` for details and to
`<slug>_implementation_todo.md` as the living checklist.

## Adversarial Validation Requirements

The adversarial prompt must tell the sub-agent to inspect evidence, not trust
the implementer summary. It should require PASS or FAIL and a written report.

Ask the validator to check:

- quantitative gates and command evidence;
- reward hacking or metric gaming that violates the original intent;
- missing or weak tests;
- missing docs or unclear user/contributor guidance;
- simple, skimmable code organization aligned with local `GUIDELINES.md`;
- asserts for required data, narrow states, type hints, and useful docstrings;
- commit quality, including atomicity, signed-off commits, and clear messages;
- gaps, blocked claims, and paper-facing or production-facing uncertainty.

The validator should return PASS only when the feature satisfies the plan and
the evidence is reproducible enough for the stated claim.

## Script

Use the helper from the skill directory:

```bash
python ~/.codex/skills/goal-scaffold/scripts/scaffold_goal_docs.py \
  --repo-root . \
  --feature-name "SparseVLM full MME reproduction" \
  --summary-file /tmp/feature_summary.md
```

If no summary file exists, pass `--summary` with a short quoted description.
After generation, edit the files directly to incorporate details from the user
and local repo examples.

Read `references/goal_contract.md` only when more detail is needed about goal
wording or adversarial validation structure.
