# Rutina "Cerrar el día"

Rutina operativa que Claude y Codex ejecutan cuando el usuario pide "cerrar el día" (o equivalente: "cierre", "cierra el diario"). Fuente canónica online; cada IA la lee desde su AGENTS.md / CLAUDE.md local y la aplica tal cual.

## Ámbito

- Repositorio: `diario` (remoto `https://github.com/csilvasantin/diario.git`).
- Checkout local en Mac Mini: `/Users/csilvasantin/Claude/diario/` (repo limpio). Si trabajas desde otro checkout, asegúrate de que está en `main` y sincronizado con `origin/main` antes de empezar.
- URL pública de verificación: `https://csilvasantin.github.io/diario/`.

## Firma de la entrada

Cada IA firma su entrada con su nombre entre corchetes en el título:

- Claude → `# Diario - D de mes de YYYY [Claude]`
- Codex → `# Diario - D de mes de YYYY [Codex]`
- Yarig.ai → gestionado automáticamente por el servidor Yarig (no lo escribe Claude ni Codex)

Si varias IAs cierran el mismo día, conviven en el mismo fichero `YYYY-MM-DD.md` separadas por `---`. Regla 1-2-3 del diario: un fichero por fecha, sin duplicar.

## Pasos

1. **Pre-check en `/Users/csilvasantin/Claude/diario/`**:
   - `git status --short --branch`
   - `git log --since='YYYY-MM-DD 00:00' --until='YYYY-MM-DD 23:59:59' --date=iso --stat --oneline --all`
   - `git reflog --date=iso --since='YYYY-MM-DD 00:00'`
   - `date '+%Y-%m-%d %H:%M:%S %Z %z'`

2. **Crear o actualizar** `YYYY-MM-DD.md` con estas seis secciones numeradas (sub-items a./b./c.):
   1. Que se hizo
   2. Que se valido
   3. Avances
   4. Problemas encontrados
   5. Decisiones tomadas
   6. Siguientes pasos

   Registrar solo hechos verificados con `git` y con el trabajo real de la sesión. No rellenar.

3. **Actualizar `index.html`** del diario para que la nueva fecha aparezca en la UI pública (filtros Todos / Claude / Codex / Yarig.ai).

4. **Commit + push** desde `/Users/csilvasantin/Claude/diario/`:
   - `git add YYYY-MM-DD.md index.html`
   - `git commit -m "Diario YYYY-MM-DD [Claude|Codex]"`
   - `git push origin main`

   GitHub Actions (`update-repos.yml`) regenera `repos.html` automáticamente.

5. **Verificar URL**: comprobar que `https://csilvasantin.github.io/diario/` responde y muestra la entrada del día.

6. **Reportar** al usuario la URL pública (no captura). Cumple la preferencia de compartir URLs por Telegram/chat en vez de screenshots.

## Yarig.ai — setup del servidor (una sola vez)

El servidor Yarig (`10.-Yarig.aiTheGame/server.js`) escribe automáticamente al diario cada vez que un usuario añade o cierra tareas (con debounce de 5 min). No requiere acción manual en el cierre.

Para activarlo en el Mac Mini (solo la primera vez o tras actualizar server.js):

```bash
cd ~/Claude/github-csilvasantin/Yarig.aiTheGame   # o donde esté el clone
git pull origin main
# matar el proceso anterior y relanzar:
pkill -f "node server.js" 2>/dev/null; node server.js &
```

Usa el `gh` CLI ya autenticado en el Mac Mini — no necesita GITHUB_TOKEN.

## Lo que NO hace esta rutina

- No llama a `sync-to-drive.sh` (el backup a Google Drive se ejecuta de forma periódica vía launchd).
- No toca otros repos ni otros checkouts del diario (p.ej. `/Users/csilvasantin/Documents/Admirito/github-csilvasantin/diario/`).
- No envía Telegram, no hace version bumps ni backups fechados (esas rutinas existen para `xtanco` / `Admira`, no para el cierre del diario).
- No escribe la entrada Yarig.ai — eso lo hace el servidor automáticamente.
