---
name: Actualizarse
cron_utc: "0 7 * * *"
hora_local_madrid: "09:00"
model: claude-sonnet-4-6
allowed_tools: [Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch]
mcp_required: Google-Calendar
persist_session: false
---

## Propósito

Puesta al día matinal: revisar los cambios que las otras IAs (Claude, Gemini,
Codex) han volcado en el GitHub de csilvasantin desde los distintos
ordenadores de AdmiraNext.

## Prompt

```
Esta rutina es ponerse al dia de los cambios que hayan realizado las diferentes
IAs (Claude, Gemini o Codex) en los diferentes ordenadores de ADmiraNext y se
han volcado en el github de csilvasantin
```

## Contexto de sesión al crear el trigger

No se fija `sources` ni `outcomes` concretos: el trigger lee el estado general
de los repos de la cuenta. No hace falta configurar `session_context` más allá
de `allowed_tools` y `model`.

## Referencia de la instancia original (Carlos)

- trigger_id: `trig_01HwVG9Z2T6BTADWRQaKitMv`
- creado: 2026-04-15
- no copiar los IDs, solo los valores semánticos de arriba.
