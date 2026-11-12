"""Genera los diccionarios de datos sobre la plantilla oficial del curso, en .docx y PDF.

- docs/diccionarios/diccionario_inicial_homeoffice: las 17 columnas del CSV crudo del home office.
- docs/diccionarios/diccionario_final: las columnas de data/final/homeoffice_final.csv.

Tamaño máximo y valores se calculan con los datos; descripción, tipo y unidad están definidos abajo.
Uso: python scripts/generar_diccionarios.py   (la exportación a PDF requiere Microsoft Word)
"""
import copy
import json
import sys
from pathlib import Path

import pandas as pd
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

RAIZ = Path(__file__).resolve().parent.parent
PLANTILLA = RAIZ / 'indicaciones' / 'Formato Diccionario de datos Parte II.docx'
SALIDA = RAIZ / 'docs' / 'diccionarios'

# variable: (descripción, tipo, unidad)
FINAL = {
    'id_oferta': ('Identificador de la oferta: parámetro wid de la URL o código de una ruta directa; con el prefijo CAT- cuando solo existe el código de catálogo. Clave de deduplicación e integración.', 'Categórico nominal (texto)', '–'),
    'id_catalogo': ('Código de producto de catálogo que usó la Parte I; varias ofertas pueden compartirlo.', 'Categórico nominal (texto)', '–'),
    'componente': ('Componente del home office. Proviene de la búsqueda y se corrigió cuando el título mostraba otro producto.', 'Categórico nominal', '–'),
    'titulo': ('Título de la publicación con espacios normalizados.', 'Texto libre', '–'),
    'marca': ('Primera marca reconocida en el título; "otra" si no se reconoce.', 'Categórico nominal', '–'),
    'precio': ('Precio publicado al momento de la captura.', 'Numérico continuo', 'Soles (PEN)'),
    'log_precio': ('Logaritmo en base 10 del precio.', 'Numérico continuo', 'log10(S/)'),
    'precio_relativo': ('Puntuación Z del log-precio dentro del componente: desviaciones respecto del precio típico del componente.', 'Numérico continuo', 'Desviaciones estándar'),
    'gama': ('Tercil de precio calculado dentro de cada componente mediante qcut: económica, media o alta; contrastado con K-Means y especificaciones técnicas.', 'Categórico ordinal', '–'),
    'atipico_precio': ('Precio atípico univariado (IQR o |z| > 3 sobre el log-precio) que se conservó por plausible.', 'Booleano', '–'),
    'precio_anterior': ('Precio tachado de la promoción. Nulo cuando no hay promoción (faltante estructural).', 'Numérico continuo', 'Soles (PEN)'),
    'tiene_descuento': ('La publicación muestra un precio anterior mayor que el actual.', 'Booleano', '–'),
    'descuento_pct': ('Descuento calculado con los precios; 0 sin promoción (imputación estructural marcada por tiene_descuento).', 'Numérico continuo', '%'),
    'descuento_anunciado_pct': ('Descuento que anuncia la tarjeta ("NN% OFF"). Nulo sin promoción.', 'Numérico discreto', '%'),
    'descuento_inflado': ('El descuento anunciado supera al calculado en más de 1,5 puntos.', 'Booleano', '–'),
    'ofrece_cuotas': ('La tarjeta informa pago en cuotas.', 'Booleano', '–'),
    'numero_cuotas': ('Número de cuotas sin interés. Nulo si no ofrece cuotas (faltante estructural).', 'Numérico discreto', 'Cuotas'),
    'monto_cuota': ('Monto de cada cuota. Nulo si no ofrece cuotas.', 'Numérico continuo', 'Soles por cuota'),
    'tiene_resenas': ('La tarjeta muestra calificación o unidades vendidas.', 'Booleano', '–'),
    'calificacion': ('Calificación promedio de los compradores. Nula cuando la tarjeta no la muestra (MAR, sin imputar).', 'Numérico continuo', 'Puntos (1 a 5)'),
    'vendidos_min': ('Unidades vendidas: cota inferior del texto "+N vendidos". Nula cuando no se muestra (MAR).', 'Numérico discreto', 'Unidades'),
    'envio': ('Condición de envío de la tarjeta.', 'Categórico nominal', '–'),
    'envio_gratis': ('El envío es gratuito.', 'Booleano', '–'),
    'entrega_manana': ('La tarjeta promete entrega al día siguiente.', 'Booleano', '–'),
    'vendedor': ('Nombre de la tienda; "no informado" cuando la tarjeta no lo muestra.', 'Categórico nominal', '–'),
    'vendedor_visible': ('La tarjeta muestra el nombre de la tienda.', 'Booleano', '–'),
    'tienda_de_marca': ('El nombre de la tienda contiene la marca del producto.', 'Booleano', '–'),
    'es_publicidad': ('La URL es un anuncio patrocinado (redirección mclics).', 'Booleano', '–'),
    'es_gamer': ('Indicador de presencia de "gamer" o "gaming" en el título; permite comparar precios entre publicaciones con y sin esa etiqueta.', 'Booleano', '–'),
    'ram_gb': ('Memoria RAM según el título. Solo laptops; nulo en los demás componentes.', 'Numérico discreto', 'GB'),
    'almacenamiento_gb': ('Almacenamiento según el título. Solo laptops.', 'Numérico discreto', 'GB'),
    'pulgadas': ('Tamaño de pantalla según el título. Solo monitores.', 'Numérico continuo', 'Pulgadas'),
    'inalambrico': ('El título indica conexión inalámbrica. Solo teclado, mouse y audífonos.', 'Booleano', '–'),
    'ergonomica': ('El título indica silla ergonómica. Solo sillas.', 'Booleano', '–'),
    'en_ambas_capturas': ('La oferta también figura en la captura de categorías del 13/09/2026.', 'Booleano', '–'),
    'precio_13_09': ('Precio de la misma oferta el 13/09/2026. Solo ofertas presentes en ambas capturas.', 'Numérico continuo', 'Soles (PEN)'),
    'variacion_precio_pct': ('Variación del precio entre el 13/09 y el 15/09. Solo ofertas presentes en ambas capturas.', 'Numérico continuo', '%'),
    'pagina': ('Página de resultados en la que apareció la oferta.', 'Numérico discreto (metadato)', 'Página'),
    'posicion_pagina': ('Posición de la tarjeta dentro de la página.', 'Numérico discreto (metadato)', 'Posición'),
    'url_publicacion': ('Enlace de la publicación, con parámetros de seguimiento.', 'Texto (URL)', '–'),
    'fecha_extraccion': ('Fecha y hora de la captura, sin zona horaria.', 'Fecha y hora', 'Segundos'),
}

