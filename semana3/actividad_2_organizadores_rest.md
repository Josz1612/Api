Organizadores gráficos: Fundamentos REST
REST
Significa: Representational State Transfer
Principio clave 1: Recursos identificados por URLs
Principio clave 2: Uso de métodos HTTP estándar (GET, POST, PUT, DELETE)
Principio clave 3: Stateless (sin estado entre peticiones)
Recursos vs Representaciones
Recurso = Entidad conceptual (ej: un usuario, un producto)
Representación = Forma concreta (ej: JSON, XML)
Ejemplo: /users/123
El recurso es: el usuario con id 123
La representación es: el JSON devuelto
Códigos HTTP esenciales
200: OK (éxito)
201: Created (recurso creado)
400: Bad Request (petición inválida)
404: Not Found (no encontrado)
500: Internal Server Error (error del servidor)