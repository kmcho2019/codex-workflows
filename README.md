# Codex Workflows

Portable Codex workflow assets for personal use across machines.

This repository keeps reusable skills and global guidance in git so a new
server or container can install them with symlinks instead of manual copying.

## Layout

```text
codex-workflows/
  skills/
    goal-scaffold/
      SKILL.md
      agents/openai.yaml
      references/
      scripts/
  agents/
    AGENTS.md
    GUIDELINES.md
  install.sh
```

## Install

Clone the repo, then run:

```bash
bash install.sh
```

The installer symlinks:

- `skills/*` into `~/.codex/skills/`
- `skills/*` into `~/.agents/skills/`
- `agents/AGENTS.md` into `~/.codex/AGENTS.md`
- `agents/GUIDELINES.md` into `~/.codex/GUIDELINES.md`

Both skill locations are installed for portability across Codex setups.
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
| `goal-scaffold` | Create feature-goal planning docs under `docs/feature_history/<KST timestamp>_<slug>/` before manually launching `/goal` |

## Rules

- Do not store secrets, API keys, license keys, private datasets, or model
  weights here.
- Keep skills small and procedural.
- Put reusable scripts inside the relevant skill's `scripts/` directory.
- Put longer workflow references inside the relevant skill's `references/`
  directory.
- Keep machine-specific paths in local config or environment variables.
