# 🎨 Semana 2: Interfaz Web con HTML/CSS/JavaScript

## 📋 Objetivo
Crear interfaces web interactivas para visualizar y gestionar productos, con dashboard de estadísticas usando Chart.js.

## 🛠️ Tecnologías Utilizadas
- **HTML5**: Estructura de páginas
- **CSS3**: Estilos y diseño responsive
- **JavaScript (Vanilla)**: Interactividad
- **Chart.js**: Gráficos y visualizaciones
- **Fetch API**: Consumo de la API REST

## 📁 Archivos Principales
- `web/templates.py`: Generación de HTML dinámico
- `web/styles.py`: Estilos CSS centralizados
- `main.py`: Endpoints que sirven las páginas web

## 🌐 Páginas Implementadas

### 🏠 Homepage (/)
- Presentación del sistema
- Navegación a secciones principales

### 📊 Dashboard (/dashboard)
- Gráficos interactivos con Chart.js
- Estadísticas de productos
- Métricas en tiempo real

### 🛍️ Catálogo (/catalog)
- Lista de productos con filtros
- CRUD visual de productos
- Formularios interactivos

### 👤 Admin (/admin)
- Panel de administración
- Gestión avanzada

## 🎨 Características de Diseño
- **Responsive**: Se adapta a móviles y tablets
- **Degradados modernos**: Colores azul/morado
- **Animaciones CSS**: Hover effects y transiciones
- **Cards**: Diseño con tarjetas y sombras

## 🚀 Cómo Ver

```bash
# Levantar servidor
uvicorn main:app --reload --port 8000

# Visitar páginas
# Homepage: http://localhost:8000/
# Dashboard: http://localhost:8000/dashboard
# Catálogo: http://localhost:8000/catalog
```

## 📖 Documentación Completa
Ver archivo detallado: [docs/SEMANA2_INTERFAZ_WEB.md](../docs/SEMANA2_INTERFAZ_WEB.md)

## ✅ Criterios de Éxito
- [x] Interfaz web funcional
- [x] Dashboard con gráficos Chart.js
- [x] CRUD visual de productos
- [x] Diseño responsive
- [x] Integración completa con API
- [x] Fetch API para comunicación
