# ¿Cuánto cuesta equipar un home office en el Perú?

Proyecto final del curso **DS3021 Análisis Computacional de Datos** (UTEC, 2026). Estima el costo de equipar un
home office a partir de precios publicados en **Mercado Libre Perú**, obtenidos con web scraping (Parte I) y
preprocesados, integrados y analizados con un pipeline de datos reproducible (Parte II).

La Ley N.º 31572 (Teletrabajo) obliga al empleador a proveer los equipos o a compensar los propios según su valor
de mercado, pero en el Perú ese valor no se publica. Este proyecto lo construye con datos.

## Resultado principal

Un home office de seis componentes (laptop, monitor, silla de oficina, teclado, mouse y audífonos) cuesta, según
el nivel de equipamiento:

| Perfil | Costo mediano | Rango (suma de cuartiles 1 y 3) |
| --- | ---: | ---: |
| Económico | S/ 3 644 | S/ 2 812 – S/ 4 202 |
| Medio | S/ 6 332 | S/ 5 491 – S/ 7 373 |
| Alto | S/ 12 323 | S/ 10 464 – S/ 16 239 |

- La laptop concentra entre el 67 % y el 77 % del costo de cada perfil.
- Las ofertas con descuento no son más baratas que las demás de su componente (Mann-Whitney, p = 0,0008).
- El 98 % de las ofertas tiene cuotas sin interés: financiar no encarece.
- La etiqueta "gamer" encarece laptops y periféricos, pero no monitores ni sillas.

La Parte I había estimado una sola cifra, S/ 6 335,44 (suma de medianas). La Parte II muestra que esa cifra coincide
con el perfil medio, pero oculta una diferencia de 3,4 veces entre el perfil económico y el alto.

## Estructura

```
data/
  ec1_homeoffice/homeoffice_ml_crudo.csv   dataset inicial: captura de home office, 15/09/2026 (solo lectura)
  crudos/mercadolibre_raw.csv              dataset inicial: captura de categorías, 13/09/2026 (solo lectura)
  limpios/, calidad/, ec1_homeoffice/      salidas de la Parte I
  intermedio/                              salidas de las etapas 01–03 del pipeline
  evidencia/                               cada registro excluido o marcado, con su etapa y motivo
  final/
    homeoffice_final.csv                   DATASET FINAL: 2 714 ofertas × 41 variables (UTF-8)
    precios_por_gama.csv                   costo por componente y gama
    perfiles_home_office.csv               costo por perfil
    integracion_ofertas_comunes.csv        ofertas presentes en ambas capturas
    home_office.sqlite                     almacén consultable con SQL (5 tablas)
    metricas.json                          toda cifra citada en el informe y la presentación
    manifiesto.json                        filas, columnas y SHA-256 de cada CSV final
notebooks/
  01_ingesta_y_limpieza.ipynb
  02_faltantes_y_atipicos.ipynb
  03_integracion_y_reduccion.ipynb
  04_transformacion_e_ingenieria_de_caracteristicas.ipynb
  05_analisis_y_visualizacion.ipynb
  comun.py                                 rutas, estilo de figuras, evidencia y balance
  ACD_Proyecto_Parte_I.ipynb, generar_figuras*.ipynb   Parte I
pipeline.py                                orquestador del pipeline de la Parte II
scripts/                                   generadores de diccionarios, informe y presentación
docs/
  diccionarios/                            diccionarios inicial (categorías y home office) y final, .docx y PDF
  parte_2/informe/                         documento maestro de la Parte II, .docx y PDF
  parte_2/presentacion/                    presentación de la Parte II, .pptx y PDF
  parte_2/figuras/                         figuras generadas por los notebooks
  informe_home_office.pdf, latex/, ppt/    entregables de la Parte I
specs/001-preprocesamiento-analisis-home-office/   especificación, plan, tareas y evaluación (flujo SDD)
indicaciones/                              enunciados y plantillas oficiales del curso
```

## Cómo ejecutar

Requisitos: Python 3.11.

```bash
pip install -r requirements.txt
python pipeline.py
```

`pipeline.py` ejecuta en orden las seis etapas y guarda cada notebook con sus salidas:

| Etapa | Qué hace | Notebook o función |
| --- | --- | --- |
| 01 Ingestión | valida el esquema, tipa los textos, identifica cada oferta, deduplica y separa lo que no es el componente | `01_ingesta_y_limpieza` |
| 02 Transformación | diagnostica el tipo de cada faltante y trata los atípicos | `02_faltantes_y_atipicos` |
| 03 Transformación | integra con la captura del 13/09 y retira columnas redundantes | `03_integracion_y_reduccion` |
| 04 Transformación | transforma, construye 24 variables derivadas, define gamas y costos | `04_transformacion_e_ingenieria_de_caracteristicas` |
| 05 Almacenamiento | carga los CSV finales y la evidencia en SQLite y escribe el manifiesto | `pipeline.py` |
| 06 Serving | consulta el almacén, analiza, grafica y formula insights | `05_analisis_y_visualizacion` |