INICIAL = {
    'categoria': ('Búsqueda del scraper (laptops, monitores, sillas-de-oficina, teclados, mouse, audifonos).', 'Categórico nominal', '–'),
    'pagina': ('Página de resultados recorrida.', 'Numérico discreto', 'Página'),
    'posicion_pagina': ('Posición de la tarjeta en la página.', 'Numérico discreto', 'Posición'),
    'id_publicacion': ('Código MPE extraído por el scraper; corresponde al producto de catálogo, no a la oferta.', 'Categórico nominal (texto)', '–'),
    'titulo': ('Título de la tarjeta, tal como se capturó.', 'Texto libre', '–'),
    'moneda': ('Símbolo de moneda de la tarjeta.', 'Categórico nominal', '–'),
    'precio_actual_texto': ('Precio vigente como texto peruano (punto de miles, coma decimal).', 'Texto', 'Soles (PEN)'),
    'precio_anterior_texto': ('Precio tachado como texto; vacío sin promoción.', 'Texto', 'Soles (PEN)'),
    'descuento_texto': ('Descuento anunciado ("NN% OFF"); vacío sin promoción.', 'Texto', '%'),
    'cuotas_texto': ('Financiamiento ("N cuotas de S/ X sin interés"); vacío si no ofrece cuotas.', 'Texto', '–'),
    'vendedor_texto': ('Nombre de la tienda cuando la tarjeta lo muestra.', 'Texto', '–'),
    'envio_texto': ('Condición de envío ("Llega gratis mañana", "Envío gratis", "Llega mañana").', 'Texto', '–'),
    'resenas_texto': ('Calificación y unidades vendidas ("4.8 | +100 vendidos").', 'Texto', '–'),
    'etiqueta_texto': ('Etiqueta de la tarjeta; vacía en toda la captura.', 'Texto', '–'),
    'url_publicacion': ('Enlace de la publicación o del anuncio patrocinado.', 'Texto (URL)', '–'),
    'url_fuente': ('Página de resultados de la que se extrajo la tarjeta.', 'Texto (URL)', '–'),
    'fecha_extraccion': ('Fecha y hora de la captura de la página.', 'Fecha y hora', 'Segundos'),
}


def miles(n):
    return f'{n:,}'.replace(',', ' ')


def formato_numero(valor, decimales=2):
    texto = f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')
    return texto.rstrip('0').rstrip(',') if ',' in texto else texto


