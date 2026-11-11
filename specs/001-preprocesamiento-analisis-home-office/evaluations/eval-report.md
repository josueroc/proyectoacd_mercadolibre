# Requirements Evaluation Report

**Feature**: `specs/001-preprocesamiento-analisis-home-office` · **Fecha**: 2026-11-10 · **Fuentes**:
`spec.md` (tras `/speckit-clarify`, 5 aclaraciones) y `.specify/memory/constitution.md` v1.0.0.

## 0. Readiness and extracted baselines

| Input | Required usable content | Status |
| --- | --- | --- |
| Constitution | Core principles and constraints | PASS |
| Spec Goal | Explicit objective | PASS |
| Personas | Target users and their needs | PASS |
| Requirements | FR and NFR tables with IDs | PASS |

**Extracted Baselines:**
1. Core Principles: I Reproducibilidad (no negociable); II Justificación metodológica; III Fidelidad al
   material del curso; IV Trazabilidad de los datos; V Verificación automática; VI Visualización interpretada.
2. Goal & Out-of-Scope: preprocesar, integrar, transformar y analizar los datos de la Parte I para generar
   "insights accionables sobre el costo de equipar un home office" (Input) con un pipeline reproducible.
   Fuera de alcance: nueva extracción, modelos predictivos, series de tiempo, apps como producto principal,
   otros componentes, análisis geoespacial, datos personales.
3. Personas: trabajador o estudiante que presupuesta su puesto; RR. HH. o empleador que provee o compensa
   equipos; docente evaluador; equipo del proyecto que presenta y edita los entregables.

**Hygiene Findings:**
- IDs completos y sin duplicados: FR-001 a FR-031, NFR-001 a NFR-006, SC-001 a SC-010.
- El objetivo está repartido entre *Input*, *Assumptions* y la constitución; no hay una sección propia. No
  bloquea la evaluación.
- Sin enunciados contradictorios tras reemplazar la aclaración de formato (LaTeX → `.docx`).

**Readiness:** `READY TO EVALUATE`

## 1. Persona-needs coverage

| Role | Need | Requirement(s) | Coverage |
| --- | --- | --- | --- |
| Trabajador / estudiante | Presupuestar el home office según nivel de equipamiento | FR-018, FR-020, FR-023 | Full |
| RR. HH. / empleador | Valor de mercado verificable por componente para proveer o compensar | FR-020, FR-021, FR-023 | Partial |
| Docente evaluador | Rigor del preprocesamiento y reproducibilidad | FR-006–FR-016, FR-024–FR-029, NFR-001, NFR-002 | Full |
| Equipo del proyecto | Entregables editables en los formatos oficiales | FR-028, FR-030, FR-031 | Full |

## 2. Reverse traceability and scope

| Requirement | Serves | Constitution / Goal Alignment | Status |
| --- | --- | --- | --- |
| FR-001–FR-005 | Docente; dataset confiable | IV Trazabilidad; I Reproducibilidad | Justified |
| FR-006–FR-009 | Docente; dataset sin sesgos | II Justificación | Justified |
| FR-010–FR-012 | Docente; trabajador (precios plausibles) | II Justificación | Justified |
| FR-013–FR-014 | Docente; validación de precios entre fechas | II, IV | Justified |
| FR-015–FR-016 | Docente | II Justificación | Justified |
| FR-017–FR-019 | Trabajador; RR. HH. | Goal (costo por nivel) | Justified |
| FR-020–FR-023 | Trabajador; RR. HH. | Goal; VI Visualización | Justified |
| FR-024–FR-026 | Docente | I Reproducibilidad; V Verificación | Justified |
| FR-027–FR-031 | Docente; equipo | I Reproducibilidad; entregables del enunciado | Justified |
| NFR-001–NFR-006 | Docente; equipo | I, III, IV, VI | Justified |

Ningún requisito queda huérfano, fuera de alcance ni en contradicción con la constitución. FR-011 usa
agrupamiento para detectar atípicos multivariados, no para predecir: no viola la exclusión de modelos
predictivos.

