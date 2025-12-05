# 📘 Semana 5: Testing y Aseguramiento de Calidad

## 🎯 Objetivos de la Semana

- ✅ Implementar pruebas unitarias
- ✅ Pruebas de integración de API
- ✅ Pruebas de carga (load testing)
- ✅ Validación de resiliencia

## 📂 Archivos Principales

- `test_api.py` - Pruebas unitarias e integración
- `load_test.py` - Pruebas de carga con Locust
- `TEST-RESILIENCIA.ps1` - Script de pruebas de resiliencia

## 🧪 Tipos de Pruebas

### 1. Pruebas Unitarias (pytest)

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_producto():
    response = client.post("/api/productos", json={
        "nombre": "Test Product",
        "categoria": "Test",
        "precio": 10.0,
        "stock": 100
    })
    assert response.status_code == 201
    assert response.json()["nombre"] == "Test Product"

def test_listar_productos():
    response = client.get("/api/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 2. Pruebas de Integración

```python
def test_flujo_completo_compra():
    # 1. Crear producto
    response = client.post("/api/productos", json={...})
    producto_id = response.json()["id"]
    
    # 2. Verificar stock inicial
    response = client.get(f"/api/productos/{producto_id}")
    stock_inicial = response.json()["stock"]
    
    # 3. Realizar compra
    response = client.post(
        f"/api/productos/{producto_id}/comprar?cantidad=5"
    )
    assert response.status_code == 200
    
    # 4. Verificar stock actualizado
    response = client.get(f"/api/productos/{producto_id}")
    assert response.json()["stock"] == stock_inicial - 5
```

### 3. Pruebas de Carga (Locust)

```python
from locust import HttpUser, task, between

class EcoMarketUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def listar_productos(self):
        self.client.get("/api/productos")
    
    @task(2)
    def ver_producto(self):
        self.client.get("/api/productos/1")
    
    @task(1)
    def comprar_producto(self):
        self.client.post("/api/productos/1/comprar?cantidad=1")
```

## 🚀 Cómo Ejecutar las Pruebas

### Pruebas Unitarias con pytest
```bash
# Instalar pytest
pip install pytest pytest-asyncio

# Ejecutar todas las pruebas
pytest test_api.py -v

# Ejecutar con cobertura
pytest test_api.py --cov=main --cov-report=html
```

### Pruebas de Carga con Locust
```bash
# Instalar Locust
pip install locust

# Ejecutar Locust
locust -f load_test.py

# Abrir UI web
# http://localhost:8089
```

### Configuración de Locust
- **Users**: 100 usuarios concurrentes
- **Spawn rate**: 10 usuarios por segundo
- **Host**: http://localhost:8000

### Pruebas de Resiliencia
```powershell
# Ejecutar script PowerShell
.\TEST-RESILIENCIA.ps1
```

## 📊 Métricas de Rendimiento

### Endpoints a Probar

| Endpoint | RPS Esperado | Latencia (ms) |
|----------|-------------|---------------|
| GET /api/productos | 1000+ | < 50 |
| GET /api/productos/{id} | 800+ | < 30 |
| POST /api/productos | 500+ | < 100 |
| POST .../comprar | 300+ | < 150 |

## ✅ Casos de Prueba

### Funcionales
- ✅ Crear producto con datos válidos
- ✅ Crear producto con datos inválidos
- ✅ Actualizar producto existente
- ✅ Eliminar producto
- ✅ Comprar con stock suficiente
- ✅ Comprar con stock insuficiente
- ✅ Buscar productos
- ✅ Filtrar por categoría

### No Funcionales
- ✅ Rendimiento bajo carga
- ✅ Tiempo de respuesta < 200ms
- ✅ Concurrencia de 100+ usuarios
- ✅ Resiliencia ante fallos

### Seguridad (Preparación para Semana 8)
- ⏳ Validación de entrada
- ⏳ Sanitización de datos
- ⏳ Rate limiting
- ⏳ Autenticación/Autorización

## 📈 Resultados Esperados

### Cobertura de Código
```
Objetivo: > 80% de cobertura
- main.py: 85%
- web/templates.py: 60% (HTML templates)
- eventos.py: 90%
```

### Performance Benchmarks
```
✅ 95% de requests < 200ms
✅ 99% de requests < 500ms
✅ 0% de errores en condiciones normales
✅ < 1% de errores bajo carga extrema
```

## 🔧 Configuración de Pytest

```ini
# pytest.ini
[pytest]
testpaths = .
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

## 🎓 Conceptos Clave

- **Unit Testing**: Probar componentes individuales
- **Integration Testing**: Probar flujos completos
- **Load Testing**: Simular carga de usuarios
- **Stress Testing**: Llevar sistema al límite
- **Coverage**: Porcentaje de código probado
- **Assertions**: Verificar resultados esperados

## 📝 Reporte de Pruebas

```bash
# Generar reporte HTML
pytest test_api.py --html=report.html

# Generar reporte de cobertura
pytest test_api.py --cov=main --cov-report=html
open htmlcov/index.html
```

## 🐛 Debugging de Pruebas

```python
# Imprimir información de debug
def test_algo():
    response = client.get("/api/productos")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}")
    assert response.status_code == 200

# Usar breakpoints con pdb
import pdb; pdb.set_trace()
```

## 🎯 Mejores Prácticas

1. **Escribe pruebas antes** (TDD cuando sea posible)
2. **Pruebas independientes**: No deben depender entre sí
3. **Usa fixtures**: Reutiliza configuración común
4. **Limpia después**: Restaura estado inicial
5. **Nombres descriptivos**: `test_crear_producto_con_stock_negativo_falla`
6. **Prueba casos límite**: Valores mínimos, máximos, nulos
