Entrega completa — Semana 7 (Actividades IA)

---

## Resumen

Objetivo: entregar material didáctico y reproducible sobre programación del lado del servidor: rutas, controladores, middleware, validación, autenticación, pruebas y observabilidad.

Framework de ejemplo usado: FastAPI (Python) para los snippets, pero las ideas son agnósticas a la tecnología.

---

## Ejercicio 1 — Esqueleto de API + contratos

Prompt inicial (para IA):

"Actúa como arquitecto/a de APIs REST. Contexto: Semana 7 (servidor). Necesito un CRUD de /products con versión en ruta (/api/v1). Requisitos: validación robusta en entrada (JSON Schema) y serialización de salida (sin nulls). Manejo de errores uniforme: { data:null, error:{code,msg,details}, meta:{} }. Seguridad básica: límite tamaño de payload y sanitización XSS/SQLi sin libs propietarias. Documentación: OpenAPI 3.0 mínima (paths, schemas). Entregables: 1) Árbol de rutas y controladores. 2) DTO de request/response con ejemplos válidos/ inválidos. 3) Esqueleto de código en el framework elegido (o pseudocódigo). 4) OpenAPI YAML mínima. 5) Casos de borde (ID inexistente, body vacío, tipos erróneos)."

Respuesta de IA (simulada):

- Estructura de proyecto sugerida y árbol de rutas.
- DTOs JSON con ejemplos válidos e inválidos.
- Esqueleto de código en FastAPI (ya incluido en `deliverables/example_fastapi.py`).
- OpenAPI mínima (`deliverables/openapi.yaml`).

Crítica técnica (qué mejorar):

- Añadir límite de payload (1MB) y sanitización simple en middleware (strip + eliminar tags HTML).
- Asegurar que la serialización elimina claves null (`exclude_none=True` en pydantic o post-procesado).

Prompt mejorado:

"Diseña un CRUD `/api/v1/products` con validación JSON Schema. Especifica: límite de payload 1MB, sanitización simple de strings (strip + eliminar etiquetas HTML), serialización que elimina claves con null, estructura uniforme de errores {data:null,error:{code,msg,details},meta:{}}, y ejemplos de request/response. Entrega: OpenAPI YAML, JSON Schema, pseudocódigo del middleware de sanitización, y 5 casos de borde con respuestas esperadas." 

Entregables prácticos incluidos:

- `deliverables/openapi.yaml`
- `deliverables/product.schema.json`
- `deliverables/example_fastapi.py`

Casos de borde (respuestas esperadas):

- ID inexistente: 404 — `{ "data": null, "error": {"code":"NOT_FOUND","msg":"Producto no encontrado","details":null }, "meta":{} }`
- Body vacío: 400 — `{ "data": null, "error": {"code":"BAD_REQUEST","msg":"Body vacío","details":["Campo 'name' requerido"] }, "meta":{} }`
- Tipos erróneos (price string): 400 con detalle de validación.
- Payload >1MB: 413 Payload Too Large.
- Nombre con HTML: sanitizar y aceptar o rechazar según política (recomendado sanitizar).

---

## Ejercicio 2 — Middleware de autenticación + rate limiting

Prompt inicial (IA):

"Eres especialista en seguridad backend. Diseña middleware para: Auth Bearer JWT (HS256), expira 15 min; refresh token por cookie httpOnly (SameSite=Lax). Rate limit: 100 req/15m por IP y 1000 req/15m por userId. Roles: admin, user; /api/v1/admin/* solo para admin. Logs estructurados (correlationId) + métricas (p50/p95, 4xx/5xx por endpoint). Entrega: A) Diagrama ASCII B) Código de ejemplo C) Tabla de respuestas 401/403/429 D) 3 pruebas exitosas y 3 fallidas."

Respuesta (simulada): diagrama ASCII, pseudocódigo de middlewares, tabla de respuestas y pruebas ejemplo.

Crítica técnica:

- Usar una solución centralizada para el rate limiter (Redis) si el servicio es multi-instanacia. Añadir manejo de revocación de refresh tokens (lista negra) y rotación de claves JWT.

Prompt mejorado (iteración):

