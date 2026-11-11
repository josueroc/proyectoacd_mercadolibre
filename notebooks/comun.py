"""Utilidades compartidas por los notebooks de la Parte II.

Contiene rutas, estilo de figuras y el registro de evidencia, balance y métricas. No contiene lógica de
datos: cada decisión de preprocesamiento vive, explicada, en su notebook.
"""
import json
import os
from pathlib import Path

# scikit-learn intenta contar núcleos físicos con una llamada que falla en algunos Windows; un valor fijo evita
# el aviso y no cambia los resultados.
os.environ.setdefault('LOKY_MAX_CPU_COUNT', '1')

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- rutas
RAIZ = Path(__file__).resolve().parent.parent
CRUDO_HO = RAIZ / 'data' / 'ec1_homeoffice' / 'homeoffice_ml_crudo.csv'   # dataset inicial, solo lectura
CRUDO_CAT = RAIZ / 'data' / 'crudos' / 'mercadolibre_raw.csv'             # dataset inicial, solo lectura
INTERMEDIO = RAIZ / 'data' / 'intermedio'
EVIDENCIA = RAIZ / 'data' / 'evidencia'
FINAL = RAIZ / 'data' / 'final'
FIGURAS = RAIZ / 'docs' / 'parte_2' / 'figuras'
METRICAS = FINAL / 'metricas.json'
for _carpeta in (INTERMEDIO, EVIDENCIA, FINAL, FIGURAS):
    _carpeta.mkdir(parents=True, exist_ok=True)

SEMILLA = 42

# ---------------------------------------------------------------- dominio
# Búsqueda de origen en el scraping -> nombre del componente.
COMPONENTES = {
    'laptops': 'laptop',
    'monitores': 'monitor',
    'sillas-de-oficina': 'silla',
    'teclados': 'teclado',
    'mouse': 'mouse',
    'audifonos': 'audifonos',
}
ORDEN_COMPONENTES = list(COMPONENTES.values())
ORDEN_GAMAS = ['económica', 'media', 'alta']

# ---------------------------------------------------------------- estilo
# Paleta categórica de referencia (skill dataviz), validada para 6 series en pares adyacentes
# sobre fondo blanco. Orden fijo: el color sigue al componente, nunca a su posición en el gráfico.
COLOR_COMPONENTE = dict(zip(ORDEN_COMPONENTES,
                            ['#2a78d6', '#eb6834', '#1baf7a', '#eda100', '#e87ba4', '#008300']))
# Rampa ordinal de un solo tono (azul 250/450/650), validada con --ordinal.
COLOR_GAMA = dict(zip(ORDEN_GAMAS, ['#86b6ef', '#2a78d6', '#104281']))
TINTA = '#0b0b0b'
TINTA_SECUNDARIA = '#52514e'
TINTA_TENUE = '#898781'
REJILLA = '#e1e0d9'
ACENTO = '#e34948'       # resaltar un subconjunto (por ejemplo, atípicos) frente al resto en gris


def aplicar_estilo():
    """Estilo común. Con 8 pulgadas de ancho insertadas a 16 cm, 12 pt se leen como unos 9,5 pt (NFR-006).

    También fija la semilla de numpy: algunos gráficos (stripplot) dispersan los puntos al azar.
    """
    np.random.seed(SEMILLA)
    plt.rcParams.update({
        'figure.figsize': (8, 4.5),
        'figure.dpi': 110,
        'savefig.dpi': 200,
        'savefig.bbox': 'tight',
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'font.size': 12,
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.titlelocation': 'left',
        'axes.labelsize': 12,
        'axes.labelcolor': TINTA_SECUNDARIA,
        'axes.edgecolor': TINTA_TENUE,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.color': REJILLA,
        'grid.linewidth': 0.8,
        'axes.axisbelow': True,
        'xtick.color': TINTA_SECUNDARIA,
        'ytick.color': TINTA_SECUNDARIA,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
        'legend.frameon': False,
        'text.color': TINTA,
    })


def soles(valor, decimales=0):
    """Formato peruano: S/ 1 234,50."""
    texto = f'{valor:,.{decimales}f}'.replace(',', ' ').replace('.', ',')
    return f'S/ {texto}'


# ---------------------------------------------------------------- escritura determinista
def escribir_csv(df, ruta):
    """CSV en UTF-8, sin índice, con fin de línea y formato de fecha fijos (NFR-002)."""
    df.to_csv(ruta, index=False, encoding='utf-8', lineterminator='\n',
              date_format='%Y-%m-%d %H:%M:%S')
    return ruta


def _a_json(valor):
    if isinstance(valor, (np.integer,)):
        return int(valor)
    if isinstance(valor, (np.floating,)):
        return None if np.isnan(valor) else round(float(valor), 6)
    if isinstance(valor, (np.bool_,)):
        return bool(valor)
    if isinstance(valor, (pd.Timestamp,)):
        return valor.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError(f'No serializable: {type(valor)}')


def registrar(seccion, **valores):
    """Guarda cifras en data/final/metricas.json bajo una sección; el informe y la presentación las leen de ahí."""
    datos = json.loads(METRICAS.read_text(encoding='utf-8')) if METRICAS.exists() else {}
    datos.setdefault(seccion, {}).update(json.loads(json.dumps(valores, default=_a_json)))
    METRICAS.write_text(json.dumps(datos, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8',
                        newline='\n')


def leer_metricas():
    return json.loads(METRICAS.read_text(encoding='utf-8'))


# ---------------------------------------------------------------- trazabilidad
def guardar_evidencia(df, archivo, etapa, motivo):
    """Guarda registros excluidos o marcados con su etapa y motivo en data/evidencia/ (constitución IV)."""
    assert 'id_oferta' in df.columns, 'La evidencia debe identificar cada registro por id_oferta.'
    salida = df.copy()
    salida.insert(0, 'motivo', motivo)
    salida.insert(0, 'etapa', etapa)
    salida = salida.sort_values(['id_oferta', 'motivo'], kind='stable')
    escribir_csv(salida, EVIDENCIA / archivo)
    return len(salida)


def registrar_balance(etapa, entrada, salida, **excluidos):
    """Comprueba entrada = salida + excluidos y lo registra en metricas.json (SC-003, FR-026)."""
    total = salida + sum(excluidos.values())
    assert entrada == total, (
        f'Balance roto en la etapa {etapa}: entrada {entrada} != salida {salida} + excluidos {excluidos}')
    registrar('balance', **{etapa: {'entrada': entrada, 'salida': salida, **excluidos}})


def guardar_figura(fig, nombre, pregunta, lectura):
    """Guarda la figura y registra la pregunta que responde y su lectura analítica (constitución VI)."""
    assert pregunta.strip() and lectura.strip(), 'Cada figura necesita su pregunta y su interpretación.'
    fig.savefig(FIGURAS / f'{nombre}.png', facecolor='white')
    registrar('figuras', **{nombre: {'pregunta': pregunta, 'lectura': lectura}})
    plt.show()
    print(f'Lectura: {lectura}')
