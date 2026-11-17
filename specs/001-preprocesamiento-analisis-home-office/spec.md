# Feature Specification: Preprocesamiento, análisis y pipeline de datos del home office (Parte II)

**Feature Branch**: `feature/parte-2-preprocesamiento`

**Created**: 2026-11-10

**Status**: Draft

**Input**: User description: "Parte II del proyecto final DS3021: preprocesamiento de datos y Data Analytics
Product sobre los datasets de Mercado Libre Perú obtenidos en la Parte I, partiendo de los CSV ya
descargados, sin volver a hacer scraping. Debe cubrir limpieza (inconsistencias, valores faltantes con su
tipología, outliers), integración de los dos datasets, reducción y transformación, feature engineering,
análisis y visualización con insights accionables sobre el costo de equipar un home office, y un pipeline
de ingestión, transformación y almacenamiento. Entregables del enunciado: repositorio con README.md,
requirements.txt y carpetas data, notebooks y docs; dataset final en CSV y diccionario final en PDF;
documento maestro y presentación. Técnicas basadas en el material de clase."

## Clarifications

### Session 2026-11-10

- Q: ¿Cuál debe ser el dataset principal de la Parte II? → A: El de home office (scraping del 15/09/2026,
  3 680 registros crudos) como dataset principal, con el de categorías (scraping del 13/09/2026, 5 080
  registros crudos) integrado como segunda fuente. Ambos provienen del web scraping de la Parte I.
- Q: ¿Qué entregables documentales produce esta feature, además del trabajo técnico? → A: El documento
  maestro en PDF y la presentación, ambos alimentados por las cifras y figuras de los notebooks.
- Q: ¿En qué formato debe quedar el documento maestro para que el equipo pueda editarlo? → A: Word (`.docx`)
  sobre la plantilla oficial `indicaciones/Formato Proyecto Final Parte II.docx`, exportado a PDF; la
  presentación en PowerPoint (`.pptx`). (La respuesta inicial fue LaTeX; el usuario la cambió al entregar las
  plantillas oficiales del curso.)
- Q: ¿Qué formato debe seguir el diccionario de datos final? → A: La plantilla oficial
  `indicaciones/Formato Diccionario de datos Parte II.docx` (columnas Variable, Descripción, Tipo, Tamaño
  máximo, Valores y Unidad), en `.docx` y exportado a PDF; las limitaciones van como notas bajo la tabla.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Dataset final de home office limpio y justificado (Priority: P1)

El equipo necesita un dataset final de publicaciones de componentes de home office en el que cada
inconsistencia, valor faltante y valor atípico se haya detectado, clasificado y tratado con una
justificación respaldada por evidencia, sin perder información útil ni introducir sesgos.

**Why this priority**: Es el núcleo evaluable del enunciado (preprocesamiento, 20 % de la rúbrica) y la base
de todo lo demás: sin un dataset final confiable, ni la ingeniería de características ni el análisis tienen
valor.

**Independent Test**: Ejecutar solo la etapa de preprocesamiento sobre los datos crudos y comprobar que
produce el dataset final, la evidencia de cada registro excluido y una justificación escrita para cada
tratamiento, con el balance de registros cuadrado.

**Acceptance Scenarios**:

1. **Given** los datos crudos de home office, **When** se ejecuta el preprocesamiento, **Then** cada columna
   con valores faltantes tiene un diagnóstico de su tipo (MCAR, MAR o MNAR) con evidencia y una estrategia de
   tratamiento coherente con ese tipo.
2. **Given** los precios de cada componente, **When** se ejecuta la detección de atípicos, **Then** cada
   atípico queda marcado con el criterio que lo detectó y su tratamiento (conservar, transformar o excluir)
   queda justificado.
3. **Given** el dataset final, **When** se compara con los datos crudos, **Then** el número de registros de
   entrada es igual a los registros finales más los excluidos, y cada excluido tiene su motivo.
4. **Given** textos con formatos mixtos (precios peruanos, reseñas, envío, descuento), **When** se
   normalizan, **Then** cada valor numérico derivado es consistente con su texto de origen o el caso queda
   registrado como inconsistencia.

