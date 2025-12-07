Bitácora de Decisiones Arquitectónicas (EcoMarket)
Recurso principal: products
Endpoints: GET, POST, PUT, DELETE sobre /products y /products/{id}
Validaciones: nombre no vacío, price >= 0, stock >= 0
Formato de errores: siempre JSON {"error": "mensaje"}
PUT y DELETE devuelven 404 si el producto no existe
Decisión difícil: PUT no crea, solo actualiza
Mejoras futuras: paginación, filtros, autenticación, persistencia