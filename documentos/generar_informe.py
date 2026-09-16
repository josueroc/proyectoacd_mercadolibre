# -*- coding: utf-8 -*-
"""Genera el informe corregido de la Parte I en .docx."""
import pathlib
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

SALIDA = pathlib.Path(r"C:\Users\yared\Documents\ACD\Proyecto\proyectoacd_mercadolibre\documentos\Informe_Parte_I_DS3021_corregido.docx")

doc = Document()

# ---------------------------------------------------------------- estilos
normal = doc.styles['Normal']
normal.font.name = 'Arial'
normal.font.size = Pt(11)
normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
pf = normal.paragraph_format
pf.space_after = Pt(8)
pf.line_spacing = 1.15
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def forzar_arial(estilo):
    rpr = estilo.element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    for attr in ('asciiTheme', 'hAnsiTheme', 'cstheme', 'eastAsiaTheme'):
        if rfonts.get(qn('w:' + attr)) is not None:
            del rfonts.attrib[qn('w:' + attr)]
    for attr in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
        rfonts.set(qn('w:' + attr), 'Arial')

for nombre, tam in (('Heading 1', 13), ('Heading 2', 11.5), ('Heading 3', 11)):
    st = doc.styles[nombre]
    st.font.name = 'Arial'
    forzar_arial(st)
    st.font.size = Pt(tam)
    st.font.bold = True
    st.font.color.rgb = RGBColor(0, 0, 0)
    st.paragraph_format.space_before = Pt(14 if nombre == 'Heading 1' else 10)
    st.paragraph_format.space_after = Pt(6)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    st.paragraph_format.keep_with_next = True

for nombre in ('List Bullet', 'List Number'):
    st = doc.styles[nombre]
    st.font.name = 'Arial'
    forzar_arial(st)
    st.font.size = Pt(11)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

seccion = doc.sections[0]
seccion.top_margin = seccion.bottom_margin = Cm(2.5)
seccion.left_margin = seccion.right_margin = Cm(2.5)

# ---------------------------------------------------------------- utilidades
def p(texto='', estilo=None, alineacion=None, negrita=False, tam=None, cursiva=False):
    par = doc.add_paragraph(style=estilo)
    if texto:
        run = par.add_run(texto)
        run.bold = negrita
        run.italic = cursiva
        if tam:
            run.font.size = Pt(tam)
    if alineacion is not None:
        par.alignment = alineacion
    return par

def h(texto, nivel=1):
    return doc.add_heading(texto, level=nivel)

def vinetas(items):
    for item in items:
        doc.add_paragraph(item, style='List Bullet')

def numerada(items):
    """Lista numerada manual: evita que Word reinicie o continúe numeraciones ajenas."""
    for i, item in enumerate(items, start=1):
        par = doc.add_paragraph()
        par.paragraph_format.left_indent = Cm(0.75)
        par.paragraph_format.first_line_indent = Cm(-0.75)
        par.paragraph_format.space_after = Pt(4)
        par.add_run(f'{i}. ').bold = True
        par.add_run(item)

def sombrear(celda, color='D9D9D9'):
    tc = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), color)
    tc.append(shd)

def tabla(encabezados, filas, anchos, tam=9):
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    # Encabezado repetido en cada página.
    trPr = t.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))
    for celda, texto, ancho in zip(t.rows[0].cells, encabezados, anchos):
        celda.width = Cm(ancho)
        sombrear(celda)
        par = celda.paragraphs[0]
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.space_after = Pt(2)
        run = par.add_run(texto)
        run.bold = True
        run.font.size = Pt(tam)
    for fila in filas:
        celdas = t.add_row().cells
        for celda, texto, ancho in zip(celdas, fila, anchos):
            celda.width = Cm(ancho)
            par = celda.paragraphs[0]
            par.paragraph_format.space_after = Pt(2)
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = par.add_run(str(texto))
            run.font.size = Pt(tam)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t

def indice_automatico():
    par = doc.add_paragraph()
    fld = OxmlElement('w:fldSimple')
    fld.set(qn('w:instr'), r'TOC \o "1-1" \h \z \u')
    run_xml = OxmlElement('w:r')
    txt = OxmlElement('w:t')
    txt.text = 'Actualizar el índice: clic derecho sobre esta tabla y "Actualizar campos".'
    run_xml.append(txt)
    fld.append(run_xml)
    par._p.append(fld)

def pie_con_numero():
    pie = seccion.footer.paragraphs[0]
    pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = pie.add_run()
    for instr in ('begin', 'PAGE', 'end'):
        el = OxmlElement('w:fldChar') if instr != 'PAGE' else OxmlElement('w:instrText')
        if instr == 'PAGE':
            el.set(qn('xml:space'), 'preserve')
            el.text = ' PAGE '
        else:
            el.set(qn('w:fldCharType'), instr)
        run._r.append(el)
    run.font.size = Pt(9)
    run.font.name = 'Arial'

# ---------------------------------------------------------------- portada
for linea, negrita in (('UNIVERSIDAD DE INGENIERÍA Y TECNOLOGÍA', True),
                       ('FACULTAD DE COMPUTACIÓN', True),
                       ('CARRERA DE DATA SCIENCE', True)):
    p(linea, alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=negrita, tam=12)

p()
p()
p('PRIMER AVANCE DEL PROYECTO FINAL:', alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=True, tam=13)
p('ADQUISICIÓN DE DATOS DE PUBLICACIONES DE PRODUCTOS EN MERCADO LIBRE PERÚ MEDIANTE WEB SCRAPING',
  alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=True, tam=13)
p()
p()
p('CURSO:', alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=True, tam=12)
p('ANÁLISIS COMPUTACIONAL DE DATOS', alineacion=WD_ALIGN_PARAGRAPH.CENTER, tam=12)
p()
p('ESTUDIANTES:', alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=True, tam=12)
for nombre in ('Yared Riveros Rodríguez', 'Mauricio Terán Taica', 'Franco Nicolás Roque Castillo',
               'Josué Luna Rocha', 'Álvaro Mauricio García Hurtado'):
    p(nombre, alineacion=WD_ALIGN_PARAGRAPH.CENTER, tam=12)
