Pruebas Manuales de la API (simuladas)
1. GET /products
Comando: curl http://localhost:8000/products
Resultado esperado: 200 OK, lista de productos
2. GET /products/1
Comando: curl http://localhost:8000/products/1
Resultado esperado: 200 OK, producto con id=1
3. GET /products/999
Comando: curl http://localhost:8000/products/999
Resultado esperado: 404 Not Found, {"error": "Producto no encontrado"}
4. POST /products
Comando: curl -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"id": 10, "name": "Queso", "price": 30, "stock": 5}'
Resultado esperado: 201 Created, producto creado
5. PUT /products/1
Comando: curl -X PUT http://localhost:8000/products/1 -H "Content-Type: application/json" -d '{"id": 1, "name": "Manzana Roja", "price": 12, "stock": 90}'
Resultado esperado: 200 OK, producto actualizado
6. DELETE /products/2
Comando: curl -X DELETE http://localhost:8000/products/2
Resultado esperado: 204 No Content
7. DELETE /products/999
Comando: curl -X DELETE http://localhost:8000/products/999
Resultado esperado: 404 Not Found, {"error": "Producto no encontrado"}