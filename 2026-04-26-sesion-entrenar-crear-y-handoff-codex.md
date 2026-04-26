# 2026-04-26 · Sesión completa Entrenar + Crear, handoff a Codex/MacMini

AdmiraNext Consejo — SCUMM Interface · `v26.25.04.9` → `v26.26.04.51`
Tag de cierre: `v26.26.04.50` (convención: `.50` siempre marca cierre cross-ordenador)

> Esta entrada cubre **una sesión larga** que reemplaza dos verbos (Sintetizar → Entrenar; Mirar → Crear), añade backend queue en Render, magic link desde Telegram y cierra release para continuar desde otro Mac (MacMini con Codex).

---

## 1. Verbo ENTRENAR sustituye a SINTETIZAR (v26.26.04.1 → .10)

### Concepto
Pegas URLs de vídeos o libros en la action-line; el Consejo los archiva en un **corpus por consejero × generación** en `localStorage`. Cada consejero tiene su propia memoria.

### Frontend (`public/council-scumm.html`)
- Botón verb `data-verb="sintetizar"` → `entrenar`. Sustituido en VERB_TO_PANEL, names map y dispatch de `selectVerb`.
- Storage: `localStorage['entrenar:<gen>:<persona>']` = JSON array de `{url, source, kind, ts, title?}`.
- `classifyEntrenarUrl(url)` clasifica en `video|book|other`:
  - **video**: youtu.be / youtube.com / vimeo / twitch / tiktok / instagram (reel|tv) / `.mp4|.mov|.webm|.m4v`
  - **book**: `amazon.[a-z.]+/(.+/)?(dp|gp/product)/`, goodreads, librotea, casadellibro, fnac, libreriacanaima, bookdepository, `.pdf|.epub|.mobi`
  - **other**: lo demás
- Panel "Corpus de entrenamiento" en el inventario lateral del SCUMM bar:
  - Filas clicables `.entrenar-corpus-row[data-persona]` con conteo dorado.
  - Click → `showEntrenarFor(persona)` activa las dos ventanas overlay del fondo del retrato.
  - **Selección SOLO por panel** (eliminado hover y mouseleave en `.council-image` para evitar parpadeo).
- Overlays de fondo:
  - `.window-overlay.racional` (izq) = vídeos · `.window-overlay.creativo` (der) = libros.
  - **Ventanas espejo**: `left:15%` y `right:15%`, `top:5.3%`, `width:19.5%`, `height:16%`.
  - `overflow-y:auto` con scrollbar cian translúcida (`scrollbar-color:rgba(120,220,255,0.55)`).
  - Listas en **orden inverso** (más nuevo arriba, `.slice().reverse()`).
  - Cada `<li>` lleva debajo `<div class="analizar-desc">` con la descripción:
    - `title` del item si existe (oEmbed YT/Vimeo o microlink), o
    - fallback "Fuente · dd/mm".

### Detección automática de destinatario
- `_fetchUrlTitle(url)` saca metadatos:
  - YouTube → `youtube.com/oembed` (devuelve `title + author_name`).
  - Vimeo → `vimeo.com/api/oembed.json`.
  - Resto → `api.microlink.io` (fallback CORS-friendly, `~50 req/IP/día`) → devuelve `title · author`.
- `_detectTargetConsejeros(haystack, gen)` busca `persona.toLowerCase()` en `(title + url)` normalizado (`-_+%20` → espacios). Devuelve los matches.
- Flujo en `executeEntrenar`:
  - 1+ match → archiva SOLO en ellos.
  - 0 matches → abre **picker manual** sobre el panel del corpus.

### Picker manual (cuando no hay auto-match)
- `_renderEntrenarPicker(entry)` reemplaza el contenido del panel del corpus:
  - Header dorado "🎯 ELIGE DESTINATARIO".
  - Botón "👥 Todos" (estilo SCUMM madera + borde dorado).
  - 8 filas pulsando con animación `entrenar-pickable` (background dorado oscilante).
- Click en una fila → `_completePendingPick(persona)` archiva sólo en él.
- Click en "Todos" → archiva en los 8.
- Estado `_pendingEntrenar` se limpia en `exitEntrenarMode()` y al cambiar generación.

---

## 2. Magic link Telegram (?train=&target=) — v26.26.04.11 / .51

### Frontend
- IIFE redirect en `<head>` preserva todos los params al añadir `_v=<now>` (antes los machacaba).
- En `DOMContentLoaded`:
  - Si `?train=<url>` → activa Entrenar y dispara `executeEntrenar(url)` automáticamente.
  - Si además `?target=<X>` → guarda `window._trainTarget=X` antes de `sendMessage()`.
  - Limpia params con `history.replaceState` para que un refresh no re-dispare.
- `_resolveTrainTarget(target, gen)` resuelve:
  - `all|todos|*|everyone` → 'all' (8 consejeros)
  - persona exacta o substring (ej. "Wozniak", "Steve Jobs", "Disney")
  - rol abreviado (CEO, CTO, CCO…)
  - `null` si ambiguo o desconocido (cae al picker con aviso)
- Cuando target resuelve → archiva directo, marca el acuse como "(Telegram)".