p()
p()
p('LIMA – PERÚ', alineacion=WD_ALIGN_PARAGRAPH.CENTER, tam=12)
p('2026', alineacion=WD_ALIGN_PARAGRAPH.CENTER, tam=12)
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---------------------------------------------------------------- índice
p('ÍNDICE GENERAL', alineacion=WD_ALIGN_PARAGRAPH.CENTER, negrita=True, tam=13)
indice_automatico()
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---------------------------------------------------------------- 1
h('1. IDENTIFICACIÓN')
p('La distribución de responsabilidades se organizó de forma secuencial: cada integrante recibe como '
  'insumo el entregable del integrante anterior, ejecuta su tarea y produce el material que necesita la '
  'siguiente etapa. El cuadro siguiente resume esa distribución y el entregable con el que se verifica '
  'cada aporte.')
tabla(['Parte', 'Integrante', 'Responsabilidades', 'Entregable verificable', 'Estado'],
      [['Parte 1', 'Yared Riveros Rodríguez',
        'Selección y justificación de la fuente de datos; redacción de las secciones Contexto, Objetivos y '
        'Fuentes de datos.', 'Secciones 2, 3 y 6 del informe.', 'Completado'],
       ['Parte 2', 'Franco Nicolás Roque Castillo',
        'Desarrollo del script de web scraping (paginación, cabeceras, pausas, manejo de errores y guardado '
        'incremental) y extracción del dataset crudo.',
        'Sección 1 del notebook; CSV crudo con 5 080 registros.', 'Completado'],
       ['Parte 3', 'Mauricio Terán Taica',
        'Limpieza y control de calidad del dataset; redacción de la sección Dataset preliminar.',
        'Sección 2 del notebook; dataset limpio con 4 412 registros; tablas de control de calidad; '
        'sección 4 del informe.', 'Completado'],
       ['Parte 4', 'Josué Luna Rocha',
        'Elaboración del diccionario de datos en el formato Word solicitado.',
        'Diccionario de datos con las 14 variables.', 'Completado'],
       ['Parte 5', 'Álvaro Mauricio García Hurtado',
        'Redacción de Identificación, Alcance, Estrategia y Viabilidad; ensamblaje del notebook y del '
        'informe final.', 'Secciones 1, 5, 7 y 8; notebook único; informe en PDF.', 'Completado']],
      [1.5, 3.0, 4.6, 3.7, 2.2])
p('El trabajo se integra en un repositorio Git compartido, donde cada parte corresponde a archivos '
  'identificables y el historial de cambios registra el aporte de cada integrante.')

# ---------------------------------------------------------------- 2
h('2. CONTEXTO')
h('2.1 Descripción del problema', 2)
p('El comercio electrónico peruano dejó de ser un canal marginal para convertirse en un componente '
  'relevante de la economía nacional. De acuerdo con la Cámara Peruana de Comercio Electrónico (CAPECE), '
  'en 2024 el sector movilizó alrededor de US$ 15 600 millones, con un crecimiento de 21,2 % respecto del '
  'año anterior, y pasó de representar 2,4 % del PBI en 2019 a 5,5 % en 2024; ese mismo año, cerca de '
  '18,7 millones de peruanos —el 55 % de la población— realizaron al menos una compra en línea [1] [2]. '
  'Durante el primer semestre de 2025 las ventas crecieron 18 % en volumen y alcanzaron US$ 8 700 '
  'millones [3].')
p('Una parte sustancial de esa actividad se concentra en marketplaces, plataformas donde miles de '
  'vendedores independientes publican su oferta en un mismo espacio. En ese modelo, un mismo producto '
  'puede ofrecerse simultáneamente por decenas de vendedores con precios, descuentos, esquemas de cuotas '
  'y condiciones de envío distintas. El resultado es una marcada dispersión de precios y una asimetría de '
  'información: el comprador carece de una referencia objetiva para juzgar si el precio que observa es '
  'competitivo, y el pequeño vendedor no dispone de un mecanismo sencillo para comparar su oferta con la '
  'del resto del mercado.')
p('El problema se agrava porque no existe en el Perú una fuente pública que difunda, de manera '
  'estructurada y descargable, los precios y atributos de las publicaciones de los marketplaces. La '
  'información está disponible —es pública y accesible desde cualquier navegador—, pero se encuentra '
  'dispersa en miles de páginas HTML diseñadas para el consumo visual y no para el análisis. Convertir esa '
  'información en un conjunto de datos ordenado es, precisamente, el problema que aborda esta primera '
  'parte del proyecto.')

h('2.2 Impacto', 2)
vinetas([
    'Consumidores: sin una referencia de mercado, las decisiones de compra se toman sobre información '
    'parcial, lo que favorece sobreprecios y dificulta distinguir un descuento real de uno meramente '
    'nominal.',
    'Micro y pequeñas empresas: los vendedores que operan en marketplaces fijan sus precios por intuición '
    'o por observación manual de la competencia, un procedimiento lento y poco sistemático.',
    'Investigación y política pública: la ausencia de datos abiertos sobre precios en línea limita el '
    'estudio de la inflación digital, de la competencia entre vendedores y del comportamiento del '
    'consumidor peruano.',
])

h('2.3 Relevancia del análisis computacional de datos', 2)
p('El problema descrito no es abordable de manera manual: obtener incluso un millar de publicaciones '
  'exigiría revisar y transcribir decenas de páginas de resultados, con un alto costo de tiempo y un '
  'riesgo elevado de error. La adquisición automatizada de datos mediante web scraping permite construir, '
  'en minutos y de forma reproducible, un conjunto de datos estructurado a partir de contenido público '
  'disperso.')
p('Una vez estructurado, el dataset habilita análisis que hoy no son posibles con fuentes abiertas '
  'peruanas: medir la dispersión de precios dentro de una misma categoría, comparar el nivel de precios '
  'entre categorías, estudiar la difusión del financiamiento en cuotas y su relación con el precio, '
  'detectar valores atípicos y, en etapas posteriores del curso, entrenar modelos de predicción o '
  'segmentación. Esta primera parte del proyecto se concentra en la adquisición, el control de calidad y '
  'la documentación de esos datos, que constituyen la base sobre la que se apoyarán las siguientes fases.')

