Principios de Diseño para EcoMarket
Basado en: [Éxitos/Fracasos | Desafíos Técnicos | Arquitecturas Reales]
Principio Clave que Adoptaremos: Las sucursales operarán de forma autónoma (offline-first), gestionando el inventario local y notificando asíncronamente a la API Central tras cada venta.
Justificación: Las experiencias en retail muestran que depender de la red central puede detener operaciones; la autonomía local garantiza ventas continuas incluso ante fallas de conectividad.
Riesgo que Mitigaremos: Evitaremos las consultas de inventario síncronas entre sucursales y la central, ya que la latencia y posibles caídas afectarían la experiencia de compra y la disponibilidad.
Justificación: Una espera de varios segundos por una consulta de stock es inaceptable en el punto de venta; la gestión local y la notificación asíncrona aseguran velocidad y resiliencia.
Diagrama de Arquitectura
mermaid graph TD Sucursal1[API Sucursal 1] Central[API Central]

Sucursal1 -- Notificación de venta (asíncrona) --> Central
Sucursal1 -- Consulta de inventario local --> Sucursal1
Central -- Inventario global --> Central
La Sucursal 1 gestiona su inventario local y, tras una venta, notifica de forma asíncrona a la API Central para actualizar el inventario global.
La comunicación es de tipo "notificación" (push), no "pregunta" (pull).
Estrategia de Consistencia
Se utilizó un modelo de consistencia eventual. Esto significa que la sucursal actualiza su inventario local de inmediato para priorizar la velocidad y disponibilidad en la tienda. Luego, notifica de forma asíncrona a la API Central para que el inventario global se actualice eventualmente. El trade-off es que pueden existir discrepancias temporales entre el inventario local y el central, pero se garantiza que ambos se sincronizarán con el tiempo.