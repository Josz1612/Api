# Semana 2: Sockets TCP/UDP en Python Esta semana se enfoca en los fundamentos de la comunicación en red utilizando Sockets.


 Implementarás servidores y clientes de eco en Python para comprender las diferencias entre los protocolos TCP y UDP.
 
 
  ## Objetivos de Aprendizaje - 
  Comprender qué es un **socket**, cómo se conecta y la función de los **puertos**. - Diferenciar entre **TCP** (orientado a conexión, confiable) y **UDP** (sin conexión, rápido). - Implementar un sistema de **eco cliente/servidor** funcional. - Realizar pruebas de conectividad local y en red (LAN). --- 
  
  
  ## Conceptos Clave - **Socket:** Punto de comunicación entre procesos mediante red (IP:PUERTO). - **Cliente/Servidor:** El servidor *escucha* en un puerto; el cliente *conecta* a ese puerto. - 
  
  
  **TCP (Transmission Control Protocol):** Conexión confiable, ordenada, orientada a flujo. Asegura entrega. - **UDP (User Datagram Protocol):** Datagramas sin conexión. Menor latencia, pero no garantiza entrega ni orden. - **Buffer:** Tamaño de lectura/escritura (ej. 1024 bytes) que afecta cómo se procesan los mensajes. --- 
  
  
  ## Estructura de Archivos - guia_autogestionada_sockets_tcp_udp_en_python_y_c.html: **Guía principal**. Contiene la teoría, instrucciones paso a paso y código fuente. - python/: Directorio con los scripts de Python. - cp_server.py: Servidor de eco TCP. - cp_client.py: Cliente de eco TCP. - udp_server.py: Servidor de eco UDP. - udp_client.py: Cliente de eco UDP. - events.py: Definición de eventos del sistema. - users_service.py: Servicio de gestión de usuarios. - local_files.txt: Archivo de prueba para operaciones locales. - remote_files.txt: Archivo de prueba para operaciones remotas. - Dockerfile: Configuración para contenedorización. - requirements.txt: Dependencias del proyecto. --- ## Instrucciones de Ejecución 
  
  
  ### Python (Requisito: Python 3.10+) **TCP (Puerto 5000):** 1. Abrir terminal y ejecutar servidor: `�ash python python/tcp_server.py ` 2. Abrir otra terminal y ejecutar cliente: `�ash python python/tcp_client.py ` **UDP (Puerto 5001):** 1. Abrir terminal y ejecutar servidor: `�ash python python/udp_server.py ` 2. Abrir otra terminal y ejecutar cliente: `�ash python python/udp_client.py ` --- ## Experimentos Comparativos 
  
  
  ### A. Conexión Caída (TCP) - **Acción:** Con el cliente conectado, detén el servidor TCP (Ctrl+C). - 
  **Observación:** El cliente debería lanzar una excepción o error de conexión cerrada. TCP mantiene un estado de conexión activo. 
  
  
  ### B. Sin Servidor (UDP) - **Acción:** Ejecuta el cliente UDP sin el servidor activo. - **Observación:** El cliente envía el mensaje sin error inmediato. UDP es "fire and forget" (disparar y olvidar); no verifica si hay alguien escuchando antes de enviar.
  
  
   ### C. Tamaño de Buffer - **Acción:** Reduce el buffer a 8 bytes en el código ( ecv(8)). - **Observación:** Si envías un mensaje largo ("Hola Mundo Cruel"), lo recibirás en fragmentos. --- ## Solución de Problemas (Troubleshooting) | Problema | Solución | |----------|----------| | **Puerto en uso** | Cambia los puertos en el código (ej. 5050, 5051). | | **Firewall** | En Windows/Linux, permite el tráfico en los puertos 5000/5001. | | **Cliente no conecta** | Verifica que el servidor está corriendo y escuchando en la IP correcta (.0.0.0 para escuchar en todas las interfaces). | | **Caracteres extraños** | Asegúrate de usar codificación UTF-8 en ambos extremos. | ---
   
   
    ## Entregables Un archivo comprimido PracticaSockets_Nombre.zip que contenga: - Carpeta python/ con tus scripts. - [REPORTE.md](./REPORTE.md) con evidencias y respuestas a las preguntas de reflexión.