# ---------------------------------------------------------------- 3
h('3. OBJETIVOS')
h('3.1 Objetivo general', 2)
p('Construir, documentar y validar un conjunto de datos estructurado sobre publicaciones de productos de '
  'Mercado Libre Perú, obtenido mediante técnicas de web scraping en Python, que reúna como mínimo 1000 '
  'registros únicos y al menos ocho atributos —numéricos y categóricos—, y que sirva de base para analizar '
  'la dispersión de precios y las estrategias promocionales del comercio electrónico peruano.')
h('3.2 Objetivos específicos', 2)
numerada([
    'Seleccionar una fuente web peruana pública y pertinente, verificando su accesibilidad técnica y las '
    'condiciones establecidas en su archivo robots.txt antes de iniciar la extracción.',
    'Desarrollar un script en Python que recorra al menos cinco categorías de productos y hasta veinte '
    'páginas de resultados por categoría, empleando Selenium para la navegación —el sitio no entrega las '
    'tarjetas de resultados a peticiones simples— y BeautifulSoup para el análisis del HTML, gestionando '
    'la paginación mediante el botón de avance del sitio, que genera el patrón de URL _Desde_N.',
    'Incorporar al script un User-Agent realista, pausas de diez segundos entre peticiones mediante '
    'time.sleep(), manejo de excepciones con try-except y guardado incremental de los resultados, de modo '
    'que una falla puntual de conexión no comprometa la ejecución completa.',
    'Extraer un mínimo de ocho atributos por publicación, combinando variables numéricas (precio actual, '
    'número de cuotas, monto de cada cuota, página y posición en los resultados) y categóricas '
    '(identificador de la oferta, título, categoría de búsqueda, moneda, texto de financiamiento, enlace '
    'de la publicación, enlace de la página de resultados y fecha de extracción), superando el mínimo de '
    'seis atributos exigido por el enunciado.',
    'Consolidar un dataset de 1000 registros o más, sin duplicados, identificados de forma unívoca por el '
    'código de la oferta —recuperado del parámetro wid de la URL o, en su defecto, de una ruta directa de '
    'publicación—, y exportarlo en formato CSV con codificación UTF-8.',
    'Asegurar que ninguna columna del dataset final supere el 10 % de valores nulos y que los formatos de '
    'precio, fecha y texto sean consistentes en todos los registros.',
    'Documentar la totalidad de las variables en un diccionario de datos que precise nombre, descripción, '
    'tipo, tamaño máximo, valores posibles y unidad de medida.',
    'Entregar un único notebook comentado y reproducible, ACD_Proyecto_Parte_I.ipynb, organizado en dos '
    'secciones —Extracción y Limpieza—, que permita a un tercero replicar el proceso completo siguiendo '
    'únicamente las instrucciones del documento.',
])

# ---------------------------------------------------------------- 4
h('4. DATASET PRELIMINAR')
h('4.1 Descripción de la muestra', 2)
p('Se procesaron 5 080 observaciones crudas de Mercado Libre Perú, obtenidas entre las 19:54:05 y las '
  '20:22:54 del 13 de setiembre de 2026, según las marcas temporales del scraper. El archivo no registra '
  'zona horaria. Las búsquedas de origen fueron celulares, laptops, televisores, refrigeradoras y '
  'audífonos. El dataset final contiene 4 412 ofertas con identificadores únicos y 14 columnas.')
p('La unidad de observación es la oferta identificada en la URL, conservando su última aparición en el '
  'archivo. La muestra procede de páginas de resultados y no es aleatoria ni representativa de todo el '
  'mercado peruano. La categoría es la búsqueda de origen y puede incluir accesorios o productos '
  'relacionados. Los precios describen ofertas, no transacciones realizadas.')

h('4.2 Preparación y control de calidad', 2)
p('Se normalizaron espacios, se transformaron los precios a formato numérico, se estandarizó la moneda a '
  'PEN y se convirtieron las fechas a tipo datetime. Se extrajeron el número de cuotas y el monto por '
  'cuota de los textos observados, manteniendo los nulos cuando la información no estaba disponible.')
p('El identificador extraído originalmente por el scraper se conserva como id_extraido. Para '
  'id_publicacion se tomó el parámetro wid de la URL o, cuando estaba ausente, el código de una ruta '
  'directa sin /p/. Se separaron 56 filas sin campos esenciales válidos y se retiraron 605 observaciones '
  'repetidas, conservando la última por fecha y orden de archivo. Adicionalmente se excluyeron 7 ofertas '
  'con precios cuestionados, identificadas por código y precio: Xiaomi Redmi Note 13 Pro+ a '
  'S/ 1 250 000, refrigerador Daewoo a S/ 999 999, televisor Daewoo a S/ 99 999, refrigeradora Indurama a '
  'S/ 2, dos televisores Daewoo a S/ 10 y Lenovo V15 a S/ 29 000. Son exclusiones puntuales acordadas para '
  'esta muestra, no límites generales aplicables a todos los productos. Estos importes ya estaban en el '
  'CSV crudo; no fueron generados por la conversión numérica. La exclusión es una decisión de calidad para '
  'el análisis, sin verificar el precio real ni imputar reemplazos. Los registros separados se guardaron '
  'como evidencia para revisión.')
p('No se encontraron duplicados de fila completa en el CSV original; las repeticiones se detectaron por '
  'identificador de oferta, aunque sus posiciones, fechas o enlaces de seguimiento fueran diferentes.')
p('Se excluyeron precio_anterior_texto y vendedor_texto del dataset principal debido a sus ausencias '
  'originales de 40,08 % y 64,07 %, respectivamente. Ambas columnas permanecen en el CSV crudo. No se '
  'imputaron precios anteriores, vendedores ni descuentos. La falta de un precio anterior no permite '
  'concluir que el descuento sea cero.')

h('4.3 Variables y cobertura', 2)
p('Las variables comerciales incluyen título, categoría, moneda, precio actual, número de cuotas, monto de '
  'la cuota y el texto de financiamiento. Los identificadores, la página, la posición, las URL y la fecha '
  'proporcionan trazabilidad. El dataset incluye variables numéricas y categóricas, supera los 1000 '
  'registros y los seis atributos mínimos, y ninguna columna supera el 10 % de valores nulos. La tabla '
  'presenta los tipos en pandas antes de exportar; el formato CSV no conserva los tipos y deben declararse '
  'al volver a cargarlo.')
