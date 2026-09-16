# Prompt para Gemini — correcciones del informe en Google Docs

Copiar todo este documento como un solo prompt en el Google Docs del informe
(`Informe_Parte_I_DS3021`). Está escrito para que Gemini pueda ejecutarlo sin acceso al repositorio:
todos los datos que necesita están aquí.

---

## ROL Y REGLAS

Eres un editor técnico. Vas a corregir el documento abierto: *Primer avance del proyecto final —
Adquisición de datos de publicaciones de productos en Mercado Libre Perú mediante web scraping*
(curso DS3021, UTEC).

Reglas obligatorias:

1. **No inventes ninguna cifra.** Usa exclusivamente los datos de la sección «HECHOS VERIFICADOS». Si una
   instrucción exige un dato que no está aquí, deja `[COMPLETAR]` y avísame al final.
2. Aplica **solo** las instrucciones numeradas. No reescribas secciones que no se mencionan.
3. Mantén el estilo del documento: español formal, tercera persona, sin viñetas nuevas donde había
   párrafos, y respetando la numeración de secciones existente.
4. Las tablas de este prompt están en formato de texto con barras `|`. **Insértalas como tablas reales de
   Google Docs**, con el mismo formato que las tablas que ya tiene el documento.
5. Cuando una instrucción diga «buscar», usa ese texto para localizar el pasaje; puede haber diferencias
   menores de espaciado.
6. Al terminar, escribe al final del chat (no en el documento) una lista de las instrucciones aplicadas y
   de las que no pudiste aplicar, con el motivo.

---

## HECHOS VERIFICADOS DEL PROYECTO

Todo lo siguiente está comprobado en el código y en los archivos entregados. Es la única fuente de cifras.

**Extracción**

- Herramientas: Python 3.11, **Selenium** (navegación), **BeautifulSoup** (análisis del HTML), pandas.
  `requests` se usa únicamente para descargar `robots.txt`.
- Motivo del uso de Selenium: el sitio no entrega las tarjetas de resultados a peticiones simples de
  `requests`; devuelve páginas incompletas. Se aplicó el plan de contingencia previsto en el Anexo A.5.
- Categorías recorridas: **5** — celulares, laptops, televisores, refrigeradoras, audífonos.
- Páginas recorridas: **95 de 100 posibles** (20 en celulares, laptops, televisores y audífonos; 15 en
  refrigeradoras, que agotó los resultados antes). Máximo configurado: 20 páginas por categoría.
- Paginación: avance con el botón real `Siguiente` del sitio, que genera las URL con el sufijo `_Desde_N`.
- Pausa entre peticiones: **10 segundos fijos** con `time.sleep()`.
- User-Agent declarado: cadena de Google Chrome 152 en Windows 10/11, identificable y sin rotación.
- Manejo de errores: `try-except` por página. Guardado incremental: cada página se añade al CSV apenas se
  procesa.
- Fecha y duración de la extracción: **13 de setiembre de 2026, de 19:54:05 a 20:22:54 (29 minutos)**.
- Resultado crudo: **5 080 registros y 13 columnas**, en CSV UTF-8.

**Verificación de robots.txt**

- Se descargan los `robots.txt` de **dos dominios**: `www.mercadolibre.com.pe` y
  `listado.mercadolibre.com.pe` (el subdominio de listados **tiene reglas propias**, distintas del dominio
  principal; el informe actual solo menciona el primero).
- Los archivos se interpretan con `urllib.robotparser` y se comprueba, para el User-Agent declarado, cada
  URL que el scraper visita: la portada de cada categoría y una URL paginada con sufijo `_Desde_N`. Las seis
  resultaron permitidas.
- Se comprueba además que las rutas que el proyecto se compromete a no visitar (`/gz/cart/`,
  `/gz/checkout/`, `/perfil/vendedor/`) estén efectivamente restringidas: lo están.
- Los archivos descargados se guardan fechados como evidencia. Si alguna ruta estuviera prohibida, el
  notebook se detiene y no extrae.

**Limpieza y dataset final**

- Dataset final: **4 412 ofertas únicas y 14 columnas**, CSV en UTF-8.
- Del crudo se separaron **56 filas** sin campos esenciales válidos, se retiraron **605 repeticiones** por
  identificador de oferta y se excluyeron **7 ofertas con precios cuestionados**. Suma comprobada:
  5 080 = 56 + 605 + 7 + 4 412.
