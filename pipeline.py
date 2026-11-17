"""Pipeline de datos de la Parte II: ingestión, transformación, almacenamiento y análisis.

Ejecuta en orden los notebooks de cada etapa, carga el resultado en SQLite y se detiene en la primera etapa que
falle. Contrato: specs/001-preprocesamiento-analisis-home-office/contracts/pipeline-cli.md

    python pipeline.py              # todas las etapas
    python pipeline.py --desde 03   # reanuda desde una etapa
    python pipeline.py --hasta 05   # se detiene después de una etapa
"""
import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import warnings
from pathlib import Path

import nbformat
import pandas as pd
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

# Avisos del kernel de Jupyter que no afectan los resultados y taparían la salida del pipeline.
os.environ.setdefault('LOKY_MAX_CPU_COUNT', '1')
os.environ.setdefault('PYDEVD_DISABLE_FILE_VALIDATION', '1')
os.environ.setdefault('PYTHONWARNINGS', 'ignore')
warnings.filterwarnings('ignore', message='Proactor event loop')

RAIZ = Path(__file__).resolve().parent
NOTEBOOKS = RAIZ / 'notebooks'
FINAL = RAIZ / 'data' / 'final'
EVIDENCIA = RAIZ / 'data' / 'evidencia'
ALMACEN = FINAL / 'home_office.sqlite'

ETAPAS = {
    '01': ('Ingestión y limpieza', '01_ingesta_y_limpieza.ipynb'),
    '02': ('Valores faltantes y atípicos', '02_faltantes_y_atipicos.ipynb'),
    '03': ('Integración y reducción', '03_integracion_y_reduccion.ipynb'),
    '04': ('Transformación e ingeniería de características', '04_transformacion_e_ingenieria_de_caracteristicas.ipynb'),
    '05': ('Almacenamiento en SQLite', None),
    '06': ('Análisis y visualización', '05_analisis_y_visualizacion.ipynb'),
}

# Tabla del almacén -> (CSV de data/final, clave primaria)
TABLAS = {
    'publicaciones': ('homeoffice_final.csv', ['id_oferta']),
    'precios_por_gama': ('precios_por_gama.csv', ['componente', 'gama']),
    'perfiles': ('perfiles_home_office.csv', ['perfil']),
    'ofertas_comunes': ('integracion_ofertas_comunes.csv', ['id_oferta']),
}


class EtapaFallida(Exception):
    pass


def ejecutar_notebook(archivo):
    """Ejecuta el notebook en su carpeta y lo guarda con sus salidas, que son la evidencia de la etapa."""
    ruta = NOTEBOOKS / archivo
    if not ruta.exists():
        raise EtapaFallida(f'no existe {ruta.relative_to(RAIZ)}')
    cuaderno = nbformat.read(ruta, as_version=4)
    ejecutor = ExecutePreprocessor(timeout=900, kernel_name='python3', record_timing=False)
    try:
        ejecutor.preprocess(cuaderno, {'metadata': {'path': str(NOTEBOOKS)}})
    except CellExecutionError as error:
        # El mensaje de nbconvert incluye la celda y el traceback; basta con el error final (p. ej. el assert).
        sin_color = re.sub(r'\x1b\[[0-9;]*m', '', str(error))
        ultima_linea = [linea for linea in sin_color.strip().splitlines() if linea.strip()][-1]
        raise EtapaFallida(ultima_linea) from None
    finally:
        nbformat.write(cuaderno, ruta)


def cargar_almacen():
    """Etapa de almacenamiento: copia los CSV finales y la evidencia a un SQLite consultable con SQL."""
    ALMACEN.unlink(missing_ok=True)
    conteos = {}
    with sqlite3.connect(ALMACEN) as conexion:
        for tabla, (archivo, clave) in TABLAS.items():
            datos = pd.read_csv(FINAL / archivo)
            if datos.duplicated(clave).any():
                raise EtapaFallida(f'clave {clave} repetida en {archivo}')
            datos.to_sql(tabla, conexion, index=False)
            conexion.execute(f'CREATE UNIQUE INDEX ix_{tabla} ON {tabla} ({", ".join(clave)})')
            conteos[tabla] = len(datos)

        partes = []
        for ruta in sorted(EVIDENCIA.glob('*.csv')):
            evidencia = pd.read_csv(ruta, dtype=str)
            evidencia['archivo'] = ruta.name
            # Cada archivo detalla el motivo con su propia columna; se unifican en `detalle`.
            columnas_detalle = [c for c in ('tipo', 'detalle', 'decision', 'regla') if c in evidencia]
            evidencia['detalle'] = (evidencia[columnas_detalle].bfill(axis=1).iloc[:, 0] if columnas_detalle
                                    else pd.NA)
            partes.append(evidencia.reindex(columns=['archivo', 'etapa', 'motivo', 'detalle', 'id_oferta', 'titulo',
                                                     'precio']))
        excluidos = pd.concat(partes, ignore_index=True)
        excluidos.to_sql('excluidos', conexion, index=False)
        conexion.execute('CREATE INDEX ix_excluidos ON excluidos (id_oferta, etapa)')
        conteos['excluidos'] = len(excluidos)

        for tabla, esperado in conteos.items():
            obtenido = conexion.execute(f'SELECT COUNT(*) FROM {tabla}').fetchone()[0]
            if obtenido != esperado:
                raise EtapaFallida(f'la tabla {tabla} tiene {obtenido} filas y debía tener {esperado}')
    escribir_manifiesto()
    return conteos


def escribir_manifiesto():
    """Filas, columnas y SHA-256 de cada CSV final, para comprobar que dos ejecuciones coinciden (NFR-002)."""
    manifiesto = {}
    for ruta in sorted(FINAL.glob('*.csv')):
        contenido = ruta.read_bytes().replace(b'\r\n', b'\n')
        datos = pd.read_csv(ruta)
        manifiesto[ruta.name] = {'filas': len(datos), 'columnas': datos.shape[1],
                                 'sha256': hashlib.sha256(contenido).hexdigest()}
    (FINAL / 'manifiesto.json').write_text(json.dumps(manifiesto, indent=2, sort_keys=True) + '\n', encoding='utf-8',
                                           newline='\n')


def main(argumentos=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--desde', choices=list(ETAPAS), default='01', help='primera etapa a ejecutar')
    parser.add_argument('--hasta', choices=list(ETAPAS), default='06', help='última etapa a ejecutar')
    args = parser.parse_args(argumentos)
    if args.desde > args.hasta:
        parser.error('--desde debe ser anterior o igual a --hasta')

    inicio_total = time.perf_counter()
    for codigo, (nombre, archivo) in ETAPAS.items():
        if not args.desde <= codigo <= args.hasta:
            continue
        print(f'[{codigo}] {nombre} ...', flush=True)
        inicio = time.perf_counter()
        try:
            detalle = cargar_almacen() if archivo is None else ejecutar_notebook(archivo)
        except EtapaFallida as error:
            print(f'[{codigo}] FALLÓ: {error}', file=sys.stderr)
            print(f'Pipeline detenido en la etapa {codigo}; las etapas siguientes no se ejecutaron.', file=sys.stderr)
            return 1
        extra = f' {detalle}' if detalle else ''
        print(f'[{codigo}] OK en {time.perf_counter() - inicio:.1f} s{extra}', flush=True)
    print(f'Pipeline completo en {time.perf_counter() - inicio_total:.1f} s.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
