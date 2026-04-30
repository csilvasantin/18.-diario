# Rutina "Handoff"

Snapshot de continuidad: la IA captura el estado de trabajo del usuario en el Mac actual, le asigna un código corto y lo publica en el diario para que cualquier IA en cualquier otra máquina pueda retomar exactamente donde se dejó.

## Cuándo se invoca

Cuando el usuario pide cualquiera de estas variantes:
- "handoff", "haz handoff", "hazme un handoff"
- "snapshot de la sesión", "pásame el handoff"
- "subir handoff al diario", "rutina handoff"
- "voy a cambiar de máquina, prepárame el handoff"

Es **iniciado por el usuario**. Nunca se ejecuta automáticamente: las hooks van en `settings.json`, esto NO es un hook.

## Qué es un handoff

Un fichero Markdown autocontenido que describe:
1. **Foco actual** (1-2 frases) — qué se está haciendo y por qué.
2. **Estado del repo activo** (último commit, branch, archivos modificados sin commitear, commits sin pushear).
3. **Estado del resto de repos del ámbito del usuario** (los 16 según `repos.html` / memoria) — solo los que tengan cambios o actividad hoy.
4. **Servicios y procesos activos** (workers desplegados, launchd, dev servers conocidos).
5. **Decisiones tomadas en esta sesión** que no son obvias del git log.
6. **Pendientes y siguientes pasos**, ordenados por prioridad.
7. **Cómo continuar** — comandos exactos para clonar, abrir y reanudar en otra máquina.

**No incluir nunca**: API keys, tokens, secrets, contenido del `.env`, contraseñas. El diario es público (GitHub Pages).

## Formato del código

`HX-XXXX` donde `XXXX` son 4 caracteres del alfabeto sin confusiones:

```
ABCDEFGHJKMNPQRSTUVWXYZ23456789
```

(sin `0`, `O`, `1`, `I`, `L` — para que se pueda dictar por teléfono).

## Pasos

1. **Generar código** (4 chars del alfabeto base32 sin confusiones).
2. **Capturar timestamp** real con `date '+%Y-%m-%d %H:%M:%S %Z %z'`.
3. **Resumir foco actual** preguntando al usuario o, si está claro, inferiéndolo de los últimos mensajes de la sesión.
4. **Pre-check de repos**:
   - En el repo principal de la sesión (el que se ha tocado más): `git status --short --branch`, `git log -5 --oneline`, `git log @{u}..HEAD --oneline` (commits sin push).
   - En el resto de los 16 repos: solo si `git log --since='hoy 00:00' --oneline` devuelve algo, anota brevemente.
5. **Crear `/Users/csilvasantin/Claude/diario/handoff/YYYY-MM-DD-CODE.md`** con esta plantilla:

   ```markdown
   # Handoff CODE — TÍTULO CORTO
   
   - **Origen**: Mac mini (csilvasantin@MacMini.local)
   - **Cierre**: YYYY-MM-DD HH:MM:SS CEST +0200
   - **Foco**: una o dos frases
   
   ## 1. En qué estabas
   ...
   
   ## 2. Estado del repo activo
   ...
   
   ## 3. Otros repos con actividad hoy
   ...
   
   ## 4. Servicios y procesos
   ...
   
   ## 5. Decisiones de la sesión
   ...
   
   ## 6. Pendientes / siguiente paso
   ...
   
   ## 7. Cómo retomar en la otra máquina
   ```bash
   gh repo clone csilvasantin/diario && cd diario
   cat handoff/YYYY-MM-DD-CODE.md
   # luego clonar el repo activo y seguir desde ahí
   ```
   ```

6. **Actualizar `index.html`** — añadir un atajo en la cabecera "Último handoff: HX-XXXX → handoff/YYYY-MM-DD-CODE.md". Si ya existe el atajo, sustituir.
7. **Commit + push**:
   ```bash
   cd /Users/csilvasantin/Claude/diario
   git add handoff/YYYY-MM-DD-CODE.md index.html
   git commit -m "Handoff CODE — TÍTULO CORTO"
   git push origin main
   ```
8. **Verificar URL pública** (esperar a que GitHub Pages haya servido el `.md` antes de enviar a Telegram):
   ```bash
   until curl -sS -o /dev/null -w '%{http_code}\n' \
     https://csilvasantin.github.io/diario/handoff/YYYY-MM-DD-CODE.md \
     | grep -q '^200$'; do sleep 8; done
   ```
9. **Entregar el handoff por Telegram** con el script canónico — esto es el paso crítico para que el usuario pueda copy-pegar en cualquier máquina sin abrir nada:
   ```bash
   /Users/csilvasantin/Claude/diario/scripts/send-handoff-telegram.py \
     /Users/csilvasantin/Claude/diario/handoff/YYYY-MM-DD-CODE.md
   ```
   El script envía, por orden:
   - Un mensaje cabecera `📦 Handoff HX-XXXX · TÍTULO` con la URL pública.
   - El contenido completo del Markdown troceado en mensajes ≤3500 chars con el prefijo `[HX-XXXX · i/N]`. Cada chunk se rompe en límite de sección (`#`/`##`) cuando es posible. Long-press en cada uno para copiar.
   - El mismo `.md` como documento adjunto descargable (`sendDocument` del bridge tira de la URL pública).
10. **Reportar** al usuario el código + URL pública. NO captura.

## Cómo retomar (lado receptor)

Tres caminos posibles, todos válidos:

**A) Copy-paste desde Telegram** (camino canónico cuando estás de viaje):
- Abre el chat con @AdmiraXPBot y busca el mensaje `📦 Handoff HX-XXXX`.
- Long-press → Copiar sobre los chunks `[HX-XXXX · i/N]`.
- Pega el contenido en la nueva máquina (consola IA, nota, lo que sea).
- Alternativa: pulsa el adjunto `.md` para descargar el archivo entero.

**B) Vía URL pública**:
- Abre la URL del mensaje cabecera de Telegram, es la canónica:
  `https://csilvasantin.github.io/diario/handoff/YYYY-MM-DD-CODE.md`.
- Cualquier IA puede leer ese URL directamente.

**C) Vía git en la nueva máquina**:
```bash
gh repo clone csilvasantin/diario && cd diario
cat handoff/YYYY-MM-DD-CODE.md
```

En cualquiera de los tres caminos, la IA lee el handoff y reproduce los comandos de la sección 7. Para "encadenar" sesión: tras retomar, generar otro handoff cuando se quiera saltar de máquina otra vez. La cadena queda en `handoff/`.

## Lo que NO hace esta rutina

- No edita `2026-XX-XX.md` (las entradas diarias siguen su flujo de `CERRAR-EL-DIA.md`).
- No incluye secretos.
- No fuerza commits en otros repos del ámbito; solo los reporta.
- No envuelve en GitHub Actions ni en cron — es una rutina por petición.
- No se confunde con "Cerrar el día": el cierre del día es un acta diaria; el handoff es un punto de continuidad de sesión, puede haber varios al día.

## Archivado

Los handoffs viven en `handoff/`. Una vez que el usuario confirma que retomó en la otra máquina y ya no los necesita, se pueden mover a `handoff/_archived/` con commit ligero. Por defecto se conservan: ocupan poco y el histórico es útil.
