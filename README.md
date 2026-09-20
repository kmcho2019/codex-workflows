# Codex Workflows

Portable Codex workflow assets for personal use across machines.

This repository keeps reusable skills and global guidance in git so a new
server or container can install them with symlinks instead of manual copying.

## Layout

```text
codex-workflows/
  skills/
    autoreview/
    grill-me/
    handoff/
    publication-figures/
    goal-scaffold/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
    teach/
  agents/
    AGENTS.md
    GUIDELINES.md
  third_party_licenses/
  install.sh
```

## Install

Clone the repo, then run:

```bash
bash install.sh
```

The installer symlinks:

- Active skills from `skills/*` into `~/.codex/skills/`
- Active skills from `skills/*` into `~/.agents/skills/`
- Active skills from `skills/*` into `~/.claude/skills/`
- `agents/AGENTS.md` into `~/.codex/AGENTS.md`
- `agents/GUIDELINES.md` into `~/.codex/GUIDELINES.md`

All three skill locations are installed for portability across agent setups.
`autoreview` is disabled for now: installation skips it and removes its symlinks
when they point to this checkout. Its source remains in `skills/autoreview/`;
remove the autoreview exclusion in `install.sh` and rerun it to re-enable.
Existing non-symlink targets are moved aside with a timestamped
`.backup.YYYYMMDD_HHMMSS` suffix before the symlink is created.

## Update

```bash
git pull
bash install.sh
```

Codex usually detects skill changes on restart. If a skill does not appear,
restart the Codex session.

## Current Skills

| Skill | Purpose |
| --- | --- |
| `adversarial-validate` | Test code, docs, claims, or visuals against explicit acceptance evidence |
| `autoreview` (disabled) | Retained pre-commit or pre-ship code review helper |
| `goal-audit` | Measure an active goal against repository evidence and identify the next priority |
| `goal-scaffold` | Create feature-goal planning docs under `docs/feature_history/<KST timestamp>_<slug>/` before manually launching `/goal` |
| `grill-me` | Stress-test a plan, decision, or idea through focused rounds of questions |
| `handoff` | Write a temporary handoff document so another agent can continue the work |
| `publication-figures` | Create polished, accessible, and reproducible figures for papers and professional reports |
| `review-bundle` | Package curated repository context for an external second opinion |
| `teach` | Teach focused lessons and practice, with an ongoing workspace when requested |

## Attribution

Some skills are copied or adapted from other MIT-licensed skill collections.
License texts are kept in `third_party_licenses/`.

| Skills | Source | Imported from | License |
| --- | --- | --- | --- |
| `grill-me` | https://github.com/mattpocock/skills | commit `9c9f36c` | MIT, see `third_party_licenses/mattpocock-skills-MIT.txt` |
| `handoff`, `teach` | https://github.com/mattpocock/skills | commit `5d78bd0` | MIT, see `third_party_licenses/mattpocock-skills-MIT.txt` |
| `autoreview` | https://github.com/openclaw/agent-skills | commit `283f069` | MIT, see `third_party_licenses/openclaw-agent-skills-MIT.txt` |
| `publication-figures` | https://github.com/alphaXiv/OpenResearch/tree/86d9be4bd2f771b7bbfda068d43468fe3e88a24a/agent-skills/orx-figures | commit `86d9be4` | MIT, see `third_party_licenses/alphaxiv-openresearch-MIT.txt` |

`grill-me` is self-contained here and is adapted from the upstream
`grill-me` alias plus the upstream `grilling` skill instructions.

## Rules

- Do not store secrets, API keys, license keys, private datasets, or model
  weights here.
- Keep skill triggers precise and instructions focused on outcomes.
- Following [GPT-6 Astra skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), load workflow-specific references only when needed.
- Put reusable scripts inside the relevant skill's `scripts/` directory.
- Put longer workflow references inside the relevant skill's `references/`
  directory.
- Keep machine-specific paths in local config or environment variables.