---

### User Story 2 - Integración de las dos extracciones (Priority: P2)

El equipo necesita combinar el dataset de home office con el de categorías de contraste para enriquecer el
análisis: identificar las publicaciones que aparecen en ambos, comparar sus precios entre las dos fechas de
captura y unificar la información de los componentes compartidos (laptops y audífonos).

**Why this priority**: La integración es parte explícita del preprocesamiento en el enunciado y permite
validar la estabilidad de los precios entre fechas, pero el análisis principal puede hacerse sin ella.

**Independent Test**: Ejecutar la integración sobre los dos datasets limpios y verificar que identifica las
publicaciones comunes, resuelve los conflictos entre fuentes con una regla documentada y reporta la
variación de precio de cada publicación común.

**Acceptance Scenarios**:

1. **Given** los dos datasets limpios, **When** se integran por identificador de publicación, **Then** el
   resultado distingue publicaciones solo de home office, solo de categorías y presentes en ambas, y las
   cifras de cada grupo suman el total.
2. **Given** una publicación presente en ambas extracciones con valores distintos, **When** se integra,
   **Then** se aplica una regla de prioridad documentada y la diferencia de precio queda registrada.
3. **Given** los desafíos de integración del curso (identificación de entidades, datos sin sentido, formato
   de índice, desajuste de agregación, duplicados y redundancia), **When** se revisa la integración,
   **Then** cada desafío presente en estos datos está identificado y tratado.

---

### User Story 3 - Variables derivadas y perfiles de home office (Priority: P2)

Un trabajador o un área de recursos humanos necesita saber cuánto cuesta un home office según el nivel de
equipamiento, no solo un precio promedio. Para eso el equipo construye variables derivadas de los datos
(descuento real, calificación, unidades vendidas, condiciones de envío, tipo de vendedor, marca y
especificaciones técnicas extraídas del título) y segmenta cada componente en gamas.

**Why this priority**: El feature engineering es un criterio propio de la rúbrica (10 %) y los perfiles
responden la pregunta del proyecto con más precisión que la suma de medianas de la Parte I.

**Independent Test**: Ejecutar la construcción de variables sobre el dataset final y comprobar que cada
variable derivada tiene definición, cobertura reportada y al menos un uso en el análisis, y que cada
componente queda asignado a una gama.

**Acceptance Scenarios**:

1. **Given** el dataset final, **When** se construyen las variables derivadas, **Then** cada una tiene una
   regla de cálculo documentada, su porcentaje de cobertura y una justificación de su aporte al análisis.
2. **Given** las publicaciones de un componente, **When** se segmentan en gamas, **Then** cada publicación
   pertenece a exactamente una gama y los límites de cada gama están publicados.
3. **Given** las gamas de los seis componentes, **When** se arma un home office por perfil, **Then** se
   obtiene un costo de referencia con un rango para cada perfil.

---

### User Story 4 - Análisis, visualización e insights para el usuario (Priority: P3)

Un trabajador, un estudiante o un área de recursos humanos necesita hallazgos claros y accionables:
cuánto presupuestar, dónde están las mejores relaciones precio-calidad, si los descuentos anunciados son
reales, cuánto pesa el financiamiento en cuotas y qué ofertas parecen anómalas.

**Why this priority**: El análisis y los insights suman 30 % de la rúbrica, pero dependen de las historias
anteriores.

**Independent Test**: Revisar el notebook de análisis y comprobar que cada pregunta analítica tiene un
gráfico legible, una interpretación escrita y, cuando corresponde, un insight dirigido a un usuario.

**Acceptance Scenarios**:

1. **Given** el dataset final con variables derivadas, **When** se ejecuta el análisis, **Then** se
   reportan patrones, relaciones entre variables, anomalías y segmentaciones, cada uno con su gráfico o
   tabla.
2. **Given** cada gráfico del análisis, **When** se revisa, **Then** tiene título, ejes con unidades y una
   interpretación analítica escrita.
3. **Given** los hallazgos, **When** se redactan los insights, **Then** cada insight indica a qué usuario
   sirve, qué acción recomienda y qué cifra lo respalda.

