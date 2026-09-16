# Secciones pendientes del informe (Parte 5)

Borrador de las cuatro secciones que el informe todavía marca como pendientes —1 Identificación, 5 Alcance,
7 Estrategia y 8 Viabilidad—, redactadas a partir de lo que el repositorio realmente contiene. Se copian al
formato Word oficial (`indicaciones/Formato Proyecto Final Parte I.docx`) junto con la sección 4, que genera
el notebook en `documentos/Dataset_preliminar.md`.

Pendiente de completar por el equipo: las evidencias de participación de cada integrante, que la rúbrica
pondera con 20 % y que este documento no puede sustituir.

---

## 1. Identificación

La distribución de responsabilidades se organizó de forma secuencial: cada integrante recibe como insumo el
entregable del integrante anterior, ejecuta su tarea y produce el material que necesita la siguiente etapa.

| Parte | Integrante | Responsabilidades | Entregable verificable | Estado |
| --- | --- | --- | --- | --- |
| Parte 1 | Yared Riveros Rodríguez | Selección y justificación de la fuente; redacción de Contexto, Objetivos y Fuentes de datos. | Secciones 2, 3 y 6 del informe. | Completado |
| Parte 2 | Franco Nicolás Roque Castillo | Script de web scraping (paginación, cabeceras, pausas, manejo de errores, guardado incremental) y extracción del dataset crudo. | Sección 1 del notebook; `datos/crudos/mercadolibre_raw.csv` (5 080 registros). | Completado |
| Parte 3 | Mauricio Terán Taica | Limpieza y control de calidad del dataset; redacción de la sección Dataset preliminar. | Sección 2 del notebook; `datos/limpios/mercadolibre_limpio.csv` (4 412 registros); `datos/calidad/`; sección 4 del informe. | Completado |
| Parte 4 | Josué Luna Rocha | Diccionario de datos en el formato Word solicitado. | `documentos/Diccionario de datos.docx` y `.pdf` (14 variables). | Completado |
| Parte 5 | Álvaro Mauricio García Hurtado | Redacción de Identificación, Alcance, Estrategia y Viabilidad; ensamblaje del notebook y del informe final. | Secciones 1, 5, 7 y 8; notebook único `ACD_Proyecto_Parte_I.ipynb`; informe en PDF. | En curso |

El trabajo se integra en el repositorio `proyectoacd_mercadolibre`, donde cada parte corresponde a archivos
identificables y el historial de commits registra el aporte de cada integrante.

---

## 5. Alcance

### Qué se desarrolla en esta primera entrega

- **Adquisición.** Extracción automatizada de publicaciones de cinco categorías de Mercado Libre Perú
  (celulares, laptops, televisores, refrigeradoras y audífonos) desde las páginas de resultados de
  `listado.mercadolibre.com.pe`, con recorrido de hasta veinte páginas por categoría.
- **Limpieza y control de calidad.** Normalización de textos, conversión de precios y fechas a tipos
  numéricos y temporales, recuperación del identificador de oferta, separación de registros incompletos,
  deduplicación por oferta y documentación de cada exclusión con su evidencia.
- **Documentación.** Diccionario de datos con las 14 variables del archivo final, descripción de la muestra
  preliminar y un notebook reproducible que permite repetir todo el proceso.
- **Entregables.** Dataset preliminar en CSV con codificación UTF-8, diccionario de datos e informe.

### Qué queda fuera

- **Análisis exploratorio profundo y modelado.** No se realizan pruebas estadísticas, segmentación ni
  modelos predictivos: corresponden a las siguientes partes del proyecto.
- **Seguimiento histórico de precios.** El dataset es una fotografía del 13 de setiembre de 2026, no una
  serie temporal. No permite medir variaciones de precio en el tiempo.
- **Reseñas individuales y datos del vendedor.** No se extraen opiniones de compradores ni información de
  perfiles; las rutas de perfil están además restringidas por `robots.txt`.
- **Atributos ausentes de las tarjetas de resultados.** Calificación, número de opiniones, condición, marca
  y envío gratuito no figuran en las páginas de listado y quedan fuera del dataset; el precio anterior y el
  vendedor se capturaron pero superan el 10 % de nulos y permanecen solo en el CSV crudo.
- **Representatividad del mercado.** La muestra proviene de cinco búsquedas y no es aleatoria: describe las
  ofertas observadas, no el universo del comercio electrónico peruano ni transacciones efectivas.
- **Redistribución.** El dataset es de uso académico dentro del curso DS3021 y no se publica con fines
  comerciales.

---

## 7. Estrategia

### Herramientas

Python 3.11 con Selenium (navegación), BeautifulSoup (análisis del HTML) y pandas (consolidación, limpieza y
exportación). El trabajo se versiona en Git y se ejecuta desde un único notebook, `ACD_Proyecto_Parte_I.ipynb`,
dividido en las secciones Extracción y Limpieza.

### Procedimiento de obtención

