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

1. **Sello de persona (SIEMPRE, automático, lo primero).** Deja la máquina con el FONDO
   de la persona del agente que retoma (regla de flota `s:PRIORIDAD_IDENTIDAD_FONDO`:
   Claude·admira=Neo, Claude·gmail=Morfeo, Codex·admira=Trinity, Codex·gmail=Oráculo,
   Grok=Cypher). Es idempotente y portable — vale para cualquier Mac:
   ```bash
   # clona la cúpula si falta (cuenta Cloudflare csilvasantin@gmail.com)
   [ -d ~/Claude/admira-vault/.git ] || git clone https://github.com/csilvasantin/admira-vault ~/Claude/admira-vault
   bash ~/Claude/admira-vault/ensure-persona.sh
   ```
   `ensure-persona.sh` hace pull, regenera los fondos si hay Pillow, aplica YA el fondo de
   la persona activa y verifica el servicio dinámico `com.admira.persona-wallpaper`. Si el
   servicio NO está cargado, imprime el comando único para arrancarlo (la persistencia la
   lanza Carlos: el harness bloquea a los agentes). Pásale ese comando si aparece.

2. **Localiza el repo** del diario (clónalo si no existe en este Mac):
   ```bash
   bash "$HOME/Documents/New project/csilvasantin-repos/18.-diario/skills/lib/locate-repo.sh"
   ```
   Si este Mac no tiene nada clonado todavía:
   `gh repo clone csilvasantin/18.-diario` y entra en la carpeta.

3. **Identifica qué handoff retomar**:
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

4. **Lee el handoff completo** y resume a Carlos en 2-3 líneas: foco, repo activo,
   y el primer siguiente paso pendiente (sección 6).

5. **Reproduce la sección 7 "Cómo retomar"**: clona/abre el repo activo que indica el
   handoff, sitúate en la branch correcta y deja el entorno listo para seguir.

6. **Confirma con Carlos** antes de ejecutar acciones destructivas o pushes; a partir de
   ahí, continúa el trabajo desde donde lo dejó la sesión anterior.

7. **Encadenar**: cuando Carlos vaya a saltar otra vez de máquina, genera un nuevo
   handoff con el skill `handoff`. La cadena queda registrada en `handoff/`.
