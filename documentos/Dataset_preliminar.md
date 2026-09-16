# 4. Dataset preliminar

## 4.1 Descripción de la muestra
Se procesaron 5,080 observaciones crudas de Mercado Libre Perú, obtenidas entre 2026-09-13 19:54:05 y 2026-09-13 20:22:54, según las marcas temporales del scraper. El archivo no registra zona horaria. Las búsquedas de origen fueron celulares, laptops, televisores, refrigeradoras y audifonos. El dataset final contiene 4,412 ofertas con identificadores únicos y 14 columnas.

La unidad de observación es la oferta identificada en la URL, conservando su última aparición en el archivo. La muestra procede de páginas de resultados y no es aleatoria ni representativa de todo el mercado peruano. La categoría es la búsqueda de origen y puede incluir accesorios o productos relacionados. Los precios describen ofertas, no transacciones realizadas.

## 4.2 Preparación y control de calidad
Se normalizaron espacios, se transformaron precios a formato numérico, se estandarizó la moneda a PEN y se convirtieron las fechas a datetime. Se extrajeron el número de cuotas y el monto por cuota de los textos observados, manteniendo los nulos cuando la información no estaba disponible.

El identificador extraído originalmente por el scraper se conserva como id_extraido. Para id_publicacion se tomó el parámetro wid de la URL o, cuando estaba ausente, el código de una ruta directa sin /p/. Se separaron 56 filas sin campos esenciales válidos y se retiraron 605 observaciones repetidas, conservando la última por fecha y orden de archivo. Adicionalmente se excluyeron 7 ofertas con precios cuestionados, identificadas por código y precio: Xiaomi Redmi Note 13 Pro+ a S/ 1.250.000, refrigerador Daewoo a S/ 999.999, televisor Daewoo a S/ 99.999, refrigeradora Indurama a S/ 2, dos televisores Daewoo a S/ 10 y Lenovo V15 a S/ 29.000. Son exclusiones puntuales acordadas para esta muestra, no límites generales aplicables a todos los productos. Estos importes ya estaban en el CSV crudo; no fueron generados por la conversión numérica. La exclusión es una decisión de calidad para el análisis, sin verificar el precio real ni imputar reemplazos. Los registros separados se guardaron como evidencia para revisión.

No se encontraron duplicados de fila completa en el CSV original (0); las repeticiones se detectaron por identificador de oferta, aunque sus posiciones, fechas o enlaces de seguimiento fueran diferentes.

Se excluyeron precio_anterior_texto y vendedor_texto del dataset principal debido a sus ausencias originales de 40.08 % y 64.07 %, respectivamente. Ambas columnas permanecen en el CSV crudo. No se imputaron precios anteriores, vendedores ni descuentos. La falta de un precio anterior no permite concluir que el descuento sea cero.

## 4.3 Variables y cobertura
Las variables comerciales incluyen titulo, categoria, moneda, precio_actual, numero_cuotas, monto_cuota y cuotas_texto. Los identificadores, páginas, posiciones, URL y fecha proporcionan trazabilidad. El dataset incluye variables numéricas y categóricas, supera los 1000 registros y los seis atributos mínimos, y ninguna columna supera el 10 % de valores nulos. La tabla presenta los tipos en pandas antes de exportar; CSV no conserva tipos y deben declararse al volver a cargarlo.

| variable | tipo_pandas | nulos | porcentaje_nulos | valores_distintos |
| --- | --- | --- | --- | --- |
| id_publicacion | string | 0 | 0.0 | 4412 |
| id_extraido | string | 0 | 0.0 | 4412 |
| categoria | string | 0 | 0.0 | 5 |
| titulo | string | 0 | 0.0 | 4181 |
| moneda | string | 0 | 0.0 | 1 |
| precio_actual | Float64 | 0 | 0.0 | 1952 |
| numero_cuotas | Int64 | 55 | 1.25 | 2 |
| monto_cuota | Float64 | 55 | 1.25 | 2225 |
| cuotas_texto | string | 55 | 1.25 | 2335 |
| pagina | Int64 | 0 | 0.0 | 20 |
| posicion_pagina | Int64 | 0 | 0.0 | 60 |
| url_publicacion | string | 0 | 0.0 | 4412 |
| url_fuente | string | 0 | 0.0 | 95 |
| fecha_extraccion | datetime64[ns] | 0 | 0.0 | 99 |

## 4.4 Estadísticos descriptivos
Todos los precios se expresan en soles (PEN). Tras las exclusiones puntuales descritas, se conservaron los demás valores extremos porque su magnitud por sí sola no prueba un error. Las estadísticas siguientes excluyen los siete casos documentados en precios_excluidos.csv. No se ha verificado el precio real de cada publicación ni se afirma que todos los precios restantes sean correctos. Las diferencias entre categorías no equivalen a diferencias entre productos comparables.

| categoria | registros | precio_minimo | precio_mediano | precio_promedio | precio_maximo |
| --- | --- | --- | --- | --- | --- |
| audifonos | 959 | 16.9 | 138.0 | 376.08 | 8959.0 |
| celulares | 937 | 38.61 | 1632.0 | 2075.04 | 9498.0 |
| laptops | 928 | 459.0 | 4898.5 | 5807.42 | 24665.0 |
| refrigeradoras | 646 | 52.0 | 1314.0 | 1805.08 | 20741.0 |
| televisores | 942 | 25.0 | 1289.5 | 1907.65 | 59999.0 |

## 4.5 Vista previa
Se muestra una selección de columnas de las primeras cinco filas. El CSV contiene la totalidad de los atributos descritos.

| id_publicacion | categoria | titulo | precio_actual | numero_cuotas |
| --- | --- | --- | --- | --- |
| MPE636405849 | celulares | Apple iPhone 17 Pro Max (256 GB) - Color plata | 4849.0 | 6 |
| MPE1067071458 | celulares | Celular Samsung Galaxy S26 Ultra 512gb | 4129.0 | 6 |
| MPE1087974300 | celulares | Apple iPhone 17 Pro Max (256 GB) - Azul profundo | 4849.0 | 6 |
| MPE1097141956 | celulares | Apple iPhone 17 Pro (256 GB) - Azul profundo | 4479.0 | 6 |
| MPE724292960 | celulares | Samsung Galaxy A56 5G Dual Sim 256GB 12GB Negro 6.7'' | 1517.0 | 6 |

## 4.6 Limitaciones
No se extrajeron calificación, número de opiniones, condición, marca ni envío gratuito. Por tanto, estos datos no permiten analizar esas características ni la reputación del vendedor. Tampoco permiten calcular descuentos de manera completa. La deduplicación conserva una sola observación por oferta y no constituye una serie histórica. La identidad se recuperó de las URL guardadas y no se verificó mediante consultas adicionales al sitio.
