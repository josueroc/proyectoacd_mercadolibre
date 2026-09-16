# Proyecto ACD — Mercado Libre Perú

Adquisición, limpieza y documentación de publicaciones de productos de Mercado Libre Perú mediante web
scraping. Primer avance del proyecto final del curso **DS3021 — Análisis Computacional de Datos** (UTEC, 2026).

Fuente: `listado.mercadolibre.com.pe` · Muestra: 5 080 observaciones crudas → **4 412 ofertas únicas y 14 variables**
en cinco búsquedas (celulares, laptops, televisores, refrigeradoras, audífonos), extraídas el 2026-09-13.

## Estructura

```
datos/crudos/mercadolibre_raw.csv      CSV crudo del scraper (Parte 2), sin limpiar
datos/limpios/mercadolibre_limpio.csv  dataset final: 4 412 ofertas, 14 columnas, UTF-8
datos/calidad/                         evidencia: calidad por columna, resumen por categoría,
                                       filas separadas, duplicados retirados, precios excluidos
notebooks/ACD_PARTE_2.ipynb            extracción (Parte 2)
notebooks/ACD_PARTE_3.ipynb            limpieza y control de calidad (Parte 3)
documentos/Dataset_preliminar.md       sección 4 del informe, generada por la Parte 3
documentos/Diccionario de datos.docx   diccionario de datos (Parte 4), también en PDF
documentos/notas_integracion.md        ajustes pendientes entre el informe y lo realmente entregado
indicaciones/                          enunciado y formatos oficiales del curso
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
```

**Limpieza (Parte 3) — reproduce el dataset entregado en unos segundos:**

```bash
jupyter notebook notebooks/ACD_PARTE_3.ipynb
```

Ejecutar todas las celdas. Lee `datos/crudos/mercadolibre_raw.csv` y regenera `datos/limpios/`,
`datos/calidad/` y `documentos/Dataset_preliminar.md`. Las celdas de verificación son `assert`: si algún
requisito del enunciado deja de cumplirse (mínimo de 1 000 registros, 6 atributos, IDs únicos, ≤ 10 % de
nulos por columna), el notebook falla en lugar de exportar en silencio. Sobre el CSV entregado el
resultado es idéntico byte a byte al versionado en el repositorio.

**Extracción (Parte 2) — solo si se quiere rehacer la captura:**

```bash
jupyter notebook notebooks/ACD_PARTE_2.ipynb
```

Requiere Chrome instalado y toma alrededor de una hora por las pausas entre peticiones; el sitio puede
pedir una verificación manual en la ventana del navegador. **Sobrescribe `datos/crudos/mercadolibre_raw.csv`**;
para recuperar el archivo entregado: `git checkout datos/crudos`. Los precios de mercado cambian a diario,
así que una nueva captura no reproduce las cifras del informe.

## Correspondencia con el informe (Informe_Parte_I_DS3021)

| Sección del informe | Responsable | Artefacto en el repositorio | Estado |
| --- | --- | --- | --- |
| 1 Identificación | Parte 5 | — (informe) | Pendiente |
| 2 Contexto · 3 Objetivos · 6 Fuentes de datos | Parte 1 | — (informe) | Completado |
| Script de scraping y dataset crudo | Parte 2 | `notebooks/ACD_PARTE_2.ipynb`, `datos/crudos/` | Completado |
| 4 Dataset preliminar | Parte 3 | `notebooks/ACD_PARTE_3.ipynb`, `datos/limpios/`, `datos/calidad/`, `documentos/Dataset_preliminar.md` | Completado |
| Diccionario de datos | Parte 4 | `documentos/Diccionario de datos.docx` / `.pdf` | Completado |
| 5 Alcance · 7 Estrategia · 8 Viabilidad · ensamblaje | Parte 5 | — (informe) | Pendiente |

## Diferencias entre el informe y lo ejecutado

Registradas para que el informe final no afirme algo que el código no hace; el detalle está en
`documentos/notas_integracion.md`.

1. **Selenium en lugar de `requests`.** El objetivo específico 2 anunciaba `requests` + BeautifulSoup. El
   sitio exige un navegador para servir las tarjetas de resultados, así que la navegación se hace con
   Selenium y el análisis del HTML con BeautifulSoup, según el plan de contingencia del Anexo A.5. Las URL
   recorridas conservan el patrón `_Desde_N` descrito en el informe.
2. **Cobertura efectiva del recorrido.** Se recorrieron cinco categorías —el mínimo del objetivo
   específico 2, frente a las cinco a ocho sugeridas en el Anexo A.1— con hasta 20 páginas cada una:
   95 páginas de las 100 posibles, porque algunas búsquedas agotaron los resultados antes. El informe no
   debe afirmar que se recorrieron 20 páginas completas en todas las categorías.
3. **Atributos realmente disponibles.** El objetivo específico 4 y el esquema del Anexo A.4 preveían
   calificación, opiniones, condición, marca y envío gratuito: no aparecen en las tarjetas de resultados y
   no están en el dataset. `precio_anterior_texto` (40,08 % de nulos) y `vendedor_texto` (64,07 %) se
   conservan en el CSV crudo, pero quedan fuera del dataset limpio por superar el límite de 10 % de nulos.
   El dataset final entrega 14 variables numéricas y categóricas, por encima del mínimo de seis del enunciado.

## Alcance ético

Solo se extraen páginas públicas de resultados; no se recolecta información personal, se declara un
User-Agent identificable, se mantiene una pausa entre peticiones y no se emplean técnicas de evasión de
bloqueos. El dataset es de uso exclusivamente académico.
