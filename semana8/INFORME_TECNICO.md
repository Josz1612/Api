# Informe Técnico: Seguridad en Sistemas Distribuidos con JWT

## 1. Introducción y Justificación

En la arquitectura de microservicios de EcoMarket, la gestión de sesiones tradicional (basada en cookies y almacenamiento en servidor) presenta desafíos de escalabilidad. Si un usuario se autentica en una instancia del servicio, las otras instancias no conocen esa sesión a menos que se comparta una base de datos de sesiones (como Redis), lo que añade latencia y complejidad.

**JSON Web Tokens (JWT)** resuelve este problema permitiendo una autenticación **Stateless** (sin estado). El servidor no necesita recordar al usuario; toda la información necesaria para identificarlo y autorizarlo viaja cifrada y firmada dentro del propio token.

### Ventajas Clave para EcoMarket:
1.  **Escalabilidad Horizontal**: Cualquier instancia del servicio puede validar el token sin consultar una base de datos central.
2.  **Desacoplamiento**: El servicio de autenticación (`auth-service`) es independiente de los servicios de negocio (`central-api`, `sucursal-api`).
3.  **Seguridad**: Los tokens están firmados digitalmente, garantizando su integridad.

## 2. Arquitectura de Seguridad

### Flujo de Autenticación
1.  El cliente envía credenciales (`email`, `password`) al endpoint `/login`.
2.  El servidor valida las credenciales contra la base de datos.
3.  Si son correctas, genera dos tokens:
    *   **Access Token**: Vida corta (30 min). Se usa para acceder a recursos.
    *   **Refresh Token**: Vida larga (7 días). Se usa únicamente para obtener nuevos Access Tokens.
4.  El cliente almacena los tokens (ej. en `localStorage` o cookies `HttpOnly`).
5.  Para cada petición a un recurso protegido, el cliente envía el Access Token en el header `Authorization: Bearer <token>`.

### Claims Utilizados
El payload del JWT contiene "claims" (afirmaciones) sobre el usuario:

*   `sub` (Subject): ID único del usuario (`user123`).
*   `role`: Rol del usuario (`admin` o `cliente`) para Control de Acceso Basado en Roles (RBAC).
*   `iss` (Issuer): Emisor del token (`ecomarket-auth-service`).
*   `aud` (Audience): Destinatario válido (`ecomarket-api`).
*   `exp` (Expiration): Fecha de caducidad (Unix timestamp).
*   `iat` (Issued At): Fecha de emisión.
*   `jti` (JWT ID): Identificador único del token (para evitar replay attacks o listas negras).

## 3. Buenas Prácticas Implementadas

1.  **Separación de Tokens**: Uso de Access y Refresh tokens para balancear seguridad y experiencia de usuario. Si el Access Token es robado, el daño es limitado por su corta duración.
2.  **Firmas Fuertes**: Uso del algoritmo `HS256` (HMAC SHA-256) con una clave secreta robusta.
3.  **Validación Estricta**: El middleware verifica no solo la firma, sino también el emisor (`iss`) y la audiencia (`aud`).
4.  **Rate Limiting**: Protección contra ataques de fuerza bruta en el endpoint de login (límite de 5 intentos/minuto) usando `SlowAPI`.
5.  **Revocación**: Implementación de una lista de revocación para Refresh Tokens, permitiendo cerrar sesiones activas forzosamente.

## 4. Conclusión

La implementación de JWT en EcoMarket proporciona una base sólida y escalable para la seguridad del sistema. Permite que los servicios crezcan independientemente mientras mantienen un control de acceso centralizado y seguro. La adición de Rate Limiting y manejo de Refresh Tokens eleva el nivel de seguridad a estándares de producción.