tabla(['Variable', 'Tipo en pandas', 'Nulos', '% de nulos', 'Valores distintos'],
      [['id_publicacion', 'string', '0', '0,00', '4 412'],
       ['id_extraido', 'string', '0', '0,00', '4 412'],
       ['categoria', 'string', '0', '0,00', '5'],
       ['titulo', 'string', '0', '0,00', '4 181'],
       ['moneda', 'string', '0', '0,00', '1'],
       ['precio_actual', 'Float64', '0', '0,00', '1 952'],
       ['numero_cuotas', 'Int64', '55', '1,25', '2'],
       ['monto_cuota', 'Float64', '55', '1,25', '2 225'],
       ['cuotas_texto', 'string', '55', '1,25', '2 335'],
       ['pagina', 'Int64', '0', '0,00', '20'],
       ['posicion_pagina', 'Int64', '0', '0,00', '60'],
       ['url_publicacion', 'string', '0', '0,00', '4 412'],
       ['url_fuente', 'string', '0', '0,00', '95'],
       ['fecha_extraccion', 'datetime64', '0', '0,00', '99']],
      [4.6, 3.2, 2.0, 2.4, 3.4])

h('4.4 Estadísticos descriptivos', 2)
p('Todos los precios se expresan en soles (PEN). Tras las exclusiones puntuales descritas, se conservaron '
  'los demás valores extremos porque su magnitud por sí sola no prueba un error. No se ha verificado el '
  'precio real de cada publicación ni se afirma que todos los precios restantes sean correctos. Las '
  'diferencias entre categorías no equivalen a diferencias entre productos comparables.')
tabla(['Categoría', 'Registros', 'Precio mínimo', 'Precio mediano', 'Precio promedio', 'Precio máximo'],
      [['audifonos', '959', '16,90', '138,00', '376,08', '8 959,00'],
       ['celulares', '937', '38,61', '1 632,00', '2 075,04', '9 498,00'],
       ['laptops', '928', '459,00', '4 898,50', '5 807,42', '24 665,00'],
       ['refrigeradoras', '646', '52,00', '1 314,00', '1 805,08', '20 741,00'],
       ['televisores', '942', '25,00', '1 289,50', '1 907,65', '59 999,00']],
      [3.2, 2.2, 2.6, 2.6, 2.6, 2.4])

h('4.5 Vista previa', 2)
p('Se muestra una selección de columnas de las primeras cinco filas. El CSV contiene la totalidad de los '
  'atributos descritos.')
tabla(['id_publicacion', 'categoria', 'titulo', 'precio_actual', 'numero_cuotas'],
      [['MPE636405849', 'celulares', 'Apple iPhone 17 Pro Max (256 GB) - Color plata', '4 849,00', '6'],
       ['MPE1067071458', 'celulares', 'Celular Samsung Galaxy S26 Ultra 512gb', '4 129,00', '6'],
       ['MPE1087974300', 'celulares', 'Apple iPhone 17 Pro Max (256 GB) - Azul profundo', '4 849,00', '6'],
       ['MPE1097141956', 'celulares', 'Apple iPhone 17 Pro (256 GB) - Azul profundo', '4 479,00', '6'],
       ['MPE724292960', 'celulares', 'Samsung Galaxy A56 5G Dual Sim 256GB 12GB Negro 6.7"', '1 517,00', '6']],
      [3.4, 2.4, 6.2, 2.4, 2.2])

h('4.6 Limitaciones', 2)
p('No se extrajeron calificación, número de opiniones, condición, marca ni envío gratuito. Por tanto, '
  'estos datos no permiten analizar esas características ni la reputación del vendedor. Tampoco permiten '
  'calcular descuentos de manera completa. La deduplicación conserva una sola observación por oferta y no '
  'constituye una serie histórica. La identidad de cada oferta se recuperó de las URL guardadas y no se '
  'verificó mediante consultas adicionales al sitio.')

# ---------------------------------------------------------------- 5
h('5. ALCANCE')
p('Qué se desarrolla en esta primera entrega', negrita=True)
vinetas([
    'Adquisición. Extracción automatizada de publicaciones de cinco categorías de Mercado Libre Perú '
    '—celulares, laptops, televisores, refrigeradoras y audífonos— desde las páginas de resultados del '
    'subdominio de listados, con un recorrido de hasta veinte páginas por categoría.',
    'Limpieza y control de calidad. Normalización de textos, conversión de precios y fechas a tipos '
    'numéricos y temporales, recuperación del identificador de oferta, separación de registros '
    'incompletos, deduplicación por oferta y documentación de cada exclusión con su evidencia.',
    'Documentación. Diccionario de datos con las catorce variables del archivo final, descripción de la '
    'muestra preliminar y un notebook reproducible que permite repetir todo el proceso.',
    'Entregables. Dataset preliminar en CSV con codificación UTF-8, diccionario de datos e informe.',
])
p('Qué queda fuera', negrita=True)
vinetas([
    'Análisis exploratorio profundo y modelado. No se realizan pruebas estadísticas, segmentación ni '
    'modelos predictivos: corresponden a las siguientes partes del proyecto.',
    'Seguimiento histórico de precios. El dataset es una fotografía del 13 de setiembre de 2026, no una '
    'serie temporal, y no permite medir variaciones de precio en el tiempo.',
    'Reseñas individuales y datos del vendedor. No se extraen opiniones de compradores ni información de '
    'perfiles; las rutas de perfil están además restringidas por el archivo robots.txt del sitio.',
    'Atributos ausentes de las páginas de resultados. Calificación, número de opiniones, condición, marca '
    'y envío gratuito no figuran en las tarjetas del listado y quedan fuera del dataset; el precio '
    'anterior y el tipo de vendedor se capturaron, pero superan el 10 % de valores nulos y permanecen solo '
    'en el CSV crudo.',
    'Representatividad del mercado. La muestra proviene de cinco búsquedas y no es aleatoria: describe las '
    'ofertas observadas, no el universo del comercio electrónico peruano ni transacciones efectivas.',
    'Redistribución. El dataset es de uso académico dentro del curso DS3021 y no se publica con fines '
    'comerciales.',
])

