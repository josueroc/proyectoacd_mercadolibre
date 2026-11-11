# Implementation Plan: Preprocesamiento, análisis y pipeline de datos del home office (Parte II)

**Branch**: `feature/parte-2-preprocesamiento` | **Date**: 2026-11-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-preprocesamiento-analisis-home-office/spec.md`

## Summary

Convertir las dos capturas de la Parte I (home office, principal; categorías, segunda fuente) en un dataset
final de componentes de home office limpio, integrado y enriquecido con variables derivadas, y usarlo para
estimar el costo de equipar un home office por componente, gama y perfil, con insights para trabajadores y
áreas de RR. HH. El flujo se organiza como un pipeline de cinco notebooks numerados —la lógica y su
justificación viven en ellos— orquestados por `pipeline.py`, que además carga el resultado en un almacén
SQLite del que lee el análisis. Las decisiones técnicas están en [research.md](research.md); las dos más
relevantes son deduplicar e integrar por **oferta** (`wid`) en lugar de por código de catálogo, lo que
eleva las ofertas comunes entre capturas de 261 a 780, y diagnosticar cada faltante con chi-cuadrado: ninguno
resultó MCAR.

## Technical Context

**Language/Version**: Python 3.11

**Primary Dependencies**: pandas, numpy, matplotlib, seaborn, scipy, scikit-learn (material del curso);
`notebook`/`nbconvert` para ejecutar los notebooks desde el pipeline; `python-docx` y `python-pptx` para
los documentos de entrega.

**Storage**: CSV en UTF-8 (intercambio) y SQLite (`data/final/home_office.sqlite`, almacén consultable con
SQL vía `sqlite3` de la biblioteca estándar).

**Testing**: `assert` en cada notebook sobre requisitos e invariantes (constitución V); escenarios de
[quickstart.md](quickstart.md), incluida la comprobación de determinismo con `manifiesto.json`.

**Target Platform**: computadora personal con Windows, macOS o Linux. La exportación de `.docx` a PDF usa
Microsoft Word y solo es necesaria para regenerar los documentos, no para el pipeline.

**Project Type**: proyecto de análisis de datos: notebooks + script orquestador + generadores de documentos.

**Performance Goals**: pipeline completo en menos de 10 minutos (NFR-003); los datos suman menos de 9 000
filas.

**Constraints**: datos crudos de solo lectura; sin consultas al sitio web; técnicas del material de clase;
semillas fijas.

**Scale/Scope**: 3 680 + 5 080 registros crudos; 6 componentes; 5 notebooks nuevos; 1 almacén; 2 diccionarios
nuevos (inicial del home office y final), informe y presentación.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principio | Cómo lo cumple el plan | Antes | Después del diseño |
| --- | --- | --- | --- |
| I Reproducibilidad | `pipeline.py` ejecuta todo desde los crudos; rutas relativas a la raíz; `requirements.txt` completo; semilla 42; `manifiesto.json` | PASS | PASS |
| II Justificación metodológica | Cada notebook explica cada decisión junto a su celda con la evidencia calculada (chi-cuadrado, IQR, distancias) | PASS | PASS |
| III Fidelidad al curso | Técnicas de U3, U4 y U5. Fuera del material: SQLite, orquestación con `nbconvert` y generadores de documentos; justificados abajo | PASS con justificación | PASS con justificación |
| IV Trazabilidad | Crudos de solo lectura; `data/evidencia/` con motivo por registro; balance verificado por etapa | PASS | PASS |
| V Verificación automática | `assert` en cada notebook; el pipeline se detiene en la primera etapa que falla | PASS | PASS |
| VI Visualización interpretada | Cada figura del notebook 05 lleva interpretación escrita; texto ≥ 9 pt al tamaño de inserción | PASS | PASS |

## Project Structure

### Documentation (this feature)

```text
specs/001-preprocesamiento-analisis-home-office/
├── spec.md
├── plan.md                  # este archivo
├── research.md              # Fase 0
├── data-model.md            # Fase 1
├── quickstart.md            # Fase 1
├── contracts/
│   └── pipeline-cli.md      # Fase 1
├── checklists/
├── evaluations/
│   └── eval-report.md
└── tasks.md                 # /speckit-tasks
```

### Source Code (repository root)

```text
pipeline.py                                  # orquestador: etapas 01–06 (contracts/pipeline-cli.md)
requirements.txt                             # + seaborn, scipy, scikit-learn, python-docx, python-pptx
README.md                                    # reescrito para las Partes I y II

data/                                        # antes datos/
├── crudos/mercadolibre_raw.csv              # dataset inicial (categorías) — solo lectura
├── ec1_homeoffice/homeoffice_ml_crudo.csv   # dataset inicial (home office) — solo lectura
├── limpios/, calidad/, ec1_homeoffice/      # salidas de la Parte I, sin cambios
├── intermedio/                              # salidas de las etapas 01–03
├── evidencia/                               # registros excluidos o marcados, con su motivo
└── final/
    ├── homeoffice_final.csv                 # dataset final
    ├── precios_por_gama.csv
    ├── perfiles_home_office.csv
    ├── integracion_ofertas_comunes.csv
    ├── home_office.sqlite
    ├── metricas.json
    └── manifiesto.json

notebooks/
├── 01_ingesta_y_limpieza.ipynb
├── 02_faltantes_y_atipicos.ipynb
├── 03_integracion_y_reduccion.ipynb
├── 04_transformacion_e_ingenieria_de_caracteristicas.ipynb
├── 05_analisis_y_visualizacion.ipynb
├── comun.py                                 # rutas, estilo de figuras, evidencia y balance (sin lógica de datos)
└── ACD_Proyecto_Parte_I.ipynb, generar_figuras*.ipynb   # Parte I, solo rutas actualizadas

scripts/
├── generar_diccionarios.py                  # diccionario inicial (home office) y final, .docx + PDF
├── generar_informe.py                       # documento maestro sobre la plantilla oficial, .docx + PDF
└── generar_presentacion.py                  # presentación .pptx

docs/                                        # antes documentos/
├── diccionarios/                            # inicial (categorías, Parte I; home office) y final
├── parte_2/
│   ├── figuras/                             # PNG que genera el notebook 05
│   ├── Informe_Parte_II_DS3021.docx / .pdf
│   └── Presentacion_Parte_II_DS3021.pptx
└── informe_home_office.pdf, latex/, ppt/, …  # Parte I, sin cambios
```

**Structure Decision**: Repositorio de análisis de datos con la estructura que exige el enunciado (`data`,
`notebooks`, `docs`). La lógica de datos vive en notebooks numerados en el orden del pipeline, porque son el
entregable que se evalúa; `pipeline.py` solo los orquesta y hace la carga; `scripts/` agrupa los
generadores de documentos, que no forman parte del pipeline de datos.

### Asignación de requisitos a notebooks

| Notebook | Requisitos | Técnicas del curso |
| --- | --- | --- |
| 01 ingesta y limpieza | FR-001–FR-005, FR-032 | Limpieza niveles 1 y 2 (U3_L2): estructura, nombres, identificador único, tipos; deduplicación; regex sobre textos |
| 02 faltantes y atípicos | FR-006–FR-012 | Nivel 3 (U3_L3, U3_L4, U3_L5): `isna`, `crosstab`, `chi2_contingency`, estrategias 1–4; IQR, z-score, boxplot, scatter, K-Means, Mahalanobis |
| 03 integración y reducción | FR-013–FR-015 | U3_L6: `merge`, `combine_first`, los seis desafíos de integración, chi-cuadrado de redundancia |
| 04 transformación e ingeniería de características | FR-016–FR-019, FR-020 (por gama) | U3_L7: codificación binaria (`get_dummies`), discretización (`qcut`), construcción de atributos; U4_L1: logaritmo, escalamiento |
| 05 análisis y visualización | FR-020–FR-023, NFR-006 | U3_L8: `groupby`, `pivot_table`; seaborn y matplotlib |
| `pipeline.py` | FR-024–FR-026 | U5_T1–T3: ciclo de vida, pipeline, ETL |
| `scripts/` + README | FR-027–FR-031 | — |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --- | --- | --- |
| SQLite fuera del material (U5_T3 usó SQL Server + SSIS) | FR-025 exige un almacén consultable con SQL y NFR-001 que un tercero lo reproduzca | SQL Server y SSIS requieren instalar servidor y Visual Studio en Windows; no se reproducen con `requirements.txt` |
| Orquestación con `nbconvert` | FR-024 exige ejecutar todo con una instrucción sin duplicar la lógica de los notebooks | Ejecutar los notebooks a mano no cumple FR-024; Airflow o Prefect son desproporcionados para seis etapas locales |
| `python-docx`, `python-pptx` y exportación con Word | FR-030 y FR-031 exigen documentos sobre plantillas oficiales con cifras leídas de los notebooks | Copiar cifras a mano rompe la trazabilidad (principio IV) y la coincidencia entre informe y notebooks |
