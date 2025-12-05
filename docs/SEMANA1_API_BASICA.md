# 📘 Semana 1: API REST Básica con FastAPI

## 🎯 Objetivos de la Semana

- ✅ Crear una API REST básica con FastAPI
- ✅ Implementar endpoints CRUD para productos
- ✅ Configurar documentación automática con Swagger
- ✅ Establecer validación de datos con Pydantic

## 📂 Archivos Principales

- `main.py` - Servidor FastAPI con endpoints básicos
- `requirements.txt` - Dependencias del proyecto

## 🔌 Endpoints Implementados

### Productos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/productos` | Lista todos los productos |
| `GET` | `/api/productos/{id}` | Obtiene un producto por ID |
| `POST` | `/api/productos` | Crea un nuevo producto |
| `PUT` | `/api/productos/{id}` | Actualiza un producto |
| `DELETE` | `/api/productos/{id}` | Elimina un producto |

## 📊 Modelo de Datos

```python
class Producto(BaseModel):
    id: Optional[int] = None
    nombre: str
    categoria: str
    precio: float
    stock: int
    disponible: bool = True
```

## 🚀 Cómo Ejecutar

```bash
# Instalar dependencias
pip install fastapi uvicorn

# Ejecutar servidor
uvicorn main:app --reload

# Acceder a:
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## ✨ Características Implementadas

- ✅ CRUD completo para productos
- ✅ Validación automática de datos
- ✅ Documentación interactiva con Swagger UI
- ✅ Códigos de estado HTTP correctos
- ✅ Manejo básico de errores

## 📝 Notas de Aprendizaje

- **FastAPI** permite crear APIs rápidas y eficientes
- **Pydantic** valida automáticamente los datos de entrada
- **Swagger UI** genera documentación interactiva sin código adicional
- Los decoradores `@app.get`, `@app.post`, etc., definen los endpoints

## 🎓 Conceptos Clave

- **REST**: Architectural style para APIs
- **CRUD**: Create, Read, Update, Delete
- **Validación**: Asegurar que los datos sean correctos
- **Documentación**: Swagger/OpenAPI estándar
