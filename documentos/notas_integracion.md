# Notas de integración

Documento de trabajo interno. Registra qué debe ajustarse en el informe (`Informe_Parte_I_DS3021`) para que
el texto coincida con lo que el repositorio realmente contiene. Cada punto indica la sección afectada.

## Ajustes en el informe

1. **Objetivo específico 2 y sección 7 (Estrategia).** Deben describir Selenium para la navegación y
   BeautifulSoup para el análisis del HTML, con avance mediante el botón `Siguiente` y hasta veinte páginas
   por categoría. No corresponde afirmar que la extracción se hizo íntegramente con `requests` ni que se
   recorrieron veinte páginas completas en cada categoría: se capturaron 95 páginas de las 100 posibles.
   El cambio está previsto en el propio Anexo A.5 como plan de contingencia y debe declararse allí.

2. **Objetivo específico 4.** Promete calificación, número de opiniones, condición y envío gratuito, que no
   aparecen en las tarjetas de resultados ni en el CSV crudo. Hay que ajustar el objetivo a las variables
   reales o coordinar una nueva extracción. La consigna exige seis atributos numéricos y categóricos en
   conjunto, no cuatro de cada tipo: el dataset entrega catorce.

3. **Sección 6.4 y Anexo A.4.** Son propuestas previas a la extracción. El diccionario final usa las 14
   columnas del CSV limpio. No presentar precio anterior, descuento, cuotas como columna propia, vendedor,
   marca ni condición como variables del archivo final. `precio_anterior_texto` (40,08 % de nulos) y
   `vendedor_texto` (64,07 %) permanecen solo en el CSV crudo.

4. **Identificadores.** `id_extraido` es el código que obtuvo el scraper y puede corresponder a un producto
   de catálogo; `id_publicacion` se recupera del parámetro `wid` o de una ruta directa sin `/p/` y es la
   clave de deduplicación. Las URL originales se conservan para auditar esa decisión. Ya está documentado en
   el diccionario de datos.

5. **Sección 6.5 (robots.txt).** La comprobación HTTP 200 del notebook no demuestra por sí sola que se
   revisaron las reglas aplicables. El responsable de la adquisición debe conservar la evidencia de la
   revisión que el informe declara.

6. **Sección 4.** Se copia de `documentos/Dataset_preliminar.md`, que genera el notebook de la Parte 3 con
   las cifras de la ejecución. Si se vuelve a ejecutar la limpieza, hay que volver a copiar el texto.

7. **Sección 1 (Identificación) y secciones 5, 7 y 8.** Quedan a cargo de la Parte 5: completar nombres,
   estados e índice, redactar Alcance, Estrategia y Viabilidad, y ensamblar el informe en el formato Word
   oficial de `indicaciones/`.

## Trazabilidad de la limpieza

`datos/calidad/filas_para_revision.csv` (56 filas sin campos esenciales), `duplicados_retirados.csv` (605
repeticiones) y `precios_excluidos.csv` (7 precios cuestionados) son evidencia de las decisiones de la
Parte 3. No deben volver a mezclarse con el dataset limpio. La suma cuadra: 5 080 = 56 + 605 + 7 + 4 412, y
el notebook lo verifica con un `assert`.
