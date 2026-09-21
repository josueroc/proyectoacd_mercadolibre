# -*- coding: utf-8 -*-
"""Tabla del diccionario de datos, lista para copiar y pegar en el informe."""
import pathlib
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

SALIDA = pathlib.Path(r"C:\Users\yared\Documents\ACD\Proyecto\proyectoacd_mercadolibre\documentos\Tabla_diccionario_para_informe.docx")

doc = Document()
normal = doc.styles['Normal']
normal.font.name = 'Arial'
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(8)
normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

st = doc.styles['Heading 1']
st.font.name = 'Arial'
st.font.size = Pt(13)
st.font.bold = True
st.font.color.rgb = RGBColor(0, 0, 0)
rfonts = st.element.get_or_add_rPr().get_or_add_rFonts()
for attr in ('asciiTheme', 'hAnsiTheme', 'cstheme', 'eastAsiaTheme'):
    if rfonts.get(qn('w:' + attr)) is not None:
        del rfonts.attrib[qn('w:' + attr)]
for attr in ('ascii', 'hAnsi', 'cs', 'eastAsia'):
    rfonts.set(qn('w:' + attr), 'Arial')

s = doc.sections[0]
s.top_margin = s.bottom_margin = Cm(2.0)
s.left_margin = s.right_margin = Cm(2.0)

FILAS = [
    ('id_publicacion',
     'Identificador de la oferta, recuperado del parámetro wid de la URL o de una ruta directa de '
     'publicación. Se utiliza para identificar y deduplicar las ofertas.',
     'Categórico nominal, almacenado como texto', '13',
     'Prefijo MPE seguido de dígitos. Ejemplo: MPE636405849. Único y sin nulos en el dataset final.', '–'),
    ('id_extraido',
     'Identificador obtenido originalmente por el scraper. Se conserva para trazabilidad; puede '
     'identificar un producto de catálogo o una publicación.',
     'Categórico nominal, almacenado como texto', '13', 'Prefijo MPE seguido de dígitos.', '–'),
    ('categoria',
     'Término de búsqueda desde el cual se obtuvo la observación conservada. No corresponde '
     'necesariamente a la categoría oficial del producto.',
     'Categórico nominal', '14', 'celulares, laptops, televisores, refrigeradoras, audifonos.', '–'),
    ('titulo',
     'Nombre del producto u oferta mostrado en la tarjeta de resultados, con espacios normalizados.',
     'Texto libre', '200', 'Texto variable. Ejemplo: Celular Samsung Galaxy S26 Ultra 512gb.', '–'),
    ('moneda',
     'Código de moneda asociado al precio. El símbolo original S/ se normalizó a PEN.',
     'Categórico nominal', '3', 'PEN.', '–'),
    ('precio_actual',
     'Precio anunciado de la oferta al momento de la extracción, convertido a formato numérico. No '
     'representa una transacción realizada.',
     'Numérico decimal', '7', 'Valores positivos. Rango observado: 16,90 a 59 999,00.', 'Soles (PEN)'),
    ('numero_cuotas',
     'Cantidad de cuotas indicada en el texto de financiamiento de la oferta.',
     'Numérico entero', '2', '6, 12 o nulo.', 'Cuotas'),
    ('monto_cuota',
     'Importe individual de cada cuota, extraído del texto de financiamiento y convertido a número.',
     'Numérico decimal', '6', 'Rango observado: 3,16 a 4 999,00; admite nulos.', 'Soles por cuota'),
    ('cuotas_texto',
     'Texto de financiamiento capturado en la tarjeta, conservado con espacios normalizados. Es la '
     'fuente de numero_cuotas y monto_cuota.',
     'Texto libre', '36', 'Ejemplo: 6 cuotas de S/ 808, 17 sin interés. Admite nulos.', '–'),
    ('pagina',
     'Número secuencial de la página recorrida por el scraper dentro de la búsqueda de origen.',
     'Numérico entero; metadato', '2', 'Enteros de 1 a 20.', 'Página'),
    ('posicion_pagina',
     'Posición de la tarjeta dentro del conjunto de tarjetas detectadas en la página, comenzando en 1. '
     'No equivale necesariamente a una posición orgánica del buscador.',
     'Numérico entero; metadato', '2', 'Enteros de 1 a 60.', 'Posición'),
    ('url_publicacion',
     'Enlace capturado en la tarjeta. Puede dirigir a una publicación, una página de producto de '
     'catálogo o una redirección publicitaria, e incluir parámetros de seguimiento.',
     'Texto, formato URL', '1 629', 'Direcciones HTTPS de Mercado Libre capturadas por el scraper.', '–'),
    ('url_fuente',
     'Dirección de la página de resultados desde la cual se extrajo la observación. Permite identificar '
     'la búsqueda y su paginación.',
     'Texto, formato URL', '120', 'Direcciones de https://listado.mercadolibre.com.pe/.', '–'),
    ('fecha_extraccion',
     'Fecha y hora registradas por el scraper al procesar la tarjeta. No incluye zona horaria.',
     'Temporal: fecha y hora', '19',
     'Formato AAAA-MM-DD HH:MM:SS. Desde 2026-09-13 19:54:05 hasta 2026-09-13 20:22:54.',
     'Precisión de segundos'),
]

