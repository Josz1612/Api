Propuestas de Mejora para la API
Performance:
Paginación en GET /products para evitar respuestas muy grandes.
Implementación: agregar parámetros ?limit= y ?offset= y devolver metadatos de paginación.
Experiencia:
Filtros y búsqueda por nombre o rango de precio.
Implementación: parámetros de query string (?name=, ?min_price=, ?max_price=).
Confiabilidad:
Timeouts y manejo de errores de red.
Implementación: configurar timeouts en el servidor y usar lógica de reintentos en el cliente.