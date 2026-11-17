# Guion de la presentación — Parte II (DS3021)

**Tiempo:** 15 min de exposición + 5 de preguntas (Zoom). El guion suma unos **14 min** para dejar margen.
**Todos deben hablar**: si alguien no participa, no se le evalúa. Este texto también está en las notas del orador
de cada diapositiva (`scripts/presentacion/generar_presentacion.js` lo copia desde aquí).

| Integrante | Diapositivas | Tema | Tiempo |
| --- | --- | --- | --- |
| Yared | 1–5 | Pregunta, problema, contexto y objetivos | 2:00 |
| Franco | 6–7 | Pipeline e ingesta | 1:45 |
| Mauricio | 8–10 | Faltantes, atípicos e integración | 2:30 |
| Josué | 11–13 | Variables derivadas y gamas | 2:30 |
| Alvaro | 14–18 | Resultados, pruebas e insights | 3:00 |
| Franco | 19 | Demo en vivo | 1:45 |
| Alvaro | 20 | Conclusiones y cierre | 0:30 |

Cómo leerlo: 👉 es lo que hay que señalar en pantalla; el texto entre comillas es lo que se dice (con sus palabras,
no de memoria); 📖 explica un término por si lo preguntan. La rúbrica penaliza leer la diapositiva.

## Yared — diapositivas 1 a 5

### 1 · Portada (≈ 0:15)

"Buenos días, somos el grupo de Mercado Libre. Nuestra pregunta es concreta: **¿cuánto cuesta equipar un home
office en el Perú?** En la Parte I juntamos los precios con web scraping; en esta Parte II los limpiamos, los
analizamos y lo automatizamos todo."

### 2 · Agenda (≈ 0:10)

👉 Recorre la lista de arriba abajo, sin leerla.

"Vamos en el mismo orden que el pipeline: el problema, cómo limpiamos los datos, las variables que construimos, los
resultados y una demo en vivo."

### 3 · Una sola cifra no basta (≈ 0:35)

👉 Señala "S/ 6 335" y luego "×3,4".

"La **Ley 31572 de Teletrabajo** obliga al empleador a darle los equipos al trabajador o a compensarle los suyos
**según su valor de mercado**, pero nadie publica ese valor. En la Parte I dimos **una sola cifra: S/ 6 335**. Al
limpiar los datos vimos que eso esconde mucho: equiparse con lo mejor cuesta **3,4 veces** más que con lo básico.
Por eso la pregunta ahora es cuánto cuesta **según el nivel** de equipamiento."

### 4 · Mirar los datos cambió el problema (≈ 0:35)

👉 Recorre las cuatro tarjetas.

"Cuatro hallazgos cambiaron el enfoque. **Uno**: hay que contar ofertas, no modelos de producto; así las dos
capturas comparten 767 ofertas y no 258. **Dos**: buscar 'teclado' también trae kits y accesorios. **Tres**: los
datos que faltan no faltan al azar. **Cuatro**: los precios casi no cambian en dos días."

📖 *MCAR: falta completamente al azar. Que ninguna columna lo sea significa que borrar filas sesgaría los datos.*

### 5 · Objetivos (≈ 0:25)

👉 Señala la columna "Resultado".

"Con eso ajustamos los objetivos: ya no una cifra, sino **un costo por perfil con su rango**. Cada objetivo tiene
un resultado medible, en la columna derecha. Franco explica cómo está armado el pipeline."

## Franco — diapositivas 6 y 7

### 6 · Pipeline (≈ 0:55)

👉 Recorre las cinco etapas de izquierda a derecha y luego las cuatro tarjetas de abajo.

"Seguimos el ciclo de vida de datos del curso. La **generación** fue el scraping de la Parte I. Después vienen la
**ingestión**, la **transformación** —faltantes, atípicos, integración y variables—, el **almacenamiento** en una
base SQLite y el **serving**, que es el análisis. Cada etapa es un notebook, y **un solo comando,
`python pipeline.py`**, los corre en orden. Si una regla falla, por ejemplo si se pierde una fila sin explicación,
el pipeline **se detiene y dice cuál**."

📖 *SQLite: base de datos en un solo archivo, sin instalar servidor (en clase se usó SQL Server). SHA-256: la
"huella digital" de cada archivo; si dos ejecuciones dan la misma, los datos son idénticos. Balance: filas que entran
= filas que salen + excluidas.*

### 7 · De 3 680 registros a 2 714 ofertas (≈ 0:50)

👉 Señala las barras de izquierda a derecha y luego −787, −178 y −1.

"Partimos de **3 680 registros**. Convertimos los textos a números, como 'S/ 2.199' o '18 cuotas', y corregimos un
error de la Parte I: '+100 vendidos' son ventas, no opiniones. Quitamos **787 repeticiones** de la misma oferta y
**178 publicaciones que no son el componente**, como 139 kits de teclado y mouse. Quedan **2 714 ofertas**, y cada
exclusión queda guardada con su motivo. Mauricio sigue con la calidad de los datos."

