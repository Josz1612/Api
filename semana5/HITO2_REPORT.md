Hito 2 — Entrega breve (1-2 páginas)

Objetivo Implementar replicación primaria-secundaria en PostgreSQL y un router de sharding para simular particionado de datos (usuarios/productos). Proveer scripts ejecutables de configuración y pruebas de carga que demuestren: escrituras en primario, lecturas en secundarios, y medición de lag y throughput.

Justificación de replicación

Ventajas: lectura escalada (offload a réplicas), alta disponibilidad (failover manual o automático con herramientas externas), backups consistentes.
Retos: replicación asíncrona introduce lag; escrituras siguen en el primario → posibilidad de lecturas eventual-consistent; complejidad de failover/promoción.
Simulación lograda / Evidencia
Topología: docker/postgres/docker-compose.repl.yml levanta un primario y 2 secundarios en contenedores (puertos expuestos según compose).
El script load_test.py realiza:
N escrituras hacia el primario (medición de writes/sec)
Lecturas concurrentes hacia los secundarios (medición de reads/sec)
Medición de lag por timestamp UTC (compara último WAL aplicado con timestamp de commit)
Para generar evidencia persistente: extraer logs del primario y correr pgbadger (comando en README.md).
Análisis CAP y decisiones de diseño
Breve recordatorio: bajo particionamiento de red (P) hay que elegir entre Consistency (C) o Availability (A). En sistemas distribuidos solemos aplicar decisiones por dominio de datos según requisitos de negocio.

Decisiones por dominio (resumen práctico):

Inventory (stock de productos): CP

Justificación: la consistencia de inventario es crítica para evitar sobre-venta. Preferimos priorizar Consistency + Partition tolerance.
Implementación recomendada: single-writer por shard (o bloqueo coordinado), escrituras en primario con réplica asíncrona; considerar replicación síncrona para niveles críticos.
Trade-offs: menor availability durante particiones; mitigación con circuit-breakers y cola de pedidos en espera.
Cart (carritos de compra en curso): AP

Justificación: se prioriza disponibilidad (UX) — el usuario debe poder añadir items aunque haya particiones; la exactitud absoluta puede resolverse por reconciliación posterior.
Implementación recomendada: replicación asíncrona y diseño eventual-consistent; aplicar compensaciones y reconciliación (background job) para duplicados o conflictos.
Trade-offs: riesgo de inconsistencias temporales entre nodos; mitigación con timestamps, versiones (vector clock/simple last-write-wins) y reconciliación.
User profiles (perfiles de usuario): CP (moderado)

Justificación: la integridad de datos personales es importante, pero muchas lecturas pueden tolerar cierta latencia; optamos por consistencia para escrituras críticas (email, password) y eventual para lecturas caché.
Implementación recomendada: escrituras por primario (CP), y lectura desde réplicas si se tolera eventual consistency; usar mecanismos de cache invalidation tras writes.
Orders / Transacciones financieras: CP

Justificación: requiere consistencia estricta por razones de contabilidad y conciliación.
Implementación recomendada: transacciones ACID en primario; evitar lecturas no confirmadas en réplicas para decisiones críticas.
Cómo aplicar estas decisiones en la demo

La topología primaria-secundaria usada demuestra la separación de paths: writes → primario; reads → réplicas (read-scaling). Esto favorece CP para dominios críticos si las lecturas críticas se dirigen al primario o si usamos sincronización más estrita.
Para dominios AP (carrito), la demo muestra cómo lecturas desde réplicas permiten alta disponibilidad pero con posible lag; load_test.py mide ese lag para valorar el impacto.
Notas finales

Estas decisiones son trade-offs: en producción evaluar SLOs, requisitos legales y latencia antes de elegir CP vs AP para cada dominio. Herramientas como Patroni/repmgr y técnicas como quorum writes/consensus pueden cambiar las opciones disponibles.
Router de sharding
shard_router.py implementa un SimpleHashShardRouter (md5 % N) y un ConsistentHashRouter con nodos virtuales.
Validación: load_test.py tiene un modo de sharded-writes que registra distribución por shard; tras la ejecución verás número de filas escritas por shard (métricas impresas en consola).
Configuración PostgreSQL y monitoreo
Archivos relevantes en el compose: postgresql.conf y pg_hba.conf usados por los contenedores y los scripts init-*.sh para habilitar wal_level=replica y usuario de replicación.
Herramientas de monitoring: pg_stat_replication (mide estado de réplica), pgbadger (parseo de logs para queries lentas y conexiones).
Métricas clave:
Throughput (writes/sec, reads/sec)
Replication lag (segundos entre commit y aplicación en replica)
Number of connections, long-running queries
Script de pruebas
load_test.py debe ejecutarse sin errores. Produce métricas de throughput y lag en stdout. Para la entrega, incorpora la salida de una corrida corta en artifacts/ (si la deseas guardar, ejecuta python load_test.py > artifacts/mi_run.txt).
Reflexión crítica y trabajo futuro
Problemas futuros:
Cross-shard joins: costosos y complicados; requerirán re-planteo de modelo o solución OLAP.
Rebalanceo: añadir/quitar shards requiere resharding o una capa de migración de datos (relocalización/rehashing con mínimo downtime).
Failover automático: usar repmgr o Patroni para automatizar promoción de réplicas y evitar split-brain.
Checklist de la rúbrica (auto-evaluación)
Configuración PostgreSQL: 2 pts — postgresql.conf y pg_hba.conf preparados en los contenedores; wal_level=replica configurado.
Docker Compose ejecutable: 1 pt — docker-compose -f docker/postgres/docker-compose.repl.yml up debe levantar primario + 2 secundarios.
Router de sharding: 2 pts — shard_router.py incluido; hashing funcional y script de validación en load_test.py.
Script de pruebas: 1 pt — load_test.py ejecutable y produce métricas.
Diagrama CAP: 2 pts — decisiones resumidas en la sección 4.
Análisis de monitoring: 1 pt — herramientas y métricas clave mencionadas.
Reflexión crítica: 1 pt — problemas y mejoras futuras listadas.