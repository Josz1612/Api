# 📘 Semana 2: Interfaz Web con HTML/CSS

## 🎯 Objetivos de la Semana

- ✅ Crear interfaz web para consumir la API
- ✅ Implementar catálogo de productos
- ✅ Diseñar panel de administración
- ✅ Agregar dashboard con estadísticas

## 📂 Archivos Principales

- `web/templates.py` - Templates HTML de las páginas
- `web/styles.py` - Estilos CSS globales y por página
- `main.py` - Rutas para servir las páginas web

## 🌐 Páginas Implementadas

### 1. Página Principal (`/`)
- Información del proyecto
- Enlaces a todas las secciones
- Descripción de características

### 2. Catálogo (`/catalog`)
- Listado visual de productos
- Búsqueda y filtros
- Sistema de compras con actualización de stock

### 3. Panel Admin (`/admin`)
- Formularios para crear productos
- Edición inline de productos
- Eliminación con confirmación

### 4. Dashboard (`/dashboard`)
- Estadísticas en tiempo real
- Gráficos con Chart.js
- Métricas de inventario

## 🎨 Diseño y Estilos

### Tecnologías Usadas
- **HTML5** - Estructura semántica
- **CSS3** - Estilos modernos con gradientes
- **JavaScript** - Interactividad y fetch API
- **Chart.js** - Gráficos interactivos

### Características Visuales
- 🎨 Gradientes coloridos
- 📱 Diseño responsive
- ✨ Animaciones suaves
- 🌈 Paleta de colores profesional

## 🔗 Integración con la API

```javascript
// Ejemplo: Obtener productos
async function cargarProductos() {
    const response = await fetch('/api/productos');
    const productos = await response.json();
    // Renderizar en la página
}

// Ejemplo: Crear producto
async function crearProducto(datos) {
    const response = await fetch('/api/productos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(datos)
    });
}
```

## 🚀 Cómo Ver las Páginas

```bash
# Ejecutar servidor
python main.py

# Visitar:
http://localhost:8000/          # Inicio
http://localhost:8000/catalog   # Catálogo
http://localhost:8000/admin     # Admin
http://localhost:8000/dashboard # Dashboard
```

## ✨ Características Implementadas

- ✅ Interfaz responsive (móvil y desktop)
- ✅ Actualización dinámica sin recargar página
- ✅ Validación de formularios en cliente
- ✅ Notificaciones de éxito/error
- ✅ Búsqueda en tiempo real
- ✅ Gráficos interactivos

## 📊 Componentes Visuales

### Cards de Productos
- Imagen del producto
- Nombre y categoría
- Precio y stock
- Botón de compra/edición

### Formularios
- Validación en tiempo real
- Feedback visual
- Manejo de errores

### Dashboard
- Gráfico de donut (categorías)
- Métricas clave (KPIs)
- Alertas de stock bajo

## 🎓 Conceptos Clave

- **SPA Básica**: Single Page Application sin framework
- **Fetch API**: Comunicación asíncrona con el servidor
- **DOM Manipulation**: Actualización dinámica del HTML
- **Responsive Design**: Adaptación a diferentes pantallas
