Observaciones de la API jsonplaceholder
Peticiones realizadas
1. GET /posts
Código HTTP: 200 OK
Respuesta: Lista de posts en formato JSON (array de objetos)
Patrón de URL: /recurso (plural)
2. GET /posts/1
Código HTTP: 200 OK
Respuesta: Un solo post (objeto JSON)
Patrón de URL: /recurso/{id}
3. POST /posts
Código HTTP: 201 Created
Respuesta: Objeto creado con ID asignado
Patrón de URL: /recurso (plural)
Observaciones generales
Las URLs usan sustantivos en plural.
Los códigos HTTP siguen el estándar REST.
El servidor responde en JSON.
Capturas de pantalla (simuladas)
GET /posts
GET /posts/1
POST /posts