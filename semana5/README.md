# 🧪 Semana 5: Testing y Pruebas de Carga

## 📋 Objetivo
Implementar suite completa de testing: pruebas unitarias, integración, carga, y cobertura de código para garantizar calidad del sistema.

## 🛠️ Tecnologías Utilizadas
- **pytest**: Framework de testing unitario
- **pytest-asyncio**: Testing asíncrono
- **pytest-cov**: Reporte de cobertura
- **Locust**: Pruebas de carga y estrés
- **requests**: Cliente HTTP para testing

## 📁 Archivos Principales
- `test_api.py`: Tests unitarios de endpoints
- `load_test.py`: Configuración de Locust
- `TEST-RESILIENCIA.ps1`: Script de pruebas automatizadas
- `conftest.py`: Fixtures compartidos

## 🔍 Tipos de Testing

### 1. 🧩 Tests Unitarios (pytest)
```bash
# Ejecutar todos los tests
pytest -v

# Con cobertura
pytest --cov=. --cov-report=html
```

**Áreas cubiertas:**
- CRUD de productos
- Autenticación JWT
- Estrategias de resiliencia
- Validaciones de datos

### 2. 📊 Tests de Carga (Locust)
```bash
# Iniciar Locust
locust -f load_test.py --host=http://localhost:8000

# Interfaz web: http://localhost:8089
```

**Escenarios:**
- 100 usuarios concurrentes
- Rampa de carga gradual
- Endpoints críticos (GET/POST)
- Medición de tiempos de respuesta

### 3. 🔄 Tests de Integración
- Flujos completos de usuario
- Interacción entre módulos
- Persistencia de datos
- Validación end-to-end

## 📈 Métricas Clave

| Métrica | Objetivo | Actual |
|---------|----------|--------|
| Cobertura | >80% | ✅ |
| Tests unitarios | 100% pass | ✅ |
| Tiempo respuesta P95 | <500ms | ✅ |
| Throughput | >100 req/s | ✅ |

## 🎯 Fixtures y Utilidades

```python
# Cliente de testing
@pytest.fixture
def client():
    return TestClient(app)

# Datos de prueba
@pytest.fixture
def sample_product():
    return {"nombre": "Test", "precio": 100}
```

## 🚀 Ejecución Automatizada

```powershell
# Script completo de testing
.\TEST-RESILIENCIA.ps1

# Incluye:
# - Tests unitarios
# - Tests de integración
# - Reporte de cobertura
# - Validación de estrategias
```

## 📊 Reportes Generados
- **htmlcov/index.html**: Cobertura visual
- **locust_report.html**: Resultados de carga
- **pytest_results.xml**: Formato JUnit

## 📖 Documentación Completa
Ver archivo detallado: [docs/SEMANA5_TESTING.md](../docs/SEMANA5_TESTING.md)

## ✅ Criterios de Éxito
- [x] Suite pytest configurada
- [x] Cobertura >80%
- [x] Locust configurado y funcional
- [x] Tests de integración completos
- [x] CI/CD compatible (resultados JUnit)
- [x] Scripts de automatización
- [x] Documentación de casos de prueba
