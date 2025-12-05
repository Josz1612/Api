# 📘 Semana 4: Resiliencia y Manejo de Fallos

## 🎯 Objetivos de la Semana

- ✅ Implementar estrategias de reintentos
- ✅ Backoff exponencial
- ✅ Circuit breaker pattern
- ✅ Manejo robusto de errores

## 📂 Archivos Principales

- `main.py` - Modos de venta con resiliencia
- `web/templates.py` - UI para probar fallos

## 🔄 Estrategias de Resiliencia Implementadas

### 1. HTTP Directo (Sin Resiliencia)
```python
# Sin manejo de errores
response = requests.post(url, json=data)
```
**Resultado**: ❌ Falla inmediatamente si hay error

### 2. Reintentos Simples
```python
intentos = 3
for i in range(intentos):
    try:
        response = requests.post(url, json=data)
        break
    except:
        if i < intentos - 1:
            continue
        raise
```
**Resultado**: ✅ 3 intentos antes de fallar

### 3. Backoff Exponencial
```python
intentos = 3
for i in range(intentos):
    try:
        response = requests.post(url, json=data)
        break
    except:
        if i < intentos - 1:
            time.sleep(2 ** i)  # 1s, 2s, 4s
            continue
        raise
```
**Resultado**: ✅ Espera creciente entre intentos

### 4. Reintentos Sofisticados
```python
from tenacity import (
    retry, 
    stop_after_attempt, 
    wait_exponential,
    retry_if_exception_type
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(requests.RequestException)
)
def enviar_con_retry(data):
    return requests.post(url, json=data)
```
**Resultado**: ✅ Manejo profesional con library

### 5. Redis Queue (Persistencia)
```python
# Encolar venta si el servicio está caído
redis_client.lpush('sales_queue', json.dumps(data))

# Worker procesa cuando servicio vuelve
while True:
    data = redis_client.brpop('sales_queue')
    try:
        requests.post(url, json=data)
    except:
        redis_client.lpush('sales_queue', data)  # Re-encolar
```
**Resultado**: ✅ No se pierden ventas

### 6. RabbitMQ (Garantías)
```python
# Mensaje persistente con ACK manual
channel.basic_publish(
    exchange='sales',
    routing_key='sale',
    body=json.dumps(data),
    properties=pika.BasicProperties(delivery_mode=2)
)
```
**Resultado**: ✅ Garantía de entrega

## 🧪 Simulador de Fallos

### Panel de Pruebas en `/catalog`

Permite simular:
- ❌ **500**: Error interno del servidor
- ⏱️ **Timeout**: Demora excesiva
- 🔌 **Connection**: Fallo de conexión
- ❌ **404**: Endpoint no encontrado

```javascript
// Activar simulación de fallos
fetch('/api/fault-injection/activate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        fault_type: 'error_500',
        probability: 0.8  // 80% de fallos
    })
})
```

## 📊 Comparación de Estrategias

| Estrategia | Tiempo | Éxito | Complejidad |
|-----------|--------|-------|-------------|
| HTTP Directo | ⚡ Rápido | ❌ Bajo | 🟢 Simple |
| Reintentos Simples | ⏱️ Medio | ✅ Medio | 🟢 Simple |
| Backoff Exponencial | ⏱️ Medio | ✅ Alto | 🟡 Medio |
| Sofisticado (tenacity) | ⏱️ Medio | ✅ Muy Alto | 🟡 Medio |
| Redis Queue | ⏱️ Lento | ✅ Garantizado | 🔴 Complejo |
| RabbitMQ | ⏱️ Lento | ✅ Garantizado | 🔴 Complejo |

## 🚀 Cómo Probar

1. **Ejecutar la aplicación**
   ```bash
   python main.py
   ```

2. **Ir a Catálogo**
   ```
   http://localhost:8000/catalog
   ```

3. **Seleccionar modo de venta** desde el dropdown
   - HTTP Directo
   - Reintentos Simples
   - Backoff Exponencial
   - Reintentos Sofisticados
   - Redis Queue
   - RabbitMQ

4. **Activar fallos** desde el panel de simulación
   - Error 500 (80%)
   - Timeout (5 segundos)
   - Connection Error

5. **Intentar comprar** y observar el comportamiento

## ✨ Características Implementadas

- ✅ 6 estrategias diferentes de resiliencia
- ✅ Simulador visual de fallos
- ✅ Comparación en tiempo real
- ✅ Logs detallados de cada intento
- ✅ Métricas de éxito/fallo

## 🎓 Conceptos Clave

- **Retry Pattern**: Reintentar operaciones fallidas
- **Backoff Exponencial**: Aumentar tiempo de espera
- **Circuit Breaker**: Evitar sobrecarga de servicio caído
- **Queue-Based**: Procesamiento asíncrono garantizado
- **Idempotencia**: Operaciones seguras de reintentar

## 📈 Mejores Prácticas

1. **Usa backoff exponencial** para APIs externas
2. **Limita los reintentos** (máximo 3-5)
3. **Implementa timeouts** razonables
4. **Loggea todos los intentos** para debugging
5. **Usa queues** para operaciones críticas
6. **Implementa circuit breaker** para proteger servicios

## 🐛 Troubleshooting

### Todos los modos fallan
- Verificar que Redis esté corriendo (si usas Redis Queue)
- Verificar que RabbitMQ esté corriendo (si usas RabbitMQ)

### Reintentos no funcionan
- Revisar configuración de timeout
- Verificar logs del servidor
- Confirmar que el simulador de fallos esté activo
