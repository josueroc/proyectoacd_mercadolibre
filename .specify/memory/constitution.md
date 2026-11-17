<!--
Sync Impact Report:
- Version change: (none) -> 1.0.0
- Modified principles: N/A (initial ratification)
- Added sections: Core Principles I-VI, Product Context, Technology Stack, Repository Structure,
  Development Workflow, Governance
- Removed sections: N/A
- Follow-up TODOs: none
-->

# Constitución — Proyecto ACD Mercado Libre (DS3021)

## Principios fundamentales

### I. Reproducibilidad (NO NEGOCIABLE)

Todo resultado que aparezca en el informe, la presentación o el README DEBE salir de un notebook o script
versionado que se ejecute de principio a fin con *Ejecutar todas las celdas*, desde los CSV crudos del
repositorio, sin pasos manuales. Las rutas DEBEN ser relativas a la raíz del repositorio, las semillas
aleatorias DEBEN fijarse y las dependencias DEBEN estar en `requirements.txt`. Un número que no se pueda
regenerar no se publica.

### II. Justificación metodológica

Cada decisión de preprocesamiento —qué se imputa, qué se elimina, qué se considera atípico, qué se
transforma— DEBE estar respaldada por evidencia calculada en el propio notebook (tipo de faltante
MCAR/MAR/MNAR, criterio IQR o z-score, prueba chi-cuadrado, etc.) y explicada en texto junto a la celda que la
aplica. "Se eliminó porque sí" no es una justificación.

### III. Fidelidad al material del curso

Las técnicas DEBEN tomarse del material de clase de la Parte II (Unidades 3, 4 y 5: limpieza nivel 1–3,
integración, transformación, ingeniería de características, data engineering, pipelines y ETL) y de sus
librerías: pandas, numpy, matplotlib, seaborn, scipy y scikit-learn. Una herramienta o técnica fuera del
material se permite solo si es necesaria y su uso se justifica explícitamente en el plan.

### IV. Trazabilidad de los datos

Los datos crudos son de solo lectura: ningún proceso los modifica ni los sobrescribe. Cada registro que
salga del flujo (fila inválida, duplicado, atípico excluido) DEBE quedar guardado como evidencia con su
motivo, y el flujo DEBE comprobar con `assert` que el balance de registros cuadra
(entrada = salida + excluidos).

### V. Verificación automática

Los requisitos del enunciado y los invariantes de los datos DEBEN verificarse con `assert` dentro de los
notebooks (unicidad del identificador, máximo de nulos, rangos válidos, balance de registros, tipos). Un
notebook que viola un requisito DEBE fallar en lugar de exportar en silencio.

### VI. Visualización interpretada

Cada gráfico DEBE responder una pregunta del análisis, ser legible (título, ejes con unidades, escala
adecuada) e ir acompañado de una interpretación analítica escrita. No se incluyen gráficos decorativos ni
gráficos sin lectura.

## Contexto del producto

### Problema

La Ley N.º 31572 (Ley del Teletrabajo) y su reglamento obligan al empleador a proveer o compensar los
equipos del teletrabajador según su valor de mercado, pero en el Perú no existe una fuente pública de
precios de referencia. La Parte I construyó, con web scraping de Mercado Libre Perú, dos datasets: uno de
seis componentes de home office (laptop, monitor, silla de oficina, teclado, mouse y audífonos; 3 680
registros crudos, 2 936 publicaciones únicas, 15/09/2026) y uno de cinco categorías de contraste (5 080
registros crudos, 4 412 publicaciones únicas, 13/09/2026), y estimó un costo de referencia de S/ 6 335,44 como
suma de medianas.

### Objetivo de la Parte II

Preprocesar, integrar, transformar y analizar esos datos para generar hallazgos y recomendaciones útiles
sobre el costo de equipar un home office en el Perú, con un pipeline de datos documentado y reproducible.

### Usuarios

- **Trabajador o estudiante** que arma su puesto de trabajo en casa y necesita presupuestarlo.
- **Área de recursos humanos o empleador** que debe proveer equipos o calcular la compensación por uso de
  equipos propios.
- **Docente evaluador** del curso, que revisa el rigor técnico y la reproducibilidad.

## Stack tecnológico

- **Lenguaje**: Python 3.11.
- **Librerías**: pandas, numpy, matplotlib, seaborn, scipy, scikit-learn, Jupyter.
- **Almacenamiento**: archivos CSV en UTF-8; base de datos relacional ligera si el plan la justifica.
- **Control de versiones**: Git y GitHub (`josueroc/proyectoacd_mercadolibre`).

## Estructura del repositorio

El enunciado de la Parte II exige estas carpetas y archivos en la raíz:

```text
proyectoacd_mercadolibre/
├── .specify/          # Artefactos del ciclo SDD (constitución, plantillas, scripts)
├── specs/             # Especificaciones por feature (spec, plan, tasks, checklists, evaluación)
├── data/              # Datasets inicial(es) y final(es)
├── notebooks/         # Notebooks con nombres que describen lo que hacen
├── docs/              # Diccionario de datos inicial y final, informe y presentación
├── indicaciones/      # Enunciados y formatos oficiales del curso
├── README.md
└── requirements.txt
```

## Flujo de desarrollo

- Todo trabajo nuevo sigue el pipeline SDD descrito en `AGENTS.md`: especificar → aclarar → evaluar →
  planificar → checklist → tareas → analizar → **aprobación del usuario** → implementar → converger →
  publicar.
- No se escribe código de implementación sin `plan.md`, `tasks.md`, reporte de evaluación y checklists de
  la feature.
- El trabajo se hace en ramas `feature/<nombre>` creadas desde `main` y se integra con Pull Request hacia
  `main`.
- Los mensajes de commit siguen Conventional Commits. Los artefactos SDD, commits y PR se redactan en
  español, el idioma del curso y del equipo.

## Gobernanza

Esta constitución prevalece sobre cualquier otra práctica del repositorio. Una enmienda requiere proponerla
en un Pull Request, describir su impacto y actualizar la versión: MAYOR al retirar o redefinir un principio,
MENOR al añadir uno, PARCHE para aclaraciones. Toda revisión de Pull Request DEBE verificar el cumplimiento
de estos principios.

**Versión**: 1.0.0 | **Ratificada**: 2026-11-10 | **Última enmienda**: 2026-11-10
