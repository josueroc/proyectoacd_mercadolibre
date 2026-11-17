# Research — Fase 0

**Feature**: `001-preprocesamiento-analisis-home-office` · **Fecha**: 2026-11-10

Cada decisión se tomó con sondeos sobre los datos crudos (`homeoffice_ml_crudo.csv`, 3 680 × 17, y
`mercadolibre_raw.csv`, 5 080 × 13). Las cifras citadas se recalculan en los notebooks.

## R1. Identificador de publicación y deduplicación

- **Decision**: Usar como clave la **oferta** (`id_oferta`): el parámetro `wid` de la URL; si falta, el
  código de una ruta directa sin `/p/`; si tampoco existe, el código de catálogo con prefijo de respaldo
  marcado. Deduplicar por `id_oferta`, conservando la observación más reciente y, en empate, la última fila.
- **Rationale**: Es la regla que la Parte I aplicó al dataset de categorías. En home office, la Parte I
  deduplicó por código de catálogo (`/p/MPE…`): quedan 2 936 identificadores, pero solo 2 881 ofertas
  únicas recuperables (más 20 filas sin `wid`); algunas ofertas aparecen con dos códigos distintos. Además,
  integrar con la clave de catálogo encuentra 261 publicaciones comunes y con la clave de oferta, 780.
- **Alternatives considered**: Mantener el código de catálogo (rechazado: deja ofertas repetidas e impide
  integrar con categorías); clave compuesta título + precio (rechazado: frágil ante títulos repetidos).

## R2. Tipología de los valores faltantes

Prueba chi-cuadrado (U3_L3) de independencia entre "faltante" y dos variables observadas, y comparación de
la mediana de precio con y sin faltante:

| Columna cruda | % faltante | p vs. componente | p vs. página | Mediana precio con / sin faltante | Diagnóstico |
| --- | ---: | --- | --- | --- | --- |
| `precio_anterior_texto`, `descuento_texto` | 45,1 | 8,8e-18 | 6,4e-11 | S/ 278 / 349 | Estructural (MNAR): falta cuando no hay promoción |
| `resenas_texto` | 60,4 | 1,6e-108 | 6,3e-62 | S/ 437 / 193 | MAR: depende del componente y de la página |
| `vendedor_texto` | 56,7 | 2,9e-87 | 8,7e-03 | S/ 249 / 389 | MAR: depende del componente |
| `cuotas_texto` | 3,9 | 1,0e-62 | 0,08 | S/ 24 / 329 | Estructural (MNAR): productos baratos sin financiamiento |
| `envio_texto` | 6,4 | 4,5e-193 | 1,0e-26 | S/ 417 / 300 | MAR |
| `etiqueta_texto` | 100,0 | — | — | — | Columna vacía |

- **Decision** (estrategias del curso, U3_T2 y U3_L4):
  - *Promoción* — estimar e imputar por estructura: `tiene_descuento = False` y `descuento_pct = 0` cuando no
    hay precio anterior; `precio_anterior` se conserva nulo (no se inventa un precio).
  - *Cuotas* — estimar e imputar por estructura: `ofrece_cuotas = False`; `numero_cuotas` y `monto_cuota`
    quedan nulos con la justificación "no aplica".
  - *Reseñas y vendedor* — ignorar (no imputar): se crean los indicadores `tiene_resenas` y
    `vendedor_visible`; los análisis de calificación y unidades vendidas usan solo valores observados y
    declaran el sesgo hacia productos más baratos y de primeras páginas.
  - *Envío* — ignorar: categoría explícita `no informado`, no se asume "sin envío gratis".
  - *Etiqueta* — eliminar la columna (estrategia 3).
- **Rationale**: Ningún faltante es MCAR (todos los p < 0,01 contra el componente), así que eliminar filas
  sesgaría la muestra. Imputar con la media una calificación MAR también la sesgaría.
