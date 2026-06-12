---
name: handoff
description: Genera un snapshot de continuidad de la sesión ("handoff"), lo publica en el repo csilvasantin/18.-diario y lo entrega por Telegram para retomar el trabajo en cualquier otra máquina. Úsalo cuando Carlos diga "handoff", "haz handoff", "hazme un handoff", "snapshot de la sesión", "pásame el handoff", "voy a cambiar de máquina" o equivalente.
---

# Handoff — snapshot de continuidad de sesión

Captura el estado de trabajo actual, le asigna un código corto `HX-XXXX`, lo publica
en el diario público y lo manda por Telegram troceado para copy-paste en otra Mac.

Este skill es **autocontenido y portable**: no depende de ninguna memoria. La rutina
canónica vive en `HANDOFF.md` del repo, pero las rutas correctas son las de abajo
(el repo es **`18.-diario`**, NO el viejo `diario`).

## Constantes canónicas

- Repo GitHub: `csilvasantin/18.-diario`
- URL pública base: `https://csilvasantin.github.io/18.-diario/`
- Clon local: usa `skills/lib/locate-repo.sh` para resolverlo (lo clona si falta).

## Pasos

1. **Localiza el repo** (clónalo si no existe en este Mac):
   ```bash
   REPO="$(bash "$(dirname "$0")/../lib/locate-repo.sh" 2>/dev/null || bash ~/Documents/New\ project/csilvasantin-repos/18.-diario/skills/lib/locate-repo.sh)"
   echo "$REPO"
   ```
   Si no resuelves `$0`, ejecuta directamente:
   `bash "$HOME/Documents/New project/csilvasantin-repos/18.-diario/skills/lib/locate-repo.sh"`.

2. **Genera el código** `HX-XXXX` — 4 chars del alfabeto sin confusiones
   `ABCDEFGHJKMNPQRSTUVWXYZ23456789` (sin 0/O/1/I/L, para dictarlo por teléfono).

3. **Captura timestamp real**: `date '+%Y-%m-%d %H:%M:%S %Z %z'`.

4. **Resume el foco actual** (1-2 frases): qué se estaba haciendo y por qué.
   Si no está claro, pregunta a Carlos; si sí, infiérelo de los últimos mensajes.

5. **Pre-check de repos**:
   - Repo principal de la sesión: `git status --short --branch`, `git log -5 --oneline`,
     `git log @{u}..HEAD --oneline` (commits sin push).
   - Otros repos del ámbito: solo si `git log --since='hoy 00:00' --oneline` devuelve algo.

6. **Escribe `$REPO/handoff/YYYY-MM-DD-HX-XXXX.md`** con esta plantilla:
   ```markdown
   # Handoff HX-XXXX — TÍTULO CORTO

   - **Origen**: <hostname de este Mac>
   - **Cierre**: YYYY-MM-DD HH:MM:SS CEST +0200
   - **Foco**: una o dos frases

   ## 1. En qué estabas
   ## 2. Estado del repo activo
   ## 3. Otros repos con actividad hoy
   ## 4. Servicios y procesos
   ## 5. Decisiones de la sesión
   ## 6. Pendientes / siguiente paso
   ## 7. Cómo retomar en la otra máquina
   ```bash
   gh repo clone csilvasantin/18.-diario && cd 18.-diario
   cat handoff/YYYY-MM-DD-HX-XXXX.md
   # o, si ya tienes los skills instalados, solo di: "handon HX-XXXX"
   ```
   ```
   **NUNCA incluyas** API keys, tokens, secrets, `.env` ni contraseñas: el diario es público.

7. **Actualiza `index.html`** — atajo en cabecera "Último handoff: HX-XXXX → handoff/...".
   Si ya existe, sustitúyelo.

8. **Commit + push**:
   ```bash
   cd "$REPO"
   git add handoff/YYYY-MM-DD-HX-XXXX.md index.html
   git commit -m "Handoff HX-XXXX — TÍTULO CORTO"
   git push origin main
   ```

9. **Verifica la URL pública** (espera a que GitHub Pages la sirva):
   ```bash
   until curl -sS -o /dev/null -w '%{http_code}\n' \
     "https://csilvasantin.github.io/18.-diario/handoff/YYYY-MM-DD-HX-XXXX.md" \
     | grep -q '^200$'; do sleep 8; done
   ```

10. **Entrega por Telegram** con el script canónico del repo:
    ```bash
    "$REPO/scripts/send-handoff-telegram.py" "$REPO/handoff/YYYY-MM-DD-HX-XXXX.md"
    ```
    Envía cabecera `📦 Handoff HX-XXXX` con URL, el contenido troceado en chunks
    `[HX-XXXX · i/N]` para copy-paste, y el `.md` como adjunto.

11. **Reporta** a Carlos el código + URL pública. NO captura de pantalla.

## Lo que NO hace

- No edita las actas diarias `YYYY-MM-DD.md` (eso es `cerrar el día`).
- No incluye secretos. No fuerza commits en otros repos; solo los reporta.
