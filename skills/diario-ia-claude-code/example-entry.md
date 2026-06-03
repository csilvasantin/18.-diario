# Diario - 3 de junio de 2026 [Claude]

1. Que se hizo
   a. Actualizado PowerShell 7 de `7.6.1` a `7.6.2` con `winget`.
   b. Arreglado Codex en Windows: lanzador robusto `codex.cmd`, accesos directos y `codex` en el PATH.
   c. Reinstalado el paquete MSIX `OpenAI.Codex` que estaba corrupto, conservando los datos en `.codex`.

2. Que se valido
   a. Un `pwsh` nuevo reporta `7.6.2` y `codex.cmd --version` devuelve `codex-cli 0.133.0-alpha.1`.
   b. La app arranca por su identificador `OpenAI.Codex_2p2nqsd0c76g0!App`.

3. Avances
   a. Codex operativo de tres formas: icono de la barra, accesos directos y comando en terminal.

4. Problemas encontrados
   a. El paquete MSIX se quedo sin su ejecutable principal tras una autoactualizacion incompleta.

5. Decisiones tomadas
   a. Reinstalar en vez de re-registrar, porque faltaban ficheros fisicamente.

6. Siguientes pasos
   a. Si el icono vuelve a fallar, quitar el paquete `OpenAI.Codex` y reinstalar desde la Tienda.
```

---

## Equivalente para `index.html`

```js
{
  date: "2026-06-03",
  title: "3 de junio de 2026",
  author: "Claude",
  sections: [
    { heading: "Que se hizo", items: [
      "Actualizado PowerShell 7 de <code>7.6.1</code> a <code>7.6.2</code> con <code>winget</code>.",
      "Arreglado Codex en Windows: lanzador <code>codex.cmd</code>, accesos directos y <code>codex</code> en el PATH."
    ]},
    { heading: "Que se valido", items: [
      "Un <code>pwsh</code> nuevo reporta <code>7.6.2</code>; la app arranca por <code>OpenAI.Codex_2p2nqsd0c76g0!App</code>."
    ]},
    { heading: "Siguientes pasos", items: [
      "Si el icono vuelve a fallar, quitar el paquete <code>OpenAI.Codex</code> y reinstalar desde la Tienda."
    ]}
  ]
}
```