# ---------------------------------------------------------------- 6
h('6. FUENTES DE DATOS')
h('6.1 Criterios de evaluación de las fuentes candidatas', 2)
p('Antes de fijar la fuente definitiva se evaluaron tres portales peruanos incluidos entre los sugeridos '
  'en el enunciado. La comparación se realizó sobre seis criterios, definidos a partir de los requisitos '
  'técnicos del proyecto y de la rúbrica de evaluación:')
vinetas([
    'Accesibilidad técnica: si el contenido se entrega en HTML —extraíble con BeautifulSoup— y con qué '
    'esfuerzo de navegación, ya que la dependencia de JavaScript obliga a usar un navegador automatizado y '
    'eleva el tiempo de ejecución.',
    'Políticas del sitio: revisión del archivo robots.txt y de las rutas que el sitio declara como no '
    'rastreables.',
    'Volumen disponible: capacidad de superar con holgura el mínimo de 1000 registros exigido.',
    'Riqueza de atributos: presencia de al menos seis atributos relevantes, con un balance razonable entre '
    'variables numéricas y categóricas.',
    'Calidad esperada: probabilidad de mantenerse por debajo del 10 % de valores nulos en las columnas de '
    'interés analítico.',
    'Antecedentes de uso: existencia de trabajos previos de análisis de datos sobre la misma fuente, que '
    'reduzcan la incertidumbre técnica de las siguientes etapas del proyecto.',
])

h('6.2 Comparación de las fuentes evaluadas', 2)
tabla(['Criterio', 'Mercado Libre Perú', 'Falabella Perú', 'Computrabajo Perú'],
      [['URL evaluada', 'listado.mercadolibre.com.pe', 'www.falabella.com.pe', 'www.computrabajo.com.pe'],
       ['Tipo de contenido',
        'Publicaciones de productos de un marketplace (oferta multivendedor).',
        'Catálogo de productos de un retailer (oferta propia y de terceros).',
        'Avisos de empleo publicados por empresas.'],
       ['Renderizado del contenido',
        'Las páginas de resultados se entregan como HTML, extraíble con BeautifulSoup. La verificación '
        'posterior mostró que el servidor responde de forma incompleta a peticiones simples, por lo que la '
        'navegación se resolvió con Selenium; el volumen de páginas requerido sigue siendo alcanzable en '
        'menos de media hora.',
        'El catálogo se construye mayoritariamente del lado del cliente (JavaScript), por lo que exigiría '
        'Selenium y un tiempo de ejecución considerablemente mayor.',
        'El listado es accesible, pero el sitio aplica validaciones de navegador y limitación de peticiones '
        'que dificultan una extracción estable con requests.'],
       ['Paginación',
        'Explícita y predecible en la URL mediante el sufijo _Desde_N (48 resultados por página), fácil de '
        'recorrer en un bucle.',
        'Paginación por parámetro de consulta, pero dependiente de llamadas internas al catálogo.',
        'Paginación por parámetro ?p=N, sencilla, pero condicionada a la estabilidad del acceso.'],
       ['Volumen disponible',
        'Muy alto: miles de publicaciones por categoría y decenas de categorías. Superar 1000 registros es '
        'alcanzable con pocas categorías.',
        'Alto, pero el costo por registro es mayor por el renderizado dinámico.',
        'Medio: el número de avisos vigentes por categoría es limitado y rota con rapidez.'],
       ['Riqueza de atributos',
        'Alta y balanceada: precio, precio anterior, cuotas y monto de cuota (numéricos); título, marca, '
        'categoría, moneda, envío y vendedor (categóricos). La extracción confirmó que calificación, '
        'opiniones, condición y envío no figuran en las tarjetas de resultados; véase la sección 6.4.',
        'Media: precio, precio anterior y marca son accesibles, pero la calificación y el vendedor no '
        'siempre están expuestos en el listado.',
        'Baja para el análisis cuantitativo: el salario es opcional y suele omitirse, lo que pondría en '
        'riesgo el límite de 10 % de nulos por columna.'],
       ['Políticas de acceso (robots.txt)',
        'Permite el rastreo de las rutas públicas de listado y de publicación para el agente genérico; '
        'restringe rutas transaccionales y de perfil (carrito, checkout, perfiles de usuario) y bloquea '
        'rastreadores de entrenamiento de IA [5].',
        'Archivo permisivo (User-agent: * sin rutas prohibidas) acompañado de varios sitemaps [13].',
        'Restringe rutas de la aplicación y del área de usuario; requiere una revisión detallada antes de '
        'cualquier extracción.'],
       ['Antecedentes de uso en análisis de datos',
        'Amplios: datasets públicos en Kaggle, repositorios de código abierto con BeautifulSoup, '
        'conectores comerciales que cubren explícitamente el mercado peruano y una API pública oficial de '
        'consulta.',
        'Existen antecedentes de monitoreo de precios, casi siempre con herramientas de pago o navegador '
        'automatizado.',
        'Antecedentes principalmente académicos y de baja escala.'],
       ['Riesgo principal',
        'Cambios en los nombres de clases CSS del maquetado y limitación de peticiones si no se respeta una '
        'pausa entre ellas.',
        'Alta complejidad técnica y tiempo de ejecución elevado para el plazo del proyecto.',
        'Bloqueo del scraper y exceso de valores nulos en la variable de mayor interés analítico.'],
       ['Veredicto', 'SELECCIONADA', 'Descartada', 'Descartada']],
      [3.2, 4.6, 4.0, 3.8], tam=8.5)
p('Nota: la evaluación de accesibilidad y de políticas de rastreo corresponde a la revisión realizada en '
  'setiembre de 2026. Dado que la estructura de los sitios y sus archivos robots.txt pueden cambiar, la '
  'verificación se automatizó dentro del notebook y se repite antes de cada extracción.', tam=9, cursiva=True)

h('6.3 Fuente seleccionada y justificación', 2)
p('Fuente elegida: Mercado Libre Perú — https://www.mercadolibre.com.pe/ (páginas de resultados en '
  'https://listado.mercadolibre.com.pe/).')
p('Mercado Libre es el marketplace de mayor alcance en América Latina y opera en el Perú con catálogo, '
  'precios y condiciones de venta enteramente públicos. Su elección responde a cinco razones concretas:')
