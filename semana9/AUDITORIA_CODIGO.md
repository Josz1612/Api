# 🕵️ Informe de Auditoría de Código - EcoMarket

**Fecha:** 26 de Noviembre de 2025
**Auditor:** GitHub Copilot
**Alcance:** Análisis estático de código fuente y configuración en busca de secretos expuestos.

---

## 1. Hallazgos de Secretos (Hardcoded Secrets)

Se han detectado múltiples instancias de credenciales y secretos hardcodeados o con valores por defecto inseguros en el código fuente y archivos de configuración.

### 🔴 Crítico: Clave de Firma JWT Expuesta
*   **Ubicación:** `Semana8/app.py`, `Semana5/central_api.py`, `docker-compose.yml`
*   **Código Detectado:**
    ```python
    SECRET_KEY = os.getenv("JWT_SECRET", "secreto_super_seguro_para_desarrollo")
    ```
    ```yaml
    environment:
      - JWT_SECRET=secreto_super_seguro_para_desarrollo
    ```
*   **Simulación de Brecha:**
    *   **Acceso del Atacante:** Con esta clave, un atacante puede generar sus propios tokens JWT con rol de `admin` sin necesidad de contraseña.
    *   **Impacto:** Toma total del control de la API Central y Servicio de Autenticación.
    *   **Usuarios Afectados:** 100% de los usuarios.
    *   **Costo Estimado:** Pérdida total de integridad del sistema.

### 🔴 Crítico: Credenciales de Base de Datos
*   **Ubicación:** `docker-compose.yml`, `Semana7/load_test.py`, `Semana7/tools/pg_shard_router.py`
*   **Código Detectado:**
    ```yaml
    POSTGRES_PASSWORD: password
    PGPASSWORD: replicator_pass
    ```
    ```python
    'password': 'postgres'
    ```
*   **Simulación de Brecha:**
    *   **Acceso del Atacante:** Acceso total (Lectura/Escritura/Borrado) a la base de datos PostgreSQL.
    *   **Impacto:** Robo de datos de clientes, eliminación de inventario (`DROP TABLE`).

### 🟡 Alto: Credenciales de RabbitMQ
*   **Ubicación:** `Semana3/central_api.py`, `Semana4/consumer.py`, `events.py`
*   **Código Detectado:**
    ```python
    pika.PlainCredentials('ecomarket_user', 'ecomarket_password')
    ```
*   **Simulación de Brecha:**
    *   **Acceso del Atacante:** Capacidad para inyectar eventos falsos (ej. ventas falsas) o consumir mensajes privados.

---

## 2. Investigación de Contexto (OSINT)

Como parte de la auditoría, se simula una investigación en GitHub sobre la exposición de secretos similares.

*   **Búsqueda:** `grep -r "JWT_SECRET" .` (Local) vs GitHub Search.
*   **Observación:** Una búsqueda rápida en GitHub de `"JWT_SECRET = 'secret'"` o `"secreto_super_seguro_para_desarrollo"` arroja miles de resultados de repositorios públicos.
*   **Lección:** Los atacantes utilizan bots automatizados (scrapers) que escanean GitHub en tiempo real. Un secreto subido a un repositorio público se considera comprometido en cuestión de segundos.

---

## 3. Recomendaciones Inmediatas

1.  **Eliminar Valores por Defecto:** El código no debe tener strings de fallback inseguros. Debe fallar si la variable de entorno no existe.
    *   *Mal:* `os.getenv("KEY", "default")`
    *   *Bien:* `os.environ["KEY"]` (Lanza error si falta)
2.  **Uso de .env:** Mover todas las variables de entorno a un archivo `.env` que esté en `.gitignore`.
3.  **Docker Secrets:** Para entornos productivos (Swarm/K8s), usar mecanismos de inyección de secretos en lugar de variables de entorno.

---

**Estado de la Auditoría:** 🛑 FALLIDA (Se requieren correcciones urgentes antes de desplegar).