## 3. Block A — Persona satisfaction

| Role | Need | Requirement(s) | Score / 5 | Evidence quote(s) | Path to maximum |
| --- | --- | --- | --- | --- | --- |
| Trabajador / estudiante | Presupuesto por nivel | FR-018, FR-020 | 5/5 | "costo de equipar un home office por perfil de equipamiento" (FR-020) | — |
| RR. HH. / empleador | Valor de mercado por componente | FR-020, FR-021 | 4/5 | "con un valor central y un rango para cada perfil" (FR-020) | Pedir también valor central y rango **por componente y gama**, que es la unidad de compensación. |
| Docente evaluador | Rigor y reproducibilidad | FR-007, FR-008, NFR-001 | 5/5 | "diagnosticar el tipo de cada faltante (MCAR, MAR o MNAR) con evidencia" (FR-007) | — |
| Equipo del proyecto | Formatos oficiales editables | FR-028, FR-030, FR-031 | 5/5 | "sobre la plantilla oficial `Formato Proyecto Final Parte II.docx`" (FR-030) | — |

Media: (5 + 4 + 5 + 5) / 4 = 4,75 / 5 → **9,50 / 10**.

## 4. Block B — Critical problems & Constitution

| Principle / Goal | Sub-question | Score / 2 | Requirement(s) and evidence | Path to maximum |
| --- | --- | --- | --- | --- |
| I Reproducibilidad | ¿Un tercero regenera todo desde los crudos? | 2/2 | NFR-001: "regenerar todas las cifras publicadas desde los datos crudos" | — |
| II Justificación | ¿Cada tratamiento exige evidencia? | 2/2 | FR-008: "elegida según el tipo diagnosticado y justificada por escrito" | — |
| III Fidelidad al curso | ¿Las técnicas salen del material? | 2/2 | NFR-005: "las técnicas MUST provenir del material de clase" | — |
| IV Trazabilidad | ¿Ningún registro desaparece sin evidencia? | 2/2 | NFR-004: "ningún registro puede desaparecer del flujo sin quedar en evidencia" | — |
| V Verificación automática | ¿Los invariantes detienen el flujo en todas las etapas? | 1/2 | FR-026: "El pipeline MUST detenerse con un mensaje explícito" | Extender FR-026 a cada etapa y notebook, no solo al pipeline. |
| VI Visualización interpretada | ¿Cada gráfico tiene lectura? | 2/2 | FR-022: "título, ejes con unidades y una interpretación analítica escrita" | — |
| Goal | ¿Responde el costo del home office con insights? | 2/2 | FR-020, FR-023: "insights accionables, cada uno dirigido a un usuario identificado" | — |

Obtenido 13 / 14 → 13 / 14 × 10 = **9,29 / 10**.

**Mandatory Invariants (Constitution):**
- Los datos crudos no se modifican: PASS — FR-001 "sin modificarlos ni volver a consultar el sitio web".
- Balance de registros comprobado: PASS — SC-003 "entrada = salida + excluidos con motivo".
- Sin código sin plan (flujo SDD): PASS — fuera del spec, garantizado por `AGENTS.md`.

## 5. Block C — Backlog quality

Criterios por requisito: claro, atómico, único, trazable y verificable (1 punto cada uno). Se listan solo los
que pierden puntos; los 29 restantes obtienen 5/5.