def valores(serie, tipo):
    """Resumen de los valores observados, calculado con los datos."""
    datos = serie.dropna()
    nulos = serie.isna().mean() * 100
    sufijo = f'; {formato_numero(nulos, 1)} % nulos' if nulos > 0 else ''
    if datos.empty:
        return 'Vacía en toda la captura'
    if tipo.startswith('Booleano'):
        return f'Verdadero o falso{sufijo}'
    if tipo.startswith('Numérico'):
        datos = pd.to_numeric(datos, errors='coerce').dropna()
        return f'De {formato_numero(datos.min())} a {formato_numero(datos.max())}{sufijo}'
    if tipo.startswith('Fecha'):
        return f'De {datos.min()} a {datos.max()}'
    distintos = datos.astype(str).unique()
    if len(distintos) <= 8:
        orden = ['económica', 'media', 'alta']  # las gamas se listan en su orden, no alfabético
        clave = (lambda v: orden.index(v)) if set(distintos) <= set(orden) else None
        return ', '.join(sorted(distintos, key=clave)) + sufijo
    ejemplo = datos.astype(str).iloc[0]
    return f'{len(distintos)} valores distintos. Ej.: {ejemplo[:45]}{"…" if len(ejemplo) > 45 else ""}{sufijo}'


def filas_diccionario(datos, definiciones):
    faltan = set(datos.columns) - set(definiciones)
    assert not faltan, f'Variables sin documentar: {faltan}'
    filas = []
    for variable in datos.columns:
        descripcion, tipo, unidad = definiciones[variable]
        tamano = int(datos[variable].dropna().astype(str).str.len().max()) if datos[variable].notna().any() else 0
        filas.append([variable, descripcion, tipo, str(tamano), valores(datos[variable], tipo), unidad])
    return filas


ANCHOS_CM = [3.6, 4.0, 2.0, 1.7, 2.7, 1.9]   # Variable, Descripción, Tipo, Tamaño máximo, Valores, Unidad
IZQUIERDA = {1, 4}                           # columnas de texto largo


def fijar_anchos(tabla, anchos_cm):
    """Anchos fijos en la cuadrícula y en cada celda (Word y Google Docs usan uno u otro)."""
    from docx.shared import Cm
    tabla.autofit = False
    propiedades = tabla._tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    siguiente = propiedades.find(qn('w:tblLook'))  # el esquema exige tblLayout antes de tblLook
    siguiente.addprevious(layout) if siguiente is not None else propiedades.append(layout)
    for col, ancho in zip(tabla._tbl.tblGrid.findall(qn('w:gridCol')), anchos_cm):
        col.set(qn('w:w'), str(int(Cm(ancho).twips)))
    for fila in tabla.rows:
        for celda, ancho in zip(fila.cells, anchos_cm):
            celda.width = Cm(ancho)


def poner_texto(celda, texto, tamano=None, negrita=None):
    parrafo = celda.paragraphs[0]
    for run in parrafo.runs[1:]:
        run._r.getparent().remove(run._r)
    run = parrafo.runs[0] if parrafo.runs else parrafo.add_run()
    run.text = texto
    if tamano:
        run.font.size = Pt(tamano)
    if negrita is not None:
        run.bold = negrita


def parrafo_despues(ancla, texto, plantilla_formato, tamano=11, negrita=False):
    """Inserta un párrafo después de `ancla` copiando el formato de `plantilla_formato`."""
    nuevo = copy.deepcopy(plantilla_formato._p)
    ancla._p.addnext(nuevo) if hasattr(ancla, '_p') else ancla.addnext(nuevo)
    from docx.text.paragraph import Paragraph
    parrafo = Paragraph(nuevo, plantilla_formato._parent)
    for run in parrafo.runs[1:]:
        run._r.getparent().remove(run._r)
    run = parrafo.runs[0] if parrafo.runs else parrafo.add_run()
    run.text, run.font.size, run.bold = texto, Pt(tamano), negrita
    return parrafo


def generar(datos, definiciones, titulo, descripcion, notas, destino):
    doc = Document(PLANTILLA)
    parrafos = doc.paragraphs
    poner_parrafo = lambda p, t: (setattr(p.runs[0], 'text', t), [r._r.getparent().remove(r._r) for r in p.runs[1:]])
    poner_parrafo(parrafos[4], titulo)                      # "Instrucciones" -> título del archivo
    poner_parrafo(parrafos[6], descripcion)                 # texto de instrucciones -> descripción del dataset

    tabla = doc.tables[0]
    prototipo = copy.deepcopy(tabla.rows[1]._tr)
    for fila in list(tabla.rows)[1:]:
        tabla._tbl.remove(fila._tr)
    encabezado = tabla.rows[0]._tr.get_or_add_trPr()
    repetir = OxmlElement('w:tblHeader')
    repetir.set(qn('w:val'), 'true')
    encabezado.append(repetir)
    for celda in tabla.rows[0].cells:
        for run in celda.paragraphs[0].runs:
            run.font.size = Pt(10)
    for valores_fila in filas_diccionario(datos, definiciones):
        tr = copy.deepcopy(prototipo)
        tabla._tbl.append(tr)
        fila = tabla.rows[-1]
        for indice, (celda, texto) in enumerate(zip(fila.cells, valores_fila)):
            poner_texto(celda, texto, tamano=9)
            if indice in IZQUIERDA:
                celda.paragraphs[0].alignment = 0
    fijar_anchos(tabla, ANCHOS_CM)

    ancla = parrafos[-1]
    poner_parrafo(ancla, 'Notas de interpretación')
    ancla.runs[0].bold = True
    for i, nota in enumerate(notas, start=1):
        ancla = parrafo_despues(ancla, f'{i}. {nota}', parrafos[6], tamano=11)

    destino.parent.mkdir(parents=True, exist_ok=True)
    doc.save(destino)
    print(f'{destino.relative_to(RAIZ)}: {len(datos.columns)} variables')
    return destino


