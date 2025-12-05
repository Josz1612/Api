# 📘 Semana 7: Observabilidad y Monitoreo

## 🎯 Objetivos de la Semana

- ✅ Implementar logging estructurado
- ✅ Métricas de rendimiento
- ✅ Tracing distribuido
- ✅ Dashboards de monitoreo

## 📂 Archivos Principales

- `main.py` - Logging y métricas integradas
- `demo_semana7.py` - Demostración de observabilidad
- `INFORME-SEMANA7.md` - Documentación completa
- `start-semana7.ps1` - Script de inicio

## 📊 Componentes de Observabilidad

### 1. Logging Estructurado

```python
import logging
import json
from datetime import datetime

logger = logging.getLogger("ecomarket")

def log_request(request, response, duration):
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
        "duration_ms": duration * 1000,
        "client_ip": request.client.host
    }
    logger.info(json.dumps(log_data))
```

### 2. Métricas de Performance

```python
from prometheus_client import Counter, Histogram

# Contadores
requests_total = Counter(
    'api_requests_total',
    'Total de requests',
    ['method', 'endpoint', 'status']
)

# Histogramas
request_duration = Histogram(
    'api_request_duration_seconds',
    'Duración de requests'
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    request_duration.observe(duration)
    return response
```

### 3. Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "checks": {
            "database": "ok",
            "rabbitmq": "ok",
            "redis": "ok"
        }
    }

@app.get("/metrics")
async def metrics():
    """Endpoint para Prometheus"""
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
```

## 📈 Stack de Monitoreo

### Arquitectura

```
┌──────────┐     ┌────────────┐     ┌──────────┐
│   API    │────▶│ Prometheus │────▶│ Grafana  │
│(Metrics) │     │ (Storage)  │     │(Dashboards)│
└──────────┘     └────────────┘     └──────────┘
      │
      └──────────▶┌────────────┐
                  │    Logs    │
                  │ (ELK/Loki) │
                  └────────────┘
```

### Herramientas Utilizadas

1. **Prometheus** - Recolección de métricas
2. **Grafana** - Visualización y dashboards
3. **Loki** - Agregación de logs
4. **Jaeger** - Tracing distribuido (opcional)

## 🚀 Cómo Ejecutar

### 1. Iniciar Stack Completo
```bash
# Con script PowerShell
.\start-semana7.ps1

# O manualmente
docker-compose -f docker-compose-observability.yml up -d
python main.py
```

### 2. Acceder a Herramientas

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Grafana | http://localhost:3000 | admin/admin |
| Prometheus | http://localhost:9090 | - |
| API Metrics | http://localhost:8000/metrics | - |

### 3. Ver Logs
```bash
# Logs en tiempo real
tail -f logs/ecomarket.log

# Buscar errores
grep "ERROR" logs/ecomarket.log

# Analizar rendimiento
grep "duration_ms" logs/ecomarket.log | jq '.duration_ms'
```

## 📊 Métricas Implementadas

### Application Metrics

| Métrica | Tipo | Descripción |
|---------|------|-------------|
| `api_requests_total` | Counter | Total de requests |
| `api_request_duration_seconds` | Histogram | Duración de requests |
| `api_errors_total` | Counter | Total de errores |
| `api_active_connections` | Gauge | Conexiones activas |
| `products_total` | Gauge | Total de productos |
| `stock_level` | Gauge | Nivel de stock |

### System Metrics (automáticas)

- CPU usage
- Memory usage
- Disk I/O
- Network traffic

## 🎨 Dashboards de Grafana

### Dashboard Principal

**Paneles incluidos:**

1. **Overview**
   - Requests per second (RPS)
   - Error rate
   - Response time (p50, p95, p99)

2. **Endpoints**
   - Top 10 endpoints más usados
   - Latencia por endpoint
   - Errores por endpoint

3. **Business Metrics**
   - Productos creados por hora
   - Compras realizadas
   - Valor de ventas

4. **System Health**
   - CPU usage
   - Memory usage
   - Active connections

### Alertas Configuradas

```yaml
# alert_rules.yml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 0.05
        annotations:
          summary: "Tasa de errores alta"
      
      - alert: SlowResponse
        expr: histogram_quantile(0.95, api_request_duration_seconds) > 1
        annotations:
          summary: "Tiempos de respuesta lentos"
```

## ✨ Características Implementadas

- ✅ Logging estructurado en JSON
- ✅ Métricas Prometheus
- ✅ Dashboards Grafana pre-configurados
- ✅ Health checks
- ✅ Alerting básico
- ✅ Correlation IDs para tracing
- ✅ Logs centralizados

## 🔍 Tracing Distribuido

### Request Tracing

```python
import uuid

@app.middleware("http")
async def tracing_middleware(request, call_next):
    # Generar trace ID
    trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
    
    # Agregar a contexto
    request.state.trace_id = trace_id
    
    # Propagar en response
    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id
    
    return response
```

### Ejemplo de Log con Trace

```json
{
  "timestamp": "2024-12-04T10:30:00",
  "trace_id": "abc123-def456",
  "level": "INFO",
  "message": "Producto creado",
  "product_id": 42,
  "duration_ms": 125
}
```

## 📈 Análisis de Performance

### Queries Útiles (Prometheus)

```promql
# RPS promedio (últimos 5 minutos)
rate(api_requests_total[5m])

# Latencia percentil 95
histogram_quantile(0.95, rate(api_request_duration_seconds_bucket[5m]))

# Tasa de errores
rate(api_errors_total[5m]) / rate(api_requests_total[5m])

# Requests más lentos
topk(10, api_request_duration_seconds)
```

## 🎓 Conceptos Clave

- **Observabilidad**: Capacidad de entender el sistema desde afuera
- **Logging**: Registro de eventos
- **Metrics**: Mediciones numéricas en el tiempo
- **Tracing**: Seguimiento de requests a través del sistema
- **SLI/SLO**: Indicadores y objetivos de nivel de servicio
- **RED Method**: Rate, Errors, Duration

## 🐛 Debugging con Observabilidad

### Scenario: API Lenta

1. **Grafana**: Ver spike en latencia
2. **Prometheus**: Identificar endpoint problemático
3. **Logs**: Buscar requests lentos con trace_id
4. **Analizar**: Query específico o proceso pesado

```bash
# Encontrar requests lentos
cat logs/ecomarket.log | jq 'select(.duration_ms > 1000)'

# Trace completo de un request
cat logs/ecomarket.log | jq 'select(.trace_id == "abc123")'
```

## 📝 Mejores Prácticas

1. **Log levels apropiados**
   - DEBUG: Desarrollo
   - INFO: Flujo normal
   - WARNING: Cosas inusuales
   - ERROR: Errores recuperables
   - CRITICAL: Sistema caído

2. **Métricas útiles**
   - Mide lo que importa al negocio
   - No medir por medir
   - Usa histogramas para latencias

3. **Alertas inteligentes**
   - Evita alert fatigue
   - Alert sobre síntomas, no causas
   - Incluye contexto en alerts

4. **Retention policies**
   - Logs: 7-30 días
   - Métricas: 1-3 meses
   - Aggregated metrics: 1 año

## 📊 SLIs y SLOs

### Service Level Indicators

- **Availability**: 99.9% uptime
- **Latency**: p95 < 200ms
- **Error Rate**: < 0.1%

### Service Level Objectives

```yaml
# SLO Definition
slo:
  - name: availability
    target: 99.9
    window: 30d
  
  - name: latency_p95
    target: 200
    unit: ms
    window: 7d
  
  - name: error_rate
    target: 0.1
    unit: percent
    window: 24h
```
