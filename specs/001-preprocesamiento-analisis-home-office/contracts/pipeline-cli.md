# Contrato — `pipeline.py`

Interfaz que el proyecto expone a un tercero (docente, equipo) para reproducir el flujo.

## Invocación

```bash
python pipeline.py            # ejecuta todas las etapas
python pipeline.py --desde 03 # reanuda desde una etapa (requiere las salidas de las anteriores)
python pipeline.py --hasta 04 # se detiene después de una etapa
```

## Etapas

| Código | Etapa del ciclo de vida (U5_T1) | Ejecuta | Entradas | Salidas |
| --- | --- | --- | --- | --- |
| 01 | Ingestión + transformación | `notebooks/01_ingesta_y_limpieza.ipynb` | crudos de ambas capturas | `data/intermedio/01_*.csv`, `data/evidencia/01_*.csv` |
| 02 | Transformación | `notebooks/02_faltantes_y_atipicos.ipynb` | `01_homeoffice_limpio.csv` | `02_homeoffice_tratado.csv`, `data/evidencia/02_*.csv` |
| 03 | Transformación | `notebooks/03_integracion_y_reduccion.ipynb` | `02_homeoffice_tratado.csv`, `01_categorias_limpio.csv` | `03_homeoffice_integrado.csv`, `data/final/integracion_ofertas_comunes.csv` |
| 04 | Transformación | `notebooks/04_transformacion_e_ingenieria_de_caracteristicas.ipynb` | `03_homeoffice_integrado.csv` | `data/final/homeoffice_final.csv`, `precios_por_gama.csv`, `perfiles_home_office.csv` |
| 05 | Almacenamiento | función de carga en `pipeline.py` | CSV de `data/final/` y `data/evidencia/` | `data/final/home_office.sqlite`, `data/final/manifiesto.json` |
| 06 | Serving / análisis | `notebooks/05_analisis_y_visualizacion.ipynb` | `home_office.sqlite` | `data/final/metricas.json`, `docs/parte_2/figuras/*.png` |

Los notebooks se ejecutan en su lugar: quedan guardados con sus salidas, que son la evidencia que se revisa.

## Comportamiento

- Escribe en consola el inicio, la duración y el resultado de cada etapa.
- Si una etapa falla (excepción o `assert`), se detiene, informa el código de la etapa y el mensaje del
  invariante violado, y termina con código de salida distinto de 0. No ejecuta las etapas siguientes.
- Nunca escribe en `data/crudos/` ni en `data/ec1_homeoffice/homeoffice_ml_crudo.csv`.
- Código de salida 0 solo si todas las etapas solicitadas terminaron bien.

## Garantías

- Determinismo: dos ejecuciones completas producen CSV idénticos; `manifiesto.json` lo permite comprobar.
- Tiempo: el flujo completo termina en menos de 10 minutos en una computadora personal (NFR-003).
