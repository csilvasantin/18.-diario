---
name: diario-ia
description: Cierra el dia y publica automaticamente una entrada de diario sobre lo que se ha hecho con IA. Clona el repo del diario, redacta la entrada del dia (formato Diario de Carlos Silva con secciones Que se hizo / Que se valido / Avances / Problemas encontrados / Decisiones tomadas / Siguientes pasos), actualiza index.html, hace commit y push a main y verifica la URL publica. Usar cuando el usuario diga "actualizar diario", "cerrar el dia", "cierra el diario", "haz mi diario", "resume lo que hice hoy con IA" o equivalente.
---

# Diario IA — cierre automatico del dia

Skill para **Claude Code**. Cuando el usuario pide cerrar el dia, registra de forma **automatica y verificable** todo lo que se ha hecho con IA durante la jornada y lo **publica** en su repositorio de diario.

No es un parte de horas ni un texto generico: es una cronica breve, factual y trazable. Registra solo hechos observables (conversacion, comandos ejecutados, commits, diffs, ficheros tocados). Si falta evidencia, dilo; no inventes.

---

## 1. Configuracion

La skill se parametriza con `config.json` que vive **junto a este SKILL.md** (misma carpeta). Lee ese fichero al empezar.

Campos:

```json
{
  "repo": "https://github.com/USUARIO/REPO-DIARIO.git",
  "branch": "main",
  "publicUrl": "https://tu-dominio/diario/",
  "pagesApi": "USUARIO/REPO-DIARIO",
  "author": "Claude",
  "git": { "name": "Tu Nombre", "email": "tu@correo" },
  "locale": "es",
  "timezone": "Europe/Madrid"
}
```

- `repo`: URL git del repositorio del diario (donde viven los `YYYY-MM-DD.md` y el `index.html`).
- `pagesApi`: `owner/repo` para consultas a `gh api` y al estado de GitHub Pages.
- `author`: firma de la entrada. Por defecto `Claude` (esta skill corre en Claude Code). Si escribes para una persona usa `Persona + Claude`.
- `git.name` / `git.email`: identidad con la que se commitea (se pasa **inline** con `-c`, no se toca la config global).

Si `config.json` no existe o le faltan campos, **pregunta al usuario** los datos minimos (repo, publicUrl, author) y ofrece crearlo. No continues sin saber a que repo publicar.

---

## 2. Determinar la fecha

Obten la fecha local del usuario:

```bash
date '+%Y-%m-%d %H:%M:%S %Z %z'
```

Usa la zona horaria de `config.timezone` si esta definida. El nombre del fichero sera `YYYY-MM-DD.md` y el titulo `D de mes de YYYY` (mes en el idioma de `config.locale`).

---

## 3. Recoger evidencias (lo que se hizo hoy)

Reune evidencia real antes de redactar, sin inventar:

1. **Conversacion activa**: extrae de este chat las tareas cerradas, decisiones, bloqueos y validaciones del dia.
2. **Actividad git** en el directorio actual y en otros repos que se hayan tocado hoy:
   ```bash
   git -C <repo> log --since='YYYY-MM-DD 00:00' --until='YYYY-MM-DD 23:59:59' --date=iso --stat --oneline --all
   git -C <repo> status --short --branch
   git -C <repo> diff --stat
   ```
3. **Otras fuentes** que mencione el usuario: PRs, issues, despliegues, documentos, comandos de sistema ejecutados, instalaciones, fixes. Inclúyelas si las puedes confirmar.
4. Si no puedes acceder a una fuente, **dilo en la entrada** (`No se pudo validar ...` / `Queda pendiente ...`). No rellenes huecos.

Si no hay contexto suficiente, pide un resumen corto:
> Para cerrar el diario sin inventar, pasame: 1) que hiciste con IA, 2) que herramientas/modelos usaste, 3) que repos/docs/entregables tocaste, 4) que validaste y que queda pendiente.

---

## 4. Obtener un checkout limpio del repo

Clona a una carpeta temporal (evita chocar con cualquier checkout del usuario):

```bash
WORK="${TMPDIR:-/tmp}/diario-ia-$(date +%Y%m%d)"
rm -rf "$WORK" 2>/dev/null
git clone -q <config.repo> "$WORK"
cd "$WORK"
git checkout <config.branch>
```

Si el usuario ya esta dentro de un checkout del diario y lo prefiere, usa ese (asegurate de que esta en la rama configurada y sincronizado con `origin`).

---

## 5. Escribir / actualizar `YYYY-MM-DD.md`

