Semana 4: Arquitectura Orientada a Eventos y Mensajer�a (RabbitMQ)
Esta semana marca la transici�n de una arquitectura acoplada (HTTP s�ncrono) a una Arquitectura Orientada a Eventos utilizando RabbitMQ. El objetivo es desacoplar los servicios, mejorar la resiliencia y permitir la escalabilidad horizontal.

Documentaci�n de Referencia
semana4.html: Gu�a principal sobre el patr�n Pub/Sub (Fanout Exchange) para notificaciones de usuarios.
ecomarket_rabbitmq_fundamentado.html: El "Journey" hacia las colas de mensajes, justificando la necesidad de RabbitMQ para la fiabilidad en ventas.
Objetivos del Taller
Comprender el Problema: Analizar por qu� el acoplamiento HTTP s�ncrono no escala (latencia acumulada, fallos en cascada).
Implementar Pub/Sub: Usar un Fanout Exchange para que un evento (UsuarioCreado) notifique a m�ltiples suscriptores (Email, Loyalty, Analytics) sin que el publicador los conozca.
Garantizar Fiabilidad: Configurar colas durables, mensajes persistentes y confirmaciones (ACKs) para evitar p�rdida de datos.
Validar Resiliencia: Realizar pruebas de caos (matar consumidores, reiniciar RabbitMQ) para verificar la recuperaci�n autom�tica.
Estructura del Proyecto
Semana4/
 docker-compose.yml          # Infraestructura (RabbitMQ + Management UI)
 events.py                   # Definici�n de Publishers (Simple, Persistente, Robusto)
 user_publisher.py           # Publicador de eventos de usuario
 email_consumer_simple.py    # Consumidor de Email (Simulado)
 loyalty_consumer_simple.py  # Consumidor de Lealtad (Simulado)
 analytics_consumer.py       # Consumidor de Anal�tica (Reto)
 dead_letter_consumer.py     # Manejo de mensajes fallidos (DLQ)
 scripts/                    # Scripts de utilidad y demo
    demo_quick.ps1          # Script de demostracin rpida
 requirements.txt            # Dependencias (pika, etc.)
 setup_queues.py             # Script para configuración inicial de colas
Instrucciones de Ejecuci�n (Paso a Paso)
1. Infraestructura
Levantar RabbitMQ con Docker Compose:

docker-compose up -d
Acceder a la UI de RabbitMQ en: http://localhost:15672 (user: ecomarket_user, pass: ecomarket_password).

2. Escenario Pub/Sub (Usuarios)
Este escenario demuestra el desacoplamiento: un evento dispara m�ltiples acciones.

Iniciar Consumidores (en terminales separadas):
python email_consumer_simple.py
python loyalty_consumer_simple.py
Publicar Evento:
python user_publisher.py --nombre "Juan Perez" --email "juan@example.com"
Observar: Ambos consumidores deben procesar el mensaje simult�neamente.
3. Pruebas de Resiliencia (Caos)
Sigue las instrucciones de la Fase 3 en semana4.html:

Persistencia: Publica un mensaje, reinicia RabbitMQ (docker restart ...), luego inicia un consumidor. El mensaje debe procesarse.
Fallo de Consumidor: Inicia un consumidor, mata el proceso (Ctrl+C) mientras procesa, y rein�cialo. El mensaje debe volver a la cola.
Demo R�pida (Script Automatizado)
Para una demostraci�n r�pida del flujo completo (incluyendo reintentos y Dead Letter Queue), puedes usar el script de PowerShell incluido:

# Ejecuta demo_quick y abre el management UI al final
.\scripts\demo_quick.ps1 -OpenManagementUI
Nota: Este script usa FAST_RETRY=1 para acelerar los tiempos de espera de reintento para prop�sitos de demostraci�n.

Entregables
Cdigo Fuente: Implementacin de Publishers y Consumers.
Diagrama de Arquitectura: Flujo de eventos actualizado (Mermaid).
Informe de Justificacin: Taller4_Justificacion.md - Anlisis de ROI, latencia y desacoplamiento.
Video Demo: https://drive.google.com/file/d/1Z-rRrp7p7Iy2BOo8OwkQQHFhcJi9I_Ua/view?usp=sharing
Diagrama de Arquitectura (Pub/Sub)

