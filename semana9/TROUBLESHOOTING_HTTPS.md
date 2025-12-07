# 🛠️ Solución de Problemas: Conexión HTTPS Local

Si al intentar acceder a `https://localhost:8443/` recibes un error de "Connection Refused", es probable que el servicio no esté corriendo o no pueda conectarse a la base de datos.

## Causa Común
El script `central_api.py` intenta conectarse por defecto al host `pg_primary`.
- **Dentro de Docker:** Esto funciona porque `pg_primary` es el nombre del contenedor.
- **Fuera de Docker (Local):** Tu computadora no sabe qué es `pg_primary`.

## Solución

Debes indicarle al script que la base de datos está en `localhost` (ya que Docker expone el puerto 5432).

### Comando Correcto para Ejecutar Localmente

```powershell
# 1. Asegúrate que Docker esté corriendo (para la base de datos)
docker-compose up -d pg_primary

# 2. Configura las variables de entorno y ejecuta
$env:USE_HTTPS_DEV="true"
$env:DB_HOST="localhost"
python Semana5/central_api.py
```

Ahora podrás acceder a:
👉 **`https://localhost:8443/`**

---

## Alternativa: Usar Nginx (Docker)
Si prefieres no ejecutar Python manualmente, usa la URL del Gateway Nginx que ya está configurado en Docker:

👉 **`https://localhost/`** (Puerto 443 estándar)