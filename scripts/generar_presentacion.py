"""Genera la presentación de la Parte II (16:9) con las cifras de data/final/metricas.json y las figuras de los
notebooks. Uso: python scripts/generar_presentacion.py   (la exportación a PDF para revisión requiere PowerPoint)
"""
import json
import sys
from pathlib import Path

import pandas as pd
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

RAIZ = Path(__file__).resolve().parent.parent
FIGURAS = RAIZ / 'docs' / 'parte_2' / 'figuras'
SALIDA = RAIZ / 'docs' / 'parte_2' / 'presentacion' / 'Presentacion_Parte_II_DS3021.pptx'
M = json.loads((RAIZ / 'data' / 'final' / 'metricas.json').read_text(encoding='utf-8'))

# Paleta: azul marino dominante (coherente con las figuras), acento naranja, fondos claros.
MARINO, AZUL, CELESTE, HIELO = RGBColor(0x0D, 0x36, 0x6B), RGBColor(0x2A, 0x78, 0xD6), RGBColor(0x86, 0xB6, 0xEF), RGBColor(0xEE, 0xF4, 0xFC)
NARANJA, TINTA, GRIS, BLANCO = RGBColor(0xEB, 0x68, 0x34), RGBColor(0x1A, 0x1A, 0x1A), RGBColor(0x52, 0x51, 0x4E), RGBColor(0xFF, 0xFF, 0xFF)
TITULOS, CUERPO = 'Cambria', 'Calibri'
ANCHO, ALTO = 13.333, 7.5
MARGEN = 0.6


def soles(valor, decimales=0):
    return 'S/ ' + f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')


def miles(valor):
    return f'{int(valor):,}'.replace(',', ' ')


def num(valor, decimales=0):
    return f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width, self.prs.slide_height = Inches(ANCHO), Inches(ALTO)
        self.vacio = self.prs.slide_layouts[6]

    def diapositiva(self, fondo=BLANCO, notas=''):
        s = self.prs.slides.add_slide(self.vacio)
        s.background.fill.solid()
        s.background.fill.fore_color.rgb = fondo
        if notas:
            s.notes_slide.notes_text_frame.text = notas
        return s

    @staticmethod
    def texto(s, x, y, w, h, contenido, tam=16, color=TINTA, negrita=False, fuente=CUERPO, alinear=PP_ALIGN.LEFT,
              ancla=MSO_ANCHOR.TOP, cursiva=False, nombre=None, espacio=6):
        """`contenido` es un texto o una lista de párrafos; cada párrafo admite **negrita** en línea."""
        caja = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        if nombre:
            caja.name = nombre
        marco = caja.text_frame
        marco.word_wrap = True
        marco.margin_left = marco.margin_right = marco.margin_top = marco.margin_bottom = 0
        marco.vertical_anchor = ancla
        for i, parrafo_texto in enumerate([contenido] if isinstance(contenido, str) else contenido):
            p = marco.paragraphs[0] if i == 0 else marco.add_paragraph()
            p.alignment = alinear
            p.space_after = Pt(espacio)
            for j, trozo in enumerate(parrafo_texto.split('**')):
                if trozo:
                    r = p.add_run()
                    r.text = trozo
                    r.font.size, r.font.name, r.font.color.rgb = Pt(tam), fuente, color
                    r.font.bold, r.font.italic = negrita or j % 2 == 1, cursiva
        return caja

    def titulo(self, s, texto, color=MARINO):
        self.texto(s, MARGEN, 0.45, ANCHO - 2 * MARGEN, 0.9, texto, tam=32, color=color, negrita=True, fuente=TITULOS,
                   ancla=MSO_ANCHOR.MIDDLE, nombre='Título')

    @staticmethod
    def tarjeta(s, x, y, w, h, relleno=HIELO):
        forma = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        forma.adjustments[0] = 0.08
        forma.fill.solid()
        forma.fill.fore_color.rgb = relleno
        forma.line.fill.background()
        forma.shadow.inherit = False
        return forma

    def cifra(self, s, x, y, w, valor, etiqueta, color=MARINO, fondo=HIELO, tam=40):
        self.tarjeta(s, x, y, w, 1.65, fondo)
        oscuro = fondo in (MARINO, AZUL, NARANJA)
        self.texto(s, x + 0.25, y + 0.18, w - 0.5, 0.8, valor, tam=tam, color=color, negrita=True, fuente=TITULOS)
        self.texto(s, x + 0.25, y + 1.0, w - 0.5, 0.6, etiqueta, tam=13, color=BLANCO if oscuro else GRIS)

    @staticmethod
    def figura(s, nombre, x, y, w_max, h_max):
        ruta = FIGURAS / f'{nombre}.png'
        ancho_px, alto_px = Image.open(ruta).size
        escala = min(w_max / ancho_px, h_max / alto_px)
        w, h = ancho_px * escala, alto_px * escala
        imagen = s.shapes.add_picture(str(ruta), Inches(x + (w_max - w) / 2), Inches(y + (h_max - h) / 2), Inches(w), Inches(h))
        imagen.name = nombre
        return imagen

    def pie(self, s, texto):
        self.texto(s, MARGEN, ALTO - 0.55, ANCHO - 2 * MARGEN, 0.3, texto, tam=11, color=GRIS, cursiva=True)

    def numerar(self):
        for i, s in enumerate(self.prs.slides, start=1):
            if i > 1:
                self.texto(s, ANCHO - MARGEN - 0.6, ALTO - 0.55, 0.6, 0.3, str(i), tam=11, color=GRIS, alinear=PP_ALIGN.RIGHT)