---

### User Story 5 - Pipeline de datos reproducible (Priority: P3)

El docente evaluador o un tercero necesita ejecutar todo el flujo —ingestión de los datos crudos,
transformación y almacenamiento del resultado— siguiendo la documentación, y obtener los mismos resultados.

**Why this priority**: La propuesta de pipeline es un criterio propio (10 %) y la reproducibilidad es un
principio no negociable de la constitución.

**Independent Test**: En una copia limpia del repositorio, instalar las dependencias y ejecutar el flujo
con la instrucción del README; comprobar que regenera el dataset final y el almacenamiento idénticos a los
versionados.

**Acceptance Scenarios**:

1. **Given** una copia limpia del repositorio con las dependencias instaladas, **When** se ejecuta el
   pipeline con la instrucción documentada, **Then** recorre las etapas de ingestión, transformación y
   almacenamiento sin intervención manual.
2. **Given** el pipeline ejecutado dos veces, **When** se comparan las salidas, **Then** son idénticas.
3. **Given** un dato crudo que viola un invariante (identificador repetido tras la limpieza, precio no
   positivo, columna faltante), **When** se ejecuta el pipeline, **Then** se detiene con un mensaje que
   indica qué invariante falló.

---

### User Story 6 - Entregables y documentación (Priority: P4)

El docente necesita encontrar en el repositorio la estructura exigida por el enunciado (`data`,
`notebooks`, `docs`, `README.md`, `requirements.txt`), el dataset inicial y el final, el diccionario de
datos inicial y el final, y los documentos de entrega.

**Why this priority**: Son criterios de forma (dataset y diccionario 5 %, documentación 5 %) que se apoyan en
el trabajo de las historias anteriores.

**Independent Test**: Revisar el repositorio contra la lista de entregables del enunciado y comprobar que
cada uno existe, está en la carpeta exigida y es coherente con las salidas de los notebooks.

**Acceptance Scenarios**:

1. **Given** el repositorio, **When** se revisa su estructura, **Then** contiene las carpetas `data`,
   `notebooks` y `docs`, y los archivos `README.md` y `requirements.txt`.
2. **Given** el diccionario de datos final, **When** se compara con el dataset final, **Then** documenta todas
   sus variables con nombre, descripción, tipo, tamaño máximo, valores, unidad y limitaciones.
3. **Given** el documento maestro en PDF, **When** se revisa, **Then** sigue la plantilla oficial con sus
   once secciones en orden (identificación, contexto actualizado, objetivos actualizados, dataset y
   diccionario de datos final, propuesta de pipeline, preprocesamiento de datos, feature engineering,
   análisis y visualización de datos, insights encontrados, conclusiones, documentación y reproducibilidad en
   GitHub) y cada cifra coincide con la salida de los notebooks.
4. **Given** la presentación, **When** se revisa, **Then** sintetiza el flujo técnico y los resultados para
   una exposición de 15 minutos, con figuras legibles tomadas de los notebooks.

---

### Edge Cases

- Una búsqueda trae accesorios en lugar del componente (por ejemplo, fundas en la búsqueda de laptops o
  alfombrillas en la de mouse): se detectan y se tratan como datos sin sentido para el análisis de costo.
- El precio anterior es menor o igual al precio actual, o el porcentaje de descuento anunciado no coincide
  con el calculado a partir de ambos precios.
- La reseña trae solo la calificación o solo las unidades vendidas.
- Una misma publicación figura en ambas extracciones con distinta búsqueda de origen o distinto precio.
- Un título no contiene marca ni especificaciones reconocibles.
- Un componente tiene tan pocas publicaciones en una gama que su mediana no es representativa.
- Un precio extremo es plausible para un producto de gama alta (por ejemplo, una laptop de S/ 15 999) y no
  debe confundirse con un error.

## Requirements *(mandatory)*

### Functional Requirements

**Ingestión y limpieza**

- **FR-001**: El flujo MUST partir de los CSV crudos de la Parte I sin modificarlos ni volver a consultar el
  sitio web.
