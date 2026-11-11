"""Genera el documento maestro de la Parte II sobre la plantilla oficial, en .docx y PDF.

Todas las cifras se leen de data/final/metricas.json y de los CSV finales; los textos de cada figura (pregunta y
lectura) los escribió el notebook que la generó. Uso: python scripts/generar_informe.py
(la exportación a PDF y la numeración del índice requieren Microsoft Word).
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generar_diccionarios as gd  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / 'indicaciones' / 'Formato Proyecto Final Parte II.docx'
FIGURAS = RAIZ / 'docs' / 'parte_2' / 'figuras'
SALIDA = RAIZ / 'docs' / 'parte_2' / 'informe' / 'Informe_Parte_II_DS3021.docx'
REPOSITORIO = 'https://github.com/josueroc/proyectoacd_mercadolibre'
FUENTE = 'Times New Roman'
ANCHO_UTIL_CM = 16.4

M = json.loads((RAIZ / 'data' / 'final' / 'metricas.json').read_text(encoding='utf-8'))
FIG = M['figuras']
NOMBRE = {'laptop': 'Laptop', 'monitor': 'Monitor', 'silla': 'Silla de oficina', 'teclado': 'Teclado',
          'mouse': 'Mouse', 'audifonos': 'Audífonos'}
ORDEN = list(NOMBRE)
INTEGRANTES = ['Yared Riveros Rodríguez', 'Franco Nicolás Roque Castillo', 'Mauricio Terán Taica', 'Josué Luna Rocha',
               'Alvaro Mauricio García Hurtado']


def soles(valor, decimales=0):
    texto = f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')
    return f'S/ {texto}'


def num(valor, decimales=1):
    texto = f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')
    return texto


def miles(valor):
    return f'{int(valor):,}'.replace(',', ' ')


# ---------------------------------------------------------------- diagrama del pipeline
def diagrama_pipeline():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis('off')
    etapas = [
        (0.15, 'Generación\nParte I', 'Mercado Libre Perú\nscraping\n(15/09 y 13/09)', '#e1e0d9'),
        (2.35, 'Ingestión\netapa 01', 'esquema\ntipado\nclave de oferta', '#cde2fb'),
        (4.55, 'Transformación\netapas 02–04', 'faltantes, atípicos\nintegración\nvariables, gamas', '#86b6ef'),
        (6.75, 'Almacenamiento\netapa 05', 'CSV UTF-8\nSQLite, 5 tablas\nmanifiesto', '#2a78d6'),
        (8.95, 'Serving\netapa 06', 'consultas SQL\nanálisis, figuras\ninsights', '#104281'),
    ]
    for x, titulo, detalle, color in etapas:
        oscuro = color in ('#2a78d6', '#104281')
        ax.add_patch(FancyBboxPatch((x, 1.6), 1.9, 2.3, boxstyle='round,pad=0.02,rounding_size=0.12',
                                    facecolor=color, edgecolor='white', linewidth=2))
        ax.text(x + 0.95, 3.45, titulo, ha='center', va='center', fontsize=10.5, fontweight='bold', linespacing=1.3,
                color='white' if oscuro else '#0b0b0b')
        ax.text(x + 0.95, 2.3, detalle, ha='center', va='center', fontsize=9.5, linespacing=1.4,
                color='white' if oscuro else '#0b0b0b')
    for x in (2.08, 4.28, 6.48, 8.68):
        ax.annotate('', xy=(x + 0.24, 2.75), xytext=(x - 0.02, 2.75),
                    arrowprops=dict(arrowstyle='-|>', color='#52514e', lw=1.6))
    ax.add_patch(FancyBboxPatch((0.15, 0.35), 10.7, 0.85, boxstyle='round,pad=0.02,rounding_size=0.1',
                                facecolor='#f0efec', edgecolor='none'))
    ax.text(5.5, 0.78, 'Corrientes transversales\norquestación (pipeline.py)  ·  calidad (assert por etapa)  ·  '
                       'trazabilidad (evidencia y balance)  ·  versionado (Git, SDD)',
            ha='center', va='center', fontsize=9.5, color='#52514e', linespacing=1.5)
    ax.set_title('Pipeline de datos de la Parte II según el ciclo de vida de la ingeniería de datos', loc='left',
                 fontsize=12, fontweight='bold')
    ruta = FIGURAS / 'f00_pipeline.png'
    fig.savefig(ruta, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    return ruta


# ---------------------------------------------------------------- utilidades de documento
def bordes(tabla):
    propiedades = tabla._tbl.tblPr
    caja = OxmlElement('w:tblBorders')
    for lado in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        borde = OxmlElement(f'w:{lado}')
        borde.set(qn('w:val'), 'single')
        borde.set(qn('w:sz'), '4')
        borde.set(qn('w:color'), '808080')
        caja.append(borde)
    # El esquema de Word fija el orden de tblPr: tblBorders va antes de tblLayout y tblLook.
    siguiente = propiedades.find(qn('w:tblLayout'))
    if siguiente is None:
        siguiente = propiedades.find(qn('w:tblLook'))
    siguiente.addprevious(caja) if siguiente is not None else propiedades.append(caja)


def sombrear(celda, color='D9D9D9'):
    sombra = OxmlElement('w:shd')
    sombra.set(qn('w:val'), 'clear')
    sombra.set(qn('w:fill'), color)
    celda._tc.get_or_add_tcPr().append(sombra)


def fuente(run, tam=12, negrita=False, cursiva=False):
    run.font.name = FUENTE
    run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), FUENTE)
    run.font.size = Pt(tam)
    run.bold = negrita
    run.italic = cursiva


def texto_en(parrafo, texto, tam=12, negrita=False, cursiva=False):
    """Admite **negrita** y `código` (monoespaciado) en línea."""
    for i, trozo in enumerate(texto.split('**')):
        for j, fragmento in enumerate(trozo.split('`')):
            if not fragmento:
                continue
            run = parrafo.add_run(fragmento)
            fuente(run, tam - 1 if j % 2 else tam, negrita or i % 2 == 1, cursiva)
            if j % 2:
                run.font.name = 'Consolas'
                run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:eastAsia'), 'Consolas')


class Escritor:
    """Inserta contenido después de un ancla, en orden, con el formato de la plantilla."""

    def __init__(self, doc, ancla):
        self.doc, self.cursor = doc, ancla._p
        self.figuras, self.tablas = 0, 0

    def _mover(self, elemento):
        self.cursor.addnext(elemento)
        self.cursor = elemento

    def parrafo(self, texto='', tam=12, negrita=False, cursiva=False, alineacion=WD_ALIGN_PARAGRAPH.JUSTIFY,
                antes=0, despues=6, sangria=None):
        p = self.doc.add_paragraph()
        p.alignment = alineacion
        formato = p.paragraph_format
        formato.space_before, formato.space_after, formato.line_spacing = Pt(antes), Pt(despues), 1.15
        if sangria:
            formato.left_indent, formato.first_line_indent = Cm(sangria), Cm(-sangria)
        texto_en(p, texto, tam, negrita, cursiva)
        self._mover(p._p)
        return p

    def subtitulo(self, texto):
        self.parrafo(texto, negrita=True, alineacion=WD_ALIGN_PARAGRAPH.LEFT, antes=8, despues=4)

    def vinetas(self, items, tam=12):
        for item in items:
            self.parrafo(f'–\t{item}', tam=tam, sangria=0.6, despues=3)

    def tabla(self, titulo, encabezados, filas, anchos, tam=10):
        self.tablas += 1
        self.parrafo(f'Tabla {self.tablas}. {titulo}', tam=10, cursiva=True, alineacion=WD_ALIGN_PARAGRAPH.LEFT,
                     antes=6, despues=2)
        t = self.doc.add_table(rows=1, cols=len(encabezados))
        bordes(t)
        t.autofit = False
        for celda, texto in zip(t.rows[0].cells, encabezados):
            sombrear(celda)
            texto_en(celda.paragraphs[0], texto, tam, negrita=True)
            celda.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        repetir = OxmlElement('w:tblHeader')
        repetir.set(qn('w:val'), 'true')
        t.rows[0]._tr.get_or_add_trPr().append(repetir)
        for fila in filas:
            celdas = t.add_row().cells
            for celda, texto in zip(celdas, fila):
                texto_en(celda.paragraphs[0], str(texto), tam)
                celda.paragraphs[0].paragraph_format.space_after = Pt(0)
        gd.fijar_anchos(t, anchos)
        self._mover(t._tbl)
        self.parrafo('', despues=4)

    def figura(self, nombre, ancho=ANCHO_UTIL_CM, pregunta=None, lectura=None):
        self.figuras += 1
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True
        p.add_run().add_picture(str(FIGURAS / f'{nombre}.png'), width=Cm(ancho))
        self._mover(p._p)
        datos = FIG.get(nombre, {})
        self.parrafo(f'Figura {self.figuras}. {pregunta or datos["pregunta"]}', tam=10, cursiva=True,
                     alineacion=WD_ALIGN_PARAGRAPH.CENTER, despues=4)
        if lectura or datos.get('lectura'):
            self.parrafo(f'**Lectura.** {lectura or datos["lectura"]}', tam=11, despues=10)

    def salto(self):
        p = self.doc.add_paragraph()
        p.add_run().add_break(WD_BREAK.PAGE)
        self._mover(p._p)


def poner(parrafo, texto):
    """Reemplaza el texto de un párrafo conservando el formato de su primer run."""
    for run in parrafo.runs[1:]:
        run._r.getparent().remove(run._r)
    parrafo.runs[0].text = texto


# ---------------------------------------------------------------- contenido
def identificacion(e):
    e.parrafo('**Título del proyecto:** ¿Cuánto cuesta equipar un home office en el Perú? Preprocesamiento, análisis y '
              'pipeline de datos de publicaciones de Mercado Libre Perú.')
    e.parrafo('La segunda parte se organizó por etapas del pipeline de datos. Cada etapa tiene un notebook propio y '
              'produce los archivos que necesita la siguiente, de modo que el aporte de cada integrante queda '
              'identificado en el repositorio.')
    p = e.parrafo('[Confirmar la distribución de responsabilidades y añadir la evidencia de cada integrante antes de '
                  'entregar.]', tam=11, cursiva=True)
    for run in p.runs:
        run.font.highlight_color = 7  # amarillo: recordatorio visible para el equipo
    e.tabla('Distribución de responsabilidades de la Parte II.',
            ['Integrante', 'Responsabilidad', 'Evidencia en el repositorio'],
            [[INTEGRANTES[0], 'Contexto y objetivos actualizados; flujo SDD; integración del repositorio.',
              'specs/001-…; README.md'],
             [INTEGRANTES[1], 'Ingestión, limpieza y orquestación del pipeline con almacenamiento en SQLite.',
              'notebooks/01_…; pipeline.py'],
             [INTEGRANTES[2], 'Valores faltantes y atípicos; integración y reducción.', 'notebooks/02_…; 03_…'],
             [INTEGRANTES[3], 'Transformación, ingeniería de características y diccionarios de datos.',
              'notebooks/04_…; docs/diccionarios/'],
             [INTEGRANTES[4], 'Análisis, visualización, insights, informe y presentación.',
              'notebooks/05_…; docs/parte_2/']],
            [4.6, 7.0, 4.8])


def contexto(e):
    lim, integ, ing = M['limpieza'], M['integracion'], M['ingesta']
    e.parrafo('La Ley N.º 31572, Ley del Teletrabajo, y su reglamento obligan al empleador a proveer los equipos del '
              'teletrabajador o a compensar el uso de equipos propios según su valor de mercado. En el Perú no existe '
              'una fuente pública que publique ese valor para una laptop, un monitor, una silla de oficina o unos '
              'audífonos. La Parte I construyó esa fuente con web scraping de Mercado Libre Perú: una captura de seis '
              f'componentes de home office ({miles(ing["filas_crudo_ho"])} registros, 15/09/2026) y una de cinco '
              f'categorías de contraste ({miles(ing["filas_crudo_cat"])} registros, 13/09/2026), y estimó un costo de '
              f'referencia de {soles(M["costos"]["suma_medianas_parte1"], 2)} como suma de medianas.')
    e.parrafo('El preprocesamiento de la Parte II cambió la lectura de esos datos en cinco puntos que actualizan el '
              'problema:')
    e.vinetas([
        f'**La unidad correcta es la oferta, no el producto de catálogo.** La Parte I identificó el home office por '
        f'código de catálogo ({miles(lim["unicos_por_catalogo_parte1"])} publicaciones). Con el identificador de la '
        f'oferta quedan {miles(lim["ofertas_unicas"] + sum(lim["ajenas"].values()))} ofertas únicas, y las dos capturas '
        f'comparten {integ["comunes_por_oferta"]} ofertas en lugar de {integ["comunes_por_catalogo"]}.',
        f'**Una búsqueda no equivale a un componente.** Las búsquedas traen accesorios, kits de teclado y mouse y '
        f'productos de otros componentes: se separaron {sum(lim["ajenas"].values())} publicaciones y se reasignaron '
        f'{lim["reasignadas"]}. Además, {lim["anuncios_patrocinados_crudo"]} de los registros crudos son anuncios '
        f'patrocinados insertados en los resultados.',
        '**Los datos ausentes no son aleatorios.** El precio anterior falta cuando no hay promoción y las reseñas '
        'faltan más en productos caros: ninguna columna con faltantes es MCAR.',
        '**Una cifra única oculta la dispersión.** El costo depende del nivel de equipamiento: un home office de gama '
        f'alta cuesta {num(M["costos"]["perfiles"]["alto"]["costo_mediano"] / M["costos"]["perfiles"]["económico"]["costo_mediano"])} '
        'veces uno de gama económica.',
        f'**Los precios son estables en el corto plazo.** El {num(integ["sin_cambio_pct"], 0)} % de las ofertas '
        'presentes en ambas capturas mantuvo su precio en dos días.',
    ])
    e.parrafo('Con esto, el problema se precisa: no basta con una referencia de costo; trabajadores y áreas de recursos '
              'humanos necesitan saber cuánto cuesta un home office **según el nivel de equipamiento**, qué componente '
              'concentra el gasto y qué señales del mercado —descuentos, cuotas, marca, reputación— ayudan o engañan al '
              'comprar.')


def objetivos(e):
    perf, lim = M['costos']['perfiles'], M['limpieza']
    e.subtitulo('3.1 Objetivo general')
    e.parrafo('Transformar las dos capturas de Mercado Libre Perú en un dataset final limpio, integrado y enriquecido, '
              'mediante un pipeline reproducible, para estimar el costo de equipar un home office en el Perú por '
              'componente, gama y perfil, y generar recomendaciones para trabajadores y áreas de recursos humanos.')
    e.subtitulo('3.2 Revisión de los objetivos de la Parte I')
    e.tabla('Objetivos específicos de la Parte I y su estado en la Parte II.', ['N.º', 'Objetivo de la Parte I', 'Estado', 'Motivo'],
            [['1', 'Verificar robots.txt antes de extraer.', 'Cumplido; no se repite', 'La Parte II no consulta el sitio.'],
             ['2', 'Extraer con Selenium y BeautifulSoup las seis búsquedas y las cinco de contraste.', 'Cumplido; no se repite',
              'Se parte de los CSV crudos de la Parte I.'],
             ['3', 'Aplicar pausas, User-Agent, manejo de errores y guardado incremental.', 'Cumplido; no se repite',
              'Pertenece a la extracción.'],
             ['4', 'Dataset final sin duplicados con 6 o más atributos.', 'Se ajusta',
              f'Se deduplica por oferta, no por catálogo, y se excluyen {sum(lim["ajenas"].values())} publicaciones que no '
              'son el componente.'],
             ['5', 'Menos de 10 % de nulos por columna.', 'Se ajusta',
              'Se mantiene para toda columna salvo las de nulo estructural o "no aplica", que se justifican.'],
             ['6', 'Documentar todas las variables.', 'Se mantiene', 'Diccionario inicial y final en el formato del curso.'],
             ['7', 'Estimar el costo de referencia como suma de medianas.', 'Se ajusta',
              'Una sola cifra oculta la dispersión: se estima por componente, gama y perfil.'],
             ['8', 'Notebook reproducible.', 'Se amplía', 'Pipeline orquestado de seis etapas con almacenamiento en SQLite.']],
            [0.9, 5.6, 3.0, 6.9], tam=9.5)
    e.subtitulo('3.3 Objetivos específicos de la Parte II')
    a, at, integ, car = M['analisis'], M['atipicos'], M['integracion'], M['caracteristicas']
    e.tabla('Objetivos específicos de la Parte II, indicadores y resultados.', ['N.º', 'Objetivo', 'Indicador', 'Resultado'],
            [['1', 'Diagnosticar y tratar los valores faltantes según su tipo.', 'Columnas con diagnóstico y estrategia',
              '100 %; ninguna MCAR'],
             ['2', 'Detectar y tratar atípicos univariados, bivariados y multivariados.', 'Atípicos detectados y decididos',
              f'{at["univariados"]} univariados y {at["kmeans"]} multivariados; {at["excluidos_por_error"]} excluido por error'],
             ['3', 'Integrar las dos capturas por oferta.', 'Ofertas comunes', f'{integ["comunes_por_oferta"]} (frente a {integ["comunes_por_catalogo"]} por catálogo)'],
             ['4', 'Construir variables derivadas y segmentar en gamas.', 'Variables derivadas', f'{car["variables_derivadas"]} variables; 3 gamas por componente'],
             ['5', 'Estimar el costo por componente, gama y perfil.', 'Perfiles con rango',
              f'{soles(perf["económico"]["costo_mediano"])} / {soles(perf["medio"]["costo_mediano"])} / {soles(perf["alto"]["costo_mediano"])}'],
             ['6', 'Formular insights accionables.', 'Insights con usuario, acción y cifra', f'{len(M["insights"]["lista"])}'],
             ['7', 'Construir un pipeline reproducible con almacenamiento.', 'Ejecución completa y determinista',
              'Seis etapas en menos de un minuto; salidas idénticas entre ejecuciones'],
             ['8', 'Documentar el dataset final.', 'Variables documentadas', f'{M["dataset_final"]["columnas"]} de {M["dataset_final"]["columnas"]}']],
            [0.9, 6.2, 4.3, 5.0], tam=9.5)


def dataset(e):
    df, final = M['dataset_final'], pd.read_csv(RAIZ / 'data' / 'final' / 'homeoffice_final.csv')
    e.parrafo(f'El dataset final, `data/final/homeoffice_final.csv`, contiene **{miles(df["filas"])} ofertas únicas** de '
              f'seis componentes de home office y **{df["columnas"]} variables**, una fila por oferta, en CSV con '
              f'codificación UTF-8. Conserva el {num(df["conservadas_pct"], 2)} % de las ofertas válidas del crudo (las que son '
              f'una unidad del componente) y el {num(df["conservadas_vs_todas_las_unicas_pct"])} % de todas las ofertas únicas, '
              'incluidos accesorios y combos.')
    conteo = pd.Series(M['limpieza']['ofertas_por_componente'])
    final_por = final['componente'].value_counts()
    e.tabla('Ofertas del dataset final por componente.', ['Componente', 'Ofertas', 'Precio mediano'],
            [[NOMBRE[c], miles(final_por[c]), soles(M['costos']['medianas_por_componente'][c])] for c in ORDEN],
            [6.0, 4.0, 6.4])
    e.parrafo('Las variables se agrupan en identificadores (`id_oferta`, `id_catalogo`), descripción del producto '
              '(`componente`, `titulo`, `marca` y especificaciones), precio y su transformación (`precio`, `log_precio`, '
              '`precio_relativo`, `gama`), condiciones comerciales (promoción, cuotas, envío, vendedor, anuncio), reputación '
              '(`calificacion`, `vendidos_min`), integración con la captura del 13/09 y metadatos de la captura.')
    e.parrafo(f'**Limitaciones.** Las columnas con más de 10 % de nulos lo son por diseño: las especificaciones solo aplican '
              f'a un componente, el precio anterior solo existe con promoción y la reputación no siempre se muestra. Ninguna '
              f'otra columna supera {num(df["max_nulos_no_justificado"], 2)} %. Las especificaciones se extraen del título, '
              'por lo que un título incompleto deja el valor nulo. La muestra proviene de páginas de resultados ordenadas por '
              'el sitio, no es aleatoria y describe precios publicados en un día, no transacciones.')
    e.subtitulo('Diccionario de datos final')
    e.parrafo('El diccionario completo se entrega en el formato del curso en `docs/diccionarios/diccionario_final.docx` '
              'y su PDF; el diccionario inicial del dataset crudo está en `docs/diccionarios/'
              'diccionario_inicial_homeoffice.docx`. La Tabla siguiente reproduce el diccionario final.')
    e.tabla('Diccionario de datos final.', ['Variable', 'Descripción', 'Tipo', 'Tamaño máximo', 'Valores', 'Unidad'],
            gd.filas_diccionario(final, gd.FINAL), [3.3, 4.6, 2.2, 1.5, 3.0, 1.8], tam=8)


def pipeline(e):
    e.parrafo('El pipeline sigue el ciclo de vida de la ingeniería de datos visto en el curso (U5_T1): generación, '
              'ingestión, transformación, almacenamiento y *serving*. Se ejecuta con una sola instrucción, '
              '`python pipeline.py`, que corre en orden los notebooks de cada etapa, carga el resultado en una base de '
              'datos y se detiene en la primera etapa que falla, indicando cuál y por qué.')
    e.figura('f00_pipeline', pregunta='Etapas del pipeline de datos y sus corrientes transversales.',
             lectura='Los datos crudos son de solo lectura; cada etapa valida su entrada con assert, registra lo que excluye '
                     'en data/evidencia/ y entrega un archivo a la siguiente.')
    balance = M['balance']
    e.tabla('Etapas del pipeline, entradas y salidas.', ['Etapa', 'Proceso', 'Entrada', 'Salida'],
            [['01 Ingestión', 'Validación de esquema, tipado, clave de oferta, deduplicación, publicaciones ajenas',
              f'2 CSV crudos ({miles(M["ingesta"]["filas_crudo_ho"])} + {miles(M["ingesta"]["filas_crudo_cat"])} filas)',
              f'{miles(balance["01_homeoffice"]["salida"])} ofertas limpias'],
             ['02 Transformación', 'Faltantes y atípicos', '01_homeoffice_limpio.csv', f'{miles(balance["02_homeoffice"]["salida"])} ofertas tratadas'],
             ['03 Transformación', 'Integración con la captura del 13/09 y reducción', '02_homeoffice_tratado.csv + categorías',
              'Dataset integrado; ofertas comunes'],
             ['04 Transformación', 'Transformación, variables derivadas, gamas y costos', '03_homeoffice_integrado.csv',
              'Dataset final; precios por gama; perfiles'],
             ['05 Almacenamiento', 'Carga en SQLite y manifiesto', 'CSV finales y evidencia', 'home_office.sqlite (5 tablas)'],
             ['06 Serving', 'Consultas SQL, análisis y figuras', 'home_office.sqlite', f'metricas.json; {len(FIG)} figuras']],
            [2.8, 5.2, 4.4, 4.0], tam=9.5)
    e.subtitulo('Justificación técnica')
    e.vinetas([
        '**Ingestión desde archivos planos.** Los CSV de la Parte I son la interfaz de ingestión (U5_T2): se leen como '
        'texto y se valida su esquema antes de transformarlos, para que un cambio de formato detenga el flujo.',
        '**Transformación en notebooks.** Cada decisión de limpieza vive junto a su justificación, que es lo que se '
        'evalúa; el orquestador solo ejecuta, no duplica la lógica.',
        '**Almacenamiento en SQLite.** En clase el ETL se construyó con SQL Server e Integration Services (U5_T3). Aquí se '
        'usa SQLite: es una base relacional consultable con SQL que no requiere servidor ni instalación, por lo que '
        'cualquier evaluador reproduce el flujo con `requirements.txt`. Las tablas tienen clave primaria y el pipeline '
        'comprueba que cada una tenga las filas esperadas.',
        '**Calidad y trazabilidad.** Cada etapa verifica con assert la unicidad del identificador, los rangos válidos y el '
        'balance de registros (entrada = salida + excluidos). Todo registro retirado queda en `data/evidencia/` con su '
        'motivo.',
        '**Reproducibilidad.** Semilla fija, escritura determinista y un manifiesto con el SHA-256 de cada CSV final: dos '
        'ejecuciones completas producen archivos idénticos.',
    ])


def preprocesamiento(e):
    lim, fal, at, integ, bal = M['limpieza'], M['faltantes'], M['atipicos'], M['integracion'], M['balance']
    e.subtitulo('6.1 Limpieza de niveles 1 y 2')
    e.parrafo('Se validó que ambos crudos tuvieran exactamente las columnas esperadas, con nombres codificables, y se '
              'convirtieron los textos a tipos con expresiones regulares ancladas: precios en formato peruano, descuento '
              '"NN% OFF", cuotas "N cuotas de S/ X sin interés", reseñas "4.8 | +100 vendidos" y condición de envío. '
              f'Todos los textos presentes se convirtieron ({lim["textos_no_interpretables"]} no interpretables). La Parte I '
              'había leído "+100 vendidos" como número de opiniones y dejó esa columna vacía; aquí se corrige como '
              'unidades vendidas.')
    e.parrafo(f'Se recuperó el identificador de cada oferta (parámetro `wid` de la URL) y se deduplicó por oferta, '
              f'retirando {miles(lim["duplicados"])} repeticiones; {lim["ofertas_con_varios_codigos"]} ofertas aparecían con '
              'dos códigos de catálogo distintos. Después se separaron las publicaciones que no son una unidad del '
              'componente, con una regla revisada a mano: buscar palabras sueltas daba falsos positivos ("switch" aparece '
              'en teclados mecánicos legítimos).')
    aj = lim['ajenas']
    e.tabla('Publicaciones separadas por no ser una unidad del componente.', ['Tipo', 'Publicaciones', 'Tratamiento'],
            [['Accesorio o repuesto (fundas, soportes, pistones, almohadillas…)', aj['accesorio'], 'Se excluye'],
             ['Combo de varios componentes (kits de teclado y mouse)', aj['combo de varios componentes'],
              'Se excluye del costo; se analiza aparte'],
             ['Otro producto (tabletas, iPad…)', aj['otro producto'], 'Se excluye'],
             ['Producto de otro componente (laptops en la búsqueda de audífonos…)', lim['reasignadas'],
              'Se reasigna al componente correcto']],
            [8.2, 2.6, 5.6])
    e.parrafo(f'Se registraron {sum(lim["inconsistencias"].values())} inconsistencias entre campos —precio anterior no '
              'mayor que el actual y descuento anunciado distinto del calculado—; el total de las cuotas coincide con el '
              'precio en todas las publicaciones.')
    e.subtitulo('6.2 Valores faltantes (limpieza de nivel 3)')
    e.parrafo('Para cada columna se probó si el hecho de faltar es independiente del componente, de la página de '
              'resultados y de si la publicación es un anuncio (prueba chi-cuadrado, U3_L3), y se comparó la mediana del '
              'precio con y sin el dato. Ninguna columna resultó MCAR.')
    filas = []
    tipo = {'precio_anterior': ('MNAR estructural', 'Imputar por estructura: descuento 0 % con indicador'),
            'numero_cuotas': ('MNAR estructural', 'Indicador ofrece_cuotas; nulo "no aplica"'),
            'calificacion': ('MAR', 'Ignorar: indicador tiene_resenas, sin imputar'),
            'vendidos_min': ('MAR', 'Ignorar: indicador tiene_resenas, sin imputar'),
            'vendedor': ('MAR', 'Categoría "no informado" e indicador'),
            'envio': ('MAR', 'Categoría "no informado"')}
    for col, (t, estrategia) in tipo.items():
        d = fal['diagnostico'][col]
        filas.append([col, f'{num(d["pct"])} %', f'{d["p_componente"]:.1e}', f'{d["p_pagina"]:.1e}',
                      soles(d['mediana_con']), soles(d['mediana_sin']), t, estrategia])
    e.tabla('Diagnóstico y tratamiento de los valores faltantes.',
            ['Columna', '% falta', 'p comp.', 'p página', 'Mediana con dato', 'Mediana sin dato', 'Tipo', 'Estrategia'],
            filas, [2.3, 1.3, 1.5, 1.5, 1.7, 1.7, 1.9, 4.5], tam=8)
    e.parrafo('Eliminar filas se descartó en todos los casos: los faltantes dependen del componente y del precio, y '
              'borrarlos sesgaría la muestra. Imputar la calificación con la mediana del componente también se descartó: '
              f'eleva la proporción del valor más repetido a {num(fal["contraste_calificacion"]["moda_pct_imputada"], 0)} % y '
              'atribuye a productos caros la reputación de los baratos. La columna `etiqueta_texto`, vacía en toda la '
              f'captura, se eliminó. Además se anularon {fal["promociones_anuladas"]} promociones cuyo "precio anterior" no '
              'superaba al actual.')
    e.figura('f02_faltantes_por_componente', ancho=14.5)
    e.figura('f02_precio_segun_faltante')
    e.subtitulo('6.3 Valores atípicos')
    e.parrafo('El precio tiene cola derecha en todos los componentes, por lo que los criterios se aplicaron sobre el '
              'logaritmo del precio y por componente: rango intercuartílico con factor 1,5 y |z| > 3 (univariados), '
              'diagramas de dispersión de relaciones que deben cumplirse (bivariados) y K-Means con contraste de '
              'Mahalanobis (multivariados), como en U3_L5. Solo se elimina un error comprobable: un precio de relleno '
              '(cinco o más nueves), un precio incoherente con el financiamiento o un precio que el título contradice. '
              f'Con esa regla se excluyó {at["excluidos_por_error"]} publicación —una laptop de 8 GB de RAM a S/ 29 000, '
              f'sobre el percentil 99 de las laptops ({soles(at["p99_laptop"])}), la misma oferta que la Parte I ya había '
              f'excluido— y se conservaron {at["conservados_marcados"]} extremos plausibles marcados en `atipico_precio`.')
    for nombre in ('f02_atipicos_univariados', 'f02_bivariado_promocion', 'f02_atipicos_multivariados'):
        e.figura(nombre, ancho=14.5 if nombre != 'f02_atipicos_multivariados' else ANCHO_UTIL_CM)
    e.subtitulo('6.4 Integración')
    e.parrafo('Se integró el home office con la captura de categorías en la dirección "agregar atributos" (U3_T4): a cada '
              'oferta se le añade su precio del 13/09 y la variación respecto del 15/09. Ante un conflicto prevalece el home '
              'office, que es la captura más reciente y con más atributos. La dirección "agregar objetos" se descartó porque '
              'las ofertas que solo están en categorías no tienen descuento, reseñas ni envío y pertenecen a otra fecha.')
    e.tabla('Desafíos de la integración de datos y cómo se resolvieron.', ['Desafío (U3_T4)', 'Situación en estos datos', 'Tratamiento'],
            [['Identificación de entidades', 'La misma oferta aparecía con códigos de catálogo distintos.', 'Clave de oferta (wid) en ambas fuentes.'],
             ['Formato de índice no coincidente', 'Catálogo en home office y oferta en categorías.',
              f'Mismo formato: {integ["comunes_por_oferta"]} comunes frente a {integ["comunes_por_catalogo"]}.'],
             ['Datos sin sentido', 'Celulares, televisores y refrigeradoras no son home office.', 'Solo se usan las ofertas comunes.'],
             ['Desajuste de agregación', 'Fechas, páginas y búsquedas distintas.', 'Se compara oferta por oferta; no se suman capturas.'],
             ['Objetos duplicados', 'Riesgo de multiplicar filas al unir.', 'merge validado uno a uno; filas sin cambio.'],
             ['Redundancia', 'busqueda y componente repiten información (V de Cramér 0,995).', 'Se retira busqueda.']],
            [3.6, 6.4, 6.4], tam=9.5)
    e.figura('f03_clave_de_union', ancho=14.5)
    e.figura('f03_variacion_precio', ancho=14.5)
    e.subtitulo('6.5 Reducción y transformación')
    e.parrafo('La reducción retiró la única columna redundante (`busqueda`) y la columna vacía (`etiqueta_texto`). Las '
              'columnas muy correlacionadas que se conservaron tienen un uso propio: `monto_cuota` es la cifra que el usuario '
              'paga cada mes y `descuento_anunciado_pct` permite detectar promociones que exageran el ahorro. Las '
              'transformaciones —logaritmo del precio, puntuación Z dentro del componente, codificación binaria del envío y '
              'discretización en gamas— se describen en la sección siguiente.')
    filas = [[etapa.replace('_', ' '), miles(v['entrada']), miles(v['salida']),
              ', '.join(f'{k.replace("_", " ")}: {miles(n)}' for k, n in v.items() if k not in ('entrada', 'salida')) or '—']
             for etapa, v in bal.items()]
    e.tabla('Balance de registros por etapa (entrada = salida + excluidos).', ['Etapa', 'Entrada', 'Salida', 'Excluidos'],
            filas, [4.0, 2.2, 2.2, 8.0], tam=9.5)


def feature_engineering(e):
    car = M['caracteristicas']
    e.parrafo('La ingeniería de características (U4_L1, U3_L7) tuvo dos propósitos: hacer comparables los precios de '
              'componentes distintos y describir cada oferta con atributos que expliquen su precio.')
    e.subtitulo('7.1 Transformaciones')
    e.vinetas([
        '**Logaritmo del precio** (`log_precio`): corrige la cola derecha; los criterios de atípicos y los gráficos de precio '
        'se trabajan en esta escala.',
        '**Puntuación Z dentro del componente** (`precio_relativo`): cuántas desviaciones se aleja una oferta del precio '
        'típico de su componente; permite comparar un mouse con una laptop.',
        '**Codificación binaria** del envío (`get_dummies`), resumida en `envio_gratis` y `entrega_manana`.',
        '**Discretización por igual frecuencia** (`qcut`): terciles de precio por componente → `gama` económica, media o alta.',
    ])
    e.subtitulo('7.2 Variables derivadas')
    inventario = [
        ['marca', 'Primera marca reconocida en el título', 'Prima de marca'],
        ['ram_gb, almacenamiento_gb', 'Memoria y disco en el título (laptop)', 'Precio frente a especificación'],
        ['pulgadas', 'Tamaño en el título (monitor)', 'Validación de gamas'],
        ['inalambrico, ergonomica', 'Conexión inalámbrica; silla ergonómica', 'Sobreprecio por característica'],
        ['es_gamer', '"gamer" o "gaming" en el título', 'Sobreprecio gamer'],
        ['tiene_descuento, descuento_pct', 'Promoción y descuento calculado con los precios', 'Efecto de las promociones'],
        ['descuento_inflado', 'Descuento anunciado mayor que el calculado', 'Promociones engañosas'],
        ['ofrece_cuotas', 'La tarjeta informa cuotas', 'Peso del financiamiento'],
        ['tiene_resenas, vendidos_min', 'Reseñas presentes; cota inferior de vendidos', 'Popularidad frente a precio'],
        ['envio_gratis, entrega_manana', 'Condiciones de envío', 'Costo total de compra'],
        ['vendedor_visible, tienda_de_marca', 'Tienda visible; tienda de la marca', 'Tipo de vendedor'],
        ['es_publicidad', 'Anuncio patrocinado', 'Anuncios frente a resultados orgánicos'],
        ['en_ambas_capturas, variacion_precio_pct', 'Integración con el 13/09', 'Estabilidad de precios'],
        ['gama, precio_relativo, atipico_precio', 'Tercil, puntuación Z y extremo plausible', 'Costos por gama y perfil'],
    ]
    e.tabla(f'Variables derivadas ({car["variables_derivadas"]} en total), regla y uso en el análisis.',
            ['Variable', 'Regla', 'Uso'], inventario, [5.2, 6.4, 4.8], tam=9.5)
    cs = car['cobertura_specs']
    e.parrafo(f'La extracción desde el título cubre el {num(cs["ram_gb"])} % de las laptops en RAM, el '
              f'{num(cs["almacenamiento_gb"])} % en almacenamiento y el {num(cs["pulgadas"])} % de los monitores en tamaño. '
              f'La marca se reconoce en más del 79 % de las publicaciones de cada componente, salvo en sillas '
              f'({num(car["cobertura_marca"]["silla"])} %), que suelen venderse con nombres de modelo.')
    e.subtitulo('7.3 Gamas')
    lim_g = car['limites_gama']
    e.tabla('Límites de las gamas por componente (percentiles 33,3 y 66,7 del precio).',
            ['Componente', 'Económica hasta', 'Media hasta', 'Coincidencia con K-Means'],
            [[NOMBRE[c], soles(lim_g[c]['económica hasta'], 2), soles(lim_g[c]['media hasta'], 2),
              f'{num(car["coincidencia_qcut_kmeans"][c])} %'] for c in ORDEN],
            [4.4, 4.0, 4.0, 4.0])
    n_gama = pd.read_csv(RAIZ / 'data' / 'final' / 'precios_por_gama.csv')['n']
    e.parrafo(f'Se eligió igual frecuencia porque garantiza entre {n_gama.min()} y {n_gama.max()} publicaciones por gama '
              'y medianas estables; la '
              'discretización por K-Means sobre el log-precio coincide en la mayoría de los componentes. La validación con '
              'variables distintas del precio se muestra a continuación.')
    e.figura('f04_validacion_gamas')


def analisis(e):
    e.parrafo('El análisis lee el almacén SQLite (etapa *serving*) y responde una pregunta por gráfico. Para comparar '
              'grupos se usaron pruebas basadas en rangos (Mann-Whitney y Spearman), porque los precios no siguen una '
              'distribución normal.')
    secciones = [('8.1 Costo del home office', ['f05_costo_perfiles', 'f05_composicion_perfiles', 'f05_precio_por_gama']),
                 ('8.2 Promociones y financiamiento', ['f05_promociones', 'f05_cuotas']),
                 ('8.3 Reputación, marca y etiqueta "gamer"', ['f05_reputacion', 'f05_gamer', 'f05_laptops'])]
    for titulo, figuras in secciones:
        e.subtitulo(titulo)
        for nombre in figuras:
            e.figura(nombre)
    pg = pd.DataFrame(M['analisis']['precios_por_gama'])
    e.tabla('Precio mediano por componente y gama.', ['Componente', 'Económica', 'Media', 'Alta'],
            [[NOMBRE[c], soles(pg.loc['económica', c]), soles(pg.loc['media', c]), soles(pg.loc['alta', c])] for c in ORDEN],
            [5.2, 3.7, 3.7, 3.8])
    v = M['analisis']['vendedor']
    e.subtitulo('8.4 Anomalías y tipo de vendedor')
    e.parrafo(f'Los anuncios patrocinados tienen un precio relativo mediano de {num(v["anuncio patrocinado"]["mediana sí"], 2)} '
              f'frente a {num(v["anuncio patrocinado"]["mediana no"], 2)} de los resultados orgánicos (p = '
              f'{v["anuncio patrocinado"]["p (Mann-Whitney)"]:.1e}): son más baratos que el resto de su componente. Las '
              f'tiendas de la propia marca venden algo más caro (mediana {num(v["tienda de la marca"]["mediana sí"], 2)} '
              f'frente a {num(v["tienda de la marca"]["mediana no"], 2)}). Entre las anomalías, se conservaron '
              f'{M["atipicos"]["conservados_marcados"]} precios extremos plausibles y solo '
              f'{M["caracteristicas"]["descuento_inflado"]} de {miles(M["caracteristicas"]["con_descuento"])} promociones '
              'anuncian un descuento mayor que el real.')


def insights(e):
    filas = [[i['usuario'], i['hallazgo'], i['accion'], i['cifra']] for i in M['insights']['lista']]
    e.parrafo('Cada insight indica a qué usuario sirve, qué acción recomienda y la cifra calculada que lo respalda.')
    e.tabla('Insights y recomendaciones.', ['Usuario', 'Hallazgo', 'Recomendación', 'Respaldo'], filas,
            [2.8, 5.2, 4.6, 3.8], tam=9)


def conclusiones(e):
    perf, integ, fal = M['costos']['perfiles'], M['integracion'], M['faltantes']
    a = M['analisis']
    e.vinetas([
        f'**Costo del home office.** Equipar un home office en el Perú cuesta {soles(perf["económico"]["costo_mediano"])} en '
        f'gama económica, {soles(perf["medio"]["costo_mediano"])} en gama media y {soles(perf["alto"]["costo_mediano"])} en '
        f'gama alta. La cifra única de la Parte I coincide con el perfil medio, pero un presupuesto o una compensación '
        'deben fijarse por perfil.',
        f'**Dónde se concentra el gasto.** La laptop representa entre {num(min(a["composicion_laptop_pct"].values()), 0)} % y '
        f'{num(max(a["composicion_laptop_pct"].values()), 0)} % del costo; la gama de la laptop es la decisión que más mueve '
        'el presupuesto.',
        '**Preprocesamiento.** Identificar por oferta, separar lo que no es el componente y diagnosticar el tipo de cada '
        f'faltante cambiaron el dataset: {integ["comunes_por_oferta"]} ofertas comunes entre capturas en lugar de '
        f'{integ["comunes_por_catalogo"]}, {sum(M["limpieza"]["ajenas"].values())} publicaciones ajenas fuera del costo y '
        'ninguna imputación que sesgue la reputación.',
        '**Señales del mercado.** El descuento no indica precio bajo, las cuotas sin interés no encarecen, lo más vendido '
        'no es lo mejor calificado y la etiqueta "gamer" encarece laptops y periféricos, pero no monitores ni sillas.',
        '**Pipeline.** El flujo completo se reproduce con una instrucción, en menos de un minuto, con salidas idénticas '
        'entre ejecuciones y trazabilidad de cada registro excluido.',
    ])
    e.subtitulo('Limitaciones')
    e.vinetas([
        'Cada captura es de un solo día y entre ellas hay dos días: no hay serie histórica de precios.',
        'La muestra son páginas de resultados ordenadas por el sitio, no una muestra aleatoria del mercado.',
        f'La reputación falta en {num(fal["diagnostico"]["calificacion"]["pct"], 0)} % de las publicaciones y de forma no '
        'aleatoria: los análisis de calificación y ventas describen sobre todo a los productos más baratos.',
        'Las especificaciones dependen de que el título las mencione; las gamas se definen por precio y se validan con '
        'especificaciones solo de forma parcial.',
        'Los precios son publicados, no de venta, y no incluyen el costo de envío cuando no es gratuito.',
    ])
    e.parrafo('Como trabajo futuro, capturas periódicas permitirían medir la evolución de precios y actualizar la '
              'referencia de compensación con fecha.')


def documentacion(e):
    commits = subprocess.run(['git', '-C', str(RAIZ), 'rev-list', '--count', 'HEAD'], capture_output=True,
                             text=True).stdout.strip()
    e.parrafo(f'El repositorio oficial es {REPOSITORIO}. Contiene `README.md` con el problema, la estructura, la '
              'instalación y la ejecución paso a paso; `requirements.txt` con las dependencias; y las carpetas que exige el '
              'enunciado.')
    e.tabla('Estructura del repositorio.', ['Ruta', 'Contenido'],
            [['data/ec1_homeoffice/, data/crudos/', 'Dataset inicial: CSV crudos de las dos capturas (solo lectura)'],
             ['data/intermedio/, data/evidencia/', 'Salidas de cada etapa y registros excluidos con su motivo'],
             ['data/final/', 'Dataset final, precios por gama, perfiles, almacén SQLite, métricas y manifiesto'],
             ['notebooks/01_… a 05_…', 'Un notebook por etapa del pipeline, con nombre descriptivo'],
             ['pipeline.py', 'Orquestador del pipeline (python pipeline.py)'],
             ['docs/diccionarios/', 'Diccionarios de datos inicial y final (.docx y PDF)'],
             ['docs/parte_2/', 'Documento maestro, presentación y figuras'],
             ['specs/001-…, .specify/', 'Especificación, plan, tareas y evaluación del flujo SDD'],
             ['scripts/', 'Generadores de diccionarios, informe y presentación']],
            [6.0, 10.4], tam=9.5)
    e.parrafo('**Reproducción.** Con Python 3.11: `pip install -r requirements.txt` y `python pipeline.py`. El flujo '
              'completo tarda menos de un minuto; `data/final/manifiesto.json` guarda el SHA-256 de cada CSV final para '
              'comprobar que una nueva ejecución produce los mismos archivos. Los documentos se regeneran con '
              '`python scripts/generar_informe.py`.')
    e.parrafo(f'**Control de versiones.** El trabajo se desarrolló con un flujo de desarrollo guiado por especificaciones '
              '(SDD): especificación, aclaraciones, evaluación, plan, checklist y tareas en `specs/`, aprobación y luego '
              f'implementación en la rama `feature/parte-2-preprocesamiento`, con commits por etapa en formato Conventional '
              f'Commits ({commits} commits en total en el repositorio al generar este informe).')


SECCIONES = {
    'IDENTIFICACIÓN': identificacion,
    'CONTEXTO ACTUALIZADO': contexto,
    'OBJETIVOS ACTUALIZADOS': objetivos,
    'DATASET Y DICCIONARIO DE DATOS FINAL': dataset,
    'PROPUESTA DE PIPELINE': pipeline,
    'PREPROCESAMIENTO DE DATOS': preprocesamiento,
    'FEATURE ENGINEERING': feature_engineering,
    'ANÁLISIS Y VISUALIZACIÓN DE DATOS': analisis,
    'INSIGHTS ENCONTRADOS': insights,
    'CONCLUSIONES': conclusiones,
    'DOCUMENTACIÓN Y REPRODUCIBILIDAD EN GITHUB': documentacion,
}


def construir():
    diagrama_pipeline()
    doc = Document(PLANTILLA)
    parrafos = doc.paragraphs

    # Carátula
    poner(parrafos[6], '¿CUÁNTO CUESTA EQUIPAR UN HOME OFFICE EN EL PERÚ?')
    p_sub = copy.deepcopy(parrafos[6]._p)
    parrafos[6]._p.addnext(p_sub)
    from docx.text.paragraph import Paragraph
    sub = Paragraph(p_sub, parrafos[6]._parent)
    poner(sub, 'Preprocesamiento, análisis y pipeline de datos de Mercado Libre Perú')
    sub.runs[0].font.size = Pt(14)
    for parrafo, nombre in zip(parrafos[12:17], INTEGRANTES):
        poner(parrafo, nombre)
        parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for indice in (8, 9, 11):  # "CURSO:", nombre del curso y "ESTUDIANTES:" centrados como el resto
        parrafos[indice].alignment = WD_ALIGN_PARAGRAPH.CENTER
        poner(parrafos[indice], parrafos[indice].text.strip())

    def texto_de(elemento):  # texto visible; itertext() incluye nodos de propiedades que Word no muestra
        return Paragraph(elemento, doc._body).text.strip() if elemento.tag == qn('w:p') else None

    # Espacios vacíos entre el índice y la primera sección
    cuerpo = doc.element.body
    tabla_indice = doc.tables[0]._tbl
    siguiente = tabla_indice.getnext()
    while siguiente is not None and texto_de(siguiente) == '':
        eliminar, siguiente = siguiente, siguiente.getnext()
        cuerpo.remove(eliminar)

    encabezados = [p for p in doc.paragraphs if p.text.strip() in SECCIONES]
    assert len(encabezados) == len(SECCIONES), 'La plantilla no tiene las once secciones esperadas.'
    for numero, encabezado in enumerate(encabezados, start=1):
        instruccion = encabezado._p.getnext()
        while instruccion is not None and instruccion.tag == qn('w:p') and texto_de(instruccion) not in SECCIONES:
            eliminar, instruccion = instruccion, instruccion.getnext()
            cuerpo.remove(eliminar)
        if numero > 1:
            salto = doc.add_paragraph()
            salto.add_run().add_break(WD_BREAK.PAGE)
            encabezado._p.addprevious(salto._p)
        else:
            encabezado.paragraph_format.page_break_before = True
        # La plantilla numera los encabezados con una lista automática de Word: no se antepone número.
        escritor = Escritor(doc, encabezado)
        SECCIONES[encabezado.text.strip()](escritor)

    # La plantilla ya numera las páginas en el encabezado.
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    doc.save(SALIDA)
    print(f'{SALIDA.relative_to(RAIZ)} generado')
    return list(SECCIONES)


def numerar_y_exportar(titulos):
    """Con Word: escribe la página de cada sección en el índice de la plantilla y exporta a PDF."""
    try:
        import win32com.client
    except ImportError:
        print('Sin Microsoft Word (pywin32): el índice queda sin números de página y no se exporta a PDF.')
        return
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible, word.DisplayAlerts = False, 0
    documento = None
    try:
        documento = word.Documents.Open(str(SALIDA.resolve()))
        documento.Repaginate()
        indice = documento.Tables(1)
        inicio = indice.Range.End
        for fila, titulo in enumerate(titulos, start=2):
            rango = documento.Range(inicio, documento.Content.End)
            buscador = rango.Find
            buscador.ClearFormatting()
            assert buscador.Execute(FindText=titulo, MatchCase=True), f'No se encontró la sección {titulo}'
            indice.Cell(fila, 3).Range.Text = str(rango.Information(1))
        documento.Save()
        documento.SaveAs2(str(SALIDA.with_suffix('.pdf').resolve()), FileFormat=17)
        print(f'{SALIDA.with_suffix(".pdf").relative_to(RAIZ)} exportado ({documento.ComputeStatistics(2)} páginas)')
    finally:
        # Cerrar siempre el documento: si queda abierto, Word de automatización sigue vivo y bloquea el archivo.
        if documento is not None:
            documento.Close(SaveChanges=0)
        word.Quit(SaveChanges=0)


if __name__ == '__main__':
    titulos = construir()
    if '--sin-pdf' not in sys.argv:
        numerar_y_exportar(titulos)