- Las 14 columnas finales son: `id_publicacion`, `id_extraido`, `categoria`, `titulo`, `moneda`,
  `precio_actual`, `numero_cuotas`, `monto_cuota`, `cuotas_texto`, `pagina`, `posicion_pagina`,
  `url_publicacion`, `url_fuente`, `fecha_extraccion`.
- Nulos: máximo **1,25 %** en una columna (`numero_cuotas`, `monto_cuota` y `cuotas_texto`, 55 nulos cada
  una). Las demás columnas no tienen nulos.
- El identificador de oferta `id_publicacion` se recupera del parámetro `wid` de la URL o, si falta, del
  código de una ruta directa sin `/p/`. El código que había extraído el scraper se conserva como
  `id_extraido`.
- **Atributos que NO se obtuvieron**: calificación, número de opiniones, condición, marca, envío gratuito y
  cantidad vendida. No figuran en las tarjetas de las páginas de resultados.
- **Atributos capturados pero descartados del dataset final** por exceder el 10 % de nulos:
  `precio_anterior_texto` (40,08 % de nulos) y `vendedor_texto` (64,07 %). Permanecen solo en el CSV crudo.

**Entregables**

- Un único notebook, `ACD_Proyecto_Parte_I.ipynb`, con la sección 1 «Extracción» y la sección 2 «Limpieza».
- Dataset preliminar en CSV UTF-8 y diccionario de datos con las 14 variables (nombre, descripción, tipo,
  tamaño máximo, valores y unidad).

---

## INSTRUCCIONES DE EDICIÓN

### 1. Portada — limpiar el formato de los nombres

En la portada, los nombres aparecen entre líneas de guiones bajos y con longitudes distintas; uno de ellos
no las tiene. Elimina todos los guiones bajos y deja los cinco nombres alineados, uno por línea, con las
tildes correctas:

```
Yared Riveros Rodríguez
Mauricio Terán Taica
Franco Nicolás Roque Castillo
Josué Luna Rocha
Álvaro Mauricio García Hurtado
```

Corrige también el título de la línea «PRIMER AVANCE DEL PROYECTO FINAL:» para que el nombre del proyecto
quede en la línea del formato, sin los guiones bajos de la plantilla.

*Motivo: la rúbrica exige redacción y presentación profesionales, libres de errores.*

### 2. Índice — completar las páginas

El índice tiene la columna «Pág.» con guiones bajos vacíos en las ocho secciones. Sustituye el índice manual
por un índice automático (Insertar → Tabla de contenido) o completa los números de página reales una vez
terminada la edición.

### 3. Sección 1 «IDENTIFICACIÓN» — completar la tabla y borrar la nota provisional

La tabla actual tiene los nombres entre guiones bajos, la Parte 5 marcada como «Pendiente» y, debajo, este
texto: *«Sección a cargo de la Parte 5. El cuadro se presenta como propuesta preliminar: corresponde
completar los nombres de los integrantes, incorporar las evidencias de participación y actualizar los
estados antes de la entrega final.»*

- Reemplaza la tabla completa por la del **ANEXO 5** de este prompt.
- **Elimina** el párrafo provisional citado.
- Conserva el párrafo introductorio que explica la distribución secuencial de responsabilidades.
- Añade después de la tabla este párrafo:

> El trabajo se integra en un repositorio Git compartido, donde cada parte corresponde a archivos
> identificables y el historial de cambios registra el aporte de cada integrante.

*Nota para el equipo (no la escribas en el documento): la rúbrica pondera con 20 % el aporte individual con
evidencias; añadan capturas, enlaces a commits o actas de reunión en esta sección.*

### 4. Sección 3.2, objetivo específico 2 — corregir la técnica y la cobertura

Busca: *«Desarrollar un script en Python con requests y BeautifulSoup que recorra al menos cinco categorías
de productos y un mínimo de veinte páginas de resultados por categoría, gestionando la paginación mediante
el patrón de URL del sitio.»*

Reemplázalo por:

> Desarrollar un script en Python que recorra al menos cinco categorías de productos y hasta veinte páginas
> de resultados por categoría, empleando Selenium para la navegación —el sitio no entrega las tarjetas de
> resultados a peticiones simples— y BeautifulSoup para el análisis del HTML, gestionando la paginación
> mediante el botón de avance del sitio, que genera el patrón de URL `_Desde_N`.

*Motivo: el informe anuncia `requests` y un mínimo de veinte páginas por categoría; la extracción real usó
Selenium y recorrió 95 de las 100 páginas posibles. La rúbrica evalúa que la técnica declarada sea la
aplicada.*