- **FR-002**: El flujo MUST verificar la estructura de cada fuente (columnas esperadas, identificador único
  por fila tras la deduplicación, nombres de columna codificables) antes de transformarla.
- **FR-003**: El flujo MUST convertir los textos de precio, precio anterior, descuento, cuotas, reseñas
  (calificación y unidades vendidas) y envío a valores tipados, registrando como inconsistencia cada texto
  que no se pueda interpretar.
- **FR-004**: El flujo MUST detectar y registrar inconsistencias entre campos relacionados (precio anterior
  frente a precio actual, descuento anunciado frente a descuento calculado, monto de cuota por número de
  cuotas frente al precio).
- **FR-005**: El flujo MUST deduplicar por identificador de publicación con una regla documentada y guardar
  los duplicados retirados como evidencia.
- **FR-032**: El flujo MUST detectar las publicaciones que no corresponden al componente buscado (accesorios
  o productos relacionados) y excluirlas del cálculo de costos, guardándolas como evidencia con su motivo.

**Valores faltantes**

- **FR-006**: El flujo MUST cuantificar los valores faltantes por columna y por componente.
- **FR-007**: El flujo MUST diagnosticar el tipo de cada faltante (MCAR, MAR o MNAR) con evidencia
  calculada, como su relación con otras variables observadas.
- **FR-008**: El flujo MUST aplicar a cada columna con faltantes una de las estrategias del curso —ignorar,
  eliminar filas, eliminar columnas o estimar e imputar— elegida según el tipo diagnosticado y justificada
  por escrito.
- **FR-009**: Toda imputación MUST quedar marcada en el dataset para distinguir el valor observado del
  imputado.

**Valores atípicos**

- **FR-010**: El flujo MUST detectar atípicos univariados en las variables numéricas, por componente, con al
  menos un criterio estadístico —rango intercuartílico con factor 1,5 y |z| > 3— y uno visual.
- **FR-011**: El flujo MUST detectar atípicos bivariados entre variables relacionadas y atípicos
  multivariados mediante agrupamiento.
- **FR-012**: El flujo MUST decidir para cada atípico si se conserva, se transforma o se excluye, con una
  justificación que distinga errores de valores extremos plausibles. Es error comprobable un precio
  incoherente con el propio financiamiento o el precio anterior de la publicación, un precio de relleno
  (por ejemplo, 99 999) o un precio que el título contradice; los demás extremos se conservan.

**Integración, reducción y transformación**

- **FR-013**: El flujo MUST integrar los datasets de home office y de categorías por identificador de
  publicación, identificando entidades comunes y resolviendo conflictos con una regla de prioridad
  documentada.
- **FR-014**: El flujo MUST reportar la variación de precio de las publicaciones presentes en ambas
  extracciones.
- **FR-015**: El flujo MUST reducir el dataset retirando columnas constantes, vacías o redundantes, con la
  evidencia de redundancia correspondiente.
- **FR-016**: El flujo MUST aplicar, como mínimo, codificación binaria de las variables categóricas,
  discretización de variables numéricas y transformación logarítmica del precio, y justificar cada una con el
  uso que tiene en el análisis.

**Ingeniería de características**

- **FR-017**: El flujo MUST construir variables derivadas que cubran, como mínimo: descuento real,
  indicador de promoción, calificación, unidades vendidas, envío gratuito, entrega rápida, tipo de vendedor y
  marca; y, a partir del título, al menos una especificación técnica por componente: memoria y
  almacenamiento en laptops, tamaño de pantalla en monitores, conexión inalámbrica en teclados, mouse y
  audífonos, y carácter ergonómico en sillas de oficina.
- **FR-018**: El flujo MUST segmentar cada componente en gamas con una regla publicada, de modo que cada
  publicación pertenezca a exactamente una gama, y validar la segmentación con al menos una variable distinta
  del precio (por ejemplo, la memoria de las laptops o la calificación).
- **FR-019**: Cada variable derivada MUST tener su regla de cálculo, su cobertura y su aporte al análisis
  documentados.

**Análisis y visualización**

