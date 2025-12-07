# Informe de Distribución de Datos - Semana 7

## 1. Justificación de Replicación

La implementación de replicación primario-secundario en PostgreSQL responde a la necesidad de escalar las operaciones de lectura (reads) que superan significativamente a las de escritura (writes) en EcoMarket (ratio 80/20).

**Ventajas:**
- **Escalabilidad de Lectura:** Los secundarios manejan las consultas de lectura, liberando al primario para procesar escrituras.
- **Alta Disponibilidad (HA):** Si el primario falla, un secundario puede ser promovido (failover), minimizando el tiempo de inactividad.
- **Backup en Caliente:** Los secundarios mantienen una copia casi en tiempo real de los datos.

**Retos:**
- **Lag de Replicación:** Existe un retraso (lag) entre que se escribe un dato en el primario y aparece en los secundarios. Esto implica consistencia eventual.
- **Complejidad:** Requiere monitoreo constante del lag y gestión de failover.

## 2. Simulación Lograda

Se configuró un clúster con 1 nodo primario y 2 secundarios usando Docker Compose.

**Evidencia:**
- **Writes:** Ejecutados exitosamente en el primario (puerto 5432).
- **Reads:** Distribuidos entre los secundarios (puertos 5433, 5434).
- **Lag:** Medido en < 1 segundo en pruebas locales, lo cual es excelente para la mayoría de los casos de uso de EcoMarket.

## 3. Análisis CAP

En el contexto del Teorema CAP (Consistencia, Disponibilidad, Tolerancia a Particiones), hemos tomado las siguientes decisiones para EcoMarket:

| Subdominio | Decisión CAP | Justificación |
| :--- | :--- | :--- |
| **Inventario** | **CP (Consistencia/Partición)** | No podemos vender productos que no existen. Preferimos rechazar una venta (baja disponibilidad) a vender sin stock (inconsistencia). |
| **Carrito de Compras** | **AP (Disponibilidad/Partición)** | La experiencia de usuario es prioridad. Permitimos agregar productos siempre, reconciliando conflictos (ej. stock agotado) en el checkout. |
| **Historial de Órdenes** | **AP (Disponibilidad/Partición)** | Es aceptable que un usuario no vea su orden inmediatamente en el historial (consistencia eventual) a cambio de que la página cargue rápido siempre. |

## 4. Sharding

Se implementó un `ShardRouter` en Python que demuestra dos estrategias:
1.  **Hash Simple:** Distribución uniforme pero alto costo de rebalanceo al agregar nodos.
2.  **Consistent Hashing:** Minimiza el movimiento de datos al escalar horizontalmente, ideal para crecimiento dinámico.

Las pruebas de carga (`load_test.py`) validaron que el sharding distribuye efectivamente las escrituras, aumentando el throughput total del sistema.