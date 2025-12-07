Reflexión Profunda de Seguridad (Fase 0)
Fecha: 26 de Noviembre de 2025 Tema: Impacto de Secretos Comprometidos y Naturaleza de JWT

1. Si un atacante obtiene tu JWT_SECRET de GitHub, ¿puede generar tokens para usuarios que nunca han hecho login? ¿Por qué?
Respuesta: SÍ, ABSOLUTAMENTE.

¿Por qué? Los JWT (JSON Web Tokens) son stateless (sin estado). Esto significa que el servidor no consulta una base de datos de "sesiones activas" para validar un token; simplemente verifica la firma matemática del token.

La firma se genera así: HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), JWT_SECRET).
Si el atacante tiene el JWT_SECRET, puede construir un payload arbitrario (ej: {"sub": "usuario_inexistente", "role": "admin"}), firmarlo con el secreto y enviarlo a la API.
La API recibirá el token, verificará la firma con su copia del secreto, y al coincidir, confiará ciegamente en que el token es legítimo, otorgando acceso. No importa si el usuario existe o no, o si nunca se logueó.
2. ¿Por qué un JWT robado es más peligroso que una sesión tradicional robada?
Respuesta: Por la dificultad de revocación inmediata.

Sesión Tradicional: Es solo un ID (referencia). El servidor busca ese ID en una base de datos o caché (Redis) en cada petición. Si detectas un robo, borras el ID del servidor y el atacante pierde acceso instantáneamente.
JWT: Es un pase "autocontenido". Contiene los permisos y la fecha de expiración dentro de sí mismo. El servidor no guarda copia.
Si un atacante roba un JWT válido por 1 hora, tiene acceso garantizado por 1 hora.
El servidor no puede "borrar" el token porque no lo tiene guardado. Para invalidarlo, se requiere implementar listas negras (Blacklists) complejas o rotar el secreto (lo que desconectaría a todos los usuarios).
3. ¿Qué diferencia hay entre que te roben el token en tránsito vs. que te roben el secreto del servidor?
Respuesta: La diferencia entre robar una llave y robar la fábrica de llaves.

Escenario	Token Robado (Tránsito/MITM)	Secreto Robado (GitHub/Server)
Alcance	Compromete a UN usuario específico.	Compromete a TODOS los usuarios y al sistema entero.
Poder	Solo permite hacer lo que ese usuario puede hacer.	Permite crear usuarios "Dios" (Super Admin) invisibles.
Duración	Hasta que el token expire (ej. 30 min).	Indefinida (hasta que cambies el secreto y redespliegues).
Detección	Difícil, parece tráfico normal del usuario.	Imposible de detectar en los logs de acceso (los tokens parecen válidos).
4. Si implementas HTTPS pero tu JWT_SECRET está en GitHub, ¿sigues vulnerable? ¿A qué exactamente?
Respuesta: SÍ, sigues en Riesgo Crítico.

¿A qué exactamente? A la falsificación de identidad (Forged Tokens).

HTTPS protege el túnel de comunicación. Evita que alguien en la cafetería (MITM) lea los tokens que viajan del usuario al servidor.
JWT_SECRET protege la integridad de la credencial.
Si el secreto es público, el atacante no necesita interceptar nada. Simplemente:
Toma el secreto de GitHub.
Genera un token de Admin en su propia computadora.
Se conecta a tu API segura (HTTPS).
La API descifra el túnel TLS, lee el token, valida la firma (que es correcta porque se firmó con el secreto filtrado) y le abre la puerta.
Conclusión: HTTPS es inútil contra un atacante que tiene las llaves maestras de la criptografía de tu aplicación.