- **FR-020**: El análisis MUST estimar un valor central y un rango de precio por componente y gama, y el
  costo de equipar un home office por perfil de equipamiento, con un valor central y un rango para cada
  perfil.
- **FR-021**: El análisis MUST explorar patrones, relaciones entre variables, anomalías y segmentaciones,
  incluyendo al menos: dispersión de precios por componente y gama, efecto de las promociones, peso del
  financiamiento en cuotas, relación entre calificación, unidades vendidas y precio, y diferencias por
  marca y tipo de vendedor.
- **FR-022**: Cada gráfico MUST tener título, ejes con unidades y una interpretación analítica escrita.
- **FR-023**: El análisis MUST concluir con insights accionables, cada uno dirigido a un usuario identificado
  y respaldado por una cifra calculada.

**Pipeline y almacenamiento**

- **FR-024**: El flujo MUST organizarse como un pipeline con etapas explícitas de ingestión,
  transformación y almacenamiento, ejecutable con una instrucción documentada.
- **FR-025**: El pipeline MUST almacenar el resultado en un formato tabular estándar y en un almacén
  consultable con SQL, y documentar la decisión.
- **FR-026**: Cada etapa del flujo —pipeline y notebooks— MUST detenerse con un mensaje explícito cuando se
  viole un invariante de los datos.

**Entregables**

- **FR-027**: El repositorio MUST contener las carpetas `data` (dataset inicial y final), `notebooks` (con
  nombres que describen lo que hace cada uno) y `docs` (diccionario de datos inicial de cada dataset crudo
  —categorías y home office— y diccionario final), y los archivos `README.md` y `requirements.txt`.
- **FR-028**: El dataset final MUST entregarse en CSV con codificación UTF-8. El diccionario de datos final
  MUST seguir la plantilla oficial del curso (Variable, Descripción, Tipo, Tamaño máximo, Valores, Unidad),
  entregarse en `.docx` y en PDF, documentar todas las variables del dataset final y registrar sus
  limitaciones en notas bajo la tabla.
- **FR-029**: El README MUST describir el problema, la estructura del repositorio, la instalación, la
  ejecución paso a paso y la correspondencia entre entregables y archivos.
- **FR-030**: La feature MUST producir el documento maestro sobre la plantilla oficial
  `Formato Proyecto Final Parte II.docx`, con sus once secciones en el orden de la plantilla, en `.docx` y
  exportado a PDF; cada cifra y figura MUST provenir de las salidas de los notebooks.
- **FR-031**: La feature MUST producir la presentación en `.pptx` para una exposición de 15 minutos —entre 12
  y 16 diapositivas, repartibles entre los cinco integrantes— que sintetice el flujo técnico, los resultados y
  los insights, con las mismas cifras que el documento maestro.
- **FR-033**: El documento maestro MUST incluir: un contexto actualizado con los hallazgos de la adquisición y
  del preprocesamiento; una tabla de objetivos de la Parte I con su estado (se mantiene, se ajusta o se
  retira) y el motivo; un diagrama del pipeline; y conclusiones que respondan a cada objetivo actualizado y
  declaren las limitaciones del proyecto.

### Non-Functional Requirements

- **NFR-001**: Reproducibilidad — un tercero MUST poder regenerar todas las cifras publicadas desde los datos
  crudos siguiendo solo el README.
- **NFR-002**: Determinismo — dos ejecuciones sobre los mismos datos MUST producir salidas idénticas.
- **NFR-003**: Tiempo — el flujo completo MUST ejecutarse en menos de 10 minutos en una computadora personal.
- **NFR-004**: Trazabilidad — ningún registro puede desaparecer del flujo sin quedar en evidencia con su
  motivo.
- **NFR-005**: Fidelidad al curso — las técnicas MUST provenir del material de clase; cualquier excepción se
  justifica por escrito.
- **NFR-007**: Trazabilidad del repositorio — el historial MUST tener commits coherentes con Conventional
  Commits, al menos uno por etapa del pipeline.
- **NFR-006**: Legibilidad — los textos de los gráficos MUST tener al menos 9 puntos al tamaño en que se
  insertan en el documento y en la presentación.

