# Proyecto ACD — Mercado Libre Perú

Adquisición, limpieza y documentación de publicaciones de productos de Mercado Libre Perú mediante web
scraping. Primer avance del proyecto final del curso **DS3021 — Análisis Computacional de Datos** (UTEC, 2026).

Fuente: `listado.mercadolibre.com.pe` · Muestra: 5 080 observaciones crudas → **4 412 ofertas únicas y 14 variables**
en cinco búsquedas (celulares, laptops, televisores, refrigeradoras, audífonos), extraídas el 2026-09-13.

## Estructura

```
notebooks/ACD_Proyecto_Parte_I.ipynb   notebook único: sección 1 Extracción, sección 2 Limpieza
datos/crudos/mercadolibre_raw.csv      CSV crudo del scraper, sin limpiar
datos/limpios/mercadolibre_limpio.csv  dataset final: 4 412 ofertas, 14 columnas, UTF-8
datos/calidad/                         evidencia: diagnóstico del crudo, calidad por columna, resumen por
                                       categoría, filas separadas, duplicados retirados, precios excluidos
datos/calidad/robots/                  robots.txt descargados el día de la verificación
documentos/Informe_Parte_I_DS3021_corregido.docx  informe completo con las 8 secciones (y su PDF)
documentos/Dataset_preliminar.md       sección 4 del informe, generada por el notebook
documentos/Diccionario de datos.docx   diccionario de datos, también en PDF
documentos/Informe_secciones_pendientes.md  borrador de las secciones 1, 5, 7 y 8 del informe
documentos/notas_integracion.md        ajustes pendientes entre el informe y lo realmente entregado
indicaciones/                          enunciado y formatos oficiales del curso
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
jupyter notebook notebooks/ACD_Proyecto_Parte_I.ipynb
```

*Ejecutar todas las celdas.* Con la configuración de fábrica (`EJECUTAR_SCRAPER = False`, celda 1.1) el
notebook **no vuelve a extraer**: verifica `robots.txt`, diagnostica el CSV crudo entregado y rehace toda la
limpieza en segundos, regenerando `datos/limpios/`, `datos/calidad/` y `documentos/Dataset_preliminar.md`
con un resultado idéntico byte a byte al versionado en el repositorio.

Las celdas de verificación son `assert`: si un requisito del enunciado deja de cumplirse (mínimo de 1 000
registros, 6 atributos, IDs únicos, ≤ 10 % de nulos por columna, rutas permitidas por `robots.txt`), el
notebook falla en lugar de exportar en silencio.

Para rehacer la captura desde cero, poner `EJECUTAR_SCRAPER = True`. Requiere Chrome instalado, toma
alrededor de media hora por las pausas entre peticiones, puede pedir una verificación manual en la ventana
del navegador y **sobrescribe `datos/crudos/mercadolibre_raw.csv`**; para recuperar el archivo entregado:
`git checkout datos/crudos`. Los precios cambian a diario, así que una nueva captura no reproduce las cifras
del informe.

## Cumplimiento del enunciado

| Requisito | Estado | Dónde se verifica |
| --- | --- | --- |
| Técnica de scraping (BeautifulSoup / Scrapy / Selenium) | Cumple | Selenium + BeautifulSoup, secciones 1.3 y 1.4 |
| ≥ 6 atributos, numéricos y categóricos | Cumple | 14 variables; `assert` en 2.5 |
| Manejo de paginación | Cumple | 1.4 `avanzar_siguiente`, 1.5; patrón `_Desde_N` |
| ≥ 1 000 registros | Cumple | 4 412 ofertas; `assert` en 1.7 y 2.5 |
| ≤ 10 % de nulos por columna | Cumple | máximo 1,25 %; `assert` en 2.5 |
| CSV en UTF-8 | Cumple | `datos/limpios/mercadolibre_limpio.csv` |
| Diccionario de datos en el formato Word | Cumple | `documentos/Diccionario de datos.docx` |
| `robots.txt` verificado | Cumple | 1.2: reglas interpretadas por ruta, evidencia en `datos/calidad/robots/` |
| `User-Agent` realista, `time.sleep()`, `try-except`, guardado incremental | Cumple | 1.1 y 1.5 |
| Notebook documentado y reproducible | Cumple | `notebooks/ACD_Proyecto_Parte_I.ipynb` |
| Informe en PDF con las ocho secciones | Cumple | `documentos/Informe_Parte_I_DS3021_corregido.docx` y su exportación en PDF |
| Evidencias de participación por integrante | **Pendiente** | las reúne el equipo (20 % de la rúbrica) |

## Correspondencia con el informe

| Sección del informe | Responsable | Artefacto en el repositorio | Estado |
| --- | --- | --- | --- |
| 1 Identificación | Parte 5 | `documentos/Informe_Parte_I_DS3021_corregido.docx` | Completado |
| 2 Contexto · 3 Objetivos · 6 Fuentes de datos | Parte 1 | — (informe) | Completado |
| Script de scraping y dataset crudo | Parte 2 | notebook § 1, `datos/crudos/` | Completado |
| 4 Dataset preliminar | Parte 3 | notebook § 2, `datos/limpios/`, `datos/calidad/`, `documentos/Dataset_preliminar.md` | Completado |
| Diccionario de datos | Parte 4 | `documentos/Diccionario de datos.docx` / `.pdf` | Completado |
| 5 Alcance · 7 Estrategia · 8 Viabilidad | Parte 5 | `documentos/Informe_Parte_I_DS3021_corregido.docx` | Completado |
| Ensamblaje del informe en Word y exportación a PDF | Parte 5 | `documentos/Informe_Parte_I_DS3021_corregido.docx` / `.pdf` | Completado |

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

Solo se extraen páginas públicas de resultados, verificadas contra `robots.txt` antes de cada ejecución; no
se recolecta información personal, se declara un User-Agent identificable, se mantiene una pausa entre
peticiones y no se emplean técnicas de evasión de bloqueos. El dataset es de uso exclusivamente académico.
