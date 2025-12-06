# Fundamentos de Sistemas Distribuidos

## Introducción

Los sistemas distribuidos representan un paradigma fundamental en la arquitectura de software moderna, permitiendo que múltiples componentes trabajen de forma coordinada a través de redes de comunicación. Este documento explora los conceptos esenciales, diferencias arquitectónicas y tecnologías de comunicación que sustentan estos sistemas.

---

## 1. Taxonomía de Arquitecturas de Sistemas

### 1.1 Sistemas Centralizados

#### Características Principales

Los sistemas centralizados concentran todo el procesamiento, almacenamiento y control en un único servidor o conjunto de servidores bajo una autoridad central única.

**Arquitectura típica:**
- Servidor central que gestiona todas las operaciones
- Clientes que dependen completamente del servidor central
- Base de datos única y centralizada
- Lógica de negocio concentrada en un solo punto

#### Ventajas

- **Simplicidad administrativa**: Un único punto de gestión facilita configuración, mantenimiento y actualizaciones
- **Control total**: La autoridad centralizada puede aplicar políticas de forma uniforme
- **Consistencia de datos**: Más fácil garantizar integridad y coherencia
- **Menor complejidad inicial**: Desarrollo y despliegue más directos
- **Costos iniciales reducidos**: Menos infraestructura distribuida

#### Desventajas

- **Punto único de fallo (SPOF)**: Si el servidor central falla, todo el sistema queda inoperativo
- **Escalabilidad limitada**: Dificultad para crecer más allá de la capacidad del servidor central
- **Cuellos de botella**: El servidor puede saturarse con alto volumen de peticiones
- **Latencia geográfica**: Usuarios distantes experimentan mayor retraso
- **Riesgo de sobrecarga**: Todos los procesos compiten por los mismos recursos

#### Ejemplos de Aplicación

- Mainframes tradicionales en instituciones bancarias
- Sistemas de gestión empresarial (ERP) monolíticos
- Bases de datos relacionales tradicionales en arquitectura cliente-servidor
- Aplicaciones web simples con servidor único

---

### 1.2 Sistemas Distribuidos

#### Características Principales

Arquitectura donde múltiples componentes autónomos, separados físicamente, colaboran a través de una red para presentarse ante los usuarios como un sistema unificado.

**Principios fundamentales:**
- Componentes independientes comunicándose mediante paso de mensajes
- Coordinación para alcanzar objetivos comunes
- Transparencia: el usuario percibe un sistema único
- Recursos compartidos entre nodos

#### Ventajas

- **Escalabilidad horizontal**: Capacidad de añadir más nodos para aumentar capacidad
- **Tolerancia a fallos**: Redundancia permite que el sistema continúe operando si un componente falla
- **Distribución de carga**: El trabajo se reparte entre múltiples nodos
- **Rendimiento mejorado**: Procesamiento paralelo acelera operaciones
- **Ubicación geográfica**: Nodos cercanos a usuarios reducen latencia
- **Utilización eficiente de recursos**: Aprovechamiento de hardware heterogéneo

#### Desafíos

- **Complejidad arquitectónica**: Diseño, implementación y debugging más complicados
- **Sincronización**: Coordinar estados entre nodos requiere protocolos sofisticados
- **Consistencia eventual**: Difícil mantener datos consistentes en tiempo real
- **Latencia de red**: Comunicación entre nodos introduce retrasos
- **Gestión de fallos parciales**: Algunos nodos pueden fallar mientras otros continúan
- **Seguridad distribuida**: Más puntos de ataque potenciales

#### Ejemplos de Aplicación

- Plataformas de computación en la nube (AWS, Azure, Google Cloud)
- Arquitecturas de microservicios (Netflix, Uber, Amazon)
- Bases de datos distribuidas (Cassandra, MongoDB, CockroachDB)
- Sistemas de archivos distribuidos (HDFS, GlusterFS)
- CDN (Content Delivery Networks) como Cloudflare, Akamai

---

### 1.3 Sistemas Descentralizados

#### Características Principales

Variante extrema de sistemas distribuidos donde no existe autoridad central ni coordinador único. Cada nodo tiene autonomía completa y las decisiones se toman mediante consenso.

**Propiedades distintivas:**
- Ausencia de punto central de control
- Nodos con igualdad de privilegios (peer-to-peer)
- Toma de decisiones mediante consenso distribuido
- Mayor énfasis en transparencia y verificabilidad

#### Ventajas

