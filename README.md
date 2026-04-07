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
