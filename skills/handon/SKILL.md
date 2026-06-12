---
name: handon
description: Retoma el trabajo a partir de un handoff previo (lado receptor) en una máquina nueva o distinta. Lee el snapshot de continuidad del repo csilvasantin/18.-diario y reanuda exactamente donde se dejó. Úsalo cuando Carlos diga "handon", "retoma el handoff", "retomar HX-XXXX", "carga el handoff", "sigue desde el handoff" o pegue un código HX-XXXX para continuar.
---

# Handon — retomar desde un handoff (lado receptor)

Carga un snapshot de continuidad generado con el skill `handoff` y reanuda el trabajo
en esta máquina. Es el reverso de `handoff`.

Autocontenido y portable: clona el repo si falta, no depende de ninguna memoria.

## Constantes canónicas

- Repo GitHub: `csilvasantin/18.-diario`
- URL pública base: `https://csilvasantin.github.io/18.-diario/handoff/`

## Pasos

1. **Localiza el repo** (clónalo si no existe en este Mac):
   ```bash
   bash "$HOME/Documents/New project/csilvasantin-repos/18.-diario/skills/lib/locate-repo.sh"
   ```
   Si este Mac no tiene nada clonado todavía:
   `gh repo clone csilvasantin/18.-diario` y entra en la carpeta.

2. **Identifica qué handoff retomar**:
   - Si Carlos dio un código `HX-XXXX`, busca el archivo:
     ```bash
     ls "$REPO/handoff/"*HX-XXXX*.md
     ```
   - Si no dio código, usa el **más reciente**:
     ```bash
     git -C "$REPO" pull --quiet origin main
     ls -t "$REPO/handoff/"*.md | head -1
     ```
   - Alternativa sin git (de viaje): leer la URL pública directamente
     `https://csilvasantin.github.io/18.-diario/handoff/YYYY-MM-DD-HX-XXXX.md`,
     o copy-paste de los chunks `[HX-XXXX · i/N]` que Carlos pegue desde Telegram.

3. **Lee el handoff completo** y resume a Carlos en 2-3 líneas: foco, repo activo,
   y el primer siguiente paso pendiente (sección 6).

4. **Reproduce la sección 7 "Cómo retomar"**: clona/abre el repo activo que indica el
   handoff, sitúate en la branch correcta y deja el entorno listo para seguir.

5. **Confirma con Carlos** antes de ejecutar acciones destructivas o pushes; a partir de
   ahí, continúa el trabajo desde donde lo dejó la sesión anterior.

6. **Encadenar**: cuando Carlos vaya a saltar otra vez de máquina, genera un nuevo
   handoff con el skill `handoff`. La cadena queda registrada en `handoff/`.
