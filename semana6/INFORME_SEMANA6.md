Informe de Escalabilidad Horizontal - Semana 6
1. Justificación de Escalabilidad
La implementación de un balanceador de carga (Nginx) frente a múltiples instancias del servicio de usuarios responde a la necesidad de manejar picos de tráfico que una sola instancia no podría soportar.

Ventajas:

Mayor Throughput: Al distribuir la carga entre 2 instancias, duplicamos teóricamente la capacidad de procesamiento de solicitudes por segundo.
Alta Disponibilidad: Si una instancia falla, Nginx redirige el tráfico a la instancia restante, evitando tiempo de inactividad total.
Escalabilidad Transparente: Podemos agregar más instancias (user-service-3, etc.) sin modificar el cliente ni detener el servicio.
Retos:

Complejidad Operativa: Requiere gestionar múltiples contenedores y la configuración del balanceador.
Estado: Las sesiones de usuario deben ser gestionadas externamente (ej. Redis) o usar "sticky sessions", ya que las peticiones pueden llegar a cualquier instancia. En este caso, el servicio es stateless, lo que facilita el balanceo.
2. Distribución Lograda
Se configuró Nginx con el algoritmo least_conn (mínimas conexiones), que envía las nuevas solicitudes a la instancia con menos carga activa.

Evidencia de Distribución: Al realizar múltiples peticiones a http://localhost/users, las respuestas muestran alternancia en el campo served_by:

// Respuesta 1
{
  "users": [...],
  "served_by": "1"
}

// Respuesta 2
{
  "users": [...],
  "served_by": "2"
}
Esto confirma que el tráfico se está distribuyendo entre user-service-1 y user-service-2.

3. Mejoras Futuras
Auto-scaling: Implementar un orquestador como Kubernetes para aumentar/disminuir instancias automáticamente según el uso de CPU/Memoria.
Métricas: Integrar Prometheus y Grafana para visualizar el tráfico por instancia y latencia en tiempo real.
Health Checks Activos: Utilizar Nginx Plus o un sidecar para health checks más avanzados que verifiquen la salud de la aplicación (endpoint /health) y no solo la conexión TCP.