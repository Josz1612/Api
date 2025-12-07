Reflexión de Diseño
Decisión más difícil: Elegir si PUT debe crear o solo actualizar. Decidimos que solo actualiza y devuelve 404 si no existe.
Códigos HTTP: Elegimos 200 para éxito, 201 para creación, 400 para errores de validación, 404 para no encontrado, 204 para borrado exitoso.
Como frontend developer, me gustaría que los errores incluyeran un campo "code" para facilitar el manejo en el cliente.