- **Resiliencia extrema**: No hay punto único de fallo central
- **Resistencia a censura**: Difícil que una autoridad bloquee el sistema
- **Transparencia**: Operaciones visibles para todos los participantes
- **Democratización**: Ninguna entidad controla unilateralmente el sistema
- **Inmutabilidad**: Registros permanentes y verificables (en blockchain)

#### Desafíos

- **Coordinación compleja**: Alcanzar consenso entre nodos independientes es costoso
- **Rendimiento limitado**: Protocolos de consenso pueden ser lentos
- **Vulnerabilidades de seguridad**: Ataques Sybil, 51%, eclipse
- **Gobernanza difícil**: Implementar cambios requiere consenso amplio
- **Consumo de recursos**: Algunos algoritmos (PoW) son muy costosos energéticamente

#### Ejemplos de Aplicación

- Blockchain y criptomonedas (Bitcoin, Ethereum)
- Redes P2P de compartición de archivos (BitTorrent)
- Sistemas de nombres descentralizados (IPFS)
- Aplicaciones descentralizadas (DApps)
- Protocolos de mensajería distribuida (Matrix, XMPP)

---

## 2. Tecnologías de Comunicación en Sistemas Distribuidos

### 2.1 Sockets

#### Definición y Conceptos

Un **socket** es una abstracción de software que representa un punto terminal de comunicación bidireccional entre dos procesos, ya sea en la misma máquina o a través de una red.

**Componentes de un socket:**
- **Dirección IP**: Identifica el host en la red
- **Número de puerto**: Identifica el proceso específico en el host
- **Protocolo**: Define reglas de comunicación (TCP o UDP)

#### Tipos de Sockets

**Sockets TCP (SOCK_STREAM):**
- Comunicación orientada a conexión
- Garantiza entrega ordenada y confiable
- Control de flujo y congestión
- Usado cuando la integridad de datos es crítica

**Sockets UDP (SOCK_DGRAM):**
- Comunicación sin conexión
- No garantiza entrega ni orden
- Menor sobrecarga, mayor velocidad
- Usado en streaming, gaming, DNS

#### Funcionamiento Cliente-Servidor con Sockets

**Proceso del servidor:**
1. Crear socket con `socket()`
2. Vincular socket a dirección/puerto con `bind()`
3. Escuchar conexiones entrantes con `listen()`
4. Aceptar conexión con `accept()`
5. Recibir/enviar datos con `recv()`/`send()`
6. Cerrar conexión con `close()`

**Proceso del cliente:**
1. Crear socket con `socket()`
2. Conectar al servidor con `connect()`
3. Enviar/recibir datos con `send()`/`recv()`
4. Cerrar conexión con `close()`

#### Aplicaciones

- Servidores web y aplicaciones
- Protocolos de red de bajo nivel
- Juegos multijugador en tiempo real
- Chat y mensajería instantánea
- Transferencia de archivos

---

### 2.2 HTTP y APIs REST

#### HTTP (Hypertext Transfer Protocol)

**Características fundamentales:**
- Protocolo de capa de aplicación para sistemas hipermedia
- Modelo request-response sin estado (stateless)
- Basado en texto, legible por humanos
- Usa TCP/IP como transporte subyacente

**Métodos HTTP principales:**
- **GET**: Recuperar recurso (idempotente, seguro)
- **POST**: Crear nuevo recurso
- **PUT**: Actualizar/reemplazar recurso completo
- **PATCH**: Actualización parcial de recurso
- **DELETE**: Eliminar recurso
- **HEAD**: Obtener headers sin cuerpo
- **OPTIONS**: Consultar métodos soportados

**Códigos de estado HTTP:**
- **1xx**: Informacional
- **2xx**: Éxito (200 OK, 201 Created, 204 No Content)
- **3xx**: Redirección (301 Moved, 304 Not Modified)
- **4xx**: Error del cliente (400 Bad Request, 401 Unauthorized, 404 Not Found)
- **5xx**: Error del servidor (500 Internal Error, 503 Service Unavailable)

#### REST (Representational State Transfer)

**Principios arquitectónicos REST:**

1. **Interfaz uniforme**: 
   - Recursos identificados por URIs
   - Manipulación mediante representaciones
   - Mensajes autodescriptivos
   - HATEOAS (Hypermedia as the Engine of Application State)

2. **Sin estado (Stateless)**:
   - Cada petición contiene toda la información necesaria
   - El servidor no mantiene contexto de sesión
   - Mejora escalabilidad y simplicidad

3. **Cacheable**:
   - Respuestas deben indicar si son cacheables
   - Mejora rendimiento y escalabilidad

4. **Sistema en capas**:
   - Arquitectura jerárquica donde cada componente no ve más allá de su capa inmediata
   - Permite intermediarios (proxies, gateways, load balancers)

