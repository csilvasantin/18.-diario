---
name: Cerrar el Dia
cron_utc: "0 21 * * *"
hora_local_madrid: "23:00"
model: claude-opus-4-7
allowed_tools: [Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch]
mcp_required: Google-Calendar
persist_session: false
---

## Propósito

Cierre del día: sube a GitHub el trabajo realizado con Claude Code y actualiza
el diario público y la tabla de repos.

## Prompt

```
Con esto lo que haremos es subir a GitHub el trabajo que hayamos realizado con
Claude Code y actualizaremos el diario https://csilvasantin.github.io/18.-diario/
y los repos https://csilvasantin.github.io/18.-diario/repos.html si un dia en
concreto no se ha hecho nada se documenta y ya esta
```

## Contexto de sesión al crear el trigger

- `session_context.sources`: repo donde se empuja el diario.
  En la cuenta original es `https://github.com/csilvasantin/18.-diario` con
  `allow_unrestricted_git_push: true`. Cámbialo por el tuyo si tu diario vive
  en otro repo.
- `session_context.outcomes.git_repository`: mismo repo, branch `main`.

## Referencia de la instancia original (Carlos)

- trigger_id: `trig_019SiYmDTAiAhovnPS1NcVr7`
- creado: 2026-04-19
- no copiar los IDs, solo los valores semánticos de arriba.
