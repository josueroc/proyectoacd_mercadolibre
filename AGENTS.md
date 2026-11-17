# Proyecto ACD — Mercado Libre Perú (DS3021)

Reglas para agentes de IA que trabajen en este repositorio. El contexto del proyecto, sus principios y su
stack están en `.specify/memory/constitution.md`: leerlo antes de cualquier tarea.

## Pipeline SDD

Todo trabajo nuevo sigue este orden. No se saltan ni se reordenan pasos sin instrucción explícita del
usuario.

| Paso | Skill / acción | Resultado |
| --- | --- | --- |
| 1 | Pedido del usuario | Objetivo, comportamiento esperado y criterios de aceptación. |
| 2 | Carga de contexto | Leer `.specify/memory/*` e `indicaciones/`. |
| 3 | `/speckit-specify` | `specs/NNN-<nombre>/spec.md`. |
| 4 | `/speckit-clarify` | Hasta 5 preguntas al usuario; respuestas codificadas en el spec. |
| 5 | `/speckit-evaluate` | `evaluations/eval-report.md`. Si no aprueba, se corrige antes de seguir. |
| 6 | `/speckit-plan` | `plan.md` y artefactos de diseño. |
| 7 | `/speckit-checklist` | `checklists/*.md` de calidad. |
| 8 | `/speckit-tasks` | `tasks.md` ordenado por dependencias. |
| 9 | `/speckit-analyze` | Consistencia entre spec, plan y tasks. |
| 10 | **Aprobación del usuario** | No se implementa sin un "sí" explícito. |
| 11 | `/speckit-implement` | Ejecución de `tasks.md`. |
| 12 | `/speckit-converge` | Auditoría del código contra el spec; lo pendiente se agrega como tareas y se completa. |
| 13 | Publicación | Commit (Conventional Commits), push a `feature/<nombre>` y Pull Request hacia `main`. |

## Reglas transversales

- **Regla de parada**: antes de escribir código de implementación, verificar que existan `plan.md`,
  `tasks.md`, `evaluations/eval-report.md` y `checklists/` de la feature. Si faltan, no se escribe código.
- **Idioma**: artefactos SDD, commits y Pull Requests en español.
- **Ramas**: `feature/<nombre>` desde `main`; Pull Request hacia `main`.
- **Datos crudos**: son de solo lectura. Nada los sobrescribe.
- **Material del curso**: `material-clase-2da-parte/` es material de consulta local; no se versiona.

## Verificación antes de terminar

- [ ] Pipeline SDD completo hasta el paso 12.
- [ ] Los notebooks corren de principio a fin con *Ejecutar todas las celdas*.
- [ ] Las cifras del informe y del README coinciden con las salidas de los notebooks.
- [ ] Cambios publicados en la rama de la feature y Pull Request abierto hacia `main`.
