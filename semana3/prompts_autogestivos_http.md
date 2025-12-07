Prompts Autogestivos para HTTP y APIs REST
🎯 PROMPT 1: PRE-CLASE (Individual - 30 min)
"Conviértete en Detective de APIs"
Tu misión: Descubrir cómo funcionan las APIs que usas diariamente, sin darte cuenta.

Paso 1: Investigación Práctica (10 min)
📋 INSTRUCCIONES PASO A PASO:

1. Abre dos ventanas:
   - Navegador en: https://jsonplaceholder.typicode.com/
   - Herramientas de desarrollador (F12 → pestaña Network)

2. Ejecuta EXACTAMENTE estas acciones y observa:
   
   Acción A: Haz clic en "GET /posts"
   📝 Anota: ¿Qué código aparece? ¿Cuántos elementos devuelve?
   
   Acción B: Modifica la URL a "/posts/1" y presiona Enter
   📝 Anota: ¿Cómo cambió la respuesta? ¿Qué código HTTP ves?
   
   Acción C: Usa Postman o curl para hacer POST /posts con:
   {
     "title": "Mi primer post",
     "body": "Esto es una prueba",
     "userId": 1
   }
   📝 Anota: ¿Qué código obtuviste? ¿Qué devolvió el servidor?

3. Patrón de observación:
   Completa esta tabla:
   | Acción | URL | Método HTTP | Código respuesta | ¿Qué hace? |
   |--------|-----|-------------|------------------|------------|
   | Listar | /posts | GET | ___ | ___ |
   | Obtener uno | /posts/1 | GET | ___ | ___ |
   | Crear | /posts | POST | ___ | ___ |
✅ Criterio de éxito: Tienes capturas de pantalla de las 3 peticiones Y puedes explicar qué patrón observas en las URLs.

Paso 2: Fundamentos Teóricos (15 min)
🎥 VIDEO OBLIGATORIO: "REST API concepts and examples"
Enlace: [proporcionar enlace específico]

MIENTRAS VES EL VIDEO, completa este organizador gráfico:

┌─────────────────────────────────────────┐
│ CONCEPTO: REST                          │
├─────────────────────────────────────────┤
│ Significa: R_____ E_____ S_____ T_____  │
│                                         │
│ Principio clave 1: ________________     │
│ Principio clave 2: ________________     │
│ Principio clave 3: ________________     │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ RECURSOS vs REPRESENTACIONES           │
├─────────────────────────────────────────┤
│ Recurso = _________________________     │
│ Representación = ___________________     │
│ Ejemplo: /users/123                     │
│ - El recurso es: ___________________    │
│ - La representación es: _____________    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ CÓDIGOS HTTP ESENCIALES                 │
├─────────────────────────────────────────┤
│ 200: ______________________________     │
│ 201: ______________________________     │
│ 400: ______________________________     │
│ 404: ______________________________     │
│ 500: ______________________________     │
└─────────────────────────────────────────┘
📤 Entregable: Documento con capturas + organizador gráfico completado.

🎯 PROMPT 2: DISEÑO DE API (Grupal - 15 min)
"Arquitectos de APIs"
Contexto del problema: EcoMarket tiene 50 productos en inventario. Necesitan que sus empleados puedan consultar, agregar, modificar y eliminar productos desde una app móvil.

Desafío de Diseño
👥 TRABAJO EN EQUIPO - Roles asignados:
- API Designer: Lidera el diseño de URLs y recursos
- Business Analyst: Valida que cubra necesidades del negocio  
- Tech Reviewer: Verifica que siga principios REST
- Documentador: Registra decisiones y justificaciones

⏱️ TIEMPO: 15 minutos exactos

🎯 PRODUCTO FINAL: Esquema de API completo

