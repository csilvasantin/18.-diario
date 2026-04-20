# Rutinas compartidas — Triggers remotos de Claude Code

Este directorio contiene las definiciones portables de los **triggers remotos**
(`/v1/code/triggers`) que Carlos usa en su cuenta `csilva@admira.com`.

Los triggers de claude.ai están atados a la cuenta que los creó
(`account_uuid`, `environment_id`, MCP `connector_uuid`), por lo que **no se
pueden compartir directamente**. En su lugar, aquí se publican las **recetas**
para que cualquier cuenta de Claude Code pueda recrearlas idénticas en su
propio espacio.

## Cómo importarlas en tu cuenta

Abre Claude Code autenticado con tu cuenta (por ejemplo
`csilvasantin@gmail.com`) y pega este prompt:

```
Lee los archivos en diario/routines/*.md de este repo
(https://github.com/csilvasantin/diario) y créame los 3 triggers remotos
correspondientes en mi cuenta usando la herramienta RemoteTrigger con
action=create. Para cada archivo usa el campo cron, model, allowed_tools y
prompt tal cual están definidos. Si el archivo menciona un MCP requerido
(ej. Google Calendar) y yo no lo tengo conectado, avísame antes de crear
ese trigger.
```

## Qué ajustar después de importar

1. **MCP Google Calendar**: cada rutina declara `mcp_required: Google-Calendar`.
   Si lo quieres, conéctalo en claude.ai → Settings → Connectors antes de
   ejecutar el prompt de arriba.
2. **Repo destino en "Cerrar el Dia"**: la rutina original escribe en
   `carlossilvasantin/diario`. Si tu diario vive en otro repo, edita el campo
   `session_context.sources` al crearla o cámbialo después con
   `RemoteTrigger update`.
3. **Zona horaria**: los cron están en UTC tal como los almacena la API. Las
   horas "locales" que verás en la UI dependen de la tz de tu cuenta.

## Lista de rutinas

| Archivo | Hora local (Europe/Madrid) | Cron UTC | Modelo |
|---|---|---|---|
| [cerrar-el-dia.md](cerrar-el-dia.md) | 23:00 | `0 21 * * *` | opus-4-7 |
| [update.md](update.md) | 21:00 | `0 19 * * *` | sonnet-4-6 |
| [actualizarse.md](actualizarse.md) | 09:00 | `0 7 * * *` | sonnet-4-6 |