### Key Entities *(include if feature involves data)*

- **Publicación**: oferta de un producto en Mercado Libre Perú identificada por su código; tiene precio,
  condiciones comerciales (descuento, cuotas, envío), reputación (calificación, unidades vendidas) y un
  título del que se extraen marca y especificaciones.
- **Componente**: tipo de equipo del home office (laptop, monitor, silla de oficina, teclado, mouse,
  audífonos); agrupa publicaciones de una misma búsqueda.
- **Captura**: extracción de un día y una configuración (home office del 15/09/2026, categorías del
  13/09/2026); una publicación puede aparecer en más de una captura.
- **Gama**: segmento de precio y características dentro de un componente.
- **Perfil de home office**: combinación de un componente de cada tipo en una gama; tiene un costo de
  referencia con rango.
- **Registro excluido**: publicación o fila retirada del flujo, con su etapa y su motivo.
- **Diccionario de datos**: descripción de cada variable de un dataset (nombre, descripción, tipo, tamaño
  máximo, valores, unidad y limitaciones).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un tercero regenera todas las cifras del informe desde los datos crudos en menos de 10
  minutos, siguiendo solo el README, y obtiene exactamente los mismos valores.
- **SC-002**: El 100 % de las columnas con valores faltantes y el 100 % de los criterios de atípicos tienen
  diagnóstico, tratamiento y justificación escritos.
- **SC-003**: El balance de registros cuadra en el 100 % de las etapas: entrada = salida + excluidos con
  motivo.
- **SC-004**: El dataset final conserva al menos el 95 % de las publicaciones únicas válidas de los datos
  crudos.
- **SC-005**: Ninguna columna del dataset final supera el 10 % de valores faltantes sin una justificación
  documentada de por qué el faltante significa "no aplica".
- **SC-006**: Se construyen al menos 10 variables derivadas y cada una se usa en al menos un análisis o
  gráfico.
- **SC-007**: Se reporta un costo de referencia con rango para al menos 3 perfiles de home office.
- **SC-008**: Se formulan al menos 5 insights accionables, cada uno con su usuario destinatario y la cifra
  que lo respalda.
- **SC-009**: El 100 % de los gráficos incluye interpretación escrita.
- **SC-010**: El 100 % de las variables del dataset final está documentado en el diccionario de datos final.

## Assumptions

- La pregunta del proyecto es la del informe entregado en la Parte I: cuánto cuesta equipar un home office
  en el Perú.
- El dataset principal es el de home office (3 680 registros crudos, 17 columnas, 15/09/2026). El de
  categorías (5 080 registros crudos, 13/09/2026) es la segunda fuente: se integra con el principal y aporta
  la comparación de precios entre fechas para laptops y audífonos. Ambos provienen del web scraping de la
  Parte I con el mismo método y distinta configuración.
- Los datos crudos de la Parte I son definitivos: no se repite el scraping y las cifras describen las ofertas
  del 13 y 15 de setiembre de 2026.
- El enunciado exige las carpetas `data`, `notebooks` y `docs`; las carpetas actuales `datos` y `documentos`
  se reorganizan bajo esos nombres conservando su contenido.
- Las técnicas se toman del material de clase de las Unidades 3, 4 y 5; se usan sus librerías.
- Los datos crudos de la Parte I permanecen en el repositorio como dataset inicial.
- La presentación oral, su ensayo y la exposición por Zoom quedan a cargo del equipo.

## Out of Scope

- Nueva extracción de datos o cualquier consulta al sitio web.
- Modelos predictivos o de aprendizaje supervisado: el enunciado limita el alcance a preprocesamiento,
  análisis y fundamentos de ingeniería de datos.
- Series de tiempo: cada captura es de un solo día; la comparación entre las dos fechas no constituye una
  serie.
- Aplicaciones o interfaces de usuario como producto principal; un tablero, si existe, es complementario.
- Componentes que no forman parte de la definición de home office de la Parte I (escritorio, cámara web,
  iluminación, conexión a internet).
- Análisis geoespacial: los datos no contienen ubicación.
- Datos personales de compradores o vendedores.