El flujo completo tarda menos de un minuto. Opciones: `python pipeline.py --desde 03` reanuda desde una etapa y
`--hasta 04` se detiene después de una. Si una etapa viola un invariante (identificador repetido, balance de
registros roto, nulos fuera de lo justificado), el pipeline se detiene, nombra el invariante y sale con código 1.

**Reproducibilidad.** Dos ejecuciones producen CSV idénticos: compare `data/final/manifiesto.json` o ejecute
`git status data/` después de correr el pipeline. Los datos crudos nunca se modifican.

**Documentos.** El informe, los diccionarios y la presentación se regeneran desde las salidas del pipeline:

```bash
python scripts/generar_diccionarios.py
python scripts/generar_informe.py
python scripts/generar_presentacion.py
```

La exportación a PDF y la numeración del índice del informe usan Microsoft Word y PowerPoint; sin ellos se generan
igual los `.docx` y `.pptx`.

**Parte I.** `notebooks/ACD_Proyecto_Parte_I.ipynb` extrae y limpia el dataset de categorías. Con
`EJECUTAR_SCRAPER = False` trabaja sobre el CSV crudo del repositorio en segundos; con `True` repite la captura
(requiere Google Chrome y sobrescribe `data/crudos/mercadolibre_raw.csv`).

## Entregables de la Parte II

| Entregable del enunciado | Ubicación |
| --- | --- |
| Documento maestro (PDF) | `docs/parte_2/informe/Informe_Parte_II_DS3021.pdf` (y su `.docx`) |
| Repositorio con `README.md` y `requirements.txt` | este repositorio |
| Carpeta `data` con dataset inicial y final | `data/ec1_homeoffice/homeoffice_ml_crudo.csv`, `data/crudos/mercadolibre_raw.csv` y `data/final/homeoffice_final.csv` |
| Carpeta `notebooks` con nombres descriptivos | `notebooks/01_…` a `05_…` |
| Carpeta `docs` con diccionario inicial y final | `docs/diccionarios/` |
| Data assets: dataset final (CSV) y diccionario final (PDF) | `data/final/homeoffice_final.csv`, `docs/diccionarios/diccionario_final.pdf` |
| Documento de presentación | `docs/parte_2/presentacion/Presentacion_Parte_II_DS3021.pptx` |

## Correspondencia con el contenido del informe

| Sección | Dónde se desarrolla |
| --- | --- |
| Contexto y objetivos actualizados | informe, secciones 2 y 3 |
| Propuesta de pipeline | `pipeline.py`; informe, sección 5 |
| Preprocesamiento: limpieza, integración, reducción y transformación | notebooks 01 a 04 |
| Feature engineering | notebook 04 |
| Análisis y visualización | notebook 05 |
| Insights y conclusiones | notebook 05; informe, secciones 9 y 10 |
| Dataset y diccionario final | `data/final/`, `docs/diccionarios/`; informe, sección 4 |
| Documentación y reproducibilidad | este README; informe, sección 11 |

## Desarrollo guiado por especificaciones

La Parte II se desarrolló con un flujo SDD (spec-driven development) descrito en `AGENTS.md`: especificación,
aclaraciones, evaluación, plan, checklist y tareas en `specs/001-preprocesamiento-analisis-home-office/`, aprobación
y luego implementación por etapas, con un commit en formato Conventional Commits por etapa. Los principios del
proyecto (reproducibilidad, justificación metodológica, fidelidad al material del curso, trazabilidad, verificación
automática y gráficos interpretados) están en `.specify/memory/constitution.md`.

## Equipo

| Integrante | Parte I |
| --- | --- |
| Yared Riveros Rodríguez | Fuente de datos, contexto y objetivos; extracción del home office |
| Franco Nicolás Roque Castillo | Script de web scraping del dataset de categorías |
| Mauricio Terán Taica | Limpieza y control de calidad |
| Josué Luna Rocha | Diccionario de datos |
| Alvaro Mauricio García Hurtado | Alcance, estrategia y viabilidad; figuras e informe en LaTeX |

La distribución de la Parte II está en la sección 1 del documento maestro.

## Alcance ético

Solo se extrajeron páginas públicas de resultados, verificadas contra `robots.txt`. No se recolectó información
personal, se declaró un `User-Agent` identificable, se mantuvo una pausa entre peticiones y no se usaron técnicas
de evasión de bloqueos. La Parte II no vuelve a consultar el sitio. Los datos son de uso académico.
