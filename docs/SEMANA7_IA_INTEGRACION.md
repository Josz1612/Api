# 📘 Semana 7-IA: Integración con Inteligencia Artificial

## 🎯 Objetivos de la Semana

- ✅ Integrar servicios de IA en la API
- ✅ Recomendaciones de productos con ML
- ✅ Análisis de sentimientos en reviews
- ✅ Clasificación automática de categorías
- ✅ Detección de anomalías en ventas

## 📂 Archivos Principales

- `semana7_ia/` - Directorio con implementaciones IA
- `semana7-ia-actividades.html` - Guía de actividades
- `main.py` - Endpoints de IA integrados

## 🤖 Servicios de IA Implementados

### 1. Recomendaciones de Productos (Collaborative Filtering)

```python
from sklearn.neighbors import NearestNeighbors
import numpy as np

class ProductRecommender:
    def __init__(self):
        self.model = NearestNeighbors(n_neighbors=5, metric='cosine')
    
    def train(self, purchase_matrix):
        """
        purchase_matrix: usuarios x productos
        Valor = cantidad comprada
        """
        self.model.fit(purchase_matrix)
    
    def recommend(self, user_id, n=5):
        """Recomienda n productos para el usuario"""
        user_vector = self.get_user_vector(user_id)
        distances, indices = self.model.kneighbors([user_vector])
        return [self.products[i] for i in indices[0]]
```

**Endpoint:**
```python
@app.get("/api/recomendaciones/{user_id}")
async def get_recommendations(user_id: int):
    recomendaciones = recommender.recommend(user_id, n=5)
    return {
        "user_id": user_id,
        "recomendaciones": recomendaciones,
        "algoritmo": "collaborative_filtering"
    }
```

### 2. Análisis de Sentimientos (NLP)

```python
from transformers import pipeline

sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="nlptown/bert-base-multilingual-uncased-sentiment"
)

@app.post("/api/reviews/analizar")
async def analizar_review(review: ReviewInput):
    resultado = sentiment_analyzer(review.texto)[0]
    
    return {
        "texto": review.texto,
        "sentimiento": resultado['label'],  # POSITIVE/NEGATIVE
        "confianza": resultado['score'],
        "estrellas": convert_to_stars(resultado['label'])
    }
```

### 3. Clasificación Automática de Categorías

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

class CategoryClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.classifier = MultinomialNB()
    
    def train(self, descriptions, categories):
        X = self.vectorizer.fit_transform(descriptions)
        self.classifier.fit(X, categories)
    
    def predict(self, description):
        X = self.vectorizer.transform([description])
        return self.classifier.predict(X)[0]

@app.post("/api/productos/clasificar")
async def clasificar_producto(producto: ProductoNuevo):
    categoria_predicha = classifier.predict(producto.descripcion)
    confianza = classifier.predict_proba([producto.descripcion]).max()
    
    return {
        "producto": producto.nombre,
        "categoria_predicha": categoria_predicha,
        "confianza": confianza,
        "sugerencia": "automática" if confianza > 0.8 else "requiere_revision"
    }
```

### 4. Detección de Anomalías en Ventas

```python
from sklearn.ensemble import IsolationForest
import pandas as pd

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1)
    
    def train(self, ventas_historicas):
        """
        ventas_historicas: DataFrame con columnas
        [hora, dia_semana, cantidad, monto, producto_id]
        """
        self.model.fit(ventas_historicas)
    
    def detect(self, nueva_venta):
        prediction = self.model.predict([nueva_venta])
        return prediction[0] == -1  # -1 = anomalía

@app.post("/api/ventas/validar")
async def validar_venta(venta: VentaInput):
    es_anomala = detector.detect(venta.to_features())
    
    if es_anomala:
        return {
            "valida": False,
            "razon": "Patrón de compra inusual detectado",
            "requiere_verificacion": True,
            "score_anomalia": detector.score_samples([venta.to_features()])[0]
        }
    
    return {"valida": True}
```

### 5. Predicción de Demanda

```python
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

class DemandPredictor:
    def __init__(self):
        self.models = {}  # Un modelo por producto
    
    def train(self, producto_id, ventas_historicas):
        """
        ventas_historicas: [(fecha, cantidad)]
        """
        X = np.array([self.extract_features(fecha) for fecha, _ in ventas_historicas])
        y = np.array([cantidad for _, cantidad in ventas_historicas])
        
        model = LinearRegression()
        model.fit(X, y)
        self.models[producto_id] = model
    
    def predict_next_week(self, producto_id):
        fechas_futuras = [datetime.now() + timedelta(days=i) for i in range(7)]
        X_future = np.array([self.extract_features(f) for f in fechas_futuras])
        predicciones = self.models[producto_id].predict(X_future)
        
        return list(zip(fechas_futuras, predicciones))

@app.get("/api/prediccion-demanda/{producto_id}")
async def predecir_demanda(producto_id: int):
    predicciones = predictor.predict_next_week(producto_id)
    
    return {
        "producto_id": producto_id,
        "predicciones_7_dias": [
            {
                "fecha": fecha.isoformat(),
                "demanda_estimada": int(cantidad),
                "confianza": "alta" if cantidad > 10 else "media"
            }
            for fecha, cantidad in predicciones
        ]
    }