numerada([
    'Es una fuente peruana, pública y directamente pertinente. El dominio .com.pe expone la oferta '
    'dirigida al mercado nacional, con precios en soles y condiciones de envío locales, lo que hace que el '
    'dataset resultante describa efectivamente el comercio electrónico peruano y no un promedio regional.',
    'Su contenido es extraíble con las técnicas del curso. Las páginas de resultados exponen los datos en '
    'el HTML, de modo que el análisis se resuelve con BeautifulSoup. La navegación requiere un navegador '
    'automatizado —Selenium—, pero la estructura regular del listado mantiene el script simple: la '
    'extracción completa tomó veintinueve minutos.',
    'La paginación es explícita y predecible. El desplazamiento entre páginas se controla mediante el '
    'sufijo _Desde_N en la URL, con incrementos regulares de 48 resultados, lo que permite recorrer '
    'decenas de páginas con un bucle simple y satisface de forma directa el requisito de manejo de '
    'paginación.',
    'El volumen y la riqueza de atributos son holgadamente suficientes. Cada categoría contiene miles de '
    'publicaciones y cada publicación expone simultáneamente atributos numéricos y categóricos. El '
    'requisito de 6 atributos y 1000 registros se supera recorriendo unas pocas categorías: el dataset '
    'final reúne 4 412 ofertas y 14 variables.',
    'Existen antecedentes documentados de su uso analítico. Como se detalla en la sección 6.6, hay '
    'conjuntos de datos publicados, código abierto y documentación técnica construidos sobre esta misma '
    'fuente, lo que ofrece referencias verificables para el desarrollo del script, la definición de las '
    'variables y la limpieza posterior.',
])

h('6.4 Descripción de la página web y de los datos disponibles', 2)
p('El sitio organiza su contenido en tres niveles relevantes para la extracción. El primero es el árbol de '
  'categorías, accesible desde el menú principal, que agrupa la oferta en rubros como tecnología, '
  'electrodomésticos, hogar o deportes. El segundo son las páginas de resultados alojadas en el subdominio '
  'listado.mercadolibre.com.pe, donde cada página presenta alrededor de 48 publicaciones en formato de '
  'tarjeta, con el precio y los atributos comerciales principales ya visibles. El tercero son las páginas '
  'de publicación individual, en el subdominio articulo.mercadolibre.com.pe, que amplían la ficha técnica '
  'y las opiniones. La estrategia prevista prioriza las páginas de resultados, ya que concentran la mayor '
  'cantidad de atributos por petición y permiten alcanzar el volumen requerido con un número reducido de '
  'solicitudes al servidor. El siguiente cuadro resume los atributos identificados y su ubicación:')
tabla(['Atributo', 'Tipo', 'Descripción', 'Ubicación'],
      [['Título de la publicación', 'Categórico', 'Nombre comercial del producto tal como lo publica el vendedor.', 'Listado'],
       ['Precio actual', 'Numérico', 'Precio vigente de la publicación.', 'Listado'],
       ['Precio anterior', 'Numérico', 'Precio tachado cuando existe promoción; permite calcular el descuento.', 'Listado (si aplica)'],
       ['Porcentaje de descuento', 'Numérico', 'Diferencia relativa entre el precio anterior y el actual.', 'Listado (si aplica) o derivado'],
       ['Moneda', 'Categórico', 'Unidad monetaria de la publicación (S/ o US$).', 'Listado'],
       ['Número de cuotas', 'Numérico', 'Cantidad de cuotas de financiamiento ofrecidas.', 'Listado (si aplica)'],
       ['Monto de la cuota', 'Numérico', 'Importe de cada cuota de financiamiento.', 'Listado (si aplica)'],
       ['Envío gratis', 'Categórico', 'Indica si la publicación ofrece envío sin costo.', 'Listado'],
       ['Condición', 'Categórico', 'Estado del producto: nuevo, usado o reacondicionado.', 'Publicación'],
       ['Calificación promedio', 'Numérico', 'Puntuación de 1 a 5 otorgada por los compradores.', 'Publicación'],
       ['Número de opiniones', 'Numérico', 'Cantidad de reseñas asociadas a la publicación.', 'Publicación'],
       ['Cantidad vendida', 'Numérico', 'Unidades vendidas informadas por la plataforma.', 'Publicación'],
       ['Marca', 'Categórico', 'Marca del producto.', 'Publicación / ficha técnica'],
       ['Categoría', 'Categórico', 'Categoría de búsqueda desde la que se extrajo el registro.', 'Asignado por el script'],
       ['Identificador y URL', 'Categórico', 'Código MPE de la oferta y su enlace, usados para deduplicar.', 'Listado']],
      [4.2, 2.2, 6.6, 3.2])
p('Esta tabla corresponde a los atributos identificados en la exploración previa de la fuente. La '
  'extracción confirmó la disponibilidad de título, precio actual, moneda, cuotas, categoría, '
  'identificador y enlace en las páginas de resultados, pero no la de calificación, número de opiniones, '
  'condición, marca, envío gratuito y cantidad vendida, que la plataforma no expone en las tarjetas del '
  'listado. El precio anterior y el tipo de vendedor sí se capturaron, pero quedaron fuera del archivo '
  'final por superar el límite de 10 % de valores nulos. La composición definitiva del dataset se detalla '
  'en la sección 4.')

h('6.5 Cumplimiento de robots.txt y consideraciones éticas', 2)
p('La revisión del archivo robots.txt de Mercado Libre muestra que las rutas públicas de listado y de '
  'publicación permanecen abiertas al agente genérico (User-agent: *), mientras que se restringen rutas '
  'transaccionales y de área privada —carrito, proceso de compra y perfiles de usuario— y se bloquea por '
  'completo a determinados rastreadores dedicados al entrenamiento de modelos de inteligencia artificial '
  '[5] [11]. En consecuencia, la extracción se limita exclusivamente a las páginas de resultados, sin '
  'acceder a ninguna ruta restringida.')