### 5. Sección 3.2, objetivo específico 3 — precisar la pausa

Busca: *«pausas entre peticiones mediante time.sleep()»* y reemplaza por *«pausas de diez segundos entre
peticiones mediante time.sleep()»*. El resto del objetivo se mantiene igual.

*Motivo: el informe menciona más adelante pausas «de un mínimo de dos segundos» y «de entre dos y cuatro
segundos», pero el script ejecutado usa diez segundos fijos. Las tres cifras deben coincidir (ver también
las instrucciones 16 y 19).*

### 6. Sección 3.2, objetivo específico 4 — ajustar los atributos a los realmente obtenidos

Busca: *«Extraer un mínimo de ocho atributos por publicación, con al menos cuatro variables numéricas
(precio actual, precio anterior, calificación y número de opiniones) y cuatro categóricas (título,
categoría, condición y disponibilidad de envío gratuito).»*

Reemplázalo por:

> Extraer un mínimo de ocho atributos por publicación, combinando variables numéricas (precio actual,
> número de cuotas, monto de cada cuota, página y posición en los resultados) y categóricas (identificador
> de la oferta, título, categoría de búsqueda, moneda, texto de financiamiento, enlace de la publicación,
> enlace de la página de resultados y fecha de extracción), superando el mínimo de seis atributos exigido
> por el enunciado.

*Motivo: calificación, número de opiniones, condición y envío gratuito no figuran en las tarjetas de las
páginas de resultados y no están en el dataset; el precio anterior se capturó pero quedó fuera del archivo
final por tener 40,08 % de nulos. Un objetivo que promete datos inexistentes en el entregable es la
inconsistencia más visible del informe.*

### 7. Sección 3.2, objetivo específico 5 — precisar el identificador

Busca: *«identificados de forma unívoca por el código de publicación»* y reemplaza por:

> identificados de forma unívoca por el código de la oferta, recuperado del parámetro `wid` de la URL o, en
> su defecto, de una ruta directa de publicación

*Motivo: el código visible en la ruta `/p/MPE...` corresponde al producto de catálogo y no a la oferta; usarlo
como clave habría fusionado ofertas distintas.*

### 8. Sección 3.2, objetivo específico 8 — nombrar el entregable

Busca: *«Entregar un notebook comentado y reproducible»* y reemplaza por:

> Entregar un único notebook comentado y reproducible, `ACD_Proyecto_Parte_I.ipynb`, organizado en dos
> secciones —Extracción y Limpieza—

El resto de la frase se mantiene.

### 9. Sección 4 «DATASET PRELIMINAR» — reemplazar el marcador de posición

La sección contiene hoy solo un encargo: *«Sección a cargo de la Parte 3. Debe describir la muestra
obtenida: número final de registros y de columnas…»*.

Elimina ese texto por completo y sustitúyelo por el contenido del **ANEXO 1**, respetando sus subtítulos
(4.1 a 4.6) y convirtiendo sus dos tablas en tablas de Google Docs.

### 10. Sección 5 «ALCANCE» — reemplazar el marcador de posición

Elimina el texto *«Sección a cargo de la Parte 5. Debe delimitar de forma explícita…»* y sustitúyelo por el
contenido del **ANEXO 2**.

### 11. Sección 6.2, tabla comparativa, fila «Renderizado del contenido» — corregir la celda de Mercado Libre

Busca en esa celda: *«Las páginas de resultados se entregan como HTML servido por el servidor: los datos son
visibles con requests + BeautifulSoup, sin necesidad de un navegador.»*

Reemplázala por:

> Las páginas de resultados se entregan como HTML, extraíble con BeautifulSoup. La verificación posterior
> mostró que el servidor responde de forma incompleta a peticiones simples, por lo que la navegación se
> resolvió con Selenium; el volumen de páginas requerido sigue siendo alcanzable en menos de media hora.

*Motivo: la comparación de fuentes descarta Falabella precisamente por exigir Selenium, mientras que la
fuente elegida terminó exigiéndolo también. Si no se corrige, la justificación de la elección queda
contradicha por el propio proyecto.*

### 12. Sección 6.2, tabla comparativa, fila «Políticas de acceso (robots.txt)» — añadir la referencia faltante

En la celda correspondiente a Falabella Perú, al final de *«Archivo permisivo (User-agent: * sin rutas
prohibidas) acompañado de varios sitemaps»*, añade la cita **[13]**.