Una entrada por fecha (regla 1-2-3 del diario: **no mezclar dias, no duplicar**). Si el fichero del dia ya existe:
- mismo autor -> actualiza/fusiona sin duplicar;
- otro autor -> conviven en el mismo fichero separados por `---`.

Formato del fichero (firma con `config.author` entre corchetes; **textos SIN tildes** para evitar problemas de encoding):

```markdown
# Diario - D de mes de YYYY [Claude]

1. Que se hizo
   a. <accion concreta>

2. Que se valido
   a. <comprobacion / comando que devolvio X>

3. Avances
   a. <avance real que queda>

4. Problemas encontrados
   a. <bloqueo / error y como se sorteo>

5. Decisiones tomadas
   a. <decision y por que>

6. Siguientes pasos
   a. <que deberia pasar despues>
```

Reglas: una accion por sub-item; envuelve comandos, rutas, ramas, commits y nombres tecnicos en backticks; **omite secciones sin contenido real**; entre 1 y 5 sub-items por seccion salvo que se pida mas detalle.

---

## 6. Actualizar `index.html` (UI publica)

El `index.html` del diario lee las entradas de un array JS `const entries = [ ... ]`, ordenado con **lo mas reciente primero**. Anade o reemplaza la entrada del dia:

- Si ya existe una entrada con la misma `date` y mismo `author`, **reemplazala entera**.
- Si no existe, **insertala justo despues de `const entries = [`** (queda la primera).

Objeto de la entrada:

```js
{
  date: "YYYY-MM-DD",
  title: "D de mes de YYYY",
  author: "Claude",
  sections: [
    { heading: "Que se hizo",            items: ["..."] },
    { heading: "Que se valido",          items: ["..."] },
    { heading: "Avances",                items: ["..."] },
    { heading: "Problemas encontrados",  items: ["..."] },
    { heading: "Decisiones tomadas",     items: ["..."] },
    { heading: "Siguientes pasos",       items: ["..."] }
  ]
}
```

- `author` debe ser exactamente `config.author`.
- Convierte los backticks Markdown a `<code>...</code>` y los enlaces a `<a href='...' target='_blank'>...</a>`.
- Escapa correctamente para JS (comillas, `<`, backslashes en rutas Windows: `bin\\&lt;hash&gt;`).
- Headings sin tildes: `Que se hizo`, `Que se valido`, `Avances`, `Problemas encontrados`, `Decisiones tomadas`, `Siguientes pasos`.

**Valida el array antes de continuar** (que el JS siga parseando):

```bash
node -e "const fs=require('fs');const h=fs.readFileSync('index.html','utf8');const m=h.match(/const entries = \[[\s\S]*?\n\];/);let entries;eval(m[0].replace('const entries','entries'));console.log('OK',entries.length,'entradas; primera:',entries[0].date,entries[0].author);"
```

Si `node` no esta disponible, revisa el diff manualmente con cuidado.

---

## 7. Commit y push

Commitea con identidad **inline** (no toca la config global) e incluye el autor entre corchetes en el mensaje (el badge de LLM del diario lo detecta del mensaje):

```bash
git add YYYY-MM-DD.md index.html
git -c user.name="<config.git.name>" -c user.email="<config.git.email>" \
    commit -q -m "Diario YYYY-MM-DD [<config.author>]"
git push -q origin HEAD:<config.branch>
```

GitHub Actions del repo regenera `repos.html` solo. No hace falta tocarlo.

---

## 8. Verificar y reportar

Verifica por **API de GitHub** (no te fies de `curl` a webs: en muchos sandbox no hay egress y devuelve vacio -> falso negativo):

```bash
gh api repos/<config.pagesApi>/contents/YYYY-MM-DD.md --jq '.name'
gh api repos/<config.pagesApi>/commits/<branch> --jq '.sha[0:7]+" | "+.commit.message'
gh api repos/<config.pagesApi>/pages/builds/latest --jq '{status,commit}'
```

Espera a que el build de Pages quede en `built`. Las entradas se renderizan por JS, asi que `WebFetch` no las "lee"; confirma el dato via `gh api` sobre el fichero fuente.

Reporta al usuario:
1. La **URL publica** (`config.publicUrl`) — preferir enlace, no captura.
2. Un resumen de 1 linea de lo registrado.
3. Que fuentes usaste y que no pudiste verificar.

---

## Resumen del flujo

`config -> fecha -> evidencias -> clone -> YYYY-MM-DD.md -> index.html (+validar) -> commit+push -> verificar gh api/Pages -> reportar URL`

Honestidad ante todo: solo hechos trazables; si algo no se pudo confirmar, se dice.