- **Alternatives considered**: Imputación por mediana del componente (U3_L4, `groupby` + `fillna`) para la
  calificación — rechazada como valor final, pero se muestra su efecto en el notebook como comparación.

## R3. Detección y tratamiento de atípicos

- **Decision**:
  - *Univariados* (U3_L5): IQR y z-score sobre `log10(precio)` por componente, más boxplot e histograma.
    Se usa el logaritmo porque los precios tienen cola derecha (en todos los componentes el promedio supera a
    la mediana).
  - *Bivariados*: diagrama de dispersión precio frente a precio anterior y precio frente a
    `numero_cuotas × monto_cuota`; se marcan los puntos que violan la relación esperada.
  - *Multivariados* (U3_L5): K-Means por componente sobre variables numéricas estandarizadas y de cobertura
    completa; se marcan las observaciones más alejadas de su centroide (percentil 99) y los grupos de menos
    de 1 % de las observaciones.
  - *Tratamiento* (U3_T3): los errores comprobables (precio incoherente con el producto o con su propio
    financiamiento) se excluyen con su motivo; los extremos plausibles se conservan y el análisis usa
    medianas, rangos intercuartílicos y escala logarítmica.
- **Rationale**: Los máximos de silla (S/ 45 499) o laptop (S/ 29 000, la misma oferta que la Parte I excluyó
  en categorías) son errores; una laptop de S/ 15 999 es un producto real de gama alta. El IQR sobre el precio
  bruto marcaría como atípicos a casi todos los productos de gama alta.
- **Alternatives considered**: Distancia de Mahalanobis (también en U3_L5) — se reporta como contraste;
  eliminar todo lo que esté fuera del IQR — rechazado porque borra la gama alta.

## R4. Publicaciones ajenas al componente

- **Decision**: Una publicación es ajena cuando su título **no nombra el componente** (lista de sustantivos y
  sinónimos por componente: laptop, notebook, macbook, portátil; monitor, pantalla; mouse, ratón; silla;
  teclado, keyboard; audífonos, auriculares, headset, earbuds) **o** cuando el título empieza con un sustantivo
  de accesorio (funda, soporte, pad, almohadillas, repuesto…). Las candidatas se revisan y se guardan como
  evidencia con el motivo.
- **Rationale**: Las palabras clave sueltas producen falsos positivos: "switch" aparece en 81 teclados
  mecánicos y "cable" en audífonos con cable. La regla basada en el sustantivo del componente aísla casos
  como "Soporte de brazo para escritorio" en la búsqueda de mouse.
- **Alternatives considered**: Umbral de precio mínimo por componente (rechazado como criterio único:
  hay mouse legítimos de S/ 21); lista de palabras de accesorio sin contexto (rechazada por falsos positivos).

## R5. Gamas y perfiles de home office

- **Decision**: Discretización por igual frecuencia (U3_L7, `qcut`) del precio en terciles **por
  componente**: gama económica, media y alta. Perfil de home office = un componente de cada tipo en la misma
  gama; valor central = suma de medianas de la gama; rango = suma de los cuartiles 1 y 3 de la gama.
  Se valida la segmentación comprobando que las especificaciones suben con la gama (por ejemplo, la memoria
  mediana de las laptops).
- **Rationale**: Responde lo que la Parte I dejó pendiente (separar gamas) con una técnica del curso,
  interpretable para RR. HH. y el trabajador.
- **Alternatives considered**: K-Means de una dimensión sobre el log-precio (U3_L7, discretización por
  agrupamiento) — se reporta como contraste; reglas por especificación (rechazadas: cobertura desigual entre
  componentes).

## R6. Integración de las dos extracciones

- **Decision**: Integrar por `id_oferta` en la dirección **agregar atributos**: a cada publicación de home
  office se le añade el precio observado el 13/09 en categorías, la búsqueda de origen en esa captura y la
  variación de precio. Ante un conflicto, prevalece home office (captura más reciente y con más atributos).
  La dirección **agregar objetos** (sumar las laptops y audífonos que solo están en categorías) se evalúa y se
  rechaza: esas filas no tienen descuento, reseñas ni envío y pertenecen a otra fecha.