*Motivo: la referencia [13] aparece en la lista final pero no se cita en el cuerpo del informe.*

### 13. Sección 6.3 — corregir la numeración de la lista

Las cinco razones que justifican la fuente están numeradas **9, 10, 11, 12 y 13** por un error de lista
heredado de la sección anterior. Renuméralas como **1, 2, 3, 4 y 5**, sin cambiar su texto (salvo la razón 2,
que se corrige en la instrucción siguiente).

### 14. Sección 6.3, segunda razón — corregir la afirmación sobre la técnica

Busca: *«Su contenido es extraíble con la técnica adecuada al curso. Las páginas de resultados se entregan
como HTML desde el servidor, de modo que la información puede obtenerse con requests y BeautifulSoup, sin
recurrir a un navegador automatizado. Esto reduce el tiempo de ejecución y la complejidad del script frente
a alternativas como Falabella.»*

Reemplázalo por:

> Su contenido es extraíble con las técnicas del curso. Las páginas de resultados exponen los datos en el
> HTML, de modo que el análisis se resuelve con BeautifulSoup. La navegación requiere un navegador
> automatizado —Selenium—, pero la estructura regular del listado mantiene el script simple: la extracción
> completa tomó veintinueve minutos.

### 15. Sección 6.4 — aclarar el estatus de la tabla de atributos

Después del párrafo que empieza *«Con catorce atributos identificados —siete numéricos y siete
categóricos—…»*, añade esta aclaración:

> Esta tabla corresponde a los atributos identificados en la exploración previa de la fuente. La extracción
> confirmó la disponibilidad de título, precio actual, moneda, cuotas, categoría, identificador y enlace en
> las páginas de resultados, pero no la de calificación, número de opiniones, condición, marca, envío
> gratuito y cantidad vendida, que la plataforma no expone en las tarjetas del listado. El precio anterior y
> el tipo de vendedor sí se capturaron, pero quedaron fuera del archivo final por superar el límite de 10 %
> de valores nulos. La composición definitiva del dataset se detalla en la sección 4.

### 16. Sección 6.5 — actualizar la pausa y la verificación de robots.txt

a) Busca: *«Se incluirá una pausa entre peticiones mediante time.sleep(), con un intervalo mínimo de dos
segundos, a fin de no generar carga significativa sobre el servidor.»* y reemplaza por:

> Se incluye una pausa de diez segundos entre peticiones mediante `time.sleep()`, a fin de no generar carga
> significativa sobre el servidor. Con ese intervalo, la extracción completa de las cinco categorías tomó
> veintinueve minutos.

b) Después del primer párrafo de la sección 6.5 (el que describe el archivo `robots.txt`), añade este
párrafo nuevo:

> La verificación se automatizó dentro del notebook y se ejecuta antes de cada extracción. El proceso
> descarga los archivos `robots.txt` de los dos dominios involucrados —`www.mercadolibre.com.pe` y el
> subdominio de listados `listado.mercadolibre.com.pe`, que declara reglas propias—, los interpreta con el
> módulo `urllib.robotparser` y comprueba, para el User-Agent declarado, cada dirección que el script va a
> visitar, incluidas las URL paginadas con el sufijo `_Desde_N`. Todas resultaron permitidas, y las rutas que
> el proyecto se compromete a no visitar —carrito, proceso de compra y perfiles de vendedor— se confirmaron
> restringidas. Los archivos descargados se conservan fechados como evidencia de la revisión. Si alguna ruta
> estuviera prohibida, la ejecución se detiene antes de extraer.

c) En la viñeta sobre el vendedor, busca *«El campo relativo al vendedor se registrará únicamente como
categoría (por ejemplo, tienda oficial u otro vendedor).»* y reemplaza por:

> El campo relativo al vendedor se registró únicamente como categoría y, al presentar más del 60 % de
> valores ausentes, quedó fuera del dataset final.

*Motivo: la rúbrica y las consideraciones del enunciado exigen verificar las políticas del sitio; comprobar
que el archivo responde no equivale a leer sus reglas, y el dominio realmente rastreado no era el citado.*

### 17. Sección 7 «ESTRATEGIA» — reemplazar el marcador de posición

Elimina el texto *«Sección a cargo de la Parte 5. Debe describir las herramientas y el procedimiento de
obtención de los datos…»* y sustitúyelo por el contenido del **ANEXO 3**.

### 18. Sección 8 «VIABILIDAD» — reemplazar el marcador de posición

