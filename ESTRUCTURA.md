# 📚 Estructura del Proyecto EcoMarket API

## 📂 Organización por Semanas

Este repositorio contiene el desarrollo completo del proyecto EcoMarket API, organizado cronológicamente por semanas de trabajo.

### 🗂️ Estructura de Carpetas

```
EcoMarket-Compartir1/
│
├── 📁 docs/                    # Documentación completa por semanas
│   ├── README.md               # Índice principal de documentación
│   ├── SEMANA1_API_BASICA.md
│   ├── SEMANA2_INTERFAZ_WEB.md
│   ├── SEMANA3_MENSAJERIA.md
│   ├── SEMANA4_RESILIENCIA.md
│   ├── SEMANA5_TESTING.md
│   ├── SEMANA6_ESCALABILIDAD.md
│   ├── SEMANA7_OBSERVABILIDAD.md
│   ├── SEMANA7_IA_INTEGRACION.md
│   ├── SEMANA8_JWT_AUTENTICACION.md
│   └── SEMANA9_HTTPS_SECRETS.md
│
├── 📁 semana3/                 # Semana 3: Mensajería con RabbitMQ
│   ├── docker-rabbitmq-project/
│   ├── producer.py
│   ├── consumer.py
│   ├── email_consumer.py
│   ├── loyalty_consumer.py
│   └── events.py
│
├── 📁 semana6/                 # Semana 6: Escalabilidad
│   ├── nginx.conf
│   ├── shard_router.py
│   ├── test_load_balancer.py
│   ├── README_BALANCEO.md
│   ├── README-LOADBALANCER.md
│   └── INFORME-ESCALABILIDAD.md
│
├── 📁 semana7/                 # Semana 7: Observabilidad
│   ├── demo_semana7.py
│   ├── start-semana7.ps1
│   ├── README-SEMANA7.md
│   ├── INFORME-SEMANA7.md
│   └── semana_7.html
│
├── 📁 semana7-ia/              # Semana 7-IA: Integración con IA/ML
│   ├── INDICE.md
│   ├── ejercicio1/
│   ├── ejercicio2/
│   ├── ejercicio3/
│   ├── ejercicio4/
│   └── ejercicio5/
│
├── 📁 semana8/                 # Semana 8: Autenticación JWT
│   ├── README.md
│   ├── GUIA_DEMO.md
│   ├── AUDITORIA_COMPLETA.md
│   ├── auth.py
│   ├── endpoints.py
│   ├── middleware.py
│   └── models.py
│
├── 📁 semana9/                 # Semana 9: HTTPS/TLS y Secrets
│   ├── config.py
│   ├── generar_certificados.py
│   ├── HTTPS_SETUP.md
│   ├── SEMANA9_COMPLETADA.md
│   └── semana9.html
│
├── 📁 web/                     # Interfaces web
│   ├── templates.py
│   └── styles.py
│
├── main.py                     # Aplicación principal FastAPI
├── requirements.txt            # Dependencias del proyecto
├── docker-compose.yml          # Configuración Docker
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
```

## 🚀 Inicio Rápido

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/Josz1612/Eligardo-Trabajos.git
   cd Eligardo-Trabajos
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Levantar la API:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Acceder a:**
   - API: http://localhost:8000
   - Documentación: http://localhost:8000/docs
   - Dashboard: http://localhost:8000/dashboard

## 📖 Documentación por Semanas

- **[Semana 1](docs/SEMANA1_API_BASICA.md)**: API REST básica con FastAPI
- **[Semana 2](docs/SEMANA2_INTERFAZ_WEB.md)**: Interfaz web con HTML/CSS/JS
- **[Semana 3](docs/SEMANA3_MENSAJERIA.md)**: Mensajería con RabbitMQ
- **[Semana 4](docs/SEMANA4_RESILIENCIA.md)**: Patrones de resiliencia
- **[Semana 5](docs/SEMANA5_TESTING.md)**: Testing y pruebas de carga
- **[Semana 6](docs/SEMANA6_ESCALABILIDAD.md)**: Escalabilidad y load balancing
- **[Semana 7](docs/SEMANA7_OBSERVABILIDAD.md)**: Observabilidad con Prometheus/Grafana
- **[Semana 7-IA](docs/SEMANA7_IA_INTEGRACION.md)**: Integración con IA/ML
- **[Semana 8](docs/SEMANA8_JWT_AUTENTICACION.md)**: Autenticación JWT
- **[Semana 9](docs/SEMANA9_HTTPS_SECRETS.md)**: HTTPS/TLS y gestión de secretos

## 🛠️ Tecnologías Utilizadas

- **Backend:** FastAPI, Python 3.11+
- **Base de Datos:** PostgreSQL (con replicación y sharding)
- **Mensajería:** RabbitMQ
- **Balanceo:** Nginx
- **Observabilidad:** Prometheus, Grafana
- **IA/ML:** scikit-learn, transformers
- **Autenticación:** JWT (PyJWT)
- **Seguridad:** HTTPS/TLS, pydantic-settings
- **Testing:** pytest, Locust
- **Contenedores:** Docker, Docker Compose

## 👨‍💻 Autor

**José Palacios**
- GitHub: [@Josz1612](https://github.com/Josz1612)
- Repositorio: [Eligardo-Trabajos](https://github.com/Josz1612/Eligardo-Trabajos)

## 📜 Licencia

Proyecto académico - Universidad