### Memorizer2Bot (`src/bot.py` en `~/Claude/repos/Memorizer` del MacMini)

```python
async def cmd_entrenar(update, context):
    # /entrenar <url> [destinatario]
    raw_url = context.args[0]
    target = " ".join(context.args[1:]).strip() if len(context.args) > 1 else "todos"
    encoded_url = urlquote(raw_url, safe="")
    encoded_target = urlquote(target, safe="")
    magic = f"{CONSEJO_BASE_URL}?train={encoded_url}&target={encoded_target}"
    # Reply con magic link clicable
```

- Sintaxis:
  - `/entrenar https://…` → todos (default)
  - `/entrenar https://… Wozniak` → solo Wozniak
  - `/entrenar https://… CTO` → CTO de la generación
  - `/entrenar https://… "Walt Disney"` → match exacto
  - `/entrenar https://… todos` → explícito
- El bot está en proceso `python3 -m src.bot` lanzado con `nohup` desde `~/Claude/repos/Memorizer`. Logs en `data/bot.log`. PID actual: 25377.

---

## 3. Verbo CREAR sustituye a MIRAR (v26.26.04.12 → .15)

### Concepto
Escribes un prompt en la action-line, una imagen generada se materializa en el centro de la mesa dentro de un marco que cambia según la generación.

### Frontend
- Botón `data-verb="mirar"` → `crear`. Panel inventario "CALIDAD / TAMAÑO" con 4 opciones (Estándar/HD × Cuadrada/Apaisada).
- Nuevo `<div class="table-viewer" id="table-viewer">` insertado en `.council-image`:
  - Posición: `left:32% top:65% width:36% height:26%` (sobre la mesa, parte inferior).
  - Modos: `.mode-mac` (leyendas, marco beige Apple II + scanlines verdes) · `.mode-hologram` (coetáneos, translúcido cian + scanlines + esquinas sci-fi + flicker `hologram-flicker`).
  - Botones `⛶` (`toggleTableViewerFullscreen` con Fullscreen API) y `✕` (`closeTableViewer`).
  - Reglas `:fullscreen` que ocultan marco/scanlines y ponen `object-fit:contain`.
- Placeholder mientras genera (`_renderCrearGenerating(prompt)`):
  - Spinner 🎨 (`crear-spin` animation).
  - Barra indeterminada `.crear-progress` con sweep en `currentColor`.
  - Mensaje de fase rotativo (`CONECTANDO → INTERPRETANDO PROMPT → TRAZANDO BOCETO → COLOREANDO → AFINANDO DETALLES → RENDERIZANDO`) cada 2.4s.
  - Texto del prompt con `-webkit-line-clamp:2` + ellipsis (no desborda el marco).
- `_renderCrearImage(imageUrl)` reemplaza el placeholder con `<img>` cuando hay resultado.

### Backend Render (`council-api.py`)
Cola in-memory con TTL 1h. Endpoints (todos requieren `X-Council-Token: admira2026`):

```
POST /api/council/crear              → encola {prompt,calidad,gen,ts} → {id,status:'pending'}
GET  /api/council/crear/<id>          → polling de estado
GET  /api/council/crear-pending       → agente lee la cola
POST /api/council/crear/<id>/result   → agente entrega {imageUrl}
POST /api/council/crear/<id>/error    → agente reporta {error}
```

`ALLOWED_ORIGINS` añade `localhost:3030` y `127.0.0.1:3030` para preview local.

### executeCrear flow
1. POST a `/api/council/crear` con prompt + calidad → recibe `{id}`.
2. `setInterval` cada 3s contra `GET /api/council/crear/<id>`. Timeout 80 intentos (~4 min).
3. Cuando `status:'done'` → `_renderCrearImage(imageUrl)`.
4. Cuando `status:'error'` → muestra error en action-line.

### Bug de token (v26.26.04.17)
El frontend tenía hardcoded `COUNCIL_API_TOKEN = "G3ADHakf…"` (token antiguo) que NO coincidía con `COUNCIL_API_TOKEN=admira2026` del `.env` y de la env var en Render. Cualquier request devolvía 403. Fix: cambio a `"admira2026"`. Verificado contra Render con curl directo.

---

## 4. Loop manual del agente (Claude in Chrome)

Demostración exitosa esta sesión:
1. Usuario escribió prompt en Crear → frontend guardó en `localStorage['crear:lastJob']` (handshake antiguo, antes del backend Render).
2. Yo (Claude) abrí ChatGPT en pestaña MCP, leí el prompt vía DOM del Consejo en otra pestaña.
3. Tipo prompt en ChatGPT → genera imagen (golden retriever escalando Montserrat, 1254x1254).
4. Click en imagen → "Guardar" → `~/Downloads/ChatGPT Image 26 abr 2026, 19_00_39.png` (2.9MB).
5. Bash: `sips -Z 1024 -s format jpeg` → 376KB → `curl -F file=@… https://catbox.moe/user/api.php` → URL pública `https://files.catbox.moe/dz01va.jpg`.
6. JS en pestaña Council escribe `localStorage['crear:lastJob']` con `status:'done'` + `imageUrl` → polling lo detecta → `_renderCrearImage` pinta sobre la mesa.