📖 *`wid`: el código de la oferta concreta (producto + vendedor) que aparece en la URL. Expresión regular: un patrón
de texto para extraer, por ejemplo, el monto de "18 cuotas de S/ 122,17".*

## Mauricio — diapositivas 8 a 10

### 8 · Valores faltantes (≈ 0:55)

👉 Señala el mapa de calor y luego las tres tarjetas.

"Antes de rellenar o borrar, hay que saber **por qué falta** un dato. Con la prueba chi-cuadrado vimos que en las
seis columnas faltar depende del componente: **ninguna falta al azar**. Hay dos casos. El **precio anterior** falta
porque **no hay promoción**: ponemos descuento 0 %. Las **reseñas** faltan más en los productos caros: **no las
inventamos**, porque si las rellenáramos con la mediana le daríamos a un producto caro la nota de uno barato."

📖 *MNAR estructural: el dato no existe (no hay promoción). MAR: su ausencia se explica con otra variable que sí
vemos (componente, precio). p < 0,001: la relación casi seguro no es casualidad.*

### 9 · Atípicos (≈ 0:45)

👉 Señala 36, 29 y 1.

"Un atípico es un precio muy lejos del resto **de su componente**: una silla de S/ 3 000 es rara, una laptop no.
Encontramos **36** mirando solo el precio y **29** combinando varias variables. Revisamos los títulos y casi todos
son **productos reales**, como sillas Steelcase: se quedan, marcados. Solo eliminamos **uno**, un error claro: una
laptop básica de 8 GB a **S/ 29 000**."

📖 *IQR y z-score: reglas para decidir qué tan lejos es "demasiado lejos". Se aplican al logaritmo del precio porque
los precios van de S/ 8 a más de S/ 45 000. K-Means agrupa productos parecidos; Mahalanobis mide la distancia al
centro considerando varias variables a la vez.*

### 10 · Integración de las dos capturas (≈ 0:50)

👉 Señala las barras 258 frente a 767 y luego "75 %".

"Teníamos dos capturas: la del 13 y la del 15 de septiembre. Uniéndolas por código de catálogo, como en la Parte I,
coinciden **258 ofertas**; uniéndolas por **oferta**, **767: el triple**. A cada oferta le **agregamos su precio
del 13**, sin sumar filas, y así medimos que el **75 % no cambió de precio**. También retiramos la columna búsqueda,
que repetía la información del componente. Josué sigue con las variables."

📖 *V de Cramér 0,995: búsqueda y componente están casi perfectamente asociadas, así que una sobra.*

## Josué — diapositivas 11 a 13

### 11 · 24 variables derivadas (≈ 0:45)

👉 Señala las cuatro transformaciones de arriba y luego las cuatro familias.

"Primero, cuatro transformaciones: el **logaritmo** para que los precios altos no dominen; el **precio relativo**,
que compara un mouse con una laptop en la misma escala; **indicadores 0/1** para el tipo de envío; y las **gamas**.
Luego creamos **24 variables** en cuatro familias. Por ejemplo, del título sacamos la **RAM** y las **pulgadas**,
que encontramos en cerca del 90 % de laptops y monitores."

📖 *Precio relativo (z): cuántas desviaciones estándar está un precio sobre o bajo lo típico de su componente.
get_dummies: convierte una categoría en columnas de 0 y 1.*

### 12 · ¿Por qué terciles y no K-Means? (≈ 1:05)

👉 Señala en el gráfico las barras de sillas: terciles parejos frente a K-Means con solo 19 en gama alta.

"Esta es la decisión que más nos pueden preguntar. Para las gamas probamos dos métodos del curso: **dividir el precio
en tres partes iguales** (terciles) o **agrupar con K-Means**. K-Means separa algo mejor los grupos, pero los deja
muy desbalanceados: solo **19 sillas** en gama alta. Elegimos terciles por tres razones: 'gama alta' significa lo
mismo en todos los componentes; cada gama tiene más de 100 ofertas, así que la mediana es estable; y se le explica
fácil a Recursos Humanos."

📖 *Silueta (0,57 frente a 0,49): mide qué tan separados están los grupos; K-Means la maximiza por diseño. qcut:
la función de pandas que corta en grupos del mismo tamaño.*

### 13 · Validación de gamas (≈ 0:40)

👉 Señala los tres gráficos, uno por uno.

"Comprobamos que las gamas no son solo precio. Las laptops de gama alta tienen **32 GB de RAM** frente a 16; los
monitores económicos son más pequeños; y las sillas ergonómicas pasan del **34 % al 57 %**. Lo inalámbrico no
cambia entre gamas: no es lo que encarece un periférico. Con las gamas listas, Alvaro presenta los resultados."

## Alvaro — diapositivas 14 a 18