p('La verificación se automatizó dentro del notebook y se ejecuta antes de cada extracción. El proceso '
  'descarga los archivos robots.txt de los dos dominios involucrados —www.mercadolibre.com.pe y el '
  'subdominio de listados listado.mercadolibre.com.pe, que declara reglas propias—, los interpreta con el '
  'módulo urllib.robotparser y comprueba, para el User-Agent declarado, cada dirección que el script va a '
  'visitar, incluidas las URL paginadas con el sufijo _Desde_N. Todas resultaron permitidas, y las rutas '
  'que el proyecto se compromete a no visitar —carrito, proceso de compra y perfiles de vendedor— se '
  'confirmaron restringidas. Los archivos descargados se conservan fechados como evidencia de la revisión. '
  'Si alguna ruta estuviera prohibida, la ejecución se detiene antes de extraer.')
p('Adicionalmente, el proyecto adopta las siguientes salvaguardas:')
vinetas([
    'No se recolectó información personal. Los datos extraídos describen publicaciones de productos; no se '
    'almacenaron nombres, documentos, teléfonos ni direcciones de personas naturales.',
    'El campo relativo al vendedor se registró únicamente como categoría y, al presentar más del 60 % de '
    'valores ausentes, quedó fuera del dataset final.',
    'Se incluye una pausa de diez segundos entre peticiones mediante time.sleep(), a fin de no generar '
    'carga significativa sobre el servidor. Con ese intervalo, la extracción completa de las cinco '
    'categorías tomó veintinueve minutos.',
    'Se declara un User-Agent realista e identificable, evitando técnicas de evasión de bloqueos como la '
    'rotación de direcciones IP o de identidades.',
    'El dataset se destina exclusivamente a fines académicos, en el marco del curso DS3021, y no será '
    'redistribuido con fines comerciales.',
])

h('6.6 Antecedentes de uso de la fuente en análisis de datos', 2)
p('Un criterio adicional de selección fue la existencia de trabajos previos sobre la misma fuente, que '
  'reducen el riesgo técnico de las etapas siguientes al ofrecer referencias sobre la estructura de las '
  'páginas y sobre las variables habitualmente extraídas:')
vinetas([
    'Conjuntos de datos publicados en Kaggle a partir de publicaciones de Mercado Libre, entre ellos un '
    'análisis de la categoría de refrigeradores y el conjunto asociado al Mercado Libre Data Challenge '
    '[6] [7].',
    'Repositorios de código abierto que implementan la extracción con BeautifulSoup y Pandas sobre el '
    'mismo patrón de URL utilizado en el Perú, con soporte explícito para varios países de la región [8].',
    'Conectores y documentación de proveedores especializados en extracción de datos que incluyen a '
    'Mercado Libre Perú entre sus mercados soportados y describen los campos habitualmente recuperados: '
    'precios, descuentos, promociones, cuotas, cantidad vendida, envío y posición en los resultados '
    '[9] [10].',
    'Artículos técnicos que documentan el análisis del archivo robots.txt de la plataforma y el proceso '
    'completo de extracción y análisis con Python [11].',
    'La existencia de una API pública oficial de consulta de publicaciones, que puede emplearse como '
    'mecanismo de verificación cruzada de los datos extraídos y como plan de contingencia [12].',
])
p('Estos antecedentes confirman que la fuente es técnicamente viable y analíticamente útil, y facilitaron '
  'el diseño del script, la definición de las variables y los criterios de limpieza.')

# ---------------------------------------------------------------- 7
h('7. ESTRATEGIA')
h('7.1 Herramientas', 2)
p('El proyecto se desarrolla en Python 3.11 con Selenium para la navegación, BeautifulSoup para el '
  'análisis del HTML y pandas para la consolidación, la limpieza y la exportación. El trabajo se versiona '
  'en un repositorio Git y se ejecuta desde un único notebook, ACD_Proyecto_Parte_I.ipynb, dividido en dos '
  'secciones: Extracción y Limpieza.')
h('7.2 Procedimiento de obtención', 2)
numerada([
    'Verificación de políticas. Antes de extraer se descargan los archivos robots.txt del dominio '
    'principal y del subdominio de listados, se interpretan con el módulo urllib.robotparser y se '
    'comprueba, para el User-Agent declarado, que cada dirección por visitar esté permitida. Los archivos '
    'quedan guardados como evidencia fechada. Si alguna ruta estuviera prohibida, el proceso se detiene.',
    'Recorrido por categorías. Cinco categorías de rubros distintos, elegidas para dar al dataset variedad '
    'de precios y de marcas.',
    'Control de la paginación. El avance entre páginas usa el botón Siguiente del sitio, que genera las URL '
    'con el sufijo _Desde_N, con incrementos de 48 resultados. El bucle se detiene cuando la página no '
    'devuelve tarjetas o cuando repite el contenido anterior, en lugar de fijar un número rígido de '
    'páginas: por eso el recorrido efectivo fue de 95 páginas y no de 100.',
    'Cortesía con el servidor. Pausa de diez segundos entre peticiones mediante time.sleep(), User-Agent '
    'realista e identificable y ninguna técnica de evasión de bloqueos.',
    'Robustez. Cada página se procesa dentro de un bloque try-except, de modo que una falla puntual no '
    'cancela la ejecución, y los resultados se escriben de forma incremental en el CSV: una interrupción '
    'no pierde lo ya extraído.',
    'Limpieza y verificación. La segunda sección del notebook convierte el CSV crudo en el dataset final y '
    'comprueba automáticamente los requisitos del enunciado: mínimo de registros y de atributos, unicidad '
    'del identificador y máximo de 10 % de valores nulos por columna. Si alguno deja de cumplirse, la '
    'ejecución falla en lugar de exportar en silencio.',
])
h('7.3 Planes de contingencia', 2)
vinetas([
    'Cambios en el maquetado del sitio. Los nombres de las clases CSS están aislados en dos funciones del '
    'notebook: una actualización del sitio se resuelve modificando solo ese bloque.',
    'Contenido servido con JavaScript. Previsto inicialmente con requests, el sitio entregó páginas '
    'incompletas; se aplicó la contingencia prevista y la navegación pasó a Selenium, conservando '
    'BeautifulSoup para el análisis del HTML.',
    'Limitación de peticiones o verificación de navegador. Ampliar la pausa entre solicitudes y fraccionar '
    'la ejecución en varias sesiones. Cuando el sitio solicita una verificación, el notebook la delega a la '
    'persona que ejecuta y reanuda el recorrido.',
    'Inviabilidad de la extracción por HTML. Uso de la API pública de consulta de la plataforma como fuente '
    'alternativa, documentando el cambio [12].',
    'Fuente de reemplazo. Falabella Perú queda registrada como alternativa, con la advertencia de que '
    'exige un navegador automatizado y un tiempo de ejecución mayor.',
])

