Plan de Trabajo Autogestivo: HTTP y APIs REST
Enfoque Socioformativo | Duración: 90 minutos | Modalidad: Equipos de 3-4 estudiantes

Objetivo de Aprendizaje
Diseñar e implementar una API REST funcional aplicando principios HTTP, documentando decisiones arquitectónicas y evaluando la experiencia del usuario en un contexto de inventario empresarial.

FASE PRE-CLASE (30 minutos - Individual)
🎯 Prompt de Preparación Conceptual
Tu misión: Convertirte en un "detective de APIs" analizando cómo funcionan las APIs que usas todos los días.

Actividades obligatorias:

Explora una API real (10 min)

Ve a: https://jsonplaceholder.typicode.com/
Abre las herramientas de desarrollador (F12)
Haz estas peticiones y observa:
GET /posts (lista todos)
GET /posts/1 (obtiene uno específico)
POST /posts (crea nuevo - usa cualquier título/body)
Anota: ¿Qué códigos HTTP ves? ¿Qué patrones observas en las URLs?
Video de fundamentos (15 min)

Mira: "REST API concepts and examples" (YouTube)
Toma notas sobre: Recursos, representaciones, métodos HTTP, códigos de estado
Quiz de preparación (5 min)

Completa el cuestionario en línea (se proporcionará enlace)
Debe obtener mínimo 7/10 para participar en taller
Entregable: Documento con observaciones de la API y capturas de pantalla del navegador mostrando las peticiones.

FASE DURANTE CLASE (90 minutos - Equipos)
📋 Organización de Equipos
Roles rotativos (cambiar cada 30 min):

API Designer: Diseña estructura de recursos y endpoints
Developer: Implementa el código
Tester: Prueba y valida funcionamiento
Documentador: Registra decisiones y mantiene bitácora
🚀 PARTE A: Fundamentos REST (45 minutos)
Momento 1: Análisis y Diseño (15 min)
Prompt grupal:

Contexto: EcoMarket necesita una API para gestionar su inventario de productos.

Tu equipo debe decidir:

¿Cuál es el recurso principal? (pista: no es "inventario")
¿Qué operaciones necesita el negocio?
¿Cómo estructurarías las URLs siguiendo principios REST?
Entregable: Esquema de API en papel/pizarra:

Recurso: _________
GET /_______ → (qué hace)
POST /_______ → (qué hace)
GET /_______/{id} → (qué hace)
PUT /_______/{id} → (qué hace)
DELETE /_______/{id} → (qué hace)
Criterio de avance: Todos los miembros pueden explicar por qué eligieron esa estructura.

Momento 2: Implementación Básica (25 min)
Prompt de desarrollo:

Objetivo: Implementar GET y POST únicamente, pero hacerlo bien.

Pasos obligatorios:

Clona el template base: git clone [url-template]
Implementa SOLO:
GET /products (listar todos)
GET /products/{id} (obtener uno)
POST /products (crear nuevo)
Antes de programar: Discute en equipo qué códigos HTTP usar en cada caso
Implementa manejo de errores: ¿Qué pasa si piden un ID que no existe?
Validación automática: El template incluye tests. Ejecuta npm test (o equivalente) para validar tu implementación.

Criterio de avance: Tests básicos pasan + al menos 3 productos creados via Postman/curl.

Momento 3: Reflexión de Diseño (5 min)
Prompt de metacognición:

Registra en bitácora:

¿Qué decisión de diseño fue la más difícil?
¿Por qué elegiste esos códigos HTTP específicos?
Si fueras el frontend developer que consume esta API, ¿qué te gustaría que fuera diferente?
🔧 PARTE B: Robustez y Experiencia (45 minutos)
Momento 1: Completar CRUD (20 min)
Prompt de extensión:

Desafío: Ahora implementa PUT y DELETE, pero piensa como usuario.

Requisitos específicos:

PUT /products/{id}: ¿Debe crear si no existe o devolver 404?
DELETE /products/{id}: ¿Qué pasa si borras algo que no existe?
Añade validación: precio >= 0, stock >= 0, nombre no vacío
Consistencia: Todos los errores deben tener el mismo formato JSON
Prueba obligatoria: Cada miembro del equipo debe probar UN endpoint diferente con casos extremos (valores negativos, IDs inexistentes, etc.)

