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
| `autoreview` | Run a structured pre-commit or pre-ship code review helper |
| `goal-scaffold` | Create feature-goal planning docs under `docs/feature_history/<KST timestamp>_<slug>/` before manually launching `/goal` |
| `grill-me` | Stress-test a plan or design with one-question-at-a-time interrogation |
| `handoff` | Write a temporary handoff document so another agent can continue the work |
| `review-bundle` | Package curated repository context for an external second opinion |
| `teach` | Build a stateful teaching workspace with lessons, references, resources, and learning records |

## Attribution

Some skills are copied or adapted from other MIT-licensed skill collections.
License texts are kept in `third_party_licenses/`.

| Skills | Source | Imported from | License |
| --- | --- | --- | --- |
| `grill-me`, `handoff`, `teach` | https://github.com/mattpocock/skills | commit `5d78bd0` | MIT, see `third_party_licenses/mattpocock-skills-MIT.txt` |
| `autoreview` | https://github.com/openclaw/agent-skills | commit `283f069` | MIT, see `third_party_licenses/openclaw-agent-skills-MIT.txt` |

`grill-me` is self-contained here and is adapted from the upstream
`grill-me` alias plus the upstream `grilling` skill instructions.

## Rules

- Do not store secrets, API keys, license keys, private datasets, or model
  weights here.
- Keep skills small and procedural.
- Put reusable scripts inside the relevant skill's `scripts/` directory.
- Put longer workflow references inside the relevant skill's `references/`
  directory.
- Keep machine-specific paths in local config or environment variables.
