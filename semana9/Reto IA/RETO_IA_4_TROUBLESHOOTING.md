🤖 Reto IA #4: Troubleshooting de HTTPS
Este documento registra el diagnóstico y solución del problema más común enfrentado durante la implementación de HTTPS en el entorno de desarrollo local.

Caso de Estudio: "NET::ERR_CERT_AUTHORITY_INVALID"
1. Descripción del Problema
Síntoma:

Al intentar acceder a https://localhost:8443/dashboard, el navegador bloquea el acceso con una pantalla roja de advertencia.
Código de error: NET::ERR_CERT_AUTHORITY_INVALID (Chrome/Edge) o MOZILLA_PKIX_ERROR_SELF_SIGNED_CERT (Firefox).
Al intentar consumir la API con curl, falla la conexión:
curl: (60) SSL certificate problem: self signed certificate
Configuración:

OS: Windows
Lenguaje: Python 3.11 / FastAPI
Servidor: Uvicorn con parámetros SSL (ssl_keyfile, ssl_certfile).
Origen del Certificado: Generado localmente con OpenSSL (script generate_certs.py).
2. Diagnóstico de Causa Raíz
El problema no es un error técnico de la implementación, sino una medida de seguridad del cliente (navegador/curl).

Cadena de Confianza: Los navegadores confían en certificados firmados por Autoridades Certificadoras (CA) reconocidas mundialmente (ej. DigiCert, Let's Encrypt).
Certificado Autofirmado: Nuestro certificado server.crt dice: "Yo soy localhost y yo mismo garantizo que soy localhost".
Rechazo: Como el sistema operativo no tiene a "EcoMarket Local CA" en su lista de confianza, rechaza la conexión para prevenir posibles ataques de intermediarios (MITM).
3. Verificación Técnica
Para confirmar que el servidor está enviando el certificado correctamente (aunque no sea confiable), usamos curl en modo verbose:

Comando:

curl -v https://localhost:8443/
Salida de Logs Relevante:

*   Trying 127.0.0.1:8443...
* Connected to localhost (127.0.0.1) port 8443 (#0)
* ALPN: offers h2,http/1.1
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* Server certificate:
*  subject: C=MX; ST=Nayarit; L=Tepic; O=EcoMarket; CN=localhost  <-- NUESTRO CERTIFICADO
*  issuer: C=MX; ST=Nayarit; L=Tepic; O=EcoMarket; CN=localhost   <-- EMISOR DESCONOCIDO
* SSL certificate problem: self signed certificate
* Closing connection 0
4. Solución Paso a Paso
Solución A: Bypass (Para Desarrollo Local)
Instruir al cliente para que confíe explícitamente en este certificado específico.

En Navegador:
Hacer clic en "Configuración avanzada" o "Más información".
Seleccionar "Continuar a localhost (no seguro)".
En Curl:
Agregar la bandera -k o --insecure.
curl -k https://localhost:8443/
En Postman:
Ir a Settings -> General.
Desactivar "SSL certificate verification".
Solución B: Trust Store (Para Desarrollo Avanzado)
Instalar el certificado autofirmado en el almacén de confianza de Windows.

Doble clic en server.crt.
"Instalar certificado" -> "Equipo local".
Colocar en: "Entidades de certificación raíz de confianza".
Reiniciar navegador.
Solución C: Certificado Real (Para Producción)
Nunca usar certificados autofirmados en producción.

Adquirir un dominio (ej. api.ecomarket.com).
Usar Certbot para obtener un certificado gratuito de Let's Encrypt.
certbot certonly --standalone -d api.ecomarket.com
5. Prevención
Documentación: Incluir en el README.md una sección clara sobre cómo manejar las advertencias SSL en local.
Variables de Entorno: Usar flags como USE_HTTPS_DEV para poder desactivar HTTPS fácilmente si bloquea el desarrollo.