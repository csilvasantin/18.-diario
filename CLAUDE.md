# Proyecto 18 — Diario

> Depósito de información sobre trabajo con Inteligencia Artificial, organizado por fechas

## Contexto

Diario es un repositorio para registrar todo lo importante realizado con IA: experimentos, cambios, aprendizajes, resultados. Funciona como histórico de sesiones y decisiones clave tomadas en proyectos relacionados con IA.

## Arquitectura

- **Estructura**: Una entrada por fecha, sin mezclar días en archivos
- **Contenido**: Descripción de qué se hizo, cómo se hizo, qué resultó
- **Publicación**: Cierre relevante en HTML con URL pública verificable
- **Formato**: Markdown con histórico separado por días

## Notas para IAs

1. **Regla básica 1-2-3**: Registrar lo importante por fecha → mantener histórico separado → cerrar con HTML y URL
2. **Publicación**: Cada entrada debe tener una salida final en HTML comprobable (GitHub Pages o similar)
3. **Granularidad**: Una entrada por fecha; si hay múltiples sesiones en un día, consolidar en una sola entrada
4. **Barrera Nomeacuerd0**: Si aparece en una página pública, tratarla como filtro ligero, no como seguridad fuerte
5. **Continuidad**: La URL pública es el punto de entrega final para que otros verifiquen el trabajo realizado

## Rutinas canónicas

Las rutinas que cualquier IA del usuario debe seguir literalmente cuando él las pide:

- [`CERRAR-EL-DIA.md`](CERRAR-EL-DIA.md) — cierre del día. Genera/actualiza la entrada `YYYY-MM-DD.md`, ajusta `index.html`, commit + push, verifica URL.
- [`HANDOFF.md`](HANDOFF.md) — handoff de continuidad entre máquinas. Cuando el usuario pide "handoff", "snapshot de la sesión", "pásame el handoff" o equivalente, la IA genera un código `HX-XXXX`, escribe `handoff/YYYY-MM-DD-CODE.md` con el estado de trabajo (foco, repo activo, otros repos con actividad, servicios, decisiones, pendientes, comandos para retomar), commitea, pushea y avisa por Telegram con la URL. NO incluye secretos.
