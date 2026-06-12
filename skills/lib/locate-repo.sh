#!/usr/bin/env bash
# Localiza el clon local del repo 18.-diario y escribe su ruta absoluta en stdout.
# Si no está clonado en ninguna ubicación conocida, lo clona con `gh`.
# Uso:  REPO="$(bash skills/lib/locate-repo.sh)"
set -euo pipefail

CANDIDATES=(
  "$HOME/Documents/New project/csilvasantin-repos/18.-diario"
  "$HOME/Claude/18.-diario"
  "$HOME/18.-diario"
)

for d in "${CANDIDATES[@]}"; do
  if [ -f "$d/HANDOFF.md" ]; then
    echo "$d"
    exit 0
  fi
done

# No está clonado en este Mac: clonar en la ubicación canónica.
DEST_PARENT="$HOME/Documents/New project/csilvasantin-repos"
mkdir -p "$DEST_PARENT"
echo "Repo 18.-diario no encontrado; clonando en $DEST_PARENT ..." >&2
( cd "$DEST_PARENT" && gh repo clone csilvasantin/18.-diario >&2 )
echo "$DEST_PARENT/18.-diario"
