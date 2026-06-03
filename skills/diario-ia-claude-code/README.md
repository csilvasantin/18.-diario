# Diario IA — skill para Claude Code

Cierra tu dia con una orden. Di **"actualizar diario"** (o "cierra el dia", "haz mi diario") en Claude Code y la skill:

1. recopila lo que has hecho hoy con IA (conversacion + actividad git + lo que le pases),
2. redacta la entrada del dia en el formato del Diario,
3. clona tu repo del diario, escribe `YYYY-MM-DD.md` y actualiza `index.html`,
4. hace commit + push a `main`,
5. verifica el despliegue y te devuelve la **URL publica**.

Es la version Claude Code, totalmente automatica, equivalente a la skill `diario-ia` de Codex.

## Instalacion

1. Copia la carpeta `diario-ia/` a tus skills personales de Claude Code:
   - **macOS / Linux**: `~/.claude/skills/diario-ia/`
   - **Windows**: `C:\Users\<TU_USUARIO>\.claude\skills\diario-ia\`
2. Crea tu configuracion a partir del ejemplo:
   ```bash
   cp config.example.json config.json
   ```
3. Edita `config.json` con tu repo, dominio publico, autor e identidad git (ver campos abajo).
4. Asegurate de tener `gh` autenticado (`gh auth status`) y `git` con acceso de push a tu repo.

Listo. En tu proxima sesion, pide **"actualizar diario"**.

## Configuracion (`config.json`)

| Campo | Que es |
|---|---|
| `repo` | URL git del repositorio de tu diario |
| `branch` | rama de publicacion (normalmente `main`) |
| `publicUrl` | URL publica del diario (GitHub Pages / dominio propio) |
| `pagesApi` | `owner/repo` para `gh api` y estado de Pages |
| `author` | firma de la entrada (por defecto `Claude`) |
| `git.name` / `git.email` | identidad de commit (se aplica inline, no toca tu config global) |
| `locale` | idioma del titulo (`es`, `en`, ...) |
| `timezone` | zona horaria para fijar la fecha del dia |

## Formato del diario

Una entrada por fecha (`YYYY-MM-DD.md`) con seis secciones: *Que se hizo, Que se valido, Avances, Problemas encontrados, Decisiones tomadas, Siguientes pasos*. Textos sin tildes. La UI publica (`index.html`) lee las entradas de un array JS `const entries`. Ver `example-entry.md`.

## Requisitos

- Claude Code
- `git` y `gh` (GitHub CLI) autenticado
- `node` (opcional, para validar el array de `index.html`)

## Notas

- Solo registra hechos trazables; si algo no se puede verificar, lo dice.
- No publica secretos.
- La verificacion se hace via `gh api` (las entradas se renderizan por JS, asi que un fetch web no las "ve").
