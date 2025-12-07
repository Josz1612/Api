# Semana 8: Seguridad en Sistemas Distribuidos - Autenticación con JWT

Este directorio contiene la implementación práctica de un sistema de autenticación seguro utilizando **JSON Web Tokens (JWT)**. 

> **Nota de Integración**: Este servicio (`auth-service`) está completamente integrado en el sistema principal EcoMarket. Se ejecuta automáticamente junto con la Central y la Sucursal al usar el `docker-compose.yml` de la raíz del proyecto.

## 📋 Contenido

1.  **Teoría JWT**: Estructura y funcionamiento.
2.  **Implementación**: Servicio de autenticación con FastAPI.
3.  **Características**:
    *   Login y generación de Access Token + Refresh Token.
    *   Middleware de validación de tokens.
    *   Endpoint de renovación de tokens (Refresh).
    *   Rate Limiting para prevenir fuerza bruta.
    *   Control de acceso basado en roles (RBAC).

## 📊 Arquitectura de Autenticación

El siguiente diagrama ilustra el flujo de autenticación y autorización implementado:

```mermaid
sequenceDiagram
    participant Cliente
    participant Auth Service
    participant API Protegida
    
    Note over Cliente, Auth Service: 1. Autenticación Inicial
    Cliente->>Auth Service: POST /login (credenciales)
    Auth Service-->>Cliente: 200 OK (Access Token + Refresh Token)
    
    Note over Cliente, API Protegida: 2. Acceso a Recursos
    Cliente->>API Protegida: GET /recurso (Header: Bearer AccessToken)
    API Protegida->>API Protegida: Validar Firma y Expiración
    alt Token Válido
        API Protegida-->>Cliente: 200 OK (Datos)
    else Token Expirado
        API Protegida-->>Cliente: 401 Unauthorized
    end
    
    Note over Cliente, Auth Service: 3. Renovación de Token
    Cliente->>Auth Service: POST /refresh (Refresh Token)
    Auth Service->>Auth Service: Validar Refresh Token (BD/Memoria)
    Auth Service-->>Cliente: 200 OK (Nuevo Access Token)
```

## 📂 Entregables y Recursos Adicionales

Para facilitar la evaluación y pruebas, se incluyen los siguientes recursos en este directorio:

*   🎥 **[Video de Demostración](https://drive.google.com/file/d/1GWh-TBwyWtTmGsnRd-NaJ3UtADYZq9WS/view?usp=sharing)**: Demostración del flujo completo (Login, Acceso Denegado, Acceso Autorizado).
*   📄 **[Informe Técnico](./INFORME_TECNICO.md)**: Justificación detallada, explicación de claims y buenas prácticas de seguridad.
*   🔗 **[Guía de Integración](./INTEGRATION.md)**: Documentación sobre la integración del servicio de autenticación.
*   🚀 **[Colección Postman](./ecomarket_auth.postman_collection.json)**: Archivo JSON listo para importar en Postman con todas las peticiones configuradas y scripts de prueba.
*   ✅ **Tests Automatizados**: Ejecuta `pytest tests/test_auth.py` para validar el funcionamiento (Login, Protección de Rutas, Refresh).

## 🛠️ Tecnologías Utilizadas

*   **Python 3.9+**
*   **FastAPI**: Framework web moderno y rápido.
*   **PyJWT**: Librería para codificar y decodificar JWTs.
*   **SlowAPI**: Implementación de Rate Limiting.

## 🚀 Instalación y Ejecución

### 1. Prerrequisitos

Asegúrate de tener Python instalado. Se recomienda usar un entorno virtual.

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate
```

### 2. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3. Ejecutar el Servidor

```bash
python app.py
```

El servidor iniciará en `http://localhost:8000`. Puedes ver la documentación interactiva en `http://localhost:8000/docs`.

## 🧪 Pruebas de la API

### 1. Login (Obtener Tokens)

Autentícate para obtener tu par de tokens.

**Usuario Admin:** `admin@ecomarket.com` / `password123`
**Usuario Cliente:** `cliente@ecomarket.com` / `password123`

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d "{\"email\": \"admin@ecomarket.com\", \"password\": \"password123\"}"
```

**Respuesta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### 2. Acceder a Recurso Protegido

Usa el `access_token` obtenido para consultar un endpoint protegido.

```bash
curl -X GET "http://localhost:8000/productos" \
     -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

### 3. Probar Permisos (RBAC)

Intenta crear un producto. Si usas el token del usuario "cliente", recibirás un error 403.

```bash
curl -X POST "http://localhost:8000/productos" \
     -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI" \
     -H "Content-Type: application/json" \
     -d "{\"nombre\": \"Nuevo Producto\", \"precio\": 99}"
```

### 4. Renovar Token (Refresh)

Cuando el `access_token` expire, usa el `refresh_token` para obtener uno nuevo sin volver a hacer login.

```bash
curl -X POST "http://localhost:8000/refresh" \
     -H "Content-Type: application/json" \
     -d "{\"refresh_token\": \"TU_REFRESH_TOKEN_AQUI\"}"
```

## 🔒 Conceptos Clave de Seguridad Implementados

1.  **Statelessness**: El servidor no guarda la sesión del usuario en memoria, solo valida la firma del token.
2.  **Firmas Digitales**: Usamos el algoritmo `HS256` (HMAC con SHA-256) para garantizar que el token no ha sido modificado.
3.  **Tiempo de Expiración (TTL)**:
    *   `Access Token`: Vida corta (30 min) para minimizar el riesgo si es robado.
    *   `Refresh Token`: Vida larga (7 días), pero se puede revocar en el servidor.
4.  **Rate Limiting**: El endpoint de `/login` está limitado a 5 intentos por minuto para mitigar ataques de fuerza bruta.
5.  **Audience & Issuer**: Validamos los claims `aud` e `iss` para asegurar que el token fue emitido por nosotros y es para nosotros.

## ⚠️ Notas para Producción

*   **HTTPS**: Siempre usa HTTPS. Los JWT viajan en los headers y si no se cifran, cualquiera puede robarlos.
*   **Secret Key**: Nunca hardcodees la `SECRET_KEY` en el código. Usa variables de entorno.
*   **Algoritmos**: Para mayor seguridad entre microservicios, considera usar algoritmos asimétricos como `RS256` (Clave Pública/Privada).