# ---------------------------------------------------------------- 8
h('8. VIABILIDAD')
h('8.1 Tiempo', 2)
p('La extracción completa —cinco categorías, 95 páginas y 5 080 registros crudos— se ejecutó el 13 de '
  'setiembre de 2026 entre las 19:54:05 y las 20:22:54, según las marcas temporales del propio scraper: '
  'veintinueve minutos, de los cuales la mayor parte corresponde a las pausas deliberadas entre '
  'peticiones. La limpieza completa se ejecuta en segundos sobre el CSV ya obtenido, de modo que cualquier '
  'ajuste posterior no obliga a repetir la extracción. Frente a la fecha de entrega del 25 de setiembre de '
  '2026, el dataset quedó disponible con doce días de holgura, suficientes para la documentación y para '
  'repetir la captura si fuera necesario.')
p('Obtener un volumen equivalente de forma manual —transcribir más de cinco mil publicaciones— habría '
  'exigido decenas de horas y un riesgo alto de error de transcripción, lo que confirma la pertinencia de '
  'la adquisición automatizada.')
h('8.2 Recursos', 2)
p('Una computadora personal con Windows 11, Google Chrome y conexión doméstica a internet es suficiente: '
  'no se requieren servidores, servicios de pago ni credenciales. El almacenamiento total del proyecto, '
  'incluidos los archivos de evidencia, es de pocos megabytes. El trabajo se coordina mediante un '
  'repositorio Git compartido por los cinco integrantes.')
h('8.3 Herramientas', 2)
p('Todas las librerías empleadas son de código abierto y gratuitas —Selenium, BeautifulSoup, requests y '
  'pandas—, están declaradas en un archivo de requisitos y se instalan con una sola orden. El proceso '
  'completo se reproduce ejecutando un notebook, lo que permite a un tercero repetir la extracción y la '
  'limpieza siguiendo únicamente las instrucciones del documento.')
h('8.4 Riesgos y su control', 2)
tabla(['Riesgo', 'Control adoptado'],
      [['Cambio del maquetado del sitio', 'Selectores aislados en un solo bloque del notebook.'],
       ['Bloqueo o limitación de peticiones',
        'Pausa de diez segundos, User-Agent identificable y ejecución fraccionable.'],
       ['Interrupción de la ejecución', 'Guardado incremental en el CSV tras cada página.'],
       ['Datos de calidad insuficiente',
        'Verificaciones automáticas y evidencia documentada de cada exclusión.'],
       ['Pérdida de trabajo o descoordinación',
        'Repositorio Git con el aporte de cada integrante registrado.']],
      [7.0, 9.0], tam=10)

# ---------------------------------------------------------------- referencias
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
h('REFERENCIAS')
referencias = [
    '[1] Cámara Peruana de Comercio Electrónico (CAPECE). Observatorio Ecommerce Perú. '
    'https://www.capece.org.pe/observatorio-ecommerce/',
    '[2] Gestión. «Ecommerce en Perú: ¿quiénes compran más y qué sectores lideran las ventas online?». '
    'https://gestion.pe/economia/empresas/ecommerce-en-peru-quienes-compran-mas-y-que-sectores-lideran-las-ventas-online-noticia/',
    '[3] Forbes Perú (11 de julio de 2025). «Ventas por comercio electrónico alcanzaron los US$ 8 700 '
    'millones durante el primer semestre, según Capece». '
    'https://forbes.pe/economia-y-finanzas/2025-07-11/ventas-por-comercio-electronico-alcanzaron-los-us8-700-millones-durante-el-primer-semestre-segun-capece',
    '[4] Mercado Libre Perú. https://www.mercadolibre.com.pe/',
    '[5] Archivo robots.txt de Mercado Libre. https://www.mercadolibre.com.pe/robots.txt',
    '[6] Kaggle. «Análisis Mercado Libre – Categoría Refrigeradores». '
    'https://www.kaggle.com/datasets/andersonmontealegre/anlisis-mercado-libre-categora-refrigeradores',
    '[7] Kaggle. «Mercado Libre Data Challenge». '
    'https://www.kaggle.com/datasets/fredericods/mercado-libre-data-challenge',
    '[8] Alaniz, P. MercadoLibre-Scraper: script en Python para la extracción de datos de Mercado Libre con '
    'BeautifulSoup4 y Pandas. https://github.com/PabloAlaniz/MercadoLibre-Scraper',
    '[9] Apify. «Mercado Libre LATAM Scraper» (incluye el mercado peruano). '
    'https://apify.com/karamelo/mercadolibre-scraper-espanol-castellano',
    '[10] Oxylabs. Documentación de extracción para Mercado Libre. '
    'https://developers.oxylabs.io/documentation/es/soluciones-de-scraping/web-scraper-api/targets/latin-american-e-commerce/mercado-libre/url',
    '[11] Stochaj, P. «Scraping and Analyzing MercadoLibre, South America\'s E-Commerce Giant». Medium. '
    'https://medium.com/@paulostochaj/scraping-and-analyzing-mercadolibre-south-americas-e-commerce-giant-bc34f8fa24a8',
    '[12] Mercado Libre Developers. API pública de búsqueda de publicaciones. '
    'https://developers.mercadolibre.com.pe/',
    '[13] Archivo robots.txt de Falabella Perú. https://www.falabella.com.pe/robots.txt',
]
for ref in referencias:
    par = doc.add_paragraph(ref)
    par.paragraph_format.left_indent = Cm(1.0)
    par.paragraph_format.first_line_indent = Cm(-1.0)
    par.paragraph_format.space_after = Pt(6)
    par.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in par.runs:
        run.font.size = Pt(10)

pie_con_numero()
SALIDA.parent.mkdir(parents=True, exist_ok=True)
doc.save(SALIDA)
print('guardado:', SALIDA)