NOTAS = [
    'Valores ausentes: numero_cuotas, monto_cuota y cuotas_texto contienen 55 nulos cada una, '
    'equivalentes al 1,25 % de los registros. Un nulo significa información no disponible; no demuestra '
    'ausencia de financiamiento. Las demás variables no presentan nulos.',
    'Identificadores: id_publicacion es la clave utilizada para deduplicar. id_extraido se conserva como '
    'referencia del proceso original y no debe interpretarse automáticamente como identificador de oferta.',
    'Categorías: las búsquedas pueden incluir accesorios y productos relacionados. Cuando una oferta '
    'apareció en varias búsquedas, se conservó la categoría de la observación seleccionada.',
    'Alcance: los datos describen ofertas observadas en páginas de resultados; no representan ventas, una '
    'muestra aleatoria del mercado ni una serie histórica.',
    'Tipos de datos: el CSV almacena representaciones de valores; los tipos numéricos y temporales deben '
    'interpretarse o declararse al cargarlo. Los decimales del archivo utilizan punto.',
]

doc.add_heading('Diccionario de datos', level=1)
par = doc.add_paragraph()
par.add_run('Archivo: ').bold = True
par.add_run('mercadolibre_limpio.csv. ')
par.add_run('Contenido: ').bold = True
par.add_run('4 412 registros y 14 variables. Cada registro corresponde a una oferta identificada mediante '
            'su URL. Cuando una oferta aparece varias veces, se conserva su última observación válida '
            'según fecha y orden.')

ENCABEZADOS = ['Variable', 'Descripción', 'Tipo', 'Tamaño máximo', 'Valores', 'Unidad']
ANCHOS = [2.8, 5.2, 2.8, 1.8, 4.2, 2.2]

t = doc.add_table(rows=1, cols=6)
t.style = 'Table Grid'
t.alignment = WD_TABLE_ALIGNMENT.CENTER
t.autofit = False
t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
for celda, texto, ancho in zip(t.rows[0].cells, ENCABEZADOS, ANCHOS):
    celda.width = Cm(ancho)
    tcpr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), 'D9D9D9')
    tcpr.append(shd)
    p0 = celda.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_after = Pt(2)
    run = p0.add_run(texto)
    run.bold = True
    run.font.size = Pt(9)

for fila in FILAS:
    celdas = t.add_row().cells
    for i, (celda, texto, ancho) in enumerate(zip(celdas, fila, ANCHOS)):
        celda.width = Cm(ancho)
        p0 = celda.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER if i in (3, 5) else WD_ALIGN_PARAGRAPH.LEFT
        run = p0.add_run(texto)
        run.font.size = Pt(9)

doc.add_paragraph()
par = doc.add_paragraph()
par.add_run('Notas de interpretación').bold = True
for i, nota in enumerate(NOTAS, start=1):
    q = doc.add_paragraph()
    q.paragraph_format.left_indent = Cm(0.75)
    q.paragraph_format.first_line_indent = Cm(-0.75)
    q.paragraph_format.space_after = Pt(4)
    q.add_run(f'{i}. ').bold = True
    r = q.add_run(nota)
    r.font.size = Pt(10)

SALIDA.parent.mkdir(parents=True, exist_ok=True)
doc.save(SALIDA)
print('guardado:', SALIDA)
