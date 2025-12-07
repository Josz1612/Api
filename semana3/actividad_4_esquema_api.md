Esquema de API REST para EcoMarket
Recurso principal: products


Método	Endpoint	Descripción
GET	/products	Lista todos los productos
GET	/products/{id}	Obtiene un producto específico
POST	/products	Crea un nuevo producto
PUT	/products/{id}	Actualiza un producto
DELETE	/products/{id}	Elimina un producto



Justificación
Se usa 'products' en plural siguiendo convención REST.
PUT reemplaza todo el recurso, no crea si no existe (devuelve 404).
DELETE devuelve 404 si el producto no existe.
URLs son sustantivos, no verbos.
Se consideran casos extremos (IDs inexistentes, datos inválidos).