| Requirement | Score / 5 | Failed criteria | Evidence | Path to maximum |
| --- | --- | --- | --- | --- |
| FR-003 | 4/5 | Atómico | "convertir los textos de precio, precio anterior, descuento, cuotas, reseñas…" | Aceptable como requisito de normalización; separar solo si el plan lo exige. |
| FR-011 | 4/5 | Atómico | "atípicos bivariados … y atípicos multivariados" | Separar bivariado y multivariado. |
| FR-016 | 3/5 | Claro, verificable | "las transformaciones que el análisis requiera" | Nombrar las transformaciones mínimas: codificación binaria, discretización y logaritmo del precio. |
| FR-017 | 3/5 | Atómico, claro | "especificaciones técnicas del título relevantes para cada componente" | Listar las especificaciones por componente o remitir al plan con un mínimo verificable. |
| FR-021 | 4/5 | Atómico | "incluyendo al menos: dispersión … efecto … peso … relación … diferencias" | Aceptable como lista de cobertura mínima. |
| FR-025 | 4/5 | Claro | "un almacén que permita consultarlo" | Precisar "consultable con SQL". |
| FR-028 | 4/5 | Atómico | dataset en CSV y diccionario en `.docx`/PDF en un solo requisito | Aceptable; ambos son el mismo entregable "data assets". |
| NFR-006 | 4/5 | Verificable | "MUST leerse sin ampliar" | Fijar un tamaño mínimo de texto en las figuras. |

Obtenido 175 / 185 (37 requisitos × 5) → **9,46 / 10**.

## 6. Block D — Quality attributes and feasibility

| Scenario | Score / 2 | Requirement(s) and evidence | Missing or degraded behavior | Path to maximum |
| --- | --- | --- | --- | --- |
| Edge cases | 1/2 | Edge Cases: "Una búsqueda trae accesorios en lugar del componente" | Ningún FR obliga a detectar publicaciones que no son el componente buscado. | Añadir un FR de detección y tratamiento de publicaciones ajenas al componente. |
| Rendimiento | 2/2 | NFR-003: "en menos de 10 minutos en una computadora personal" | — | — |
| Manejo de errores | 2/2 | FR-003 "registrando como inconsistencia"; FR-026 | — | — |
| Seguridad y privacidad | 2/2 | Out of Scope: "Datos personales de compradores o vendedores" | Datos públicos, sin credenciales. | — |
| Determinismo y calidad | 2/2 | NFR-002: "producir salidas idénticas"; SC-003 | — | — |

Obtenido 9 / 10 → **9,00 / 10**.

## 7. Score summary

| Dimension | Arithmetic | Score |
| --- | --- | ---: |
| Block A — Persona satisfaction | 4,75 / 5 × 10 | 9.50 |
| Block B — Critical problems & Constitution | 13 / 14 × 10 | 9.29 |
| Block C — Backlog quality | 175 / 185 × 10 | 9.46 |
| Block D — Quality attributes | 9 / 10 × 10 | 9.00 |
| **Overall** | **9,50×0,30 + 9,29×0,30 + 9,46×0,20 + 9,00×0,20 = 2,850 + 2,787 + 1,892 + 1,800** | **9.33** |
| **Verdict** | **Overall ≥ 8,00 ✓; cada bloque ≥ 7,00 ✓; 0 requisitos fuera de alcance o contradictorios ✓** | **ACCEPTABLE** |

## 8. Critical gaps

Ninguno bloqueante. Hallazgos con corrección mínima:

- `FR-020` — RR. HH. — "un rango para cada perfil" — la compensación se calcula por equipo, no por perfil —
  pedir también valor central y rango por componente y gama.
- `FR-026` — Constitución V — "El pipeline MUST detenerse" — no cubre las etapas en notebooks — extender a
  todas las etapas.
- `Edge case de accesorios` — trabajador — sin FR que lo cubra — añadir un FR.
- `FR-016`, `FR-017` — docente — formulación abierta — nombrar el mínimo verificable.

## 9. Recommendation

Spec ACEPTABLE (9,33 / 10). Aplicar las cuatro correcciones mínimas de la sección 8 antes de `/speckit-plan`
para cerrar las brechas de los bloques A, B y D; no requieren nuevas aclaraciones del usuario.

## 10. Correcciones aplicadas tras la evaluación

Aplicadas el 2026-11-10 en `spec.md`, sin cambiar decisiones ni personas: FR-016 y FR-017 precisados, FR-020
ampliado a componente y gama, FR-026 extendido a todas las etapas, FR-032 nuevo para publicaciones ajenas al
componente, NFR-006 con tamaño mínimo de texto y FR-025 precisado como almacén consultable con SQL.
