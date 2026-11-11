# Quickstart — validación de la feature

Guía para comprobar de punta a punta que la Parte II funciona. Detalles de datos en
[data-model.md](data-model.md); interfaz del pipeline en [contracts/pipeline-cli.md](contracts/pipeline-cli.md).

## Requisitos

- Python 3.11 y Git.
- Para regenerar los documentos (opcional): Microsoft Word, que exporta los `.docx` a PDF.

## Instalación

```bash
git clone https://github.com/josueroc/proyectoacd_mercadolibre.git
cd proyectoacd_mercadolibre
pip install -r requirements.txt
```

## Escenario 1 — Pipeline completo (US1–US5)

```bash
python pipeline.py
```

**Resultado esperado**: las seis etapas terminan en orden en menos de 10 minutos y el comando sale con código
0. Existen `data/final/homeoffice_final.csv`, `data/final/home_office.sqlite`, `data/final/metricas.json` y
las figuras de `docs/parte_2/figuras/`.

## Escenario 2 — Determinismo (NFR-002)

```bash
python pipeline.py
git status --short data/final data/intermedio data/evidencia
```

**Resultado esperado**: ningún CSV aparece modificado respecto de lo versionado; `manifiesto.json` no cambia.

## Escenario 3 — Invariante violado (US5, escenario 3)

Copiar el repositorio a una carpeta temporal, duplicar una fila de `data/intermedio/02_homeoffice_tratado.csv`
y ejecutar `python pipeline.py --desde 03`.

**Resultado esperado**: el pipeline se detiene en la etapa 03 con un mensaje que nombra el invariante de
unicidad de `id_oferta` y sale con código distinto de 0.

## Escenario 4 — Trazabilidad (SC-003)

```bash
python -c "import json; print(json.load(open('data/final/metricas.json'))['balance'])"
```

**Resultado esperado**: en cada etapa, filas de entrada = filas de salida + filas en evidencia.

## Escenario 5 — Consulta del almacén (FR-025)

```bash
python -c "import sqlite3; c=sqlite3.connect('data/final/home_office.sqlite'); print(c.execute('select perfil, costo_mediano from perfiles').fetchall())"
```

**Resultado esperado**: tres perfiles con su costo, iguales a los del informe.

## Escenario 6 — Entregables (US6)

Revisar que existan `README.md`, `requirements.txt`, `data/`, `notebooks/` (con `01_` a `05_`), `docs/`
(diccionarios inicial y final en `.docx` y PDF, informe en `.docx` y PDF, presentación `.pptx`), y que cada
cifra del informe coincida con `data/final/metricas.json`.
