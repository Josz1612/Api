# 📘 Semana 3: Sistema de Mensajería y Eventos

## 🎯 Objetivos de la Semana

- ✅ Implementar sistema de eventos
- ✅ Configurar RabbitMQ con Docker
- ✅ Crear productores y consumidores
- ✅ Procesamiento asíncrono de ventas

## 📂 Archivos Principales

- `producer.py` - Productor de mensajes (ventas)
- `consumer.py` - Consumidor de mensajes
- `email_consumer.py` - Envío de emails
- `loyalty_consumer.py` - Sistema de puntos
- `events.py` - Definición de eventos
- `docker-compose.yml` - Configuración de RabbitMQ

## 🐰 Arquitectura RabbitMQ

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Producer   │─────▶│   RabbitMQ   │─────▶│  Consumer   │
│  (Ventas)   │      │   Exchange   │      │  (Email)    │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            └──────────────▶┌─────────────┐
                                            │  Consumer   │
                                            │  (Loyalty)  │
                                            └─────────────┘
```

## 🔌 Eventos Implementados

### 1. Evento de Venta
```python
{
    "event_type": "sale_completed",
    "sale_id": "12345",
    "product_id": 1,
    "product_name": "Manzana Orgánica",
    "quantity": 5,
    "total": 75.00,
    "customer_email": "cliente@example.com",
    "timestamp": "2024-12-04T10:30:00"
}
```

### 2. Exchange y Queues
- **Exchange**: `sales_events` (tipo fanout)
- **Queue 1**: `email_notifications` → Envío de emails
- **Queue 2**: `loyalty_points` → Puntos de fidelidad

## 🚀 Cómo Ejecutar

### 1. Iniciar RabbitMQ con Docker
```bash
docker-compose up -d
```

### 2. Verificar RabbitMQ
```
URL: http://localhost:15672
Usuario: guest
Password: guest
```

### 3. Iniciar Consumidores
```bash
# Terminal 1: Consumidor de emails
python email_consumer.py

# Terminal 2: Consumidor de loyalty
python loyalty_consumer.py
```

### 4. Enviar Ventas (Producer)
```bash
python send_sale.py
```

## ✨ Características Implementadas

- ✅ Sistema de eventos desacoplado
- ✅ Múltiples consumidores por evento
- ✅ Persistencia de mensajes
- ✅ Procesamiento asíncrono
- ✅ Confirmación de entrega (ACK)
- ✅ Reintentos automáticos

## 📊 Flujo de Trabajo

1. **Usuario realiza compra** en `/catalog`
2. **API procesa la venta** y actualiza stock
3. **Producer envía evento** a RabbitMQ
4. **Exchange distribuye** a todas las queues
5. **Consumidores procesan** independientemente:
   - Email: Envía confirmación al cliente
   - Loyalty: Calcula y asigna puntos

## 🔧 Configuración Docker

```yaml
# docker-compose.yml
services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"   # Puerto AMQP
      - "15672:15672" # Puerto Management
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
```

## 🎓 Conceptos Clave

- **Message Broker**: Intermediario de mensajes
- **Publisher/Subscriber**: Patrón de comunicación
- **Exchange**: Rutea mensajes a queues
- **Queue**: Almacena mensajes para consumidores
- **ACK**: Confirmación de procesamiento exitoso
- **Fanout**: Distribuye a todas las queues conectadas

## 🐛 Troubleshooting

### RabbitMQ no inicia
```bash
docker-compose down
docker-compose up -d
```

### Consumidor no recibe mensajes
- Verificar que RabbitMQ esté corriendo
- Revisar que exchange y queues existan
- Confirmar binding entre exchange y queue

## 📈 Beneficios

- ✅ **Desacoplamiento**: Producer y consumers independientes
- ✅ **Escalabilidad**: Múltiples consumers en paralelo
- ✅ **Resiliencia**: Mensajes persistidos
- ✅ **Asincronía**: No bloquea la venta
