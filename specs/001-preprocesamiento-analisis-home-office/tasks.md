---

description: "Task list for feature 001-preprocesamiento-analisis-home-office"
---

# Tasks: Preprocesamiento, análisis y pipeline de datos del home office (Parte II)

**Input**: Design documents from `/specs/001-preprocesamiento-analisis-home-office/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/pipeline-cli.md, quickstart.md

**Tests**: El spec no pide suites de pruebas aparte. La verificación es la que exige la constitución (V): `assert`
dentro de cada notebook sobre requisitos e invariantes, y los escenarios de `quickstart.md`.

**Organization**: Tareas agrupadas por historia de usuario. Dependencia declarada: US4 lee el almacén que crea
US5, por eso la fase de US5 va antes que la de US4.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Puede ejecutarse en paralelo (archivos distintos, sin dependencias pendientes)
- **[Story]**: Historia de usuario a la que pertenece (US1–US6)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Estructura exigida por el enunciado y dependencias

- [X] T001 Renombrar `datos/` → `data/` y `documentos/` → `docs/` con `git mv`, conservando subcarpetas, y crear `data/intermedio/`, `data/evidencia/`, `data/final/`, `docs/parte_2/figuras/` y `docs/diccionarios/`
- [X] T002 [P] Actualizar las rutas `datos`/`documentos` a `data`/`docs` en `notebooks/ACD_Proyecto_Parte_I.ipynb`, `notebooks/generar_figuras.ipynb` y `notebooks/generar_figuras_ppt.ipynb` (sin tocar `data/ec1_homeoffice/EC1_scraping_mercadolibre.ipynb`, registro archivado)
- [X] T003 [P] Mover el diccionario de la Parte I a `docs/diccionarios/diccionario_inicial_categorias.docx` y `.pdf`
- [X] T004 [P] Añadir a `requirements.txt` seaborn, scipy, scikit-learn, python-docx y python-pptx con versión mínima

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Utilidades compartidas por los cinco notebooks

- [X] T005 Crear `notebooks/comun.py` con: rutas relativas a la raíz (`RAIZ`, `CRUDOS`, `HO_CRUDO`, `INTERMEDIO`, `EVIDENCIA`, `FINAL`, `FIGURAS`), `SEMILLA = 42`, estilo de figuras con texto ≥ 9 pt (NFR-006), `guardar_evidencia(df, archivo, etapa, motivo)` que añade las columnas `id_oferta`, `etapa`, `motivo`, y `verificar_balance(entrada, salida, *excluidos)` con `assert` (FR-026, NFR-004)
- [X] T006 Verificar que en `notebooks/comun.py` ninguna ruta apunte a `data/crudos/` ni a `homeoffice_ml_crudo.csv` en modo escritura (constitución IV)

**Checkpoint**: estructura y utilidades listas; las historias pueden comenzar

---

## Phase 3: User Story 1 - Dataset final de home office limpio y justificado (Priority: P1) 🎯 MVP

**Goal**: Dataset de home office deduplicado por oferta, con faltantes diagnosticados y tratados, atípicos marcados y evidencia de cada exclusión.

**Independent Test**: Ejecutar `notebooks/01_ingesta_y_limpieza.ipynb` y `notebooks/02_faltantes_y_atipicos.ipynb`; deben producir `data/intermedio/02_homeoffice_tratado.csv` con el balance verificado y la evidencia en `data/evidencia/`.

### Notebook 01 — ingesta y limpieza

- [X] T007 [US1] Ingestión con validación de esquema de ambos crudos (17 y 13 columnas esperadas, nombres codificables, tipos de texto) en `notebooks/01_ingesta_y_limpieza.ipynb` (FR-001, FR-002)
- [X] T008 [US1] Normalizar espacios y convertir textos a tipos: precio y precio anterior en formato peruano, "NN% OFF", "N cuotas de S/ X", "4.8 | +100 vendidos" → `calificacion` y `vendidos_min`, y envío → `envio` ∈ {gratis mañana, gratis, mañana con costo, no informado}; registrar cada texto no interpretable en `data/evidencia/01_inconsistencias.csv` (FR-003)
- [X] T009 [US1] Calcular `id_oferta` con la regla R1 (`wid` → ruta directa sin `/p/` → código de catálogo marcado) y `id_catalogo` para ambas capturas en `notebooks/01_ingesta_y_limpieza.ipynb`
- [X] T010 [US1] Detectar inconsistencias entre campos: precio anterior ≤ precio, descuento anunciado frente al calculado, `numero_cuotas × monto_cuota` frente al precio; registrarlas sin borrar en `data/evidencia/01_inconsistencias.csv` (FR-004)
- [X] T011 [US1] Deduplicar por `id_oferta` conservando la observación más reciente y, en empate, la última fila; guardar los retirados en `data/evidencia/01_duplicados.csv` y comparar con la deduplicación por catálogo de la Parte I (FR-005, NFR-004)
- [X] T012 [US1] Detectar publicaciones ajenas al componente con la regla R4 (el título no nombra el componente o empieza con un sustantivo de accesorio), revisar las candidatas y guardarlas en `data/evidencia/01_ajenas_al_componente.csv` (FR-032)
- [X] T013 [US1] Exportar `data/intermedio/01_homeoffice_limpio.csv` y `data/intermedio/01_categorias_limpio.csv` (este último con `id_oferta` de la Parte I) y verificar con `assert`: "`id_oferta` único y sin nulos", "`precio > 0`" y balance entrada = salida + duplicados + ajenas

### Notebook 02 — faltantes y atípicos

- [X] T014 [US1] Cuantificar faltantes por columna y por componente (tabla y mapa de calor) en `notebooks/02_faltantes_y_atipicos.ipynb` (FR-006)
- [X] T015 [US1] Diagnosticar el tipo de cada faltante con `crosstab` y `chi2_contingency` contra componente y página, y con la mediana de precio con y sin faltante; concluir MCAR, MAR o MNAR por columna, con la justificación escrita junto a la celda (FR-007, SC-002)
- [X] T016 [US1] Aplicar la estrategia por tipo (R2): `tiene_descuento` y `descuento_pct = 0` estructurales; `ofrece_cuotas`; indicadores `tiene_resenas` y `vendedor_visible` sin imputar; `envio = no informado`; eliminar `etiqueta_texto`; mostrar como contraste el efecto de imputar la calificación con la mediana del componente (FR-008, FR-009)
- [X] T017 [US1] Detectar atípicos univariados sobre `log10(precio)` por componente con IQR (factor 1,5) y |z| > 3, con boxplot e histograma (FR-010)
- [X] T018 [US1] Detectar atípicos bivariados (precio frente a precio anterior; precio frente a `numero_cuotas × monto_cuota`) con diagramas de dispersión (FR-011)
- [X] T019 [US1] Detectar atípicos multivariados con K-Means por componente sobre variables estandarizadas (`random_state=42`, `n_init` explícito), marcando las distancias al centroide sobre el percentil 99 y los grupos de menos de 1 %; contrastar con Mahalanobis (FR-011)
- [X] T020 [US1] Decidir cada atípico con la regla de FR-012 (error comprobable → excluir; extremo plausible → conservar con `atipico_precio = True`); guardar `data/evidencia/02_atipicos.csv` y `data/evidencia/02_excluidos_por_error.csv` (SC-002, NFR-004)
- [X] T021 [US1] Exportar `data/intermedio/02_homeoffice_tratado.csv` y verificar con `assert`: "`tiene_descuento ⇔ precio_anterior` no nulo", "`ofrece_cuotas ⇔ numero_cuotas` no nulo", "`1 ≤ calificacion ≤ 5`", "`0 ≤ descuento_pct < 100`" y balance

**Checkpoint**: US1 completa — dataset tratado y justificado (MVP)

---

## Phase 4: User Story 2 - Integración de las dos extracciones (Priority: P2)

**Goal**: Ofertas de home office enriquecidas con su precio del 13/09 y los desafíos de integración documentados.

**Independent Test**: Ejecutar `notebooks/03_integracion_y_reduccion.ipynb`; debe reportar ofertas solo en home office, solo en categorías y en ambas, con sumas que cuadran, y producir `data/final/integracion_ofertas_comunes.csv`.

- [X] T022 [US2] Identificación de entidades: comparar el cruce por código de catálogo (Parte I) frente al cruce por `id_oferta` y documentar la diferencia (formato de índice no coincidente) en `notebooks/03_integracion_y_reduccion.ipynb` (FR-013)
- [X] T023 [US2] Integrar por `id_oferta` en la dirección "agregar atributos" con `merge`: `precio_13_09`, `en_ambas_capturas` y `variacion_precio_pct`; prioridad de home office ante conflictos; justificar el rechazo de "agregar objetos" (FR-013, FR-014)
- [X] T024 [US2] Documentar los seis desafíos de U3_T4 (entidades, datos sin sentido, formato de índice, desajuste de agregación, duplicados, redundancia) con la evidencia de cada uno
- [X] T025 [US2] Reducción: retirar columnas constantes, vacías o redundantes con evidencia (chi-cuadrado entre categóricas, correlación entre numéricas; por ejemplo `moneda` constante y `ofrece_cuotas` frente a `numero_cuotas`) (FR-015)
- [X] T026 [US2] Exportar `data/intermedio/03_homeoffice_integrado.csv` y `data/final/integracion_ofertas_comunes.csv`; verificar con `assert` las sumas de los tres grupos y que "`precio_13_09` solo existe si `en_ambas_capturas`"

**Checkpoint**: US1 y US2 funcionan de forma independiente

---

## Phase 5: User Story 3 - Variables derivadas y perfiles de home office (Priority: P2)

**Goal**: Dataset final con variables derivadas, gamas por componente y costos por gama y perfil.

**Independent Test**: Ejecutar `notebooks/04_transformacion_e_ingenieria_de_caracteristicas.ipynb`; cada variable derivada debe tener regla, cobertura y aporte documentados, y cada publicación exactamente una gama.

- [X] T027 [US3] Transformaciones con justificación: `log_precio = log10(precio)`, codificación binaria (`get_dummies`) de `componente` y `envio`, y escalamiento para comparar variables (FR-016) en `notebooks/04_transformacion_e_ingenieria_de_caracteristicas.ipynb`
- [X] T028 [US3] Construir `marca` (diccionario de marcas por componente; `otra` si no se reconoce) y `sobrecosto_cuotas_pct` (FR-017)
- [X] T029 [US3] Extraer especificaciones del título: `ram_gb` y `almacenamiento_gb` (laptop), `pulgadas` (monitor), `inalambrico` (teclado, mouse, audífonos), `ergonomica` (silla); nulo "no aplica" en los demás componentes (FR-017)
- [X] T030 [US3] Tabla de variables derivadas con regla, cobertura y aporte esperado al análisis; `assert` de al menos 10 variables derivadas (FR-019, SC-006)
- [X] T031 [US3] Discretizar el precio en terciles por componente con `qcut` → `gama` ∈ {económica, media, alta}; publicar los límites; contrastar con K-Means de una dimensión; validar con una variable distinta del precio (FR-018)
- [X] T032 [US3] Calcular `data/final/precios_por_gama.csv` (n, mínimo, Q1, mediana, Q3, máximo por componente y gama) y `data/final/perfiles_home_office.csv` (costo mediano = suma de medianas; rango = suma de Q1 y suma de Q3) con al menos 3 perfiles (FR-020, SC-007)
- [X] T033 [US3] Exportar `data/final/homeoffice_final.csv` con las columnas de `data-model.md` y verificar con `assert`: "cada publicación pertenece a exactamente una `gama`", máximo de nulos por columna solo en columnas declaradas "no aplica"/estructurales/MAR, y conservación ≥ 95 % de ofertas únicas válidas (SC-004, SC-005)

**Checkpoint**: dataset final listo

---

## Phase 6: User Story 5 - Pipeline de datos reproducible (Priority: P3)

**Goal**: `python pipeline.py` reproduce todo, carga el almacén y se detiene ante invariantes violados.

**Independent Test**: En una copia limpia, `python pipeline.py` termina con código 0 y una segunda ejecución no cambia ningún CSV (quickstart, escenarios 1–3).

- [X] T034 [US5] Implementar `pipeline.py` según `contracts/pipeline-cli.md` (NFR-001): etapas 01–06, `--desde` y `--hasta`, ejecución de notebooks con `nbconvert`, registro de inicio, duración y resultado, y detención con código ≠ 0 en la primera etapa fallida (FR-024, FR-026)
- [X] T035 [US5] Implementar la etapa 05 de carga en `pipeline.py`: `data/final/home_office.sqlite` con las tablas `publicaciones`, `precios_por_gama`, `perfiles`, `ofertas_comunes` y `excluidos`, y `data/final/manifiesto.json` con filas, columnas y SHA-256 de cada CSV final (FR-025)
- [X] T036 [US5] Ejecutar `python pipeline.py --hasta 05` dos veces y comprobar que los CSV y el manifiesto no cambian (NFR-002); ejecutar el escenario 3 del quickstart en una copia temporal

**Checkpoint**: pipeline reproducible

---

## Phase 7: User Story 4 - Análisis, visualización e insights (Priority: P3)

**Goal**: Hallazgos interpretados y accionables, con todas las cifras en `metricas.json`.

**Independent Test**: Ejecutar `notebooks/05_analisis_y_visualizacion.ipynb`; cada gráfico tiene título, ejes con unidades e interpretación, y cada insight su usuario, acción y cifra.

- [ ] T037 [US4] Leer el almacén con SQL en `notebooks/05_analisis_y_visualizacion.ipynb` y presentar costos por componente, gama y perfil con sus rangos (FR-020)
- [ ] T038 [US4] Analizar dispersión de precios por componente y gama, efecto real de las promociones (descuento calculado frente al anunciado), peso del financiamiento en cuotas, relación entre calificación, unidades vendidas y precio, y diferencias por marca y tipo de vendedor; cada variable derivada usada en al menos un análisis (FR-021, SC-006)
- [ ] T039 [US4] Analizar anomalías y segmentaciones: atípicos conservados, variación de precio entre capturas y relación entre especificaciones y gama
- [ ] T040 [US4] Guardar cada figura en `docs/parte_2/figuras/` con título, ejes con unidades, texto ≥ 9 pt y una interpretación escrita debajo en el notebook; inventario de figuras con su interpretación (FR-022, NFR-006, SC-009)
- [ ] T041 [US4] Redactar al menos 5 insights, cada uno con usuario destinatario, acción recomendada y cifra calculada (FR-023, SC-008)
- [ ] T042 [US4] Escribir `data/final/metricas.json` con toda cifra que citan el informe y la presentación, incluido el balance por etapa (SC-003)

**Checkpoint**: análisis completo; `python pipeline.py` ejecuta las seis etapas

---

## Phase 8: User Story 6 - Entregables y documentación (Priority: P4)

**Goal**: Repositorio, diccionarios, informe y presentación según el enunciado y las plantillas oficiales.

**Independent Test**: Revisar el repositorio contra el escenario 6 del quickstart.

- [ ] T043 [P] [US6] Implementar `scripts/generar_diccionarios.py`: diccionario inicial del home office (17 columnas crudas) y diccionario final (todas las columnas de `homeoffice_final.csv`) sobre `indicaciones/Formato Diccionario de datos Parte II.docx`, con notas de limitaciones, en `docs/diccionarios/` como `.docx` y PDF; `assert` de que el diccionario final cubre el 100 % de las columnas (FR-027, FR-028, SC-010)
- [ ] T044 [US6] Implementar `scripts/generar_informe.py`: documento maestro sobre `indicaciones/Formato Proyecto Final Parte II.docx`, once secciones en el orden de la plantilla, índice con páginas, figuras de `docs/parte_2/figuras/`, cifras de `data/final/metricas.json`, tabla de objetivos con estado, diagrama del pipeline y conclusiones por objetivo; salida `docs/parte_2/Informe_Parte_II_DS3021.docx` y `.pdf` (FR-030, FR-033)
- [ ] T045 [US6] Implementar `scripts/generar_presentacion.py`: 12–16 diapositivas 16:9 en `docs/parte_2/Presentacion_Parte_II_DS3021.pptx` con las mismas cifras y figuras (FR-031)
- [ ] T046 [US6] Reescribir `README.md`: problema, estructura, instalación, ejecución paso a paso, dataset inicial y final, entregables y su ubicación, equipo (FR-029)

---

## Phase 9: Polish & Cross-Cutting Concerns

- [ ] T047 Ejecutar todos los escenarios de `quickstart.md` desde una copia limpia, medir la duración del pipeline completo (< 10 min) y comprobar cifras idénticas a las versionadas; registrar el resultado (NFR-001, NFR-003, SC-001)
- [ ] T048 Verificar que cada cifra del informe y de la presentación coincide con `data/final/metricas.json`, y que cada técnica usada en los notebooks cita su sesión del curso (U3–U5) o su justificación de excepción (NFR-005)
- [ ] T049 Commits por etapa con Conventional Commits (NFR-007), push a `feature/parte-2-preprocesamiento` y Pull Request hacia `main`

---

## Dependencies & Execution Order

- **Setup (T001–T004)** → **Foundational (T005–T006)** → historias.
- **US1 (T007–T021)** es prerrequisito de todas las demás: produce el dataset tratado.
- **US2 (T022–T026)** depende de US1.
- **US3 (T027–T033)** depende de US2 (usa `03_homeoffice_integrado.csv`).
- **US5 (T034–T036)** depende de US3 (carga el dataset final).
- **US4 (T037–T042)** depende de US5 (lee el almacén).
- **US6 (T043–T046)** depende de US4 (figuras y métricas); T043 solo depende de US3.
- **Polish (T047–T049)** al final.

### Parallel Opportunities

- T002, T003 y T004 en paralelo después de T001.
- T043 (diccionarios) en paralelo con la fase de US5/US4, porque solo necesita el dataset final.

## Implementation Strategy

1. Setup + Foundational.
2. US1 (MVP): dataset tratado y justificado. **Validar** antes de seguir.
3. US2 → US3 → US5 → US4, validando cada checkpoint.
4. US6 con las salidas definitivas.
5. Polish, quickstart y Pull Request.
