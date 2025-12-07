Fase 2 — Implementando Pub/Sub con propósito
Fecha: 21-10-2025

Objetivo: Implementar y validar un Fanout Exchange (user_events) que permita publicar un evento UsuarioCreado y que múltiples consumidores lo procesen de forma independiente.

Demo rápida (5 minutos)

Asegúrate de tener RabbitMQ corriendo (docker-compose up -d o docker run rabbitmq:3-management).
En terminal A, ejecuta:
python .\email_consumer_simple.py
En terminal B, ejecuta:
python .\loyalty_consumer_simple.py
En terminal C, publica un evento (nivel 1):
python .\events_publisher_levels.py --level 1 --nombre "Juan" --email "juan@eco.com"
Observa que ambos consumers imprimen su log: email enviado y lealtad activada.

Implementación (archivos añadidos)

events_publisher_levels.py — publisher en niveles 1/2/3.
email_consumer_simple.py, loyalty_consumer_simple.py — consumers simples binded a user_events (fanout).
Checklist de Fase 2

 Exchange user_events (fanout) declarado por publisher y consumers.
 Publisher puede publicar en 3 niveles (simple, persistente, confirmaciones).
 Consumers independientes con ACK manual.
 Demo rápida verificada localmente.
Pruebas recomendadas (siguientes pasos)

Nivel 2: publicar con persistencia, reiniciar RabbitMQ y comprobar que los mensajes persisten si hay consumidores durables/queues declaradas (requiere usar queues nombradas en lugar de exclusivas).
Nivel 3: forzar desconexión del broker y comprobar reintentos/backoff.
Implementar DLQ y reintentos en consumers para errores transitorios.
Demo de reintentos y DLQ

Ejecuta setup_queues.py para crear las queues durables y DLQ:
python .\setup_queues.py
Inicia el dead-letter consumer (para inspección):
python .\dead_letter_consumer.py
Inicia los consumers:
python .\email_consumer_simple.py
python .\loyalty_consumer_simple.py
python .\analytics_consumer.py
Publica mensajes que forcen fallo y activa el flujo de retry:
python .\simulate_fail_publisher.py --count 3
Observa: los mensajes serán reencolados a retry-queues con delays (5s, 30s, 120s). Si exceden retries, aparecerán en la dead_letter_queue y dead_letter_consumer.py los mostrará.