Elimina el texto *«Sección a cargo de la Parte 5. Debe sustentar la factibilidad del proyecto…»* y
sustitúyelo por el contenido del **ANEXO 4**.

### 19. Anexo A — eliminarlo

Elimina el **Anexo A completo** (secciones A.1 a A.5) del informe. El propio documento lo define como
«documento de trabajo interno del equipo» que «puede retirarse de la versión final». Contiene además cuatro
datos que ya no corresponden a lo ejecutado: siete categorías sugeridas y más de 7 500 registros teóricos
(A.1), una pausa de entre dos y cuatro segundos (A.3), un esquema de dieciséis columnas con precio anterior,
descuento, marca, condición y envío gratuito que no existen en el dataset final (A.4) y un plan de
contingencia redactado en futuro cuando una de sus alternativas ya se aplicó (A.5).

Su contenido útil queda recogido en las secciones 6 y 7 tras estas correcciones. Conserva las REFERENCIAS,
que van después del anexo.

### 20. Revisión final de coherencia

Recorre el documento completo y comprueba que **todas** las cifras coincidan con estas, corrigiendo
cualquier valor distinto:

| Dato | Valor correcto |
| --- | --- |
| Categorías recorridas | 5 |
| Páginas recorridas | 95 de 100 posibles |
| Registros crudos | 5 080 |
| Registros del dataset final | 4 412 |
| Columnas del dataset final | 14 |
| Máximo de nulos por columna | 1,25 % |
| Pausa entre peticiones | 10 segundos |
| Duración de la extracción | 29 minutos (13/09/2026, 19:54–20:22) |
| Técnica | Selenium (navegación) + BeautifulSoup (análisis) + pandas |

Verifica también que no quede ninguna frase del tipo «Sección a cargo de la Parte N» ni ningún espacio en
blanco con guiones bajos de la plantilla.

---

## ANEXO 1 — Texto de la sección 4, DATASET PRELIMINAR

### 4.1 Descripción de la muestra

Se procesaron 5 080 observaciones crudas de Mercado Libre Perú, obtenidas entre las 19:54:05 y las 20:22:54
del 13 de setiembre de 2026, según las marcas temporales del scraper. El archivo no registra zona horaria.
Las búsquedas de origen fueron celulares, laptops, televisores, refrigeradoras y audífonos. El dataset final
contiene 4 412 ofertas con identificadores únicos y 14 columnas.

La unidad de observación es la oferta identificada en la URL, conservando su última aparición en el archivo.
La muestra procede de páginas de resultados y no es aleatoria ni representativa de todo el mercado peruano.
La categoría es la búsqueda de origen y puede incluir accesorios o productos relacionados. Los precios
describen ofertas, no transacciones realizadas.

### 4.2 Preparación y control de calidad

Se normalizaron espacios, se transformaron los precios a formato numérico, se estandarizó la moneda a PEN y
se convirtieron las fechas a tipo datetime. Se extrajeron el número de cuotas y el monto por cuota de los
textos observados, manteniendo los nulos cuando la información no estaba disponible.

El identificador extraído originalmente por el scraper se conserva como `id_extraido`. Para `id_publicacion`
se tomó el parámetro `wid` de la URL o, cuando estaba ausente, el código de una ruta directa sin `/p/`. Se
separaron 56 filas sin campos esenciales válidos y se retiraron 605 observaciones repetidas, conservando la
última por fecha y orden de archivo. Adicionalmente se excluyeron 7 ofertas con precios cuestionados,
identificadas por código y precio: Xiaomi Redmi Note 13 Pro+ a S/ 1 250 000, refrigerador Daewoo a
S/ 999 999, televisor Daewoo a S/ 99 999, refrigeradora Indurama a S/ 2, dos televisores Daewoo a S/ 10 y
Lenovo V15 a S/ 29 000. Son exclusiones puntuales acordadas para esta muestra, no límites generales
aplicables a todos los productos. Estos importes ya estaban en el CSV crudo; no fueron generados por la
conversión numérica. La exclusión es una decisión de calidad para el análisis, sin verificar el precio real
ni imputar reemplazos. Los registros separados se guardaron como evidencia para revisión.

No se encontraron duplicados de fila completa en el CSV original; las repeticiones se detectaron por
identificador de oferta, aunque sus posiciones, fechas o enlaces de seguimiento fueran diferentes.

