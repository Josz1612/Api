# 🚀 Semana 1: API REST Básica con FastAPI

## 📋 Objetivo
Implementar una API REST básica con FastAPI para gestión de productos orgánicos, incluyendo operaciones CRUD completas.

## 🛠️ Tecnologías Utilizadas
- **FastAPI**: Framework web moderno para Python
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **Python 3.11+**

## 📁 Archivos Principales
- `main.py` (raíz del proyecto): Contiene todos los endpoints CRUD

## 🔧 Endpoints Implementados

### GET /api/productos
- Lista todos los productos
- Response: Array de productos

### POST /api/productos
- Crea un nuevo producto
- Body: `{nombre, categoria, precio, stock, organico}`

### GET /api/productos/{id}
- Obtiene un producto específico por ID

### PUT /api/productos/{id}
- Actualiza un producto existente

### DELETE /api/productos/{id}
- Elimina un producto

## 🚀 Cómo Ejecutar

```bash
# Instalar dependencias
pip install -r requirements.txt

# Levantar servidor
uvicorn main:app --reload --port 8000
```

## 📊 Pruebas
- Documentación automática: http://localhost:8000/docs
- Testing con Swagger UI integrado

## 📖 Documentación Completa
Ver archivo detallado: [docs/SEMANA1_API_BASICA.md](../docs/SEMANA1_API_BASICA.md)

## ✅ Criterios de Éxito
- [x] CRUD completo de productos
- [x] Validación con Pydantic
- [x] Documentación automática con OpenAPI
- [x] Manejo de errores HTTP
- [x] Código limpio y documentado