TEMPLATE OBLIGATORIO:
┌─────────────────────────────────────────────────────────┐
│ RECURSO PRINCIPAL: ________________________             │
│                                                         │
│ OPERACIONES DE NEGOCIO REQUERIDAS:                      │
│ ✓ Ver todos los productos                               │
│ ✓ Ver detalles de un producto específico               │
│ ✓ Agregar nuevo producto                                │
│ ✓ Actualizar producto existente                        │
│ ✓ Eliminar producto                                     │
│ ✓ (Agregar otras que identifiquen)                     │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ DISEÑO DE ENDPOINTS:                                    │
├─────────────────────────────────────────────────────────┤
│ GET    /____________  → Lista todos los productos       │
│ GET    /____________  → Obtiene producto específico     │
│ POST   /____________  → Crea nuevo producto             │
│ PUT    /____________  → Actualiza producto completo     │
│ DELETE /____________  → Elimina producto                │
├─────────────────────────────────────────────────────────┤
│ ENDPOINTS ADICIONALES (si los necesitan):               │
│ ___________________  → ____________________________     │
│ ___________________  → ____________________________     │
└─────────────────────────────────────────────────────────┘

💭 JUSTIFICACIONES OBLIGATORIAS:
1. ¿Por qué eligieron ese nombre para el recurso principal?
2. ¿Consideraron usar /product o /products? ¿Por qué?
3. ¿PUT reemplaza TODO el recurso o solo campos? Decidan y justifiquen.
4. ¿Qué pasa si DELETE un producto que no existe? Decidan comportamiento.
Validación Grupal
✅ CHECKPOINT - ANTES DE CONTINUAR:
□ Cada miembro puede explicar por qué eligieron esa estructura
□ Identificaron al menos 5 operaciones de negocio
□ URLs siguen convención REST (recursos como sustantivos)
□ Consideraron casos extremos (¿qué pasa si...?)

🚨 SEÑALES DE ALERTA - Revisen si tienen:
- URLs con verbos (/createProduct ❌)
- Inconsistencias (/product vs /products)
- Falta de casos extremos considerados
📤 Entregable: Esquema en papel/pizarra + foto del equipo explicando su diseño.

🎯 PROMPT 3: IMPLEMENTACIÓN BÁSICA (Grupal - 25 min)
"Constructores de APIs"
Setup Inicial (5 min)
🛠️ PREPARACIÓN DEL ENTORNO:

1. Clone el template base:
   git clone [URL-template-curso]
   cd api-rest-template

2. Instale dependencias:
   [C#] dotnet restore
   [Python] pip install -r requirements.txt

3. Verifique que funciona:
   [C#] dotnet run
   [Python] uvicorn main:app --reload
   
   ✅ Debe ver: "Server running on port 8000"

4. Prueba rápida:
   curl http://localhost:8000/health
   ✅ Debe obtener: {"status": "OK"}
Implementación Dirigida
🎯 OBJETIVO: Implementar SOLO 3 endpoints, pero hacerlos perfectos.

📋 CHECKLIST DE IMPLEMENTACIÓN:

ENDPOINT 1: GET /products (Listar todos)
□ Devuelve array de productos
□ Status code: 200
□ Maneja caso de lista vacía (devuelve [])
□ Incluye Content-Type: application/json

ENDPOINT 2: GET /products/{id} (Obtener uno)  
□ Devuelve producto específico
□ Status code: 200 si existe
□ Status code: 404 si no existe
□ Formato de error consistente: {"error": "mensaje"}

ENDPOINT 3: POST /products (Crear nuevo)
□ Acepta JSON con: name, price, stock
□ Status code: 201 si se crea exitosamente  
□ Status code: 400 si datos inválidos
□ Devuelve el producto creado con ID asignado
□ Header Location: /products/{new_id}

🚨 REGLAS DE VALIDACIÓN (implementar todas):
- name: mínimo 2 caracteres, máximo 50
- price: debe ser número >= 0
- stock: debe ser entero >= 0
- id: generado automáticamente por servidor
Proceso de Desarrollo
⚡ METODOLOGÍA DE TRABAJO (rotar roles cada 8 min):

Iteración 1 (8 min): GET /products
- Developer: Implementa lógica básica
- Tester: Prepara casos de prueba
- Documentador: Actualiza README con endpoint

Iteración 2 (8 min): GET /products/{id}
- Cambio de roles
- Developer: Implementa + manejo de errores
- Tester: Prueba con IDs válidos e inválidos  
- Documentador: Documenta códigos de error

Iteración 3 (9 min): POST /products
- Cambio de roles
- Developer: Implementa + validaciones
- Tester: Prueba casos extremos
- Documentador: Documenta formato de requests
Validación Automática
🧪 TESTING OBLIGATORIO:

1. Tests unitarios (incluidos en template):
   npm test    # o dotnet test
   ✅ Deben pasar 8/8 tests

2. Tests manuales con curl:
   # Test 1: Lista vacía inicial
   curl http://localhost:8000/products
   Esperado: []

   # Test 2: Crear producto
   curl -X POST http://localhost:8000/products \
        -H "Content-Type: application/json" \
        -d '{"name":"Lapiz","price":5.50,"stock":100}'
   Esperado: 201 + producto con ID

   # Test 3: Obtener producto creado
   curl http://localhost:8000/products/1
   Esperado: 200 + datos del producto

   # Test 4: Producto inexistente  
   curl http://localhost:8000/products/999
   Esperado: 404 + mensaje de error

3. Documentar resultados:
   Para cada test, anotar: ✅ Pasa / ❌ Falla + razón
✅ Criterio de finalización: Tests automáticos pasan + 3 productos creados exitosamente + cada miembro puede explicar un endpoint.

🎯 PROMPT 4: ROBUSTEZ Y EXPERIENCIA (Grupal - 20 min)
"Ingenieros de Confiabilidad"
Desafío: CRUD Completo
🎯 MISIÓN: Completar PUT y DELETE pensando como el usuario final.

⚖️ DILEMAS DE DISEÑO (decidir en equipo):

DILEMA 1: PUT /products/{id} cuando el producto NO existe
Opciones:
A) Devolver 404 (Not Found)
B) Crear el producto con ese ID (Upsert)
C) Devolver 400 (Bad Request)