Momento 2: Observación de Rendimiento (15 min)
Prompt de análisis:

Conviértanse en observadores de performance:

Mide tiempos base: Usa curl con -w "@curl-format.txt" para medir tiempos de respuesta
Simula carga: Haz 50 peticiones seguidas al endpoint GET /products
Introduce latencia artificial: Añade Thread.Sleep(500) en C# o time.sleep(0.5) en Python a un endpoint
Observa el impacto: ¿Cómo cambia la experiencia?
Documenta: Tiempos promedio, percentil 95, y tu hipótesis sobre cuándo un usuario abandonaría.

Momento 3: Propuesta de Mejoras (10 min)
Prompt de innovación:

Pensando en producción real: Si esta API manejara 1000 productos y 100 peticiones por segundo, ¿qué problemas anticipas?

Tu equipo debe proponer 3 mejoras específicas:

Una mejora de performance (ej: paginación, cache, índices)
Una mejora de experiencia (ej: filtros, búsqueda, ordenamiento)
Una mejora de confiabilidad (ej: timeouts, retry logic, circuit breaker)
Formato: Para cada mejora, explica el problema que resuelve y cómo implementarla.

FASE POST-CLASE (15 minutos - Individual)
🤔 Prompt de Reflexión Personal
Completa tu diario de aprendizaje:

Conexión conceptual: "Antes de hoy, creía que una API era ______. Ahora entiendo que una API REST es ______."

Desafío técnico: "El concepto más difícil fue ______ porque ______. Lo superé ______."

Aplicación práctica: "Puedo usar este conocimiento para ______ en mi proyecto personal/profesional."

Autoevaluación (escala 1-4):

Comprendo principios REST: ___
Puedo implementar CRUD básico: ___
Entiendo códigos de estado HTTP: ___
Puedo diseñar una API simple: ___
Criterio de calidad: Respuestas específicas y conectadas con la experiencia del taller.

📊 SISTEMA DE EVALUACIÓN AUTOGESTIVA
Checklist de Validación Grupal
Antes de declarar "completado", verifiquen:

 API responde correctamente a todos los métodos implementados
 Manejo consistente de errores (mismo formato JSON)
 Documentación básica en README.md
 Al menos 5 pruebas manuales documentadas (con capturas)
 Bitácora de decisiones completada
 Cada miembro puede explicar una parte diferente del diseño
🛠️ RECURSOS Y HERRAMIENTAS
Templates de Código
C# Template: [enlace-repositorio-csharp]
Python Template: [enlace-repositorio-python]
Tests automatizados: Incluidos en templates
Herramientas de Prueba
Postman Collection: [enlace-collection] (pre-configurada)
curl Scripts: Incluidos en carpeta /scripts
Performance testing: Instrucciones en /docs/performance.md
Recursos de Apoyo
Cheatsheet HTTP: Códigos de estado más comunes
REST Quick Reference: Principios y mejores prácticas
Debugging Guide: Problemas comunes y soluciones
🎯 CONEXIONES SOCIOFORMATIVAS
Con el Contexto Profesional
Caso basado en necesidad real de PYME
Tecnologías usadas en la industria
Consideraciones de performance y UX
Con Otras Materias
Bases de Datos: Diseño de modelos de datos
Ingeniería de Software: Documentación y testing
Redes: Protocolos HTTP y performance
Con Proyecto de Vida
Portfolio técnico en GitHub
Habilidades de trabajo en equipo
Pensamiento crítico sobre trade-offs técnicos
📈 INDICADORES DE ÉXITO
Individual:

Completa pre-clase con 7/10 en quiz
Participa activamente en todos los roles
Reflexión post-clase demuestra comprensión profunda
Grupal:

API funcional con documentación
Decisiones técnicas justificadas
Propuestas de mejora factibles y específicas
Producto:

Código en repositorio Git
README con instrucciones de uso
Bitácora de decisiones arquitectónicas
Demo funcional de 5 minutos