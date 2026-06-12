#!/usr/bin/env bash
# Instala los skills /handoff y /handon de este repo en Claude Code (nivel usuario).
# Crea symlinks en ~/.claude/skills/ apuntando a las carpetas de este repo, de modo
# que en cualquier Mac nuevo baste con:  clonar el repo  +  bash install-skills.sh
#
# Idempotente: re-ejecutarlo reescribe los symlinks sin tocar nada más.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$REPO_ROOT/skills"
SKILLS_DST="$HOME/.claude/skills"

mkdir -p "$SKILLS_DST"
chmod +x "$SKILLS_SRC/lib/locate-repo.sh" "$REPO_ROOT/scripts/send-handoff-telegram.py" 2>/dev/null || true

link_skill() {
  local name="$1"
  local src="$SKILLS_SRC/$name"
  local dst="$SKILLS_DST/$name"
  if [ ! -d "$src" ]; then
    echo "  ✗ no existe $src — omitido" >&2
    return
  fi
  # Quita cualquier symlink/carpeta previa con ese nombre.
  if [ -L "$dst" ] || [ -e "$dst" ]; then
    rm -rf "$dst"
  fi
  ln -s "$src" "$dst"
  echo "  ✓ /$name → $dst"
}

echo "Instalando skills de 18.-diario en $SKILLS_DST"
link_skill handoff
link_skill handon

echo "Listo. Reinicia/recarga Claude Code y prueba: /handoff  o  /handon"