Se excluyeron `precio_anterior_texto` y `vendedor_texto` del dataset principal debido a sus ausencias
originales de 40,08 % y 64,07 %, respectivamente. Ambas columnas permanecen en el CSV crudo. No se imputaron
precios anteriores, vendedores ni descuentos. La falta de un precio anterior no permite concluir que el
descuento sea cero.

### 4.3 Variables y cobertura

Las variables comerciales incluyen título, categoría, moneda, precio actual, número de cuotas, monto de la
cuota y el texto de financiamiento. Los identificadores, la página, la posición, las URL y la fecha
proporcionan trazabilidad. El dataset incluye variables numéricas y categóricas, supera los 1 000 registros y
los seis atributos mínimos, y ninguna columna supera el 10 % de valores nulos. La tabla presenta los tipos
en pandas antes de exportar; el formato CSV no conserva los tipos y deben declararse al volver a cargarlo.

| Variable | Tipo en pandas | Nulos | % de nulos | Valores distintos |
| --- | --- | --- | --- | --- |
| id_publicacion | string | 0 | 0,00 | 4 412 |
| id_extraido | string | 0 | 0,00 | 4 412 |
| categoria | string | 0 | 0,00 | 5 |
| titulo | string | 0 | 0,00 | 4 181 |
| moneda | string | 0 | 0,00 | 1 |
| precio_actual | Float64 | 0 | 0,00 | 1 952 |
| numero_cuotas | Int64 | 55 | 1,25 | 2 |
| monto_cuota | Float64 | 55 | 1,25 | 2 225 |
| cuotas_texto | string | 55 | 1,25 | 2 335 |
| pagina | Int64 | 0 | 0,00 | 20 |
| posicion_pagina | Int64 | 0 | 0,00 | 60 |
| url_publicacion | string | 0 | 0,00 | 4 412 |
| url_fuente | string | 0 | 0,00 | 95 |
| fecha_extraccion | datetime64 | 0 | 0,00 | 99 |

### 4.4 Estadísticos descriptivos

Todos los precios se expresan en soles (PEN). Tras las exclusiones puntuales descritas, se conservaron los
demás valores extremos porque su magnitud por sí sola no prueba un error. No se ha verificado el precio real
de cada publicación ni se afirma que todos los precios restantes sean correctos. Las diferencias entre
categorías no equivalen a diferencias entre productos comparables.

| Categoría | Registros | Precio mínimo | Precio mediano | Precio promedio | Precio máximo |
| --- | --- | --- | --- | --- | --- |
| audifonos | 959 | 16,90 | 138,00 | 376,08 | 8 959,00 |
| celulares | 937 | 38,61 | 1 632,00 | 2 075,04 | 9 498,00 |
| laptops | 928 | 459,00 | 4 898,50 | 5 807,42 | 24 665,00 |
| refrigeradoras | 646 | 52,00 | 1 314,00 | 1 805,08 | 20 741,00 |
| televisores | 942 | 25,00 | 1 289,50 | 1 907,65 | 59 999,00 |

### 4.5 Vista previa

Se muestra una selección de columnas de las primeras cinco filas. El CSV contiene la totalidad de los
atributos descritos.

| id_publicacion | categoria | titulo | precio_actual | numero_cuotas |
| --- | --- | --- | --- | --- |
| MPE636405849 | celulares | Apple iPhone 17 Pro Max (256 GB) - Color plata | 4 849,00 | 6 |
| MPE1067071458 | celulares | Celular Samsung Galaxy S26 Ultra 512gb | 4 129,00 | 6 |
| MPE1087974300 | celulares | Apple iPhone 17 Pro Max (256 GB) - Azul profundo | 4 849,00 | 6 |
| MPE1097141956 | celulares | Apple iPhone 17 Pro (256 GB) - Azul profundo | 4 479,00 | 6 |
| MPE724292960 | celulares | Samsung Galaxy A56 5G Dual Sim 256GB 12GB Negro 6.7" | 1 517,00 | 6 |

### 4.6 Limitaciones

No se extrajeron calificación, número de opiniones, condición, marca ni envío gratuito. Por tanto, estos
datos no permiten analizar esas características ni la reputación del vendedor. Tampoco permiten calcular
descuentos de manera completa. La deduplicación conserva una sola observación por oferta y no constituye una
serie histórica. La identidad de cada oferta se recuperó de las URL guardadas y no se verificó mediante
consultas adicionales al sitio.

---

## ANEXO 2 — Texto de la sección 5, ALCANCE

**Qué se desarrolla en esta primera entrega**

