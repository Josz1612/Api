# 📚 Documentación por Semanas - EcoMarket API

## 📋 Índice General

Documentación completa del proyecto EcoMarket API, organizada por semanas de desarrollo.

---

## 🗓️ Cronología del Proyecto

### [📘 Semana 1: API REST Básica](SEMANA1_API_BASICA.md)
**Objetivo**: Fundamentos de FastAPI

- ✅ Endpoints CRUD completos
- ✅ Validación con Pydantic
- ✅ Documentación Swagger automática
- ✅ Manejo de errores HTTP

**Tecnologías**: FastAPI, Uvicorn, Pydantic

---

### [📘 Semana 2: Interfaz Web](SEMANA2_INTERFAZ_WEB.md)
**Objetivo**: Frontend para consumir la API

- ✅ Páginas HTML interactivas
- ✅ Catálogo de productos
- ✅ Panel de administración
- ✅ Dashboard con gráficos (Chart.js)

**Tecnologías**: HTML5, CSS3, JavaScript ES6, Chart.js

---

### [📘 Semana 3: Mensajería y Eventos](SEMANA3_MENSAJERIA.md)
**Objetivo**: Arquitectura basada en eventos

- ✅ RabbitMQ con Docker
- ✅ Productores y consumidores
- ✅ Procesamiento asíncrono de ventas
- ✅ Múltiples consumidores (email, loyalty)

**Tecnologías**: RabbitMQ, Pika, Docker

---

### [📘 Semana 4: Resiliencia](SEMANA4_RESILIENCIA.md)
**Objetivo**: Manejo robusto de fallos

- ✅ Estrategias de reintentos
- ✅ Backoff exponencial
- ✅ Circuit breaker
- ✅ Queue-based resilience (Redis, RabbitMQ)
- ✅ Simulador de fallos

**Tecnologías**: Tenacity, Redis, RabbitMQ

---

### [📘 Semana 5: Testing](SEMANA5_TESTING.md)
**Objetivo**: Aseguramiento de calidad

- ✅ Pruebas unitarias con pytest
- ✅ Pruebas de integración
- ✅ Load testing con Locust
- ✅ Cobertura de código

**Tecnologías**: pytest, Locust, coverage.py

---

### [📘 Semana 6: Escalabilidad](SEMANA6_ESCALABILIDAD.md)
**Objetivo**: Distribución y escalamiento horizontal

- ✅ Load balancer con Nginx
- ✅ Múltiples instancias de API
- ✅ Replicación de base de datos
- ✅ Sharding

**Tecnologías**: Nginx, PostgreSQL, Docker Compose

---

### [📘 Semana 7: Observabilidad](SEMANA7_OBSERVABILIDAD.md)
**Objetivo**: Monitoreo y debugging

- ✅ Logging estructurado
- ✅ Métricas con Prometheus
- ✅ Dashboards con Grafana
- ✅ Tracing distribuido
- ✅ Health checks

**Tecnologías**: Prometheus, Grafana, Loki, Jaeger

---

### [📘 Semana 7-IA: Inteligencia Artificial](SEMANA7_IA_INTEGRACION.md)
**Objetivo**: Integración de servicios de ML

- ✅ Recomendaciones de productos
- ✅ Análisis de sentimientos (NLP)
- ✅ Clasificación automática
- ✅ Detección de anomalías
- ✅ Predicción de demanda

**Tecnologías**: scikit-learn, transformers, PyTorch

---

### [📘 Semana 8: JWT y Autenticación](SEMANA8_JWT_AUTENTICACION.md)
**Objetivo**: Seguridad y control de acceso

- ✅ Autenticación con JWT
- ✅ Sistema de roles (admin, vendedor, cliente)
- ✅ Protección de endpoints
- ✅ Refresh tokens
- ✅ Demo visual interactiva

**Tecnologías**: PyJWT, OAuth2, pydantic-settings

---

### [📘 Semana 9: HTTPS y Secrets](SEMANA9_HTTPS_SECRETS.md)
**Objetivo**: Encriptación y gestión de configuración

- ✅ HTTPS con certificados SSL/TLS
- ✅ Generación de certificados
- ✅ Gestión de secrets con pydantic-settings
- ✅ Variables de entorno (.env)
- ✅ Redirección HTTP → HTTPS

**Tecnologías**: TLS/SSL, cryptography, pydantic-settings

---

## 🎯 Mapa de Conceptos

```
┌─────────────────────────────────────────────────────────┐
│                    EcoMarket API                        │
│                 Sistema Enterprise                      │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
   │  Core   │        │ Scaling │        │Security │
   │ (S1-S3) │        │ (S4-S7) │        │ (S8-S9) │
   └─────────┘        └─────────┘        └─────────┘
        │                   │                   │
   ┌────┴────┐         ┌────┴────┐         ┌────┴────┐
   │S1: API  │         │S4: Fail │         │S8: JWT  │
   │S2: UI   │         │S5: Test │         │S9: HTTPS│
   │S3: Msg  │         │S6: Scale│         └─────────┘
   └─────────┘         │S7: Obs  │
                       │S7I: AI  │
                       └─────────┘
```