1. **Verificación de políticas.** Antes de extraer se descargan los `robots.txt` de `www.mercadolibre.com.pe`
   y del subdominio de listados, se interpretan con `urllib.robotparser` y se comprueba, para el `User-Agent`
   declarado, que cada URL a visitar esté permitida. Los archivos quedan guardados como evidencia fechada en
   `datos/calidad/robots/`. Si alguna ruta estuviera prohibida, el notebook se detiene.
2. **Recorrido por categorías.** Cinco categorías de rubros distintos, elegidas para dar variedad de precios
   y marcas al dataset.
3. **Control de la paginación.** El avance entre páginas usa el botón `Siguiente` del sitio, que genera las
   URL con el sufijo `_Desde_N` (48 resultados por página). El bucle se detiene cuando la página no devuelve
   tarjetas o cuando repite el contenido anterior, en lugar de fijar un número rígido de páginas: por eso el
   recorrido efectivo fue de 95 páginas y no de 100.
4. **Cortesía con el servidor.** Pausa de diez segundos entre peticiones mediante `time.sleep()`, `User-Agent`
   realista e identificable y ninguna técnica de evasión de bloqueos.
5. **Robustez.** Cada página se procesa dentro de un bloque `try-except`, de modo que una falla puntual no
   cancela la ejecución, y los resultados se escriben de forma incremental en el CSV: una interrupción no
   pierde lo ya extraído.
6. **Limpieza y verificación.** La segunda sección del notebook convierte el CSV crudo en el dataset final y
   comprueba con `assert` los requisitos del enunciado: mínimo de registros y de atributos, unicidad del
   identificador y máximo de 10 % de nulos por columna. Si alguno deja de cumplirse, el notebook falla en
   lugar de exportar en silencio.

### Planes de contingencia

- **Cambios en el maquetado del sitio.** Los nombres de clase CSS están aislados en las funciones
  `buscar_clase` y `detectar_tarjetas`: una actualización del sitio se resuelve modificando solo ese bloque.
- **Contenido servido con JavaScript.** Previsto inicialmente con `requests`, el sitio entregó páginas
  incompletas; se aplicó la contingencia prevista y la navegación pasó a Selenium, conservando BeautifulSoup
  para el análisis del HTML.
- **Limitación de peticiones o verificación de navegador.** Ampliar la pausa entre solicitudes y fraccionar la
  ejecución en varias sesiones. Cuando el sitio solicita una verificación, el notebook la delega a la persona
  que ejecuta y reanuda el recorrido.
- **Inviabilidad de la extracción por HTML.** Uso de la API pública de consulta de la plataforma como fuente
  alternativa, documentando el cambio.
- **Fuente de reemplazo.** Falabella Perú queda registrada como alternativa, con la advertencia de que exige
  navegador automatizado y un tiempo de ejecución mayor.

---

## 8. Viabilidad

### Tiempo

La extracción completa —cinco categorías, 95 páginas, 5 080 registros crudos— se ejecutó el 13 de setiembre
de 2026 entre las 19:54:05 y las 20:22:54, según las marcas temporales del propio scraper: **29 minutos**, de
los cuales la mayor parte corresponde a las pausas deliberadas entre peticiones. La limpieza completa se
ejecuta en segundos sobre el CSV ya obtenido, de modo que cualquier ajuste posterior no obliga a repetir la
extracción. Frente a la fecha de entrega del 25 de setiembre de 2026, el dataset quedó disponible con doce
días de holgura, suficientes para la documentación y para repetir la captura si fuera necesario.

Obtener un volumen equivalente de forma manual —transcribir más de cinco mil publicaciones— habría exigido
decenas de horas y un riesgo alto de error de transcripción, lo que confirma la pertinencia de la adquisición
automatizada.

### Recursos

Una computadora personal con Windows 11, Google Chrome y conexión doméstica a internet es suficiente: no se
requieren servidores, servicios de pago ni credenciales. El almacenamiento total del proyecto, incluidos los
archivos de evidencia, es de pocos megabytes. El trabajo se coordina mediante un repositorio Git compartido
por los cinco integrantes.

### Herramientas

Todas las librerías empleadas son de código abierto y gratuitas (`selenium`, `beautifulsoup4`, `requests`,
`pandas`), están declaradas en `requirements.txt` y se instalan con una sola orden. El proceso completo se
reproduce ejecutando un notebook, lo que permite a un tercero repetir la extracción y la limpieza siguiendo
únicamente las instrucciones del documento.

### Riesgos y su control

| Riesgo | Control adoptado |
| --- | --- |
| Cambio del maquetado del sitio | Selectores aislados en un solo bloque del notebook. |
| Bloqueo o limitación de peticiones | Pausa de diez segundos, `User-Agent` identificable, ejecución fraccionable. |
| Interrupción de la ejecución | Guardado incremental en el CSV tras cada página. |
| Datos de calidad insuficiente | Verificaciones automáticas con `assert` y evidencia de cada exclusión. |
| Pérdida de trabajo o descoordinación | Repositorio Git con el aporte de cada integrante registrado. |
