#!/usr/bin/env bash
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_SUFFIX="backup.$(date +%Y%m%d_%H%M%S)"

mkdir -p "$HOME/.codex/skills"
mkdir -p "$HOME/.claude/skills"
mkdir -p "$HOME/.agents/skills"
mkdir -p "$HOME/.codex"

link_path() {
  local source="$1"
  local target="$2"
  if [ -L "$target" ] || [ ! -e "$target" ]; then
    ln -sfn "$source" "$target"
    return
  fi
  mv "$target" "$target.$BACKUP_SUFFIX"
  ln -sfn "$source" "$target"
}

for skill in "$REPO"/skills/*; do
  [ -d "$skill" ] || continue
  name="$(basename "$skill")"
  # Keep autoreview in source, but disable its installed discovery links.
  if [ "$name" = autoreview ]; then
    for target in "$HOME/.codex/skills/$name" "$HOME/.agents/skills/$name" "$HOME/.claude/skills/$name"; do
      if [ -L "$target" ] && [ "$(readlink "$target")" = "$skill" ]; then
        rm "$target"
      fi
    done
    continue
  fi
  link_path "$skill" "$HOME/.codex/skills/$name"
  link_path "$skill" "$HOME/.agents/skills/$name"
  link_path "$skill" "$HOME/.claude/skills/$name"
done

link_path "$REPO/agents/AGENTS.md" "$HOME/.codex/AGENTS.md"
link_path "$REPO/agents/GUIDELINES.md" "$HOME/.codex/GUIDELINES.md"

echo "Installed Codex workflows from $REPO"