## 📊 Evolución del Stack Tecnológico

| Semana | Backend | Frontend | Infra | Security |
|--------|---------|----------|-------|----------|
| 1 | FastAPI | - | - | - |
| 2 | FastAPI | HTML/CSS/JS | - | - |
| 3 | FastAPI | HTML/CSS/JS | RabbitMQ | - |
| 4 | + Tenacity | HTML/CSS/JS | + Redis | - |
| 5 | + Testing | HTML/CSS/JS | Redis/RabbitMQ | - |
| 6 | FastAPI | HTML/CSS/JS | + Nginx/PostgreSQL | - |
| 7 | FastAPI | + Grafana | + Prometheus | - |
| 7-IA | + ML Models | HTML/CSS/JS | Infra | - |
| 8 | + PyJWT | + JWT Demo | Infra | JWT |
| 9 | FastAPI | HTML/CSS/JS | Infra | + HTTPS/TLS |

## 🎓 Objetivos de Aprendizaje por Semana

### Semana 1-3: Fundamentos
- Crear APIs REST profesionales
- Diseñar interfaces web interactivas
- Implementar arquitectura basada en eventos

### Semana 4-5: Robustez
- Manejar fallos de forma resiliente
- Implementar pruebas automatizadas
- Garantizar calidad del código

### Semana 6-7: Escala
- Distribuir carga entre servidores
- Monitorear sistemas en producción
- Integrar inteligencia artificial

### Semana 8-9: Seguridad
- Proteger endpoints con autenticación
- Encriptar comunicaciones
- Gestionar secrets de forma segura

## 📦 Dependencias Completas

```txt
# requirements.txt (todas las semanas)

# Core (S1-S2)
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0

# Mensajería (S3)
pika==1.3.2
redis==5.0.1

# Resiliencia (S4)
tenacity==8.2.3
requests==2.31.0

# Testing (S5)
pytest==7.4.3
pytest-asyncio==0.21.1
locust==2.19.1
coverage==7.3.2

# Escalabilidad (S6)
psycopg2-binary==2.9.9
sqlalchemy==2.0.23

# Observabilidad (S7)
prometheus-client==0.19.0

# IA (S7-IA)
scikit-learn==1.3.2
transformers==4.35.2
torch==2.1.1
pandas==2.1.3
numpy==1.26.2

# Seguridad (S8-S9)
PyJWT==2.8.0
python-multipart==0.0.6
pydantic-settings==2.1.0
cryptography==41.0.7
```

## 🚀 Quick Start

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/ecomarket-api.git
cd ecomarket-api

# 2. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus secrets

# 5. Generar certificados (Semana 9)
python generar_certificados.py

# 6. Iniciar servicios (opcional)
docker-compose up -d  # RabbitMQ, Redis, PostgreSQL

# 7. Ejecutar API
python main.py

# 8. Acceder
# https://localhost:8443
```

## 📖 Cómo Navegar la Documentación

### Por Funcionalidad
- **APIs**: Semana 1
- **UI**: Semana 2
- **Async**: Semana 3
- **Resilience**: Semana 4
- **Quality**: Semana 5
- **Scale**: Semana 6, 7
- **AI**: Semana 7-IA
- **Security**: Semana 8, 9

### Por Tecnología
- **FastAPI**: Todas las semanas
- **Docker**: Semana 3, 6
- **Testing**: Semana 5
- **ML**: Semana 7-IA
- **JWT**: Semana 8
- **HTTPS**: Semana 9

### Por Dificultad
- 🟢 **Básico**: Semana 1, 2
- 🟡 **Intermedio**: Semana 3, 4, 5, 8
- 🔴 **Avanzado**: Semana 6, 7, 7-IA, 9

## 🎬 Demos y Presentaciones

Cada semana incluye:
- ✅ Código funcional completo
- ✅ Documentación detallada
- ✅ Ejemplos de uso
- ✅ Scripts de automatización
- ✅ Troubleshooting común

## 📞 Soporte

Para dudas sobre:
- **Conceptos**: Revisar sección "🎓 Conceptos Clave" de cada semana
- **Implementación**: Ver ejemplos de código en cada documento
- **Errores**: Consultar sección "🐛 Troubleshooting"

## 🏆 Proyecto Completo

Al finalizar las 9 semanas, habrás construido:

✅ **API REST** profesional y documentada
✅ **Interfaz web** moderna y responsiva
✅ **Arquitectura de eventos** desacoplada
✅ **Sistema resiliente** ante fallos
✅ **Suite de pruebas** automatizadas
✅ **Infraestructura escalable** con load balancing
✅ **Observabilidad completa** con métricas y logs
✅ **Integración de IA** para recomendaciones
✅ **Seguridad robusta** con JWT y HTTPS
✅ **Gestión de secrets** profesional

---

## 📄 Licencia

Proyecto educativo - Libre para uso académico

## 👨‍💻 Autor

Desarrollado como proyecto universitario de Arquitectura de Software

---

<div align="center">
  <h3>🌟 ¡Sistema Enterprise Completo! 🌟</h3>
  <p><strong>De API Básica a Plataforma de Producción</strong></p>
</div>