- **Rationale**: Cubre los seis desafíos de U3_T4: identificación de entidades y formato de índice (R1),
  datos sin sentido (R4), desajuste de agregación (capturas en fechas y páginas distintas), duplicados y
  redundancia (chi-cuadrado entre variables categóricas, U3_L6).
- **Alternatives considered**: `concat` de ambos datasets (rechazado por lo anterior).

## R7. Almacenamiento

- **Decision**: CSV en UTF-8 como formato de intercambio y **SQLite** como almacén consultable con SQL
  (`data/final/home_office.sqlite`), escrito con `sqlite3` de la biblioteca estándar.
- **Rationale**: Cumple la etapa *storage* del ciclo de vida de U5_T1 sin servidor ni instalación; el archivo
  se versiona y cualquiera lo abre. El análisis lee del almacén (etapa *serving*).
- **Alternatives considered**: SQL Server con SSIS, usado en U5_T3 (rechazado: requiere instalar SQL Server
  y Visual Studio en Windows; el evaluador no podría reproducirlo con `requirements.txt`); PostgreSQL
  (requiere servidor); Parquet (dependencia extra y no es consultable con SQL sin otro motor).

## R8. Orquestación del pipeline

- **Decision**: Un script `pipeline.py` en la raíz que ejecuta en orden los notebooks de transformación con
  `nbconvert` (incluido en `notebook`), luego la carga en SQLite y por último el notebook de análisis; se
  detiene en la primera etapa que falle e informa cuál.
- **Rationale**: Los notebooks son la única fuente de la lógica y de su documentación, como exige la rúbrica;
  el script solo los orquesta, sin duplicar código.
- **Alternatives considered**: Apache Airflow o Prefect, mencionados en U5_T1 (rechazados: infraestructura
  desproporcionada para cinco etapas locales); un módulo `src/` con la lógica (rechazado: vaciaría los
  notebooks que se evalúan).

## R9. Reproducibilidad y determinismo

- **Decision**: Semilla fija (`random_state=42`, `n_init` explícito en K-Means), orden explícito antes de
  cada escritura, formato de fecha fijo, y un `data/final/manifiesto.json` con filas, columnas y SHA-256 de
  cada CSV final para comprobar que dos ejecuciones coinciden.
- **Rationale**: Principio I y NFR-002.

## R10. Documento maestro, diccionarios y presentación

- **Decision**: Generar los `.docx` con `python-docx` sobre las plantillas oficiales de `indicaciones/`
  (se reemplazan los marcadores y se conserva carátula, índice y estilos) y exportarlos a PDF con Word. La
  presentación se genera con `python-pptx` en 16:9. Todas las cifras se leen de `data/final/metricas.json`,
  que escribe el notebook de análisis, y las figuras de `docs/parte_2/figuras/`.
- **Rationale**: FR-030 exige que cada cifra provenga de los notebooks; leerlas de un archivo generado evita
  copiarlas a mano. Los documentos son entregables, no datos: su generación queda fuera del pipeline.
- **Alternatives considered**: LaTeX (descartado por el usuario al entregar las plantillas oficiales en Word).

## R11. Reorganización del repositorio

- **Decision**: Renombrar `datos/` → `data/` y `documentos/` → `docs/` conservando sus subcarpetas, y
  actualizar las rutas de los notebooks de la Parte I. Los datos crudos de ambas capturas son el **dataset
  inicial**; la Parte II escribe en `data/intermedio/`, `data/evidencia/` y `data/final/`.
- **Rationale**: El enunciado exige literalmente `data`, `notebooks` y `docs`. Conservar las subcarpetas
  minimiza los cambios en el trabajo ya entregado.