- **Adquisición.** Extracción automatizada de publicaciones de cinco categorías de Mercado Libre Perú
  —celulares, laptops, televisores, refrigeradoras y audífonos— desde las páginas de resultados del
  subdominio de listados, con un recorrido de hasta veinte páginas por categoría.
- **Limpieza y control de calidad.** Normalización de textos, conversión de precios y fechas a tipos
  numéricos y temporales, recuperación del identificador de oferta, separación de registros incompletos,
  deduplicación por oferta y documentación de cada exclusión con su evidencia.
- **Documentación.** Diccionario de datos con las catorce variables del archivo final, descripción de la
  muestra preliminar y un notebook reproducible que permite repetir todo el proceso.
- **Entregables.** Dataset preliminar en CSV con codificación UTF-8, diccionario de datos e informe.

**Qué queda fuera**

- **Análisis exploratorio profundo y modelado.** No se realizan pruebas estadísticas, segmentación ni
  modelos predictivos: corresponden a las siguientes partes del proyecto.
- **Seguimiento histórico de precios.** El dataset es una fotografía del 13 de setiembre de 2026, no una
  serie temporal, y no permite medir variaciones de precio en el tiempo.
- **Reseñas individuales y datos del vendedor.** No se extraen opiniones de compradores ni información de
  perfiles; las rutas de perfil están además restringidas por el archivo robots.txt del sitio.
- **Atributos ausentes de las páginas de resultados.** Calificación, número de opiniones, condición, marca y
  envío gratuito no figuran en las tarjetas del listado y quedan fuera del dataset; el precio anterior y el
  tipo de vendedor se capturaron, pero superan el 10 % de valores nulos y permanecen solo en el CSV crudo.
- **Representatividad del mercado.** La muestra proviene de cinco búsquedas y no es aleatoria: describe las
  ofertas observadas, no el universo del comercio electrónico peruano ni transacciones efectivas.
- **Redistribución.** El dataset es de uso académico dentro del curso DS3021 y no se publica con fines
  comerciales.

---

## ANEXO 3 — Texto de la sección 7, ESTRATEGIA

**Herramientas**

El proyecto se desarrolla en Python 3.11 con Selenium para la navegación, BeautifulSoup para el análisis del
HTML y pandas para la consolidación, la limpieza y la exportación. El trabajo se versiona en un repositorio
Git y se ejecuta desde un único notebook, `ACD_Proyecto_Parte_I.ipynb`, dividido en dos secciones:
Extracción y Limpieza.

**Procedimiento de obtención**

1. **Verificación de políticas.** Antes de extraer se descargan los archivos robots.txt del dominio
   principal y del subdominio de listados, se interpretan con el módulo `urllib.robotparser` y se comprueba,
   para el User-Agent declarado, que cada dirección por visitar esté permitida. Los archivos quedan
   guardados como evidencia fechada. Si alguna ruta estuviera prohibida, el proceso se detiene.
2. **Recorrido por categorías.** Cinco categorías de rubros distintos, elegidas para dar al dataset variedad
   de precios y de marcas.
3. **Control de la paginación.** El avance entre páginas usa el botón `Siguiente` del sitio, que genera las
   URL con el sufijo `_Desde_N`, con incrementos de 48 resultados. El bucle se detiene cuando la página no
   devuelve tarjetas o cuando repite el contenido anterior, en lugar de fijar un número rígido de páginas:
   por eso el recorrido efectivo fue de 95 páginas y no de 100.
4. **Cortesía con el servidor.** Pausa de diez segundos entre peticiones mediante `time.sleep()`, User-Agent
   realista e identificable y ninguna técnica de evasión de bloqueos.
5. **Robustez.** Cada página se procesa dentro de un bloque `try-except`, de modo que una falla puntual no
   cancela la ejecución, y los resultados se escriben de forma incremental en el CSV: una interrupción no
   pierde lo ya extraído.
6. **Limpieza y verificación.** La segunda sección del notebook convierte el CSV crudo en el dataset final y
   comprueba automáticamente los requisitos del enunciado: mínimo de registros y de atributos, unicidad del
   identificador y máximo de 10 % de valores nulos por columna. Si alguno deja de cumplirse, la ejecución
   falla en lugar de exportar en silencio.

**Planes de contingencia**

- **Cambios en el maquetado del sitio.** Los nombres de las clases CSS están aislados en dos funciones del
  notebook: una actualización del sitio se resuelve modificando solo ese bloque.
