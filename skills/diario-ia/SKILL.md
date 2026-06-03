---
name: diario-ia
description: Escribir una entrada diaria, verificable y compartible sobre lo que una persona ha hecho con IA durante el dia, siguiendo el formato del Diario de Carlos Silva: fecha, autor, "Que se hizo", "Que se valido", "Avances", "Decisiones tomadas" y "Siguientes pasos". Usar al final de una jornada o cuando alguien pida cerrar/resumir el dia.
---

# Diario IA

Usa esta skill cuando una persona del equipo quiera cerrar el dia y dejar una entrada de diario sobre su trabajo con IA.

El objetivo no es hacer un parte de horas ni una celebracion generica. Es dejar una cronica breve, factual y trazable: que se hizo con IA, que evidencias lo prueban, que avance real queda, que decisiones se tomaron y que deberia pasar despues.

## Principios

- Escribe solo hechos observables o confirmados por la persona.
- No atribuyas actividad que no puedas verificar en la conversacion, comandos, commits, diffs, issues, documentos o notas aportadas.
- Manten el estilo sobrio del diario: frases directas, listas cortas, nombres concretos de ficheros, repos, comandos, modelos, herramientas y enlaces cuando existan.
- Si falta contexto, pide un resumen minimo antes de inventar. Pregunta por: tareas principales, herramientas IA usadas, repos/documentos tocados, validaciones y siguiente paso.
- Usa la zona horaria local de la persona si se conoce. Si no, usa la fecha del sistema y menciona la fecha exacta.
- El autor debe ser la IA o sistema que escribe la entrada si aplica (`Codex`, `Claude`, `ChatGPT`, `Yarig.ai`, etc.). Si escribes para una persona concreta, usa `Persona + IA`, por ejemplo `Marta + Codex`.

## Recogida de evidencias

Antes de redactar, recopila lo que puedas sin ser invasivo:

1. Lee la conversacion activa y extrae tareas cerradas, decisiones, bloqueos y validaciones.
2. Si estas en un repo, revisa estado y actividad del dia:
   - `git status --short --branch`
   - `git log --since='YYYY-MM-DD 00:00' --until='YYYY-MM-DD 23:59:59' --date=iso --stat --oneline --all`
   - `git diff --stat`
   - `git diff --name-only`
3. Si el usuario menciona documentos, tickets, PRs, tareas o chats, usa esas fuentes como evidencia primaria.
4. Si no puedes acceder a una fuente, dilo en la entrada o pregunta. No rellenes huecos con suposiciones.

## Formato de salida

Entrega una entrada Markdown lista para pegar en el diario.

Estructura obligatoria:

```markdown
# D de mes de YYYY

Autor: NombreAutor

## Que se hizo

- ...

## Que se valido

- ...

## Avances

- ...

## Decisiones tomadas

- ...

## Siguientes pasos

- ...
```

Reglas de estilo:

- Usa `Que`, no `Que` acentuado, para mantener compatibilidad con el formato actual del diario.
- Usa bullets con una accion por bullet.
- Envuelve comandos, rutas, nombres de ramas, commits y claves tecnicas con backticks.
- Incluye enlaces solo si son utiles para volver a la evidencia.
- Manten cada seccion entre 1 y 5 bullets salvo que el usuario pida mas detalle.
- Si una seccion no tiene evidencia suficiente, escribe un bullet honesto: `No se pudo validar ...` o `Queda pendiente ...`.

## Version para `index.html`

Si el usuario necesita actualizar una web como `https://www.carlossilva.info/18.-diario/`, ofrece tambien un bloque JS con el mismo contenido adaptado al array `entries`.

Forma esperada:

```js
{
  date: "YYYY-MM-DD",
  title: "D de mes de YYYY",
  author: "Codex",
  sections: [
    {
      heading: "Que se hizo",
      items: [
        "Se ..."
      ]
    },
    {
      heading: "Que se valido",
      items: [
        "<code>comando</code> devolvio ..."
      ]
    },
    {
      heading: "Avances",
      items: [
        "..."
      ]
    },
    {
      heading: "Decisiones tomadas",
      items: [
        "..."
      ]
    },
    {
      heading: "Siguientes pasos",
      items: [
        "..."
      ]
    }
  ]
}
```

En JS, convierte backticks Markdown a `<code>...</code>` y enlaces Markdown a `<a href='...' target='_blank'>...</a>`.

## Cierre del dia para equipos

Cuando alguien del equipo diga algo como "cierra mi dia", "haz mi diario", "resume lo que hice con IA" o "actualiza el diario":

1. Determina la fecha exacta.
2. Identifica la persona y la IA/herramientas usadas.
3. Recopila evidencias disponibles.
4. Redacta la entrada en el formato obligatorio.
5. Si estas dentro del repo del diario, crea o actualiza `YYYY-MM-DD.md` y, si existe, sincroniza `index.html` sin duplicar la fecha.
6. Antes de terminar, informa brevemente de que fuentes usaste y que no pudiste verificar.

## Plantilla rapida para pedir contexto

Si no hay suficiente informacion, pregunta de forma corta:

```text
Para cerrar el diario de hoy sin inventar, pasame 4 cosas:
1. Que hiciste con IA.
2. Que herramientas/modelos usaste.
3. Que archivos, repos, docs, PRs o entregables quedaron tocados.
4. Que validaste y que queda pendiente.
```

