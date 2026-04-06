# gautorepo

Repositorio autónomo orientado a objetivos.

## Propósito

`gautorepo` está diseñado para perseguir de forma autónoma los objetivos que el usuario escriba en `user/goal.md`, respetando una constitución técnica mínima, dejando auditoría clara y pidiendo ayuda al usuario solo cuando no exista otra vía gratuita y sin billing.

## Principios base

- El usuario habla con el repo mediante archivos simples y cómodos de entender.
- La instrucción más reciente del usuario tiene prioridad.
- El sistema trabaja por ciclos persistentes.
- El sistema puede crear, modificar y borrar gran parte de su propio código y workflows.
- El sistema no puede destruir su núcleo protegido.
- El sistema debe auditarse, observarse y justificarse a sí mismo.
- El sistema debe detenerse cuando el objetivo quede justificado como cumplido.

## Estructura inicial

- `user/` comunicación principal con el usuario
- `core/` núcleo protegido
- `agent/` capa autónoma editable
- `status/` estado visible y cómodo para el usuario
- `logs/` trazas auditables
- `reports/` informes legibles por usuario y GPT
- `self/` autoobservación y autoevaluación
- `.github/workflows/` orquestación

## Estado

Este repo está en fase de diseño inicial.
