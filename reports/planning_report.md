# Planning Report

Primary goal: Quiero que el repo diseñe, construya y deje operativa una mini solución autónoma dentro del propio repositorio para gestionar una lista priorizada de ideas de viaje en formato markdown, convertirla a datos estructurados, evaluarla con reglas simples y generar un informe final legible para una persona.

Interpretation signature: ee16775b989a295357b59c7729710142471ec8ab4d4f30c7821162c8ab4da405

## Deliverables
- 1. Un archivo de entrada sencillo para usuario, editable a mano.
- 2. Un parser que convierta ese archivo a JSON estructurado.
- 3. Un sistema de validación que detecte errores de formato o campos vacíos.
- 4. Un sistema de priorización simple con reglas explícitas.
- 5. Un informe final en markdown que incluya: ideas válidas; ideas inválidas; ranking final; explicación del ranking
- 6. Un pequeño conjunto de comprobaciones que permitan al repo justificar que ha cumplido el objetivo.

## Constraints
- Todo debe ser gratuito y sin billing.
- No usar servicios externos de pago.
- No depender de secretos privados.
- No romper el core protegido.
- Mantener el repo limpio y sin archivos basura.
- Si el repo necesita pedirme algo, debe explicarlo de forma clara y paso a paso.

## Behavior requirements
- Debe interpretar este objetivo y convertirlo en subtareas.
- Debe crear sus propias comprobaciones de consecución.
- Debe autoevaluarse durante el proceso.
- Debe detectar si alguna tarea no aporta valor y replanificar.
- Debe dejar trazabilidad auditable.
- Debe generar peticiones de limpieza manual si detecta archivos obsoletos.
- Debe entrar en modo de detención si considera que el objetivo ha sido cumplido y puede justificarlo.

## Success expectations
- Consideraré que el repo funciona bien si consigue:
- descomponer correctamente el objetivo
- crear archivos útiles sin ensuciar el repo
- producir una salida estructurada y legible
- justificar con informes por qué cree que lo ha cumplido
- no quedarse bloqueado sin motivo

## Test data
- El repo puede crear un archivo de ejemplo con ideas como:
- Viaje a Lisboa | presupuesto: bajo | duración: 3 días | prioridad personal: alta
- Viaje a Tokio | presupuesto: alto | duración: 10 días | prioridad personal: media
- Viaje sin destino | presupuesto: | duración:  | prioridad personal: baja
- Escapada rural | presupuesto: medio | duración: 2 días | prioridad personal: alta

## Planned tasks
- task-interpret-goal: Interpretar objetivo actual [high] (core)
- task-build-plan: Construir plan inicial [high] (core)
- task-define-checks: Definir comprobaciones de consecución [high] (verification)
- task-deliverable-1: Implementar entregable 1 [high] (deliverable)
- task-deliverable-2: Implementar entregable 2 [high] (deliverable)
- task-deliverable-3: Implementar entregable 3 [high] (deliverable)
- task-deliverable-4: Implementar entregable 4 [medium] (deliverable)
- task-deliverable-5: Implementar entregable 5 [medium] (deliverable)
- task-deliverable-6: Implementar entregable 6 [medium] (deliverable)
- task-check-constraints: Verificar restricciones activas [high] (constraints)
- task-check-behavior: Verificar requisitos de comportamiento [medium] (behavior)
- task-map-success-criteria: Mapear criterio de éxito a comprobaciones [medium] (verification)
- task-materialize-test-data: Materializar datos de prueba [medium] (test_data)
