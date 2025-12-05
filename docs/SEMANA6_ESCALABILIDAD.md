# 📘 Semana 6: Escalabilidad y Distribución

## 🎯 Objetivos de la Semana

- ✅ Implementar load balancer con Nginx
- ✅ Configurar múltiples instancias de la API
- ✅ Replicación de datos con PostgreSQL
- ✅ Sharding para distribución de datos

## 📂 Archivos Principales

- `nginx.conf` - Configuración del load balancer
- `docker-compose.yml` - Orquestación de servicios
- `shard_router.py` - Router de sharding
- `test_load_balancer.py` - Pruebas de balanceo

## 🏗️ Arquitectura de Escalabilidad

```
                    ┌──────────────┐
        ┌──────────│  Nginx LB    │◀────────┐
        │          └──────────────┘          │
        │                                     │
        ▼                                     ▼
┌──────────────┐                    ┌──────────────┐
│   API #1     │                    │   API #2     │
│  Port 8001   │                    │  Port 8002   │
└──────────────┘                    └──────────────┘
        │                                     │
        └─────────────┬───────────────────────┘
                      ▼
              ┌──────────────┐
              │  PostgreSQL  │
              │  (Replica)   │
              └──────────────┘
```

## ⚖️ Load Balancer con Nginx

### Configuración

```nginx
upstream api_backend {
    # Algoritmo Round Robin por defecto
    server localhost:8001 weight=1;
    server localhost:8002 weight=1;
    server localhost:8003 weight=1;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://api_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Algoritmos de Balanceo

1. **Round Robin** (por defecto)
   - Distribuye equitativamente
   - Simple y efectivo

2. **Least Connections**
   ```nginx
   upstream api_backend {
       least_conn;
       server localhost:8001;
       server localhost:8002;
   }
   ```

3. **IP Hash** (sticky sessions)
   ```nginx
   upstream api_backend {
       ip_hash;
       server localhost:8001;
       server localhost:8002;
   }
   ```

4. **Weighted**
   ```nginx
   upstream api_backend {
       server localhost:8001 weight=3;
       server localhost:8002 weight=1;
   }
   ```

## 🗄️ Replicación de Base de Datos

### Master-Slave Replication

```yaml
# docker-compose.yml
services:
  postgres-master:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    command: |
      postgres
      -c wal_level=replica
      -c max_wal_senders=3
  
  postgres-replica:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    command: |
      postgres
      -c hot_standby=on
```

### Ventajas
- ✅ **Alta disponibilidad**: Si master cae, replica asume
- ✅ **Lectura escalable**: Reads van a replicas
- ✅ **Backup en tiempo real**: Datos siempre sincronizados

## 🔀 Sharding (Particionamiento)

### Estrategia de Sharding

```python
class ShardRouter:
    def get_shard(self, key: str) -> str:
        """
        Distribuye datos entre shards
        usando hash del key
        """
        shard_id = hash(key) % self.num_shards
        return f"shard_{shard_id}"
    
    def route_query(self, user_id: int):
        shard = self.get_shard(str(user_id))
        return self.connections[shard]
```

### Tipos de Sharding

1. **Range-Based**
   ```
   Shard 1: user_id 1-1000
   Shard 2: user_id 1001-2000
   Shard 3: user_id 2001-3000
   ```

2. **Hash-Based**
   ```python
   shard = hash(user_id) % num_shards
   ```

3. **Geo-Based**
   ```
   Shard US: usuarios de USA
   Shard EU: usuarios de Europa
   Shard LATAM: usuarios de Latinoamérica
   ```

## 🚀 Cómo Desplegar

### 1. Levantar Nginx Load Balancer
```bash
# Con Docker
docker run -d -p 80:80 -v ./nginx.conf:/etc/nginx/nginx.conf nginx

# O instalado localmente
nginx -c /path/to/nginx.conf
```

### 2. Iniciar Múltiples Instancias API
```bash
# Terminal 1
uvicorn main:app --port 8001

# Terminal 2
uvicorn main:app --port 8002

# Terminal 3
uvicorn main:app --port 8003
```

### 3. Con Docker Compose (Recomendado)
```bash
docker-compose up -d --scale api=3
```

## 📊 Monitoreo y Métricas

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "instance_id": os.getenv("INSTANCE_ID"),
        "timestamp": datetime.now()
    }
```

### Métricas de Load Balancer

```bash
# Ver estado de Nginx
curl http://localhost/nginx_status

# Logs de distribución
tail -f /var/log/nginx/access.log
```

## ✨ Características Implementadas

- ✅ Load balancer con Nginx
- ✅ 3+ instancias de API simultáneas
- ✅ Round-robin automático
- ✅ Health checks
- ✅ Sticky sessions (opcional)
- ✅ Replicación PostgreSQL
- ✅ Sharding básico

## 🔧 Pruebas de Carga

```python
# test_load_balancer.py
import concurrent.futures
import requests

def test_distribucion():
    """Verifica que requests se distribuyan"""
    responses = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [
            executor.submit(requests.get, "http://localhost/api/productos")
            for _ in range(1000)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            responses.append(future.result())
    
    # Verificar distribución uniforme
    instances = [r.headers.get("X-Instance-ID") for r in responses]
    assert len(set(instances)) >= 3  # Al menos 3 instancias
```

## 📈 Capacidad y Límites

### Sin Load Balancer
- 🔴 **Límite**: ~500 RPS
- 🔴 **Latencia**: 100-300ms
- 🔴 **Punto único de fallo**

### Con Load Balancer (3 instancias)
- 🟢 **Capacidad**: ~1500 RPS
- 🟢 **Latencia**: 50-150ms
- 🟢 **Alta disponibilidad**

### Con Sharding
- 🟢 **Capacidad**: Lineal con # shards
- 🟢 **Datos**: Gigabytes → Terabytes
- 🟢 **Escalabilidad horizontal**

## 🎓 Conceptos Clave

- **Load Balancer**: Distribuye tráfico entre servidores
- **Horizontal Scaling**: Agregar más servidores
- **Vertical Scaling**: Aumentar recursos del servidor
- **Replication**: Copias de datos para lectura
- **Sharding**: Particionamiento de datos
- **Sticky Sessions**: Mismo usuario → mismo servidor

## 🐛 Troubleshooting

### Load Balancer no distribuye
```bash
# Verificar configuración
nginx -t

# Reiniciar Nginx
nginx -s reload
```

### Instancias no responden
```bash
# Verificar que estén corriendo
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

### Replicación no funciona
```sql
-- En master
SELECT * FROM pg_stat_replication;

-- En replica
SELECT pg_is_in_recovery();  -- Debe retornar true
```

## 📝 Mejores Prácticas

1. **Usa health checks** para detectar instancias caídas
2. **Implementa circuit breaker** en el load balancer
3. **Monitorea métricas** de cada instancia
4. **Usa conexiones persistentes** (keep-alive)
5. **Implementa caching** para reducir carga
6. **Logs centralizados** (ELK stack)
7. **Auto-scaling** basado en carga