**Pendiente**: convertir esto en loop autónomo:
- Migrar el handshake de localStorage al backend (ya hecho — endpoint `/api/council/crear-pending`).
- Cuando se trabaje en MacMini con Codex, escribir un agente que polll `crear-pending` cada N segundos, automatice ChatGPT vía Claude in Chrome (o Playwright/Puppeteer), suba la imagen a un host (catbox.moe) y postee a `/api/council/crear/<id>/result`.

---

## 5. Convención release .50

Cuando se cierra versión para sincronizar con otro Mac:
- Saltamos directamente a `vYY.DD.MM.50` independientemente del .N actual.
- Hoy: `.18` → `.50` (saltando 19-49) → reanudo en `.51`.
- Tag git annotated `vYY.DD.MM.50`.

Memoria correspondiente: [`feedback_release_50_convention.md`](https://github.com/csilvasantin/32.-ConsejoAdmiraNextGame).

---

## 6. Estado al cerrar (handoff a MacMini/Codex)

### Repos públicos involucrados
- `csilvasantin/32.-ConsejoAdmiraNextGame` — frontend SCUMM + council-api.py backend (Render auto-deploy)
- `csilvasantin/17.-Memorizer` — Memorizer2Bot con `/entrenar`
- `csilvasantin/diario` — repo público hermano (este archivo se reposteará allí)

### Versiones
- Frontend: `v26.26.04.51` (pusheada a `main`, GH Pages live)
- Tag de cierre: `v26.26.04.50`
- Backend Render: `v4.0.0` con endpoints crear (auto-deployado)
- Memorizer2Bot: corriendo en MacMini desde `~/Claude/repos/Memorizer`, PID 25377

### Commits clave (`32.-ConsejoAdmiraNextGame` rama main, hoy)
```
f141929 v26.26.04.51 — /entrenar acepta destinatario opcional (?target=)
a1b93ec v26.26.04.50 — release de cierre cross-ordenador
9a4ae6e v26.26.04.18 — orden inverso + descripciones
dc65edb v26.26.04.17 — fix token admira2026
69f3723 v26.26.04.16 — placeholder Crear compacto
c3c2e4c v26.26.04.15 — cola backend Render + fullscreen viewer
db94ca5 v26.26.04.14 — handshake localStorage Crear (legacy)
f28d4ea v26.26.04.12 — verbo Crear sustituye Mirar
7e2af06 v26.26.04.11 — magic link Telegram ?train=
5f088ad v26.26.04.10 — picker manual Entrenar
a50a39c v26.26.04.9  — detección automática destinatario
0cadf63 v26.26.04.8  — ventanas espejo + selección solo panel
7b140f0 v26.26.04.7  — selección desde panel corpus
c272622 v26.26.04.6  — ventana videos centrada + scroll vertical
f173fa2 v26.26.04.5  — viewer compacto + scrollbar SCUMM
e9d8be1 v26.26.04.3  — gating por hover (luego sustituido por panel)
32da887 v26.26.04.4  — viewer Mac/holograma sobre la mesa
570dee2 v26.26.04.13 — barra de progreso + fases Crear
8c4d794 v26.26.04.1  — verbo Entrenar sustituye Sintetizar
```

### Archivos críticos
- `public/council-scumm.html` (~3700 líneas) — toda la UI SCUMM y la lógica
- `council-api.py` (~1410 líneas) — backend FastAPI Render
- `diario/2026-04-26-*.md` — esta entrada

### Para reanudar desde MacMini
```bash
cd ~/Claude/repos/  # o donde tengas el clone
git clone https://github.com/csilvasantin/32.-ConsejoAdmiraNextGame.git || (cd 32.-ConsejoAdmiraNextGame && git pull)
cd 32.-ConsejoAdmiraNextGame
git checkout v26.26.04.50  # punto estable de cierre
# o git checkout main para tener la última (.51)
```

### Tareas pendientes inmediatas
1. **Loop autónomo del agente Crear**: leer `crear-pending` del backend, automatizar ChatGPT, subir imagen, postear `/result`. Candidatos para implementación:
   - Script Python en MacMini con `playwright` + cookies de chatgpt.com (sesión Plus) + curl al backend.
   - O Claude in Chrome MCP en una sesión Codex/Claude permanente.
2. **Cleanup mac-mini stash**: `cd ~/Claude/repos/Memorizer && git stash list` muestra `macmini-pre-pull` con cambios locales viejos (yarig.py, classifier.py, etc.). Revisar si se descartan o se commitean.
3. **Memorizer-tray vs nohup**: actualmente el bot lo arranqué con `nohup`; valorar si volver al tray app de barra de menú (`memorizer_tray.py`).
4. **Token Tailscale Funnel del Council API**: el frontend prueba primero Render, luego Tailscale Funnel. Verificar que el del MacMini siga online cuando vuelva a estar disponible.

---

_Sesión cerrada por Claude Code (Opus 4.7 1M) en MacBook Pro Negro 14, retomada en MacMini con Codex._
