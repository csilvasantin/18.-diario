# Diario

## 1 2 3 basico

1. registrar lo importante por fecha;
2. mantener el historial separado por dias;
3. cerrar siempre con HTML y una URL publica para comprobar el resultado.

## Objetivo

Es un deposito de informacion de todo lo que vamos haciendo con Inteligencia Artificial.

## Reglas practicas

1. una entrada por fecha;
2. no mezclar varios dias en un mismo archivo;
3. publicar el cierre relevante en HTML;
4. entregar una URL publica comprobable;
5. si se usa `Nomeacuerd0`, entenderlo solo como barrera ligera.
6. en el contenido del diario, priorizar estructura numerada `1. 2. 3.` en vez de listas de puntos;
7. si hace falta un segundo nivel, usar solo `a. b. c.` dentro de cada bloque numerado;
8. evitar listas largas con guiones o bullets sueltos.

## Nota para Claude

- La UI viva del diario esta en `index.html`.
- El selector de fechas ya no es una hilera de enlaces: ahora es un `select` con id `entry-selector`.
- Debe abrir por defecto en la ultima entrada disponible del array `entries`; esa logica vive en `renderDiary()` y `showEntry()`.
- El look actual sigue una direccion Matrix compartida con otros proyectos: fondo oscuro, verde fosforo, panel tipo terminal y lluvia de caracteres en `#matrix-canvas`.
- Si Claude toca la UI, debe mantener esa linea visual salvo que se pida cambiarla explicitamente.
- Para revisar cambios en local, servir esta carpeta y abrir `http://127.0.0.1:3030/`.
- Claude cierra cada sesion con el skill `/update-claude` que automatiza todo el flujo de escritura, regeneracion y push.

---

## Guia para Codex

Codex participa en este diario exactamente igual que Claude, pero identificandose como `"Codex"` en todos los registros.

### Archivos que importan

| Archivo | Que es |
|---|---|
| `index.html` | Diario web. Lee las entradas del array JS `const entries`. |
| `repos.html` | Tabla de proyectos con commits, fechas y ultimo LLM que actualizo cada repo. |
| `YYYY-MM-DD.md` | Entrada del diario del dia en Markdown (una por dia). |

---

### 1. Crear o actualizar el `.md` del dia

Nombre del archivo: `YYYY-MM-DD.md`. Si ya existe para ese dia, actualiza sin duplicar.

```markdown
# Diario - DD de mes de YYYY [Codex]

1. Que se hizo
   a. <item>

2. Que se valido
   a. <item>

3. Avances
   a. <item>

4. Problemas encontrados
   a. <item>

5. Decisiones tomadas
   a. <item>

6. Siguientes pasos
   a. <item>
```

Omite las secciones sin contenido real. Sin tildes en los textos para evitar problemas de encoding.

---

### 2. Actualizar `index.html`

Dentro del archivo hay un array JavaScript `const entries = [ ... ]`. Cada entrada:

```js
{
  date: "2026-04-15",
  title: "15 de abril de 2026",
  author: "Codex",
  sections: [
    { heading: "Que se hizo",      items: ["item 1", "item 2"] },
    { heading: "Que se valido",    items: ["item 1"] },
    { heading: "Avances",          items: ["item 1"] },
    { heading: "Siguientes pasos", items: ["item 1"] }
  ]
}
```

Reglas:
- **`author` debe ser siempre `"Codex"`** en las entradas escritas por Codex.
- Si ya existe una entrada para ese dia, reemplazala entera.
- Si no existe, anadela al final del array antes del `];` de cierre.
- Los `items` son strings. Se permite HTML inline: `<code>`, `<a href='' target='_blank'>`, `<strong>`.
- Headings sin tildes: `Que se hizo`, `Que se valido`, `Avances`, `Problemas encontrados`, `Decisiones tomadas`, `Siguientes pasos`.

---

### 3. Como aparece "Codex" en la columna LLM de `repos.html`

La tabla `repos.html` tiene una columna **LLM** que muestra que agente actualizo por ultima vez cada repo.  
El badge se asigna automaticamente leyendo el ultimo commit del repo: si el mensaje o el nombre del autor contiene `codex` (sin distinguir mayusculas), aparece el badge **Codex** en azul.

**Por eso es importante incluir la palabra "Codex" en el mensaje de commit:**

```
docs: Update Codex 2026-04-15 [skip ci]
feat: descripcion breve [Codex]
fix: descripcion breve [Codex]
```

El `[skip ci]` evita pipelines innecesarios en GitHub Actions.

---

### 4. Flujo completo al final de una sesion

```bash
# Clona o actualiza el repo
git clone https://github.com/csilvasantin/18.-diario.git /tmp/diario
# o si ya existe:
git -C /tmp/diario pull origin main

# Escribe YYYY-MM-DD.md
# Actualiza index.html (anadir/reemplazar entrada en el array entries)
# (Opcional) Regenera repos.html con el script Python del README-script si lo hay

# Commit y push
cd /tmp/diario
git add YYYY-MM-DD.md index.html repos.html
git commit -m "docs: Update Codex YYYY-MM-DD [skip ci]"
git push -u origin main
```

---

### URLs publicas

- Diario: https://csilvasantin.github.io/18.-diario/
- Tabla de repos: https://csilvasantin.github.io/18.-diario/repos.html

---

### Notas adicionales

- El diario no tiene proteccion por contrasena; el HTML es publico.
- El repo con el indicador `◉` parpadeante en la tabla es el que se actualizo mas recientemente.
- Los botones de filtro del diario (`Todos` / `Claude` / `Codex`) filtran entradas por el campo `author`.
- Claude tiene el skill `/update-claude` que hace todo esto automaticamente. Codex sigue este README de forma manual o implementa su propio equivalente.
