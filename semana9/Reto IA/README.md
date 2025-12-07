Semana 9: Seguridad Avanzada y Despliegue Seguro 🛡️
En esta semana final del Hito 2, transformamos EcoMarket de un sistema funcional pero inseguro a una "Fortaleza Digital". Implementamos una arquitectura de producción robusta utilizando SSL Termination, Gestión de Secretos y Auditorías de Seguridad.

🎯 Objetivos Alcanzados
HTTPS & SSL Termination:
Implementación de Nginx como Gateway seguro (Puerto 443).
Configuración de certificados TLS 1.3.
Redirección forzada de HTTP a HTTPS y headers de seguridad (HSTS).
Gestión de Secretos (12-Factor App):
Eliminación de credenciales hardcodeadas en el código.
Implementación de variables de entorno (.env) y validación con pydantic-settings.
Arquitectura de Producción:
Aislamiento de microservicios en red privada Docker.
Comunicación interna optimizada (HTTP) vs externa segura (HTTPS).
Auditoría y Compliance:
Análisis de vulnerabilidades y remediación.
Documentación técnica de seguridad.
🎥 Video Demo
Aquí se encuentra la demostración del flujo E2E seguro, cubriendo despliegue, HTTPS y autenticación JWT.

🔗 Enlace al Video: [https://www.youtube.com/channel/UCwAV4zSh3bemRYIfnD1br7w]
❓ ¿Dónde está el código de la Semana 9?
A diferencia de las semanas anteriores, la Semana 9 no introduce un nuevo microservicio aislado, sino que se enfoca en la Integración, Configuración y Hardening de toda la plataforma existente.

Los cambios de código y configuración de esta semana se aplicaron transversalmente en:

Nginx Gateway (Semana6/nginx_integrated.conf):

Configuración de SSL Termination, certificados y headers de seguridad.

Docker Compose (docker-compose.yml):

Reconfiguración de puertos (Central API a 8000, Auth a 8002).

Inyección de variables de entorno (.env).

Central API (Semana5/central_api.py):

Adaptación para recibir tráfico HTTP desde el Gateway.

Integración de app_config.py para manejo seguro de secretos.

Auth Service (Semana8/app.py):

Ajustes de puertos y configuración segura.

Raíz del Proyecto:

Creación de .env.example y carpeta certs/.

Nota: La carpeta Semana9/ contiene exclusivamente la evidencia documental, auditorías e informes requeridos para la validación del Hito 2.
