🔒 Guía de Implementación HTTPS (Fase 2)
Este documento detalla cómo se ha implementado HTTPS en el proyecto EcoMarket, tanto a nivel de Gateway (Nginx) como a nivel de aplicación (Python/FastAPI).

1. Generación de Certificados
Se ha utilizado un script de Python (scripts/generate_certs.py) para generar certificados autofirmados válidos para desarrollo local.

Comando:

python scripts/generate_certs.py
Resultado:

certs/server.key: Llave privada (¡NO COMPARTIR!)
certs/server.crt: Certificado público
2. Estrategia de Seguridad
A. Nivel Gateway (Recomendado para Docker/Producción)
El servicio nginx actúa como Reverse Proxy y SSL Terminator.

Escucha en puerto 443 (HTTPS).
Redirige tráfico HTTP (80) a HTTPS.
Maneja los certificados SSL.
Se comunica con los servicios internos (Central API, Auth) vía HTTP dentro de la red privada de Docker.
Acceso: https://localhost

B. Nivel Aplicación (Desarrollo Local Directo)
Para probar HTTPS directamente en los servicios de Python (sin Docker/Nginx), se ha configurado uvicorn para usar SSL si se activa la variable de entorno USE_HTTPS_DEV=true.

Ejecución Central API con HTTPS:

$env:USE_HTTPS_DEV="true"
python Semana5/central_api.py
# Acceso: https://localhost:8443
Ejecución Auth Service con HTTPS:

$env:USE_HTTPS_DEV="true"
python Semana8/app.py
# Acceso: https://localhost:8444
3. Cambios en Código
central_api.py y app.py
Se agregó lógica de inicio condicional:

if os.path.exists(ssl_key) and os.getenv("USE_HTTPS_DEV") == "true":
    uvicorn.run(..., ssl_keyfile=ssl_key, ssl_certfile=ssl_cert)
docker-compose.yml
Se montó el volumen ./certs:/app/certs:ro en los servicios para que tengan acceso a los certificados si fuera necesario activarlos internamente en el futuro.

4. Verificación
Nginx (Docker): https://localhost/ -> Debe mostrar el dashboard o API.
Directo (Python): Ejecutar script localmente y acceder a https://localhost:8443/.
Nota: Al usar certificados autofirmados, el navegador mostrará una advertencia de seguridad. Esto es normal en desarrollo. Debes aceptar el riesgo para continuar.