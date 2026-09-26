# ¿Cuánto cuesta equipar un home office en el Perú?

Proyecto final del curso **DS3021 Análisis Computacional de Datos** (UTEC, 2026-2), Parte I: adquisición de datos.

El proyecto estima el costo de equipar un home office en el Perú a partir de precios publicados en
**Mercado Libre Perú** (`listado.mercadolibre.com.pe`). Los datos se obtienen con web scraping
(Selenium para la navegación y BeautifulSoup para el análisis del HTML), sin usar APIs.

## Resultado principal

Con la mediana de precio de cada componente, un home office de seis componentes cuesta **S/ 6 335,44**.

| Componente | Publicaciones | Mediana (S/) |
| --- | ---: | ---: |
| Laptop | 466 | 4 649,00 |
| Monitor | 483 | 755,00 |
| Silla de oficina | 486 | 495,44 |
| Teclado | 493 | 190,00 |
| Audífonos | 515 | 150,00 |
| Mouse | 493 | 96,00 |
| **Total** | **2 936** | **6 335,44** |

## Datasets

| | Home office | Categorías |
| --- | --- | --- |
| Búsquedas | laptops, monitores, sillas de oficina, teclados, mouse, audífonos | laptops, audífonos, celulares, televisores, refrigeradoras |
| Fecha de extracción | 15/09/2026 | 13/09/2026 |
| Páginas | 60 (hasta 10 por búsqueda) | 95 (hasta 20 por búsqueda) |
| Registros crudos | 3 680 | 5 080 |
| Publicaciones únicas | 2 936 | 4 412 |
| Columnas del archivo final | 13 | 14 |
| Máximo de nulos por columna | 2,11 % | 1,25 % |
| Archivo final | `datos/ec1_homeoffice/homeoffice_final.csv` | `datos/limpios/mercadolibre_limpio.csv` |

El dataset de home office responde la pregunta del proyecto. El dataset de categorías se usa como contraste:
laptops y audífonos aparecen en ambos y sus medianas difieren en 5,4 % y 8,0 %.

## Estructura

```
notebooks/
  ACD_Proyecto_Parte_I.ipynb           extracción y limpieza del dataset de categorías
  generar_figuras.ipynb                figuras del informe y archivo final del home office
datos/
  crudos/mercadolibre_raw.csv          CSV crudo de categorías
  limpios/mercadolibre_limpio.csv      dataset final de categorías (UTF-8)
  calidad/                             diagnóstico, calidad por columna, filas separadas,
                                       duplicados retirados y precios excluidos
  calidad/robots/                      robots.txt descargados en la verificación
  ec1_homeoffice/
    EC1_scraping_mercadolibre.ipynb    extracción del home office (con sus salidas)
    homeoffice_ml_crudo.csv            CSV crudo del home office
    homeoffice_ml_limpio.csv           publicaciones únicas del home office, 17 columnas
    homeoffice_final.csv               dataset final del home office, 13 columnas (UTF-8)
    LEEME.txt                          origen de los archivos
documentos/
  informe_home_office.pdf              informe de la Parte I
  informe_home_office_overleaf.zip     fuente LaTeX del informe, lista para Overleaf
  latex/figuras/                       figuras generadas por generar_figuras.ipynb
  Diccionario de datos.docx            diccionario de datos del dataset de categorías (y su PDF)
  Dataset_preliminar.md                resumen del dataset de categorías, generado por el notebook
  ppt/                                 presentación de la evaluación continua 1 y sus figuras
indicaciones/                          enunciado y formatos oficiales del curso
```

Las variables del dataset de home office se describen en el Anexo A del informe.

## Cómo ejecutar

```bash
pip install -r requirements.txt
```

**Dataset de categorías.** Abrir `notebooks/ACD_Proyecto_Parte_I.ipynb` y ejecutar todas las celdas.

* Con `EJECUTAR_SCRAPER = True` (celda 1.1) se repite la captura desde el sitio. Requiere Google Chrome,
  toma alrededor de media hora por las pausas entre peticiones, puede pedir una verificación manual en la
  ventana del navegador y sobrescribe `datos/crudos/mercadolibre_raw.csv`. Como los precios cambian cada
  día, una nueva captura no reproduce las cifras del informe.
* Con `EJECUTAR_SCRAPER = False` se trabaja sobre el CSV crudo del repositorio: se verifica `robots.txt`,
  se diagnostica el crudo y se rehace la limpieza en segundos, con el mismo resultado que el versionado.

Las celdas de verificación usan `assert`: si deja de cumplirse un requisito del enunciado (1 000 registros,
6 atributos, identificadores únicos, 10 % de nulos por columna, rutas permitidas por `robots.txt`), el
notebook se detiene.

**Dataset de home office.** `datos/ec1_homeoffice/EC1_scraping_mercadolibre.ipynb` conserva las salidas de la
extracción del 15/09/2026.

**Figuras e informe.** `notebooks/generar_figuras.ipynb` lee los CSV de ambos datasets, genera
`homeoffice_final.csv` y escribe las figuras en `documentos/latex/figuras/`. El informe se compila en
Overleaf con pdfLaTeX a partir de `documentos/informe_home_office_overleaf.zip`.

## Cumplimiento del enunciado

| Requisito | Dónde se verifica |
| --- | --- |
| Técnica de scraping (Selenium y BeautifulSoup) | secciones 1.3 y 1.4 del notebook de categorías; notebook del home office |
| 6 o más atributos, numéricos y categóricos | 14 y 13 columnas en los archivos finales |
| Manejo de paginación | botón *Siguiente* y patrón `_Desde_N` en ambos notebooks |
| 1 000 registros o más | 4 412 y 2 936 publicaciones únicas |
| 10 % de nulos o menos por columna | máximos de 1,25 % y 2,11 % |
| CSV en UTF-8 | archivos finales de ambos datasets |
| Diccionario de datos | `documentos/Diccionario de datos.docx` y Anexo A del informe |
| `robots.txt`, `User-Agent`, `time.sleep()`, `try` y `except`, guardado incremental | secciones 1.1, 1.2 y 1.5 del notebook de categorías |
| Informe en PDF | `documentos/informe_home_office.pdf` |

## Equipo

| Parte | Integrante | Responsabilidad |
| --- | --- | --- |
| 1 | Yared Riveros Rodríguez | Fuente de datos, contexto y objetivos; extracción del home office |
| 2 | Franco Nicolás Roque Castillo | Script de web scraping del dataset de categorías |
| 3 | Mauricio Terán Taica | Limpieza y control de calidad |
| 4 | Josué Luna Rocha | Diccionario de datos |
| 5 | Alvaro Mauricio García Hurtado | Alcance, estrategia y viabilidad; figuras e informe en LaTeX |

## Alcance ético

Solo se extraen páginas públicas de resultados, verificadas contra `robots.txt` antes de cada ejecución.
No se recolecta información personal, se declara un `User-Agent` identificable, se mantiene una pausa entre
peticiones y no se usan técnicas de evasión de bloqueos. Los datos son de uso académico.
