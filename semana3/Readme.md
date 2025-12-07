Semana 3: API REST y Arquitectura Fase 2
Esta semana marca la evolución del sistema hacia una arquitectura empresarial robusta. Se implementan APIs REST siguiendo principios de diseño modernos y se reestructura la comunicación por sockets (Fase 2) utilizando patrones de Inyección de Dependencias (DI), Logging Estructurado y Manejo de Errores.

📚 Documentación de Referencia
Los siguientes archivos HTML contienen la teoría y guías paso a paso:

guia_api_rest.html: Guía completa sobre diseño de APIs REST, métodos HTTP, códigos de estado, seguridad y buenas prácticas.
fase2_python_mejorada.html: Guía técnica para implementar la Fase 2 en Python con DI, logging y testing.
contexto_fase2_arquitectura.html: Fundamentos teóricos sobre arquitectura en capas, asincronía y patrones de diseño.
🎯 Objetivos
Diseño REST: Comprender y aplicar recursos, verbos HTTP, códigos de estado y HATEOAS.
Arquitectura Robusta: Implementar una arquitectura en capas (Presentación, Servicios, Dominio, Datos).
Patrones de Diseño: Aplicar Inyección de Dependencias (DI) para desacoplar componentes.
Calidad de Código: Integrar logging estructurado y manejo robusto de excepciones (timeouts, desconexiones).
Testing: Desarrollar pruebas unitarias y de integración con pytest y mocks.
📂 Estructura del Proyecto (Fase 2)
El proyecto evoluciona de scripts sueltos a una estructura modular:

Semana3/
├── core/                   # Núcleo de la arquitectura
│   ├── contracts.py        # Interfaces (Protocolos/ABCs)
│   ├── container.py        # Contenedor de Inyección de Dependencias
│   ├── logging_config.py   # Configuración de logs
│   ├── exceptions.py       # Excepciones personalizadas
│   └── config.py           # Servicio de configuración
├── tcp_server/             # Servidor TCP robusto
│   └── server.py
├── tcp_client/             # Cliente TCP con manejo de errores
│   └── client.py
├── udp_server/             # Servidor UDP
│   └── server.py
├── api/                    # API REST con FastAPI
│   └── main.py
├── tests/                  # Suite de pruebas
│   ├── conftest.py         # Fixtures de pytest
│   ├── test_tcp.py         # Tests de sockets
│   └── test_api.py         # Tests de API
├── config/                 # Archivos de configuración
│   └── logging.json
├── requirements.txt        # Dependencias
├── run_server.py           # Entry point principal
├── central_api.py          # API Central (Versión integrada)
├── sucursal_api.py         # API Sucursal (Versión integrada)
├── events.py               # Definición de eventos
└── users_service.py        # Servicio de usuarios
🚀 Instrucciones de Ejecución
1. Preparación del Entorno
# Crear entorno virtual
python -m venv .venv
# Activar (Windows)
.venv\Scripts\activate
# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
2. Ejecutar Componentes (Fase 2)
Servidor TCP:

python -m tcp_server.server 5000
Servidor UDP:

python -m udp_server.server 5001
API REST (FastAPI):

uvicorn api.main:app --reload --port 8000
Cliente TCP (Prueba):

python -m tcp_client.client 127.0.0.1 5000 "Hola Mundo"
3. Ejecutar Pruebas
Para validar la robustez y la inyección de dependencias:

pytest tests/ -v
🧪 Ejercicios API REST (Guía HTML)
Sigue los ejercicios de guia_api_rest.html para probar conceptos REST usando curl o Postman:

Consultas GET: Filtrado, ordenamiento y paginación.
Manipulación de Recursos: POST, PUT, PATCH, DELETE.
Manejo de Errores: Simular errores 4xx y 5xx.
Control de Concurrencia: Uso de ETags e If-Match.
✅ Entregables
Código Fuente: Implementación completa de la estructura de carpetas Fase 2.
Tests: Suite de pruebas pasando con cobertura >80%.
Logs: Archivos de log generados en formato JSON/Estructurado.
Documentación: INFORME_TECNICO.md - Respuestas a las preguntas de reflexión y decisiones de diseño.
Diagrama de Arquitectura (Fase 2)

classDiagram
    class API {
        +FastAPI app
        +echo_message()
    }
    class ITcpEchoClient {
        <<interface>>
        +echo(host, port, msg)
    }
    class TcpEchoClient {
        +echo(host, port, msg)
    }
    class ConfigService {
        +get(key)
    }
    class DIContainer {
        +register()
        +get()
    }

    API --> ITcpEchoClient : Inyecta
    TcpEchoClient ..|> ITcpEchoClient : Implementa
    API --> ConfigService : Usa
    TcpEchoClient --> ConfigService : Usa
    API ..> DIContainer : Resuelve dependencias
