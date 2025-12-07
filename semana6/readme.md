# Semana 6: Escalabilidad Horizontal y Balanceo de Carga (Nginx)

Esta semana abordamos el problema de la saturaci�n de una instancia �nica mediante la implementaci�n de **Escalabilidad Horizontal**. Utilizamos **Nginx** como balanceador de carga (Reverse Proxy) para distribuir el tr�fico entre m�ltiples instancias del servicio de usuarios, mejorando el throughput y la disponibilidad.

##  Documentaci�n de Referencia
- **`semana6.html`**: Gu�a completa del "Journey" de escalabilidad, desde el c�lculo de costos de no escalar hasta la implementaci�n de Nginx con Health Checks.

##  Objetivos del Taller
1.  **Entender el Problema**: Analizar por qu� el escalamiento vertical tiene l�mites y c�mo una sola instancia se convierte en un punto �nico de fallo.
2.  **Implementar Nginx**: Configurar Nginx como un proxy reverso con un grupo de servidores `upstream`.
3.  **Algoritmos de Balanceo**: Probar `Round Robin` (por defecto) y `Least Connections` para distribuir la carga.
4.  **Resiliencia**: Configurar *Health Checks* pasivos (`max_fails`, `fail_timeout`) para que Nginx deje de enviar tr�fico a instancias ca�das.
5.  **Escalado Din�mico**: Agregar nuevas instancias al cl�ster sin detener el servicio.

##  Estructura del Proyecto

```text
Semana6/
 docker-compose.yml      # Orquestacin: Nginx + N instancias de users_service
 nginx/
    nginx.conf          # Configuracin del balanceador (upstream, proxy_pass)
 nginx_integrated.conf   # Configuración integrada de Nginx
 users_service.py        # Servicio de usuarios (stateless)
 app.py                  # Aplicación principal
 requirements.txt        # Dependencias (FastAPI, Uvicorn)
 semana6.html            # Gua detallada
```

##  Instrucciones de Ejecuci�n

### 1. Levantar el Cl�ster
Inicia el balanceador y 2 instancias del servicio de usuarios:
```powershell
docker-compose up -d --build
```

### 2. Validar Distribuci�n (Round Robin)
Env�a m�ltiples peticiones al balanceador (puerto 80) y observa c�mo se alternan entre las instancias.

**En PowerShell:**
```powershell
# Enviar 10 peticiones seguidas
1..10 | ForEach-Object { curl http://localhost/users }
```

**Verificar Logs:**
Observa que los logs provienen de diferentes contenedores (`user-service-1`, `user-service-2`):
```powershell
docker-compose logs -f users_service
```

### 3. Prueba de Resiliencia (Failover)
Simula la ca�da de una instancia y verifica que el sistema sigue respondiendo.

1.  Det�n una instancia:
    ```powershell
    docker stop ecomarket-users-1
    ```
2.  Env�a peticiones nuevamente. Nginx detectar� el fallo y redirigir� todo el tr�fico a la instancia restante.
3.  Reinicia la instancia:
    ```powershell
    docker start ecomarket-users-1
    ```
4.  El tr�fico deber�a volver a distribuirse autom�ticamente.

### 4. Escalado Din�mico (Reto)
Agrega una tercera instancia sin detener el sistema (requiere configuraci�n en `docker-compose.yml` o uso de `docker-compose up --scale` si est� configurado para ello):

```powershell
# Ejemplo si usas replicas en docker-compose
docker-compose up -d --scale users_service=3
```

##  Configuraci�n Clave (Nginx)

El coraz�n del balanceo reside en el bloque `upstream` en `nginx/nginx.conf`:

```nginx
upstream users_backend {
    # Algoritmo: Least Connections (opcional, por defecto Round Robin)
    least_conn;
    
    # Instancias con Health Checks pasivos
    server user-service-1:8000 max_fails=3 fail_timeout=30s;
    server user-service-2:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    location / {
        proxy_pass http://users_backend;
    }
}
```

##  Entregables
1.  **Repositorio**: C�digo con Docker Compose funcional.
2.  **Diagrama**: Flujo de tr�fico actualizado (Cliente -> Nginx -> Instancias).
3.  **Informe**: Justificaci�n de escalabilidad y evidencia de distribuci�n de carga (logs).
4. **Video corto demostrativo**: https://drive.google.com/file/d/167TJKuTeASvYWwY94D3Enoh1VYhTRtC_/view?usp=sharing