 Reto IA #5: Arquitectura de Seguridad EcoMarket
Este documento presenta el diseño de arquitectura de seguridad para el sistema EcoMarket, desarrollado como parte del Hito 2.

1. Contexto del Proyecto
Stack: Python (FastAPI) para Backend, Nginx como Gateway.
Servicios: Auth Service, Central API, Sucursal API, Consumers (Analytics, Bridge).
Base de Datos: PostgreSQL (Cluster con Replicación y Sharding).
Despliegue: Contenedores Docker orquestados con Docker Compose (Simulación de entorno Cloud).
Presupuesto: Bajo (Open Source, infraestructura commodity).
Datos Sensibles: Credenciales de usuario (hash), Tokens JWT, Datos de ventas e inventario.
2. Diagrama de Arquitectura (Mermaid)
Unable to render rich display

Lexical error on line 38. Unrecognized text.
...-x Nginx Nginx -- "2. HTTP (Clearte
---------------------^

For more information, see https://docs.github.com/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams#creating-mermaid-diagrams

graph TD
    %% Definición de Estilos
    classDef public fill:#f9f,stroke:#333,stroke-width:2px;
    classDef gateway fill:#ff9,stroke:#f66,stroke-width:4px;
    classDef secure fill:#9f9,stroke:#333,stroke-width:2px;
    classDef data fill:#9cf,stroke:#333,stroke-width:2px;
    classDef secrets fill:#ccc,stroke:#333,stroke-dasharray: 5 5;

    subgraph "Internet (Red Pública)"
        Client["👤 Cliente (Browser/App)"]:::public
        Attacker["👾 Atacante"]:::public
    end

    subgraph "EcoMarket Cloud (Docker Network)"
        
        subgraph "Capa de Borde (Edge)"
            Nginx["🛡️ Nginx Gateway<br/>(SSL Termination :443)<br/>[WAF Básico + Rate Limit]"]:::gateway
        end

        subgraph "Capa de Aplicación (Privada - HTTP)"
            Auth["🔑 Auth Service<br/>(:8002)"]:::secure
            Central["🏢 Central API<br/>(:8000)"]:::secure
            Sucursal["🏪 Sucursal API<br/>(:8001)"]:::secure
            Consumers["⚙️ Async Consumers"]:::secure
        end

        subgraph "Capa de Datos (Privada - TCP)"
            DB[("🐘 PostgreSQL Cluster<br/>(Primary + Replicas)")]:::data
            Rabbit["🐇 RabbitMQ<br/>(Event Bus)"]:::data
        end
    end

    subgraph "Gestión de Configuración"
        EnvVars["📄 Variables de Entorno (.env)<br/>[JWT_SECRET, DB_PASS]"]:::secrets
    end

    %% Flujos de Comunicación
    Client -- "1. HTTPS (TLS 1.3) Encrypted" --> Nginx
    Attacker -- "Blocked (Port 80/HTTP)" -.-x Nginx

    Nginx -- "2. HTTP (Cleartext)" --> Auth
    Nginx -- "2. HTTP (Cleartext)" --> Central
    Nginx -- "2. HTTP (Cleartext)" --> Sucursal

    %% Flujo de Autenticación
    Auth -- "3. Emite JWT" --> Client
    Client -- "4. Request + Bearer JWT" --> Nginx
    Central -- "5. Valida Firma JWT" --> Auth

    %% Acceso a Datos
    Central -- "SQL (Auth MD5)" --> DB
    Sucursal -- "AMQP (Auth Plain)" --> Rabbit
    Consumers -- "AMQP" --> Rabbit

    %% Inyección de Secretos
    EnvVars -.-> Auth
    EnvVars -.-> Central
    EnvVars -.-> DB
3. Decisiones de Diseño Justificadas
A. SSL Termination en Proxy (Nginx)
Decisión: El cifrado TLS se "termina" (desencripta) en el Gateway Nginx. La comunicación interna hacia los microservicios es HTTP plano.
Justificación:
Rendimiento: Descarga la tarea intensiva de CPU (criptografía) de los microservicios de aplicación (Python), permitiéndoles procesar más lógica de negocio.
Gestión Centralizada: Solo necesitamos gestionar y renovar certificados en un punto (Nginx) en lugar de en cada contenedor.
Simplicidad: Los microservicios no necesitan lógica de manejo de certificados.
B. Comunicación Interna HTTP (vs mTLS)
Decisión: Uso de HTTP estándar dentro de la red de Docker.
Justificación:
Aislamiento: La red bridge de Docker actúa como una VPC (Virtual Private Cloud). Los puertos internos (8000, 8001, 8002) no están expuestos al host ni a internet, solo al Gateway.
Costo/Beneficio: Implementar mTLS (Mutual TLS) añade una complejidad operativa significativa (Service Mesh, rotación de certificados por servicio) que excede el presupuesto y alcance actual. Para un entorno "Zero Trust" futuro, se consideraría Istio o Linkerd.
C. Gestión de Secretos: Variables de Entorno
Decisión: Inyección de secretos mediante archivos .env y Docker Compose.
Justificación:
Estándar 12-Factor App: Separa la configuración del código.
Seguridad Básica: Evita hardcodear contraseñas en el código fuente.
Portabilidad: Fácil de migrar a soluciones más robustas en la nube (como AWS Secrets Manager o Azure Key Vault) sin cambiar el código de la aplicación, solo la forma en que se inyectan las variables al contenedor.
4. Checklist de Implementación Priorizado
Fase 1: Fundamentos (Completado)
 Identidad: Implementar servicio de autenticación centralizado (JWT).
 Transporte Seguro: Configurar Nginx con certificados SSL/TLS.
 Enrutamiento: Configurar Reverse Proxy para ocultar la topología interna.
Fase 2: Hardening (En Progreso)
 Headers de Seguridad: HSTS, X-Frame-Options, X-Content-Type-Options en Nginx.
 Sanitización: Validar todas las entradas en los endpoints (Pydantic ya ayuda mucho aquí).
 Rate Limiting: Configurar límites de peticiones en Nginx para prevenir DoS básico.
Fase 3: Operaciones (Futuro)
 Rotación de Secretos: Script para rotar JWT_SECRET y contraseñas de DB periódicamente.
 Monitoreo de Seguridad: Alertas ante intentos fallidos de login masivos.
 Escaneo de Vulnerabilidades: Usar herramientas como Trivy para escanear las imágenes Docker.
5. Estimación de Esfuerzo
Componente	Tarea	Esfuerzo Est.	Estado
Gateway	Configuración SSL Nginx + Headers	4 horas	✅ Listo
Auth	Servicio JWT (Login, Verify)	8 horas	✅ Listo
Backend	Adaptación a HTTP (Quitar SSL nativo)	2 horas	✅ Listo
Infra	Configuración Docker Network Isolation	2 horas	✅ Listo
DevOps	Gestión de Secretos (.env)	2 horas	⚠️ Parcial
Total	Arquitectura Base de Seguridad	~18 horas	