def construir():
    d = Deck()
    lim, integ, fal, at, car, df = (M['limpieza'], M['integracion'], M['faltantes'], M['atipicos'],
                                    M['caracteristicas'], M['dataset_final'])
    perf, a = M['costos']['perfiles'], M['analisis']

    # 1 · Portada
    s = d.diapositiva(MARINO, 'Sugerencia: abre Yared. Presentar la pregunta del proyecto y que esta parte la responde '
                              'con datos limpios y por perfil de equipamiento.')
    d.texto(s, MARGEN, 0.7, 9, 0.4, 'DS3021 · Análisis Computacional de Datos · Proyecto final, Parte II', tam=14,
            color=CELESTE)
    d.texto(s, MARGEN, 1.5, 11.5, 2.2, '¿Cuánto cuesta equipar un home office en el Perú?', tam=46, color=BLANCO,
            negrita=True, fuente=TITULOS)
    d.texto(s, MARGEN, 3.75, 11, 0.6, 'Preprocesamiento, análisis y pipeline de datos de Mercado Libre Perú', tam=20,
            color=CELESTE)
    d.texto(s, MARGEN, 5.0, 11.5, 1.6, ['Yared Riveros Rodríguez · Franco Nicolás Roque Castillo · Mauricio Terán Taica',
                                        'Josué Luna Rocha · Alvaro Mauricio García Hurtado', 'UTEC · Lima, 2026'],
            tam=15, color=BLANCO)

    # 2 · Contexto actualizado
    s = d.diapositiva(notas='Ley 31572: el empleador provee o compensa equipos según su valor de mercado, que no se '
                            'publica en ninguna fuente. La Parte I dio una sola cifra; aquí se explica por qué no basta.')
    d.titulo(s, 'El problema: su valor de mercado no se publica')
    d.texto(s, MARGEN, 1.6, 6.6, 4.8, [
        'La **Ley 31572 del Teletrabajo** obliga al empleador a proveer los equipos o a compensar los propios según su '
        '**valor de mercado**.',
        'La Parte I construyó esa referencia con web scraping de Mercado Libre Perú: dos capturas, '
        f'{miles(M["ingesta"]["filas_crudo_ho"])} y {miles(M["ingesta"]["filas_crudo_cat"])} registros crudos.',
        'Al preprocesar descubrimos que **una sola cifra oculta la respuesta**: el costo depende del nivel de equipamiento, '
        'y las búsquedas mezclan accesorios, combos y anuncios.'], tam=18, espacio=14)
    d.cifra(s, 7.9, 1.7, 4.8, soles(M['costos']['suma_medianas_parte1']), 'Parte I: costo único, suma de medianas',
            color=GRIS)
    d.cifra(s, 7.9, 3.65, 4.8, f'{soles(perf["económico"]["costo_mediano"])} – {soles(perf["alto"]["costo_mediano"])}',
            'Parte II: según el perfil, de económico a alto', tam=30)

    # 3 · Objetivos actualizados
    s = d.diapositiva(notas='Objetivos de la Parte I que se cumplieron (extracción) frente a los que se ajustan: '
                            'deduplicar por oferta, justificar nulos, costo por perfil, pipeline.')
    d.titulo(s, 'Objetivos: de una cifra de referencia a un costo por perfil')
    filas = [('Preprocesar con justificación', 'Ningún faltante es MCAR; cada tratamiento según su tipo'),
             ('Integrar las dos capturas', f'{integ["comunes_por_oferta"]} ofertas comunes (por oferta, no por catálogo)'),
             ('Construir variables y gamas', f'{car["variables_derivadas"]} variables derivadas; 3 gamas por componente'),
             ('Estimar costo por perfil', 'Valor central y rango por componente, gama y perfil'),
             ('Pipeline reproducible', 'Seis etapas con una instrucción; salidas idénticas entre ejecuciones')]
    for i, (objetivo, resultado) in enumerate(filas):
        y = 1.65 + i * 1.0
        d.tarjeta(s, MARGEN, y, ANCHO - 2 * MARGEN, 0.82)
        d.texto(s, MARGEN + 0.3, y, 0.6, 0.82, str(i + 1), tam=26, color=NARANJA, negrita=True, fuente=TITULOS,
                ancla=MSO_ANCHOR.MIDDLE)
        d.texto(s, MARGEN + 1.0, y, 4.6, 0.82, objetivo, tam=17, color=MARINO, negrita=True, ancla=MSO_ANCHOR.MIDDLE)
        d.texto(s, MARGEN + 5.8, y, 6.2, 0.82, resultado, tam=16, color=TINTA, ancla=MSO_ANCHOR.MIDDLE)

    # 4 · Datos: inicial y final
    s = d.diapositiva(notas='Sugerencia: Franco. Del crudo al dataset final: qué entra, qué sale y por qué.')
    d.titulo(s, 'Del crudo al dataset final')
    d.cifra(s, MARGEN, 1.7, 3.8, miles(M['ingesta']['filas_crudo_ho']), 'registros crudos de home office (15/09)')
    d.cifra(s, MARGEN + 4.1, 1.7, 3.8, miles(lim['ofertas_unicas'] + sum(lim['ajenas'].values())),
            'ofertas únicas al deduplicar por oferta')
    d.cifra(s, MARGEN + 8.2, 1.7, 3.9, f'{miles(df["filas"])} × {df["columnas"]}', 'dataset final: ofertas × variables',
            color=BLANCO, fondo=MARINO)
    aj = lim['ajenas']
    d.texto(s, MARGEN, 3.75, ANCHO - 2 * MARGEN, 2.6, [
        f'**{miles(lim["duplicados"])} repeticiones** retiradas: la misma oferta en varias páginas o búsquedas.',
        f'**{sum(aj.values())} publicaciones que no son el componente**: {aj["combo de varios componentes"]} kits de teclado '
        f'y mouse, {aj["accesorio"]} accesorios o repuestos, {aj["otro producto"]} otros productos; {lim["reasignadas"]} '
        'reasignadas a su componente real.',
        f'**{lim["anuncios_patrocinados_crudo"]} registros crudos son anuncios patrocinados**, identificados por su URL.',
        f'Se conserva el **{num(df["conservadas_pct"], 2)} %** de las ofertas válidas; cada exclusión queda con su motivo.'],
            tam=17, espacio=10)

    # 5 · Pipeline
    s = d.diapositiva(notas='Ciclo de vida de U5_T1. SQLite en lugar de SQL Server + SSIS para que cualquiera reproduzca '
                            'con requirements.txt. El pipeline se detiene si falla un invariante.')
    d.titulo(s, 'Pipeline: una instrucción, seis etapas, salidas idénticas')
    d.figura(s, 'f00_pipeline', MARGEN, 1.45, ANCHO - 2 * MARGEN, 3.9)
    d.tarjeta(s, MARGEN, 5.55, ANCHO - 2 * MARGEN, 1.15)
    d.texto(s, MARGEN + 0.3, 5.6, ANCHO - 2 * MARGEN - 0.6, 1.05, [
        '**python pipeline.py** ejecuta los notebooks 01–05, carga **SQLite** (5 tablas con clave) y escribe un manifiesto '
        'SHA-256. Menos de un minuto; se detiene y nombra el invariante si algo falla.'], tam=16, ancla=MSO_ANCHOR.MIDDLE)

    # 6 · Identificación de entidades
    s = d.diapositiva(notas='El hallazgo de integración más importante: la clave equivocada hace pasar la misma oferta '
                            'por distinta. Mencionar los seis desafíos de U3_T4.')
    d.titulo(s, f'La clave correcta multiplica por {integ["comunes_por_oferta"] / integ["comunes_por_catalogo"]:.0f} '
                'las ofertas integrables')
    d.figura(s, 'f03_clave_de_union', MARGEN, 1.5, 7.6, 2.6)
    d.figura(s, 'f03_variacion_precio', MARGEN, 4.2, 7.6, 2.6)
    d.texto(s, 8.6, 1.6, 4.1, 5.0, [
        f'Unir por **código de catálogo** encuentra {integ["comunes_por_catalogo"]} ofertas comunes; por **oferta** '
        f'(parámetro wid), {integ["comunes_por_oferta"]}.',
        f'El **{num(integ["sin_cambio_pct"])} %** de las ofertas comunes mantuvo su precio entre el 13/09 y el 15/09.',
        'Se agregan atributos (precio del 13/09 y variación), no filas: las otras ofertas no tienen descuento, reseñas '
        'ni envío.'], tam=16, espacio=12)

    # 7 · Faltantes
    s = d.diapositiva(notas='Sugerencia: Mauricio. Chi-cuadrado contra componente, página y anuncio: todos dependen de '
                            'algo observado. Por eso no se borran filas ni se imputa la calificación.')
    d.titulo(s, 'Ningún faltante es aleatorio')
    d.figura(s, 'f02_faltantes_por_componente', MARGEN, 1.5, 7.3, 4.9)
    d.texto(s, 8.3, 1.6, 4.4, 5.0, [
        '**Promoción y cuotas: estructurales (MNAR).** Faltan porque no existen: descuento 0 % marcado y "no aplica".',
        '**Reseñas, vendedor y envío: MAR.** Dependen del componente (p < 0,001): se marcan y no se imputan.',
        f'Imputar la calificación con la mediana subiría la moda a **{num(fal["contraste_calificacion"]["moda_pct_imputada"])} %** '
        'y le daría a lo caro la reputación de lo barato.'], tam=15, espacio=12)

    # 8 · Atípicos
    s = d.diapositiva(notas='Atípicos sobre el log-precio y por componente. Solo se elimina un error comprobable; el resto '
                            'son productos reales de gama alta o muy baratos.')
    d.titulo(s, 'Atípicos: casi todos son productos reales')
    d.figura(s, 'f02_atipicos_univariados', MARGEN, 1.5, 7.6, 4.9)
    d.cifra(s, 8.6, 1.6, 4.1, str(at['univariados']), 'atípicos univariados (IQR y |z| > 3 sobre log-precio)')
    d.cifra(s, 8.6, 3.4, 4.1, str(at['kmeans']), 'multivariados por K-Means; Mahalanobis como contraste')
    d.cifra(s, 8.6, 5.2, 4.1, str(at['excluidos_por_error']), 'excluido: laptop de 8 GB a S/ 29 000', color=BLANCO,
            fondo=NARANJA)

    # 9 · Feature engineering
    s = d.diapositiva(notas='Sugerencia: Josué. Variables desde el título y gamas por terciles; la validación muestra '
                            'que cada componente se diferencia por algo distinto.')
    d.titulo(s, f'{car["variables_derivadas"]} variables derivadas y gamas validadas')
    d.figura(s, 'f04_validacion_gamas', MARGEN, 1.5, ANCHO - 2 * MARGEN, 3.6)
    cs = car['cobertura_specs']
    d.texto(s, MARGEN, 5.3, ANCHO - 2 * MARGEN, 1.4, [
        f'Del título: marca, RAM ({num(cs["ram_gb"])} % de laptops), almacenamiento, pulgadas ({num(cs["pulgadas"])} % de '
        'monitores), inalámbrico, ergonómica y "gamer". De los textos: descuento real, cuotas, reseñas, vendidos, envío.',
        '**Gamas**: terciles de precio por componente (qcut), contrastados con K-Means. La conexión inalámbrica no varía '
        'entre gamas: no es lo que encarece un periférico.'], tam=15, espacio=8)

    # 10 · Costo por perfil
    s = d.diapositiva(notas='Sugerencia: Alvaro. El resultado central. El rango suma la mitad central de la oferta de '
                            'cada componente.')
    d.titulo(s, f'Respuesta: entre {soles(round(perf["económico"]["costo_mediano"], -2))} y '
                f'{soles(round(perf["alto"]["costo_mediano"], -2))}, según el perfil')
    for i, (perfil, color, fondo) in enumerate([('económico', MARINO, HIELO), ('medio', BLANCO, AZUL), ('alto', BLANCO, MARINO)]):
        p = perf[perfil]
        x = MARGEN + i * 4.1
        d.tarjeta(s, x, 1.65, 3.85, 2.3, fondo)
        d.texto(s, x + 0.3, 1.8, 3.3, 0.5, f'Perfil {perfil}', tam=17, color=color if fondo != HIELO else GRIS, negrita=True)
        d.texto(s, x + 0.3, 2.3, 3.3, 0.9, soles(p['costo_mediano']), tam=40, color=color, negrita=True, fuente=TITULOS)
        d.texto(s, x + 0.3, 3.25, 3.3, 0.5, f'{soles(p["costo_q1"])} – {soles(p["costo_q3"])}', tam=14,
                color=color if fondo != HIELO else GRIS)
    d.figura(s, 'f05_composicion_perfiles', MARGEN, 4.15, ANCHO - 2 * MARGEN, 2.75)

    # 11 · Laptop
    lr = a['laptop_por_ram']
    s = d.diapositiva(notas='La laptop decide el presupuesto. 16 GB es lo más ofrecido y basta para oficina.')
    comp = a['composicion_laptop_pct']
    d.titulo(s, f'La laptop concentra hasta el {num(max(comp.values()))} % del gasto')
    d.figura(s, 'f05_laptops', MARGEN, 1.5, 8.2, 3.3)
    perfiles = pd.read_csv(RAIZ / 'data' / 'final' / 'perfiles_home_office.csv').set_index('perfil')
    perifericos = (perfiles[['mediana_teclado', 'mediana_mouse', 'mediana_audifonos']].sum(axis=1)
                   / perfiles['costo_mediano'] * 100).max()
    d.cifra(s, 9.15, 1.6, 3.55, f'{num(min(comp.values()))}–{num(max(comp.values()))} %', 'del costo del perfil es la laptop')
    d.texto(s, MARGEN, 5.1, ANCHO - 2 * MARGEN, 1.6, [
        f'La RAM marca escalones: **{soles(lr["8.0"])}** con 8 GB, **{soles(lr["16.0"])}** con 16 GB y **{soles(lr["32.0"])}** '
        'con 32 GB.',
        f'Elegir la gama de la laptop es la decisión que más mueve el presupuesto; teclado, mouse y audífonos juntos no '
        f'superan el {num(perifericos)} %.'],
            tam=16, espacio=8)

    # 12 · Promociones y cuotas
    s = d.diapositiva(notas='Contraintuitivo: el descuento no indica buen precio (Mann-Whitney). Cuotas sin interés en '
                            'casi todo: financiar no encarece.')
    d.titulo(s, 'Un descuento no es un buen precio; las cuotas no encarecen')
    d.figura(s, 'f05_promociones', MARGEN, 1.5, ANCHO - 2 * MARGEN, 3.6)
    d.cifra(s, MARGEN, 5.2, 5.9, f'{a["promo_componentes_mas_caras"]} de 6',
            'componentes donde la oferta con descuento cuesta más que la sin promoción', tam=32)
    d.cifra(s, MARGEN + 6.2, 5.2, 5.9, soles(a['cuota_mensual']['medio']['12 cuotas']),
            f'al mes por un perfil medio en 12 cuotas sin interés ({num(a["cuotas_pct"])} % ofrece cuotas)', tam=32)

    # 13 · Gamer y reputación
    s = d.diapositiva(notas='"Gamer" encarece mouse, laptops, teclados y audífonos, no monitores ni sillas. Lo más '
                            'vendido es lo más barato; lo mejor calificado, lo más caro.')
    d.titulo(s, 'Lo "gamer" y lo más vendido no son lo que parecen')
    d.figura(s, 'f05_gamer', MARGEN, 1.5, 7.6, 4.3)
    sv, sc = a['spearman_vendidos'], a['spearman_calificacion']
    d.texto(s, MARGEN, 6.0, 7.6, 0.8, f'El mouse "gamer" está **{num(a["gamer_diferencia"]["mouse"], 2)} desviaciones** por '
            'encima del resto; en monitores y sillas, lo gamer es más barato.', tam=15)
    d.cifra(s, 8.6, 1.6, 4.1, f'ρ = {num(sv["rho"], 2)}', 'ventas y precio: relación débil; los +1000 vendidos son '
            'más baratos que su componente', tam=34)
    d.cifra(s, 8.6, 3.45, 4.1, f'ρ = {num(sc["rho"], 2)}', 'calificación y precio: lo mejor valorado es más caro', tam=34)
    d.tarjeta(s, 8.6, 5.3, 4.1, 1.4, HIELO)
    d.texto(s, 8.85, 5.3, 3.6, 1.4, 'Lo más vendido no es lo mejor valorado.', tam=16, color=MARINO, negrita=True,
            ancla=MSO_ANCHOR.MIDDLE)

    # 14 · Insights
    s = d.diapositiva(notas='Insights con usuario, acción y cifra. Elegir dos o tres para desarrollar en voz alta.')
    d.titulo(s, 'Recomendaciones para trabajadores y RR. HH.')
    lista = M['insights']['lista']
    for i, ins in enumerate(lista[:6]):
        col, fila = i % 3, i // 3
        x, y = MARGEN + col * 4.1, 1.6 + fila * 2.6
        d.tarjeta(s, x, y, 3.85, 2.4, HIELO)
        d.texto(s, x + 0.25, y + 0.15, 3.35, 0.4, ins['usuario'], tam=12, color=NARANJA, negrita=True)
        d.texto(s, x + 0.25, y + 0.55, 3.35, 1.8, ins['accion'], tam=14, color=TINTA)
    d.pie(s, 'Las ocho recomendaciones completas, con su cifra de respaldo, están en la sección 9 del documento maestro.')

    # 15 · Conclusiones
    s = d.diapositiva(MARINO, notas='Cerrar con la respuesta y las limitaciones honestas.')
    d.titulo(s, 'Conclusiones y limitaciones', color=BLANCO)
    d.texto(s, MARGEN, 1.6, 6.0, 5.2, [
        f'Un home office cuesta **{soles(perf["económico"]["costo_mediano"])}**, **{soles(perf["medio"]["costo_mediano"])}** o '
        f'**{soles(perf["alto"]["costo_mediano"])}** según el perfil: compensar con una sola cifra es impreciso.',
        'La laptop decide el presupuesto; descuentos y etiqueta "gamer" no son señales de buen precio.',
        'Preprocesar con justificación cambió los resultados: clave de oferta, ajenas fuera, faltantes sin imputar.'],
            tam=17, color=BLANCO, espacio=14)
    d.tarjeta(s, 7.0, 1.6, 5.73, 3.7, RGBColor(0x18, 0x4F, 0x95))
    d.texto(s, 7.3, 1.8, 5.2, 3.4, [
        '**Limitaciones**',
        'Capturas de un día, con dos días de diferencia: no hay serie histórica.',
        'Resultados de búsqueda ordenados por el sitio, no una muestra aleatoria.',
        f'Reseñas ausentes en {num(fal["diagnostico"]["calificacion"]["pct"])} % y no al azar.',
        'Especificaciones extraídas del título; precios publicados, sin envío.'], tam=15, color=BLANCO, espacio=10)

    # 16 · Reproducibilidad
    s = d.diapositiva(notas='Mostrar el repositorio: estructura, README, requirements y el flujo SDD en specs/.')
    d.titulo(s, 'Reproducible en tres comandos')
    pasos = [('1', 'git clone …/proyectoacd_mercadolibre'), ('2', 'pip install -r requirements.txt'),
             ('3', 'python pipeline.py')]
    for i, (n, comando) in enumerate(pasos):
        y = 1.7 + i * 1.15
        d.tarjeta(s, MARGEN, y, 6.6, 0.95, HIELO)
        d.texto(s, MARGEN + 0.3, y, 0.5, 0.95, n, tam=26, color=NARANJA, negrita=True, fuente=TITULOS, ancla=MSO_ANCHOR.MIDDLE)
        d.texto(s, MARGEN + 1.0, y, 5.5, 0.95, comando, tam=17, fuente='Courier New', ancla=MSO_ANCHOR.MIDDLE)
    d.texto(s, 7.7, 1.7, 5.0, 4.9, [
        '**data/** dataset inicial y final, evidencia de cada exclusión',
        '**notebooks/** 01 a 05, uno por etapa',
        '**docs/** diccionarios inicial y final, informe, figuras',
        '**specs/** especificación, plan, tareas y evaluación (flujo SDD)',
        'Manifiesto SHA-256: dos ejecuciones producen los mismos CSV.'], tam=16, espacio=12)

    d.numerar()
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    d.prs.save(SALIDA)
    print(f'{SALIDA.relative_to(RAIZ)}: {len(d.prs.slides)} diapositivas')


def exportar_pdf():
    try:
        import win32com.client
    except ImportError:
        print('Sin PowerPoint (pywin32): se omite la exportación a PDF.')
        return
    app = win32com.client.DispatchEx('PowerPoint.Application')
    presentacion = None
    try:
        presentacion = app.Presentations.Open(str(SALIDA.resolve()), WithWindow=False)
        presentacion.SaveAs(str(SALIDA.with_suffix('.pdf').resolve()), 32)
        print(f'{SALIDA.with_suffix(".pdf").relative_to(RAIZ)} exportado')
    finally:
        if presentacion is not None:
            presentacion.Close()
        app.Quit()


if __name__ == '__main__':
    construir()
    if '--sin-pdf' not in sys.argv:
        exportar_pdf()