5. **Cliente-servidor**:
   - Separación de responsabilidades
   - Evolución independiente de UI y backend

**Ejemplo de API REST:**

```
GET    /api/productos           - Listar todos los productos
GET    /api/productos/123       - Obtener producto específico
POST   /api/productos           - Crear nuevo producto
PUT    /api/productos/123       - Actualizar producto completo
PATCH  /api/productos/123       - Actualizar campos específicos
DELETE /api/productos/123       - Eliminar producto
```

#### Ventajas de REST

- Simplicidad y facilidad de uso
- Escalabilidad por naturaleza stateless
- Flexibilidad en formatos (JSON, XML, etc.)
- Amplio soporte en herramientas y frameworks
- Cacheable por defecto
- Desacoplamiento cliente-servidor

#### Limitaciones de REST

- Overhead de HTTP en cada petición
- No apto para comunicación en tiempo real
- Puede requerir múltiples round-trips para operaciones complejas
- Difícil implementar suscripciones o notificaciones push

---

### 2.3 WebSocket vs REST API

#### WebSocket

**Características:**
- Protocolo de comunicación bidireccional full-duplex
- Conexión persistente sobre TCP
- Baja latencia y overhead reducido después del handshake inicial
- Permite push desde servidor sin polling

**Proceso de establecimiento:**
1. Cliente inicia handshake HTTP con header `Upgrade: websocket`
2. Servidor responde aceptando upgrade
3. Conexión HTTP se transforma en conexión WebSocket
4. Intercambio bidireccional de mensajes hasta que alguna parte cierre

**Casos de uso ideales:**
- Aplicaciones de chat en tiempo real
- Juegos multijugador online
- Dashboards con datos en vivo
- Notificaciones push instantáneas
- Colaboración en tiempo real (editores compartidos)
- Trading financiero con cotizaciones en vivo

#### Comparación REST vs WebSocket

| Aspecto | REST API | WebSocket |
|---------|----------|-----------|
| Modelo | Request-Response | Bidireccional persistente |
| Conexión | Nueva por petición | Única y persistente |
| Overhead | Alto (headers HTTP cada vez) | Bajo (después del handshake) |
| Latencia | Mayor | Menor |
| Push del servidor | Difícil (polling/long-polling) | Nativo |
| Escalabilidad | Mejor (stateless) | Más compleja (mantiene conexiones) |
| Cacheo | Soportado nativamente | No aplicable |
| Complejidad | Menor | Mayor |
| Uso de recursos | Eficiente para peticiones esporádicas | Eficiente para comunicación frecuente |

#### Estrategia Híbrida

Muchas aplicaciones modernas combinan ambos:
- **REST** para operaciones CRUD estándar y consultas ocasionales
- **WebSocket** para notificaciones en tiempo real y actualizaciones push

**Ejemplo arquitectura híbrida:**
- API REST para autenticación, registro, consultas de catálogo
- WebSocket para chat, notificaciones, actualización de estados en tiempo real

---

## 3. Contexto Histórico y Evolución

### Evolución de Paradigmas

**Década 1960-1970: Mainframes centralizados**
- Computación totalmente centralizada
- Terminales tontas conectadas a mainframes
- Procesamiento batch y tiempo compartido

**Década 1980-1990: Cliente-Servidor**
- Distribución de lógica entre cliente y servidor
- PCs como clientes inteligentes
- Bases de datos relacionales centralizadas

**Década 2000: Web Services y SOA**
- Servicios web basados en SOAP/XML
- Arquitecturas orientadas a servicios (SOA)
- Primeros pasos hacia distribución

**Década 2010: Cloud y Microservicios**
- Computación en la nube masiva
- Contenedores y orquestación (Docker, Kubernetes)
- Microservicios como estándar arquitectónico

**Década 2020: Edge Computing y Descentralización**
- Procesamiento en el borde de la red
- Blockchain y Web3
- Sistemas híbridos cloud-edge

---

## Conclusión

Los sistemas distribuidos han evolucionado desde arquitecturas centralizadas monolíticas hacia ecosistemas complejos de servicios interconectados. La elección entre centralización, distribución o descentralización depende de requisitos específicos de escalabilidad, tolerancia a fallos, consistencia de datos y complejidad operacional aceptable.

Las tecnologías de comunicación como sockets, HTTP/REST y WebSocket proporcionan las herramientas fundamentales para implementar estas arquitecturas, cada una con sus casos de uso óptimos. La tendencia actual combina múltiples paradigmas en arquitecturas híbridas que aprovechan las fortalezas de cada enfoque.