Su decisión: _____ Justificación: _________________

DILEMA 2: DELETE /products/{id} cuando ya fue eliminado
Opciones:  
A) Devolver 404 (Not Found)
B) Devolver 204 (No Content) - idempotente
C) Devolver 410 (Gone)

Su decisión: _____ Justificación: _________________

DILEMA 3: Validación en PUT
¿PUT debe validar todos los campos o solo los enviados?
Su decisión: _________________ Justificación: _________________
Implementación de Robustez
🛡️ REQUISITOS DE CALIDAD:

ENDPOINT: PUT /products/{id}
□ Maneja caso: producto existe → actualiza
□ Maneja caso: producto no existe → [su decisión del dilema]
□ Valida todos los campos (name, price, stock)
□ Devuelve producto actualizado
□ Status codes consistentes con decisión

ENDPOINT: DELETE /products/{id}  
□ Maneja caso: producto existe → elimina
□ Maneja caso: producto no existe → [su decisión del dilema]
□ Status code apropiado
□ Body de respuesta consistente

VALIDACIÓN AVANZADA:
□ price: rechaza valores negativos
□ stock: rechaza valores negativos  
□ name: rechaza strings vacíos o solo espacios
□ Todos los errores usan mismo formato JSON:
  {"error": "descripción clara del problema"}
Testing Adversarial
🥊 PRUEBAS EXTREMAS (cada miembro toma una):

Miembro 1: "El Destructor"
- Envía datos malformados: {"price": "abc"}
- Usa IDs negativos: /products/-1
- Envía JSON inválido: {"name": }
📝 Anota: ¿Cómo responde la API? ¿Es útil para debuggear?

Miembro 2: "El Perfeccionista"
- Valida todos los códigos HTTP son correctos
- Verifica headers (Content-Type, Location)
- Confirma formato consistente de errores
📝 Anota: ¿Qué inconsistencias encuentra?

Miembro 3: "El Usuario Real"
- Hace flujo completo: CREATE → READ → UPDATE → DELETE
- Simula errores típicos de frontend
- Evalúa claridad de mensajes de error
📝 Anota: ¿Qué confundiría a un desarrollador frontend?

Miembro 4: "El Auditor"
- Revisa el código buscando casos no manejados
- Verifica logging de errores
- Evalúa manejo de excepciones
📝 Anota: ¿Qué podría fallar en producción?
🎯 PROMPT 5: ANÁLISIS DE PERFORMANCE (Grupal - 15 min)
"Ingenieros de Performance"
Medición Baseline
📊 INSTRUMENTACIÓN BÁSICA:

1. Medir tiempos de respuesta:
   # Crear archivo curl-timing.txt:
   time_namelookup:  %{time_namelookup}\n
   time_connect:     %{time_connect}\n  
   time_appconnect:  %{time_appconnect}\n
   time_pretransfer: %{time_pretransfer}\n
   time_redirect:    %{time_redirect}\n
   time_starttransfer: %{time_starttransfer}\n
   time_total:       %{time_total}\n

   # Usar para medir:
   curl -w "@curl-timing.txt" http://localhost:8000/products

2. Completar tabla baseline:
   | Endpoint | Tiempo promedio | Tiempo máximo |
   |----------|----------------|---------------|
   | GET /products | ___ms | ___ms |
   | GET /products/1 | ___ms | ___ms |  
   | POST /products | ___ms | ___ms |
Simulación de Latencia
🐌 EXPERIMENTO: Impacto de la latencia en UX

1. Modifica tu código para añadir delay artificial:
   [C#] Thread.Sleep(500); // 500ms
   [Python] time.sleep(0.5) # 500ms

2. Colócalo en UN solo endpoint de tu elección
   Endpoint elegido: _________________

3. Mide el impacto:
   Antes del delay: ___ms
   Después del delay: ___ms
   Diferencia percibida: ___ms

4. Prueba de usuario:
   - Haz que un compañero use la API sin decirle del delay
   - ¿En qué punto dice "esto está lento"?
   - Tiempo percibido como "lento": ___ms
Análisis de Carga
⚡ STRESS TEST BÁSICO:

1. Script de carga (cada equipo elige uno):
   # Bash simple:
   for i in {1..50}; do
     curl -s http://localhost:8000/products > /dev/null &
   done
   wait

   # Python con threading:
   import threading, requests, time
   def hit_api():
       requests.get('http://localhost:8000/products')
   
   threads = [threading.Thread(target=hit_api) for _ in range(50)]
   start = time.time()
   [t.start() for t in threads]
   [t.join() for t in threads]
   print(f"50 requests in {time.time() - start} seconds")

2. Observaciones durante la carga:
   - ¿La API responde más lento? ___________
   - ¿Algún error 500? ___________________
   - ¿CPU del servidor al 100%? ___________

3. Hipótesis de escalabilidad:
   Con 1000 productos y 100 req/seg simultáneas:
   Problema principal que anticipamos: _________________
   Posible solución: _________________________________
🎯 PROMPT 6: PROPUESTA DE MEJORAS (Grupal - 10 min)
"Consultores de Arquitectura"
🚀 DESAFÍO FINAL: Pensamiento de Producción

CONTEXTO AMPLIADO:
EcoMarket creció. Ahora tiene:
- 10,000 productos en catálogo
- 500 empleados usando la app
- 50 transacciones por minuto en hora pico
- Sucursales en 3 ciudades (latencia de red variable)

Tu equipo debe proponer 3 mejoras específicas:

┌─────────────────────────────────────────────────────────┐
│ MEJORA 1: PERFORMANCE                                   │
├─────────────────────────────────────────────────────────┤
│ Problema identificado:                                  │
│ ________________________________                       │
│                                                         │
│ Solución propuesta:                                     │
│ ________________________________                       │
│                                                         │
│ Implementación específica:                              │
│ ________________________________                       │
│                                                         │
│ Métrica de éxito:                                       │
│ ________________________________                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ MEJORA 2: EXPERIENCIA DE USUARIO                        │
├─────────────────────────────────────────────────────────┤
│ Problema que resuelve:                                  │
│ ________________________________                       │
│                                                         │
│ Funcionalidad nueva:                                    │
│ ________________________________                       │
│                                                         │
│ Endpoint(s) necesarios:                                 │
│ ________________________________                       │
│                                                         │
│ Beneficio para el empleado:                             │
│ ________________________________                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ MEJORA 3: CONFIABILIDAD                                 │
├─────────────────────────────────────────────────────────┤
│ Escenario de falla:                                     │
│ ________________________________                       │
│                                                         │
│ Patrón de resiliencia:                                  │
│ ________________________________                       │
│                                                         │
│ Implementación técnica:                                 │
│ ________________________________                       │
│                                                         │
│ Comportamiento esperado:                                │
│ ________________________________                       │
└─────────────────────────────────────────────────────────┘

💡 BANCO DE IDEAS (pueden usar estas u otras):
Performance: paginación, cache, índices, CDN, compresión
Experiencia: búsqueda, filtros, ordenamiento, batch operations
Confiabilidad: timeouts, retry logic, circuit breaker, graceful degradation
🎯 PROMPT 7: REFLEXIÓN INDIVIDUAL (Post-clase - 15 min)
"Metacognición Técnica"
🧠 DIARIO DE APRENDIZAJE ESTRUCTURADO:

┌─────────────────────────────────────────────────────────┐
│ 1. CAMBIO CONCEPTUAL                                    │
├─────────────────────────────────────────────────────────┤
│ Antes de esta clase, pensaba que una API era:          │
│ ________________________________________________        │
│                                                         │
│ Ahora entiendo que una API REST es:                    │
│ ________________________________________________        │
│                                                         │
│ El "click" más importante fue cuando:                  │
│ ________________________________________________        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 2. DESAFÍO TÉCNICO SUPERADO                            │
├─────────────────────────────────────────────────────────┤
│ El concepto que más me costó fue:                      │
│ ________________________________________________        │
│                                                         │
│ Me costó porque:                                        │
│ ________________________________________________        │
│                                                         │
│ Lo superé mediante (estrategia específica):            │
│ ________________________________________________        │
│                                                         │
│ Ahora lo puedo explicar así:                           │
│ ________________________________________________        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 3. CONEXIONES Y APLICACIONES                           │
├─────────────────────────────────────────────────────────┤
│ Este conocimiento me ayudará en mi proyecto            │
│ personal/profesional para:                              │
│ ________________________________________________        │
│                                                         │
│ Se conecta con [otra materia] porque:                  │
│ ________________________________________________        │
│                                                         │
│ Una pregunta que me surgió para investigar:            │
│ ________________________________________________        │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ 4. AUTOEVALUACIÓN HONESTA (1-4)                        │
├─────────────────────────────────────────────────────────┤
│ Comprendo principios REST: ___/4                       │
│ Justificación: ____________________________             │
│                                                         │
│ Puedo implementar CRUD básico: ___/4                   │
│ Justificación: ____________________________             │
│                                                         │
│ Entiendo códigos HTTP: ___/4                           │
│ Justificación: ____________________________             │
│                                                         │
│ Puedo diseñar una API simple: ___/4                    │
│ Justificación: ____________________________             │
│                                                         │
│ Mi siguiente paso de aprendizaje debe ser:             │
│ ________________________________________________        │
└─────────────────────────────────────────────────────────┘

✅ CRITERIO DE CALIDAD DE REFLEXIÓN:
□ Respuestas específicas (no "estuvo bien")
□ Conecta conceptos con experiencias concretas del taller
□ Identifica estrategias de aprendizaje que funcionaron
□ Plantea aplicaciones realistas del conocimiento
□ Autoevaluación justificada con evidencia
📊 SISTEMA DE VALIDACIÓN AUTOMÁTICA
Checklist Final de Equipo
✅ ANTES DE DECLARAR "TALLER COMPLETADO":

ARTEFACTOS TÉCNICOS:
□ Repositorio Git con commits de cada miembro
□ API responde correctamente a GET, POST, PUT, DELETE  
□ Tests automáticos pasan (mínimo 8/10)
□ README.md con instrucciones de uso
□ 5+ pruebas manuales documentadas con capturas

PROCESO DE APRENDIZAJE:
□ Bitácora de decisiones completada
□ Cada miembro rotó por todos los roles
□ Reflexiones individuales entregadas
□ Propuestas de mejora específicas y factibles

CALIDAD TÉCNICA:
□ Manejo consistente de errores
□ Códigos HTTP apropiados para cada operación
□ Validación de datos implementada
□ Documentación clara para otros desarrolladores

COMPETENCIAS SOCIOFORMATIVAS:
□ Resolución colaborativa de problemas técnicos
□ Comunicación efectiva de decisiones arquitectónicas  
□ Pensamiento crítico sobre trade-offs
□ Conexión con contexto profesional real
🎯 META FINAL: Cada miembro puede explicar cualquier parte del diseño e implementación en 2 minutos, como si fuera a otro equipo de desarrollo.