- **Contenido servido con JavaScript.** Previsto inicialmente con `requests`, el sitio entregó páginas
  incompletas; se aplicó la contingencia prevista y la navegación pasó a Selenium, conservando BeautifulSoup
  para el análisis del HTML.
- **Limitación de peticiones o verificación de navegador.** Ampliar la pausa entre solicitudes y fraccionar
  la ejecución en varias sesiones. Cuando el sitio solicita una verificación, el notebook la delega a la
  persona que ejecuta y reanuda el recorrido.
- **Inviabilidad de la extracción por HTML.** Uso de la API pública de consulta de la plataforma como fuente
  alternativa, documentando el cambio.
- **Fuente de reemplazo.** Falabella Perú queda registrada como alternativa, con la advertencia de que exige
  un navegador automatizado y un tiempo de ejecución mayor.

---

## ANEXO 4 — Texto de la sección 8, VIABILIDAD

**Tiempo**

La extracción completa —cinco categorías, 95 páginas y 5 080 registros crudos— se ejecutó el 13 de setiembre
de 2026 entre las 19:54:05 y las 20:22:54, según las marcas temporales del propio scraper: veintinueve
minutos, de los cuales la mayor parte corresponde a las pausas deliberadas entre peticiones. La limpieza
completa se ejecuta en segundos sobre el CSV ya obtenido, de modo que cualquier ajuste posterior no obliga a
repetir la extracción. Frente a la fecha de entrega del 25 de setiembre de 2026, el dataset quedó disponible
con doce días de holgura, suficientes para la documentación y para repetir la captura si fuera necesario.

Obtener un volumen equivalente de forma manual —transcribir más de cinco mil publicaciones— habría exigido
decenas de horas y un riesgo alto de error de transcripción, lo que confirma la pertinencia de la
adquisición automatizada.

**Recursos**

Una computadora personal con Windows 11, Google Chrome y conexión doméstica a internet es suficiente: no se
requieren servidores, servicios de pago ni credenciales. El almacenamiento total del proyecto, incluidos los
archivos de evidencia, es de pocos megabytes. El trabajo se coordina mediante un repositorio Git compartido
por los cinco integrantes.

**Herramientas**

Todas las librerías empleadas son de código abierto y gratuitas —Selenium, BeautifulSoup, requests y
pandas—, están declaradas en un archivo de requisitos y se instalan con una sola orden. El proceso completo
se reproduce ejecutando un notebook, lo que permite a un tercero repetir la extracción y la limpieza
siguiendo únicamente las instrucciones del documento.

**Riesgos y su control**

| Riesgo | Control adoptado |
| --- | --- |
| Cambio del maquetado del sitio | Selectores aislados en un solo bloque del notebook. |
| Bloqueo o limitación de peticiones | Pausa de diez segundos, User-Agent identificable y ejecución fraccionable. |
| Interrupción de la ejecución | Guardado incremental en el CSV tras cada página. |
| Datos de calidad insuficiente | Verificaciones automáticas y evidencia documentada de cada exclusión. |
| Pérdida de trabajo o descoordinación | Repositorio Git con el aporte de cada integrante registrado. |

---

## ANEXO 5 — Tabla de la sección 1, IDENTIFICACIÓN

| Parte | Integrante | Responsabilidades | Entregable verificable | Estado |
| --- | --- | --- | --- | --- |
| Parte 1 | Yared Riveros Rodríguez | Selección y justificación de la fuente de datos; redacción de las secciones Contexto, Objetivos y Fuentes de datos. | Secciones 2, 3 y 6 del informe. | Completado |
| Parte 2 | Franco Nicolás Roque Castillo | Desarrollo del script de web scraping (paginación, cabeceras, pausas, manejo de errores y guardado incremental) y extracción del dataset crudo. | Sección 1 del notebook; CSV crudo con 5 080 registros. | Completado |
| Parte 3 | Mauricio Terán Taica | Limpieza y control de calidad del dataset; redacción de la sección Dataset preliminar. | Sección 2 del notebook; dataset limpio con 4 412 registros; tablas de control de calidad; sección 4 del informe. | Completado |
| Parte 4 | Josué Luna Rocha | Elaboración del diccionario de datos en el formato Word solicitado. | Diccionario de datos con las 14 variables. | Completado |
| Parte 5 | Álvaro Mauricio García Hurtado | Redacción de Identificación, Alcance, Estrategia y Viabilidad; ensamblaje del notebook y del informe final. | Secciones 1, 5, 7 y 8; notebook único; informe en PDF. | Completado |
