Reporte de Práctica - Semana 2 (Sockets TCP/UDP)
Respuestas a Preguntas Guía
1. ¿En qué casos elegirías TCP y en cuáles UDP? Da al menos 2 ejemplos reales.
TCP (Transmission Control Protocol): Se elige cuando la integridad y el orden de los datos son críticos, y no podemos permitirnos perder paquetes.

Ejemplo 1: Transferencia de Archivos (FTP/HTTP): Si descargamos un archivo .zip, perder un solo bit corrompería todo el archivo. TCP garantiza que llegue completo.
Ejemplo 2: Correo Electrónico (SMTP/IMAP): No queremos que un email llegue incompleto o con párrafos desordenados.
UDP (User Datagram Protocol): Se elige cuando la velocidad es prioritaria sobre la fiabilidad, y la pérdida ocasional de datos es aceptable.

Ejemplo 1: Streaming de Video en Vivo / Videollamadas (Zoom/Skype): Si se pierde un frame de video, es mejor saltarlo y mostrar el siguiente en tiempo real que detener la transmisión para recuperarlo (lo que causaría lag).
Ejemplo 2: Juegos Online (FPS/MOBA): La posición del jugador se actualiza muchas veces por segundo. Si se pierde un paquete de posición antigua, no importa porque ya viene uno más nuevo.
2. ¿Qué observaste cuando cambiaste el tamaño del buffer?
Al reducir el buffer (por ejemplo, a 8 bytes), si enviamos un mensaje largo como "Hola Mundo Cruel" (16 bytes), el servidor no puede leerlo todo de una vez.

En TCP, el flujo de datos se fragmenta. El servidor leerá "Hola Mun", luego "do Cruel", etc., en ciclos sucesivos del recv.
En UDP, si el mensaje es más grande que el buffer de recepción, el exceso de datos del datagrama se pierde (truncamiento) y se lanza una excepción o advertencia, ya que UDP preserva los límites del mensaje (message boundaries).
3. ¿Qué error aparece al desconectar el servidor TCP? ¿Por qué sucede?
Al detener el servidor mientras el cliente intenta enviar o recibir, el cliente suele lanzar una excepción ConnectionResetError (en Python) o SocketException (en C#).

Razón: TCP es un protocolo orientado a conexión. Mantiene un estado activo ("handshake"). Si un extremo desaparece abruptamente (sin enviar un paquete FIN de cierre ordenado), el sistema operativo del cliente detecta que el socket remoto ya no responde o ha enviado un paquete RST (Reset), rompiendo la ilusión de flujo continuo.
4. ¿Por qué el cliente UDP puede "enviar" aun cuando el servidor no esté activo?
UDP es un protocolo "sin conexión" (connectionless). No hay un "handshake" inicial (SYN/ACK) para establecer un canal.

El cliente simplemente empaqueta los datos en un datagrama, le pone la dirección IP de destino y lo lanza a la red ("fire and forget").
No verifica si el destino existe, si está escuchando o si quiere recibir el mensaje. Por lo tanto, el sendto no falla inmediatamente, aunque el paquete se pierda en el vacío.