# 🛡️ Semana 4: Patrones de Resiliencia

## 📋 Objetivo
Implementar 6 estrategias de resiliencia para hacer la API robusta y tolerante a fallos, incluyendo backoff exponencial y circuit breaker.

## 🛠️ Tecnologías Utilizadas
- **FastAPI**: Framework base
- **asyncio**: Programación asíncrona
- **time/random**: Control de reintentos
- **Custom decorators**: Implementación de patrones

## 📁 Archivos Principales
- `main.py`: Contiene todas las estrategias de resiliencia implementadas

## 🔧 Estrategias Implementadas

### 1. ⏱️ Timeout
- Límite de tiempo para operaciones
- Previene bloqueos indefinidos

### 2. 🔄 Retry (Reintento Simple)
- Reintentos automáticos tras fallos
- Configurable número de intentos

### 3. 📈 Exponential Backoff
- Reintentos con espera incremental
- Fórmula: `espera = base_delay * (2 ^ intento)`
- Reduce carga en servicios bajo presión

### 4. ⚡ Circuit Breaker
- Estados: CLOSED → OPEN → HALF_OPEN
- Previene cascada de fallos
- Protección automática del sistema

### 5. 🎯 Bulkhead
- Aislamiento de recursos
- Límite de operaciones concurrentes
- Previene sobrecarga

### 6. 💾 Fallback
- Respuesta alternativa en caso de fallo
- Mantiene disponibilidad del servicio
- Datos en caché o predeterminados

## 🧪 Simulador de Fallos

Endpoint implementado: `/api/fault-simulator`
- Simula diferentes tipos de fallos
- Testing de estrategias de resiliencia
- Configuración de probabilidades

## 🚀 Cómo Probar

```bash
# Levantar servidor
uvicorn main:app --reload --port 8000

# Probar estrategias
curl http://localhost:8000/api/productos  # Con resiliencia
```

## 📊 Comparación de Estrategias

| Estrategia | Uso Ideal | Latencia | Complejidad |
|------------|-----------|----------|-------------|
| Timeout | Todas | Baja | Baja |
| Retry | Fallos temporales | Media | Baja |
| Exp. Backoff | Alta carga | Media-Alta | Media |
| Circuit Breaker | Servicios externos | Baja | Alta |
| Bulkhead | Protección recursos | Baja | Media |
| Fallback | Disponibilidad crítica | Baja | Media |

## 📖 Documentación Completa
Ver archivo detallado: [docs/SEMANA4_RESILIENCIA.md](../docs/SEMANA4_RESILIENCIA.md)

## ✅ Criterios de Éxito
- [x] 6 estrategias implementadas
- [x] Decoradores reutilizables
- [x] Simulador de fallos funcional
- [x] Logging de eventos
- [x] Testing de cada estrategia
- [x] Documentación completa