def exportar_pdf(rutas):
    try:
        import win32com.client
    except ImportError:
        print('Sin Microsoft Word (pywin32): se omite la exportación a PDF.')
        return
    word = win32com.client.DispatchEx('Word.Application')
    word.Visible, word.DisplayAlerts = False, 0
    try:
        for ruta in rutas:
            documento = word.Documents.Open(str(ruta.resolve()))
            try:
                documento.SaveAs2(str(ruta.with_suffix('.pdf').resolve()), FileFormat=17)
            finally:
                documento.Close(SaveChanges=0)
            print(f'{ruta.with_suffix(".pdf").relative_to(RAIZ)}')
    finally:
        word.Quit(SaveChanges=0)


def main():
    metricas = json.loads((RAIZ / 'data' / 'final' / 'metricas.json').read_text(encoding='utf-8'))
    final = pd.read_csv(RAIZ / 'data' / 'final' / 'homeoffice_final.csv')
    crudo = pd.read_csv(RAIZ / 'data' / 'ec1_homeoffice' / 'homeoffice_ml_crudo.csv', encoding='utf-8-sig', dtype=str)
    df = metricas['dataset_final']
    lim = metricas['limpieza']

    rutas = [
        generar(crudo, INICIAL, 'Archivo: data/ec1_homeoffice/homeoffice_ml_crudo.csv (dataset inicial)',
                f'Captura de Mercado Libre Perú del 15/09/2026: {miles(len(crudo))} registros crudos y {crudo.shape[1]} columnas, '
                f'tal como los produjo el scraper de la Parte I. Todas las columnas son texto; la Parte II las convierte '
                f'a tipos en el notebook 01.',
                ['Es el dataset inicial de la Parte II y es de solo lectura: ningún proceso lo modifica.',
                 'id_publicacion identifica el producto de catálogo, no la oferta; la Parte II recupera la oferta del '
                 'parámetro wid de la URL.',
                 'Precio anterior y descuento faltan cuando no hay promoción; cuotas, cuando el producto no se financia; '
                 'reseñas, vendedor y envío dependen del componente y de la página (diagnóstico en el notebook 02).',
                 'La búsqueda incluye accesorios, combos y productos de otros componentes; se separan en el notebook 01.'],
                SALIDA / 'diccionario_inicial_homeoffice.docx'),
        generar(final, FINAL, 'Archivo: data/final/homeoffice_final.csv (dataset final)',
                f'{miles(df["filas"])} ofertas únicas de seis componentes de home office y {df["columnas"]} variables, una fila '
                f'por oferta. Resulta de limpiar, tratar faltantes y atípicos, integrar con la captura del 13/09/2026 y '
                f'construir variables derivadas (notebooks 01 a 04).',
                [f'Las columnas con más de 10 % de nulos lo son por diseño: {", ".join(sorted(df["nulos_justificados"]))}. '
                 f'Ninguna otra supera {formato_numero(df["max_nulos_no_justificado"], 2)} %.',
                 'Un nulo estructural significa "no aplica" (sin promoción, sin cuotas, especificación de otro '
                 'componente); un nulo MAR significa que la tarjeta no mostró el dato. No se imputaron.',
                 f'Se excluyeron {sum(lim["ajenas"].values())} publicaciones que no eran el componente (accesorios, combos '
                 f'y otros productos) y {metricas["atipicos"]["excluidos_por_error"]} error de precio; la evidencia está '
                 f'en data/evidencia/.',
                 'Las especificaciones (RAM, almacenamiento, pulgadas, inalámbrico, ergonómica) se extraen del título: '
                 'un título incompleto deja el valor nulo.',
                 'Los precios describen ofertas publicadas en una captura de un día, no transacciones ni una serie histórica.'],
                SALIDA / 'diccionario_final.docx'),
    ]
    if '--sin-pdf' not in sys.argv:
        exportar_pdf(rutas)


if __name__ == '__main__':
    main()
