# Goal Interpretation

## Primary goal
Usa este contenido como objetivo de prueba para validar el comportamiento autónomo del repo.

## Constraints
- - Todo debe ser gratuito y sin billing.
- - No usar servicios externos de pago.
- - No depender de secretos privados.
- - No romper el core protegido.
- - Mantener el repo limpio y sin archivos basura.
- - Debe detectar si alguna tarea no aporta valor y replanificar.
- - Viaje a Lisboa | presupuesto: bajo | duración: 3 días | prioridad personal: alta
- - Viaje a Tokio | presupuesto: alto | duración: 10 días | prioridad personal: media
- - Viaje sin destino | presupuesto: | duración:  | prioridad personal: baja
- - Escapada rural | presupuesto: medio | duración: 2 días | prioridad personal: alta
- - crear archivos útiles sin ensuciar el repo
- - no quedarse bloqueado sin motivo

## Subgoals
- Quiero que el repo diseñe, construya y deje operativa una mini solución autónoma dentro del propio repositorio para gestionar una lista priorizada de ideas de viaje en formato markdown, convertirla a datos estructurados, evaluarla con reglas simples y generar un informe final legible para una persona.
- 1. Un archivo de entrada sencillo para usuario, editable a mano.
- 2. Un parser que convierta ese archivo a JSON estructurado.
- 3. Un sistema de validación que detecte errores de formato o campos vacíos.
- 4. Un sistema de priorización simple con reglas explícitas.
- 5. Un informe final en markdown que resuma:
- - ideas válidas
- - ideas inválidas
- - ranking final
- - explicación del ranking
- 6. Un pequeño conjunto de comprobaciones que permitan al repo justificar que ha cumplido el objetivo.
- - Si el repo necesita pedirme algo, debe explicarlo de forma clara y paso a paso.
- - Debe interpretar este objetivo y convertirlo en subtareas.
- - Debe crear sus propias comprobaciones de consecución.
- - Debe autoevaluarse durante el proceso.
- - Debe dejar trazabilidad auditable.
- - Debe generar peticiones de limpieza manual si detecta archivos obsoletos.
- - Debe entrar en modo de detención si considera que el objetivo ha sido cumplido y puede justificarlo.
- El repo puede crear un archivo de ejemplo con ideas como:
- Consideraré que el repo funciona bien si consigue:
- - descomponer correctamente el objetivo
- - producir una salida estructurada y legible
- - justificar con informes por qué cree que lo ha cumplido
- Si este archivo se usa como objetivo activo, el repo debe intentar resolverlo de forma autónoma por ciclos hasta completarlo o hasta que el usuario cambie las instrucciones.