### 14 · Resultado principal (≈ 0:45)

👉 Señala las tres cifras grandes y luego la barra de participación.

"Esta es la respuesta: un home office completo cuesta **S/ 3 644** en el perfil económico, **S/ 6 332** en el medio
y **S/ 12 323** en el alto. Cada perfil suma el precio típico de cada componente en esa gama. El rango de abajo es
lo que paga la mayoría, sin el 25 % más barato ni el 25 % más caro. Y la barra muestra que la **laptop es entre el
67 y el 77 %** del costo."

### 15 · La RAM marca escalones (≈ 0:25)

👉 Señala las tres barras.

"Como la laptop decide el presupuesto, la miramos por dentro: unos **S/ 2 900 con 8 GB, S/ 4 500 con 16 y S/ 7 800
con 32**. Para oficina, **16 GB basta** y es lo más ofrecido."

### 16 · Un descuento no es un buen precio (≈ 0:45)

👉 Señala las barras rojas (más caras con promoción) y luego "98 %".

"¿Una oferta con descuento es más barata? **No necesariamente**: en laptops, mouse y audífonos las ofertas con
descuento **cuestan más** que las que no tienen promoción; solo en sillas son más baratas. Hay que comparar el
**precio final**, no el porcentaje. En cambio, **las cuotas no encarecen**: el 98 % es sin interés; un perfil medio
en 12 cuotas sale **S/ 528 al mes**."

📖 *Mann-Whitney: compara dos grupos usando el orden de los precios, sin suponer que siguen una curva normal.
n. s.: diferencia no significativa (p ≥ 0,05).*

### 17 · Lo "gamer" y lo más vendido (≈ 0:40)

👉 Señala las barras de laptop y mouse y luego las dos cifras ρ.

"Lo **'gamer'** solo cuesta más, de forma comprobada, en **laptops y mouse**: para oficina no conviene pagarlo. Y
**lo más vendido no es lo mejor valorado**: lo que más se vende es más barato que su componente, y lo mejor calificado
es más caro. Ojo: solo un tercio de las ofertas muestra reseñas."

📖 *ρ (rho de Spearman) mide si dos variables suben o bajan juntas, de −1 a 1: −0,08 es casi nada; 0,24 es débil
pero real.*

### 18 · Recomendaciones (≈ 0:25)

👉 No leas las seis tarjetas; menciona tres.

"En recomendaciones: a **Recursos Humanos**, compensar **por perfil** y con la fecha de los precios. Al
**trabajador**: decidir primero la laptop y comparar el precio final, no el descuento. Las ocho recomendaciones, con
su cifra, están en el informe. Franco hace la demo."

## Franco — diapositiva 19

### 19 · Demo en vivo (≈ 1:45)

👉 Compartir la terminal, ya en la carpeta del repositorio y con el entorno instalado.

"Ahora lo vemos funcionar." **Paso 1:** ejecutar `python pipeline.py` y comentar cada etapa mientras aparece su OK
(en una laptop normal tarda menos de un minuto). **Paso 2:** abrir el notebook 05 y mostrar que lee la base SQLite
con una consulta SQL, no los CSV; bajar hasta el gráfico de costo por perfil. **Paso 3:** abrir
`data/final/manifiesto.json` y ejecutar `git status data/final`: "los archivos no cambiaron, el resultado es
reproducible". **Plan B**, si algo falla: abrir los notebooks en GitHub con sus salidas guardadas. "Alvaro cierra."

## Alvaro — diapositiva 20

### 20 · Conclusiones y limitaciones (≈ 0:30)

"Para cerrar: un home office cuesta **S/ 3 644, S/ 6 332 o S/ 12 323** según el perfil, y la laptop es dos tercios
o más. Limpiar con criterio **cambió el resultado**. Y el descuento y lo gamer **no son señales de buen precio**.
Como limitaciones: son capturas de un solo día, en el orden que muestra el sitio y no al azar, y con pocas reseñas.
Muchas gracias; quedamos atentos a sus preguntas."

## Anexos — solo para preguntas

### 21 · Pruebas estadísticas (respaldo)

No se presenta. Si preguntan por una prueba: **chi-cuadrado** compara dos variables categóricas (¿faltar depende del
componente?); **Mann-Whitney** compara dos grupos por el orden de sus valores, sin suponer normalidad; **Spearman**
mide si dos variables suben juntas usando rangos. Con α = 0,05: si p < 0,05, la diferencia no es casual.
Responde quien presentó esa parte (Mauricio: chi-cuadrado; Alvaro: Mann-Whitney y Spearman).

### 22 · Dataset final (respaldo)

No se presenta. Si preguntan por el dataset o el diccionario: 2 714 ofertas × 41 variables; las columnas con más de
10 % de nulos lo son por diseño (por ejemplo, las pulgadas solo aplican a monitores). Responde Josué.
