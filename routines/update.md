---
name: Update
cron_utc: "0 19 * * *"
hora_local_madrid: "21:00"
model: claude-sonnet-4-6
allowed_tools: [Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch]
mcp_required: Google-Calendar
persist_session: false
---

## Propósito

Vuelco vespertino de cambios locales a la nube de GitHub y actualización de la
tabla de proyectos.

## Prompt

```
Subir todos los cambios realizados en este máquina en local a la nube de github
de csilvasantin y actualizar la tabla de proyectos.

Además, si existe el directorio ~/Claude/github-csilvasantin/Yarig.aiTheGame:
1. Hacer git pull origin main
2. Si server.js ha cambiado en el pull, reiniciar el servidor:
   pkill -f 'node.*server.js' 2>/dev/null || true
   nohup node server.js > /tmp/yarig.log 2>&1 &
   Verificar con: curl -s http://localhost:9124/yarig/status
```

## Contexto de sesión al crear el trigger

No se fija `sources` ni `outcomes` concretos: el trigger decide en cada run qué
repo tocar según lo que encuentre con cambios pendientes. No hace falta
configurar `session_context` más allá de `allowed_tools` y `model`.

## Referencia de la instancia original (Carlos)

- trigger_id: `trig_015MvTJykbJA2nCBFUqiF4sQ`
- creado: 2026-04-15
- no copiar los IDs, solo los valores semánticos de arriba.