"Diseña middleware para: JWT HS256 15min, refresh token en cookie httpOnly (SameSite=Lax) con rotación y revocación en Redis. Rate limiter con Redis (token bucket o sliding window) 100 req/15m por IP y 1000 req/15m por userId. Incluir diagrama ASCII, pseudocódigo, y 3 curl para pruebas exitosas y 3 fallidas. Explica escalado." 

Diagrama ASCII (pipeline):

```
Client -> API Gateway -> CorrelationId -> Auth (JWT) -> Rate limiter (Redis) -> RBAC -> Router -> Controller -> DB
```

Pseudocódigo (simplificado):

```python
def auth_middleware(req):
  token = get_bearer(req)
  payload = verify_jwt(token, secret)
  if not payload: return 401
  req.user = payload

def rate_limit(req):
  if not redis_allow('ip:'+req.ip, 100, 900): return 429
  if req.user and not redis_allow('user:'+req.user.id, 1000, 900): return 429
```

Respuestas estándar:

- 401: `{ "data": null, "error": {"code":"UNAUTHENTICATED","msg":"Token inválido"}, "meta":{} }`
- 403: `{ "data": null, "error": {"code":"FORBIDDEN","msg":"Acceso denegado"}, "meta":{} }`
- 429: `{ "data": null, "error": {"code":"RATE_LIMITED","msg":"Límite excedido"}, "meta":{} }`

Pruebas (ejemplos):

- Exitosas: request con JWT válido; refresh correcto; admin accede a ruta admin.
- Fallidas: token expirado → 401; user intenta ruta admin → 403; exceso de peticiones → 429.

---

## Ejercicio 3 — Validación y serialización deterministas

JSON Schema: incluido en `deliverables/product.schema.json`.

Reglas clave:

- `price` >= 0
- `currency` en [MXN,USD,EUR]
- `name` 2..80 chars
- `tags` hasta 10
- `createdAt` ISO-8601 generado por servidor

Validadores (pseudocódigo):

```python
def validate(data):
  errors=[]
  if 'name' not in data or len(data['name'])<2: errors.append(('name','nombre corto'))
  if 'price' not in data or not is_number(data['price']) or data['price']<0: errors.append(('price','>=0'))
  ...
  return errors
```

Tabla de errores (ejemplos):

- `BAD_REQUEST` — detalles con campo y mensaje.

Fuzzing: 10 casos (ejemplo):

1) `{}` → 400
2) `{name:'A',price:10}` → 400
3) `{name:'OK',price:-1}` → 400
4) `{name:'OK',price:10,currency:'XXX'}` → 400
5) `name` 2000 chars → 400
6) `tags` 50 items → 400
7) `price` 'ten' → 400
8) `createdAt` invalid format → 400
9) Control chars in strings → 400/sanitizar
10) Deeply nested unexpected objects → 400

---

## Ejercicio 4 — Pruebas de integración E2E

Escenarios y fixtures:

- Fixture limpio: iniciar DB de prueba vacía.
- Crear producto — assert 201 y response.
- Consultar, actualizar, borrar — secuencia.
- Test concurrencia: simular dos clientes que actualizan el mismo resource con version/ETag.

Scripts: `deliverables/e2e_tests.ps1` (ejemplos). Recomendación: usar pytest + httpx para pruebas automatizadas.

Indicadores a medir: cobertura de endpoints (cada endpoint llamado) y latencia media p50/p95 en las pruebas.

---

## Ejercicio 5 — Observabilidad mínima viable

Formato de log JSON recomendado:

```json
{ "ts":"2025-11-19T12:00:00Z","level":"info","correlationId":"uuid","path":"/api/v1/products","method":"GET","status":200,"latency_ms":12,"userId":null }
```

Métricas a recolectar:

- p50/p95 latencia por endpoint
- request_count
- error_rate 4xx/5xx

Dashboard sugerido y alertas ya descritos en el archivo `deliverables/SEMANA7_ENTREGA.md`.

---

## Cómo reproducir (rápido)

1) Instalar dependencias (ejemplo Python):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn pydantic
uvicorn deliverables.example_fastapi:app --reload
```

2) Ejecutar tests E2E (PowerShell):

```powershell
.\deliverables\e2e_tests.ps1
```
---