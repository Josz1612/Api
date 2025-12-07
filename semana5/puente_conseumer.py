import pika
from pika.exceptions import AMQPConnectionError
import json
import requests
import os
import time
import logging
import sys

# Configurar logging para que se vea en docker logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("BridgeConsumer")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")
CENTRAL_API_URL = os.getenv("CENTRAL_API_URL", "http://central-api:8000")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        logger.info(f"📥 [Bridge] Recibido evento de venta: {data.get('product_id')} (Cant: {data.get('quantity_sold')})")
        
        # Reenviar a Central API via HTTP
        try:
            response = requests.post(f"{CENTRAL_API_URL}/sale-notification", json=data, timeout=5)
            
            if response.status_code == 200:
                logger.info("✅ [Bridge] Sincronizado con Central API")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                logger.warning(f"⚠️ [Bridge] Central API rechazó: {response.status_code} - {response.text}")
                # Si es 404 (producto no existe) o 4xx, no reintentamos infinitamente
                if 400 <= response.status_code < 500:
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                else:
                    # Error de servidor, reintentar
                    time.sleep(2)
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [Bridge] Error conectando a Central API: {e}")
            time.sleep(2)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            
    except Exception as e:
        logger.error(f"❌ [Bridge] Error procesando mensaje: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    logger.info("⏳ Esperando a RabbitMQ...")
    time.sleep(10) # Dar tiempo a RabbitMQ para iniciar
    
    while True:
        try:
            logger.info(f"🔌 Conectando a RabbitMQ en {RABBITMQ_HOST}...")
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
            )
            channel = connection.channel()
            
            # Asegurar que la cola existe (la misma que usa sucursal_api)
            channel.queue_declare(queue='sales_queue', durable=True)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='sales_queue', on_message_callback=callback)
            
            logger.info("🚀 Bridge Consumer iniciado. Escuchando 'sales_queue'...")
            channel.start_consuming()
        except AMQPConnectionError as e:
            logger.error(f"❌ Error de conexión RabbitMQ: {e}. Reintentando en 5s...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"❌ Error inesperado: {e}. Reintentando en 5s...")
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()