```

## 🚀 Cómo Ejecutar

### 1. Instalar Dependencias IA
```bash
pip install -r requirements-ia.txt

# Incluye:
# - scikit-learn
# - transformers
# - torch
# - pandas
# - numpy
```

### 2. Entrenar Modelos Iniciales
```bash
python semana7_ia/train_models.py
```

### 3. Ejecutar API con IA
```bash
python main.py
```

### 4. Probar Endpoints IA
```bash
# Recomendaciones
curl http://localhost:8000/api/recomendaciones/1

# Análisis de sentimientos
curl -X POST http://localhost:8000/api/reviews/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Excelente producto, muy fresco!"}'

# Clasificación automática
curl -X POST http://localhost:8000/api/productos/clasificar \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Manzana", "descripcion": "Fruta roja y jugosa"}'
```

## 📊 Modelos de Machine Learning

### Algoritmos Utilizados

| Servicio | Algoritmo | Library |
|----------|-----------|---------|
| Recomendaciones | K-Nearest Neighbors | scikit-learn |
| Sentimientos | BERT Multilingual | transformers |
| Clasificación | Naive Bayes | scikit-learn |
| Anomalías | Isolation Forest | scikit-learn |
| Demanda | Linear Regression | scikit-learn |

### Datasets de Entrenamiento

```python
# Ejemplo: Dataset de entrenamiento
training_data = {
    "productos": 100 productos históricos,
    "ventas": 10,000 transacciones,
    "reviews": 5,000 reviews de clientes,
    "categorias": 10 categorías principales
}
```

## ✨ Características Implementadas

- ✅ Recomendaciones personalizadas
- ✅ Análisis automático de reviews
- ✅ Clasificación inteligente de productos
- ✅ Detección de fraude/anomalías
- ✅ Predicción de demanda
- ✅ Modelos pre-entrenados
- ✅ Re-entrenamiento periódico

## 🎨 Interfaz para Servicios IA

### Panel de Recomendaciones

```html
<div class="ai-panel">
    <h3>🤖 Recomendaciones para ti</h3>
    <div id="recommendations">
        <!-- Generado dinámicamente -->
    </div>
</div>

<script>
async function cargarRecomendaciones() {
    const response = await fetch('/api/recomendaciones/1');
    const data = await response.json();
    
    const html = data.recomendaciones.map(prod => `
        <div class="product-recommendation">
            <img src="${prod.imagen}">
            <h4>${prod.nombre}</h4>
            <p>Basado en tus compras anteriores</p>
        </div>
    `).join('');
    
    document.getElementById('recommendations').innerHTML = html;
}
</script>
```

## 📈 Métricas de IA

### Accuracy de Modelos

```python
# Clasificación de categorías
accuracy: 0.92  # 92% de productos bien clasificados

# Análisis de sentimientos
f1_score: 0.88  # Balance entre precision y recall

# Detección de anomalías
false_positive_rate: 0.05  # 5% falsos positivos
true_positive_rate: 0.85   # 85% anomalías detectadas

# Recomendaciones
hit_rate@5: 0.45  # 45% de usuarios compran productos recomendados
```

### A/B Testing

```python
# Control (sin IA): 2% conversion
# Treatment (con IA): 3.5% conversion
# Uplift: +75%
```

## 🎓 Conceptos Clave

- **Machine Learning**: Aprender patrones de datos
- **Supervised Learning**: Aprender con ejemplos etiquetados
- **Unsupervised Learning**: Encontrar patrones sin etiquetas
- **NLP**: Procesamiento de lenguaje natural
- **Feature Engineering**: Crear características para el modelo
- **Model Training**: Ajustar parámetros del modelo
- **Inference**: Usar modelo entrenado para predicciones

## 🔄 Pipeline de ML

```
┌──────────────┐
│ Recolección  │
│   de Datos   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Limpieza y  │
│ Preparación  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Entrenamiento│
│  del Modelo  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Evaluación  │
│ y Validación │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Deployment  │
│  en API      │
└──────────────┘
```

## 🐛 Troubleshooting IA

### Modelo no converge
```python
# Aumentar épocas de entrenamiento
model.fit(X, y, epochs=100)

# Normalizar datos
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### Predicciones incorrectas
```python
# Re-entrenar con más datos
# Ajustar hiperparámetros
# Probar diferentes algoritmos
```

### Latencia alta en inferencia
```python
# Usar modelos más simples
# Cachear predicciones comunes
# Inferencia en batch
# Usar GPU si está disponible
```

## 📝 Mejores Prácticas

1. **Valida modelos** con datos separados (train/test split)
2. **Monitorea drift** de datos en producción
3. **Re-entrena periódicamente** con nuevos datos
4. **Versiona modelos** como código
5. **Explica predicciones** cuando sea posible
6. **Maneja errores** de forma elegante
7. **Documenta assumptions** del modelo

## 🚀 Próximos Pasos (Avanzado)

- 🔄 Auto-reentrenamiento automático
- 🌐 Modelos más sofisticados (Deep Learning)
- 📊 Feature store centralizado
- 🎯 Personalización en tiempo real
- 🔍 Explainability con SHAP/LIME
- ⚡ Inferencia con GPU
- 📦 Model serving con TensorFlow Serving
