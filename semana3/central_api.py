# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime, timezone
import logging
import pika
from pika.exceptions import AMQPConnectionError
import json
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
import threading
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Configuración de Seguridad (Integración con Semana 8) ---
SECRET_KEY = "secreto_super_seguro_para_desarrollo"
ALGORITHM = "HS256"
# Apunta al servicio de autenticación (Docker o Local)
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8002")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{AUTH_SERVICE_URL}/login")

async def validar_token_central(token: str = Depends(oauth2_scheme)):
    try:
        # Validamos la firma usando la misma SECRET_KEY que el servicio de Auth
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="ecomarket-api")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

app = FastAPI(
    # title="🌱 EcoMarket Central API",
    # description="""
    # ## API central que gestiona el inventario maestro
    
    # ### 🏠 [← Regresar al Dashboard Principal](/)
    
    # Esta API permite:
    # - 📦 Consultar inventario central
    # - 🔔 Recibir notificaciones de ventas de sucursales
    # - 📊 Monitorear el estado del sistema
    
    # ### Enlaces útiles:
    # - 🏠 [Dashboard Central](/) - Interfaz principal
    # - 📊 [Estado del Sistema](/api/status) - Health check
    # - 📦 [Inventario](/inventory) - Lista completa de productos
    # """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Bootstrap configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    
class SaleNotification(BaseModel):
    """Notificación de venta enviada por las sucursales"""
    branch_id: str
    product_id: int
    quantity_sold: int
    timestamp: datetime
    sale_price: float

central_inventory: Dict[int, Product] = {
    1: Product(id=1, name="Manzanas Organicas", price=2.50, stock=100),
    2: Product(id=2, name="Pan Integral", price=1.80, stock=50),
    3: Product(id=3, name="Leche Deslactosada", price=3.20, stock=30),
    4: Product(id=4, name="Cafe Premium", price=8.90, stock=25),
    5: Product(id=5, name="Quinoa", price=12.50, stock=15)
}

# ===== HISTORIAL DE NOTIFICACIONES DE VENTA =====
# Agregar algunas ventas de muestra para demostración
sale_notifications: List[SaleNotification] = [
    SaleNotification(
        branch_id="Sucursal 001",
        product_id=1,
        quantity_sold=5,
        timestamp=datetime.now(timezone.utc),
        sale_price=12.50
    ),
    SaleNotification(
        branch_id="Sucursal 001", 
        product_id=2,
        quantity_sold=3,
        timestamp=datetime.now(timezone.utc),
        sale_price=5.40
    ),
    SaleNotification(
        branch_id="Sucursal 001",
        product_id=3,
        quantity_sold=2,
        timestamp=datetime.now(timezone.utc),
        sale_price=6.40
    )
]

@app.get("/", response_class=HTMLResponse, tags=["General"])
async def dashboard(request: Request):
    return templates.TemplateResponse("central_dashboard.html", {
        "request": request,
        "inventory": list(central_inventory.values()),
        "total_products": len(central_inventory),
        "notifications": sale_notifications[-10:],
        "timestamp": datetime.now(timezone.utc)
    })

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Servir favicon para evitar errores 404"""
    return HTMLResponse(content="", status_code=204)

@app.get("/api/status", tags=["General"])
async def api_status():
    return {
        "service": "EcoMarket Central API",
        "status": "operational",
        "timestamp": datetime.now(timezone.utc),
        "total_products": len(central_inventory)
    }

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc)
    }

# ===== ENDPOINTS CRUD PARA PRODUCTOS =====

# Crear producto
@app.post("/products", response_model=Product, tags=["Inventario"])
async def create_product(product: Product, token_payload: dict = Depends(validar_token_central)):
    """Crear un nuevo producto en el inventario central (Requiere Autenticación)"""
    # Verificar rol de administrador
    if token_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    try:
        if product.id in central_inventory:
            logger.warning(f"Intento de crear producto con ID existente: {product.id}")
            raise HTTPException(status_code=400, detail=f"ID de producto {product.id} ya existe")
        
        # Validaciones adicionales
        if product.price <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor que 0")
        if product.stock < 0:
            raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
        if not product.name.strip():
            raise HTTPException(status_code=400, detail="El nombre del producto es requerido")
            
        central_inventory[product.id] = product
        logger.info(f"Producto creado: {product.name} (ID: {product.id})")
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando producto: {e}")
        raise HTTPException(status_code=400, detail="Error en los datos del producto")

# Leer todos los productos
@app.get("/products", response_model=List[Product], tags=["Inventario"])
async def get_all_products():
    """Obtiene todos los productos del inventario central"""
    logger.info("Solicitud de productos recibida")
    return list(central_inventory.values())

# Leer producto por ID
@app.get("/products/{product_id}", response_model=Product, tags=["Inventario"])
async def get_product(product_id: int):
    """Obtiene un producto específico por su ID"""
    if product_id not in central_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return central_inventory[product_id]

# Actualizar producto
@app.put("/products/{product_id}", response_model=Product, tags=["Inventario"])
async def update_product(product_id: int, updated: Product, token_payload: dict = Depends(validar_token_central)):
    """Actualiza un producto existente (Requiere Autenticación)"""
    # Verificar rol de administrador
    if token_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    if product_id not in central_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    central_inventory[product_id] = updated
    logger.info(f"Producto actualizado: {updated.name} (ID: {product_id})")
    return updated

# Eliminar producto
@app.delete("/products/{product_id}", tags=["Inventario"])
async def delete_product(product_id: int, token_payload: dict = Depends(validar_token_central)):
    """Elimina un producto del inventario (Requiere Autenticación)"""
    # Verificar rol de administrador
    if token_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requieren permisos de administrador")

    if product_id not in central_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    product_name = central_inventory[product_id].name
    del central_inventory[product_id]
    logger.info(f"Producto eliminado: {product_name} (ID: {product_id})")
    return {"detail": "Producto eliminado"}

@app.get("/inventory", response_model=List[Product], tags=["Inventario"])
async def get_full_inventory():
    """Obtiene todo el inventario central (alias de /products)"""
    logger.info("Solicitud de inventario completo recibida")
    return list(central_inventory.values())

@app.get("/inventario", tags=["Inventario"])
async def get_inventario():
    """Obtiene todo el inventario central (endpoint en español)"""
    logger.info("Solicitud de inventario en español recibida")
    products = []
    for product in central_inventory.values():
        products.append({
            "id": product.id,
            "nombre": product.name,  # Convertir name a nombre
            "precio": product.price,  # Convertir price a precio
            "stock": product.stock
        })
    return products

@app.get("/api-docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_api_docs():
    """Página personalizada de documentación con botón de regreso"""
    return HTMLResponse(content="""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EcoMarket API - Documentación</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        .api-header {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
        }
        .back-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
            color: white;
            transform: translateY(-2px);
        }
        .swagger-container {
            height: calc(100vh - 200px);
            border: none;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <!-- Header personalizado -->
    <div class="api-header py-4">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-md-8">
                    <h1 class="mb-1">
                        <i class="bi bi-book"></i> EcoMarket API - Documentación
                    </h1>
                    <p class="mb-0 opacity-75">Explora y prueba todos los endpoints de la API</p>
                </div>
                <div class="col-md-4 text-md-end">
                    <a href="/" class="btn back-btn btn-lg">
                        <i class="bi bi-house-door"></i> Volver
                    </a>
                </div>
            </div>
        </div>
    </div>
                        

    <!-- Swagger UI embebido -->
    <div class="container-fluid px-4">
        <div class="row">
            <div class="col-12">
                <iframe src="/docs" class="swagger-container w-100"></iframe>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
    """)

@app.post("/sale-notification", include_in_schema=False)
async def receive_sale_notification(notification: SaleNotification):
    logger.info(f"Notificacion de venta recibida: {notification}")
    sale_notifications.append(notification)
    
    if notification.product_id not in central_inventory:
        raise HTTPException(status_code=404, detail=f"Producto {notification.product_id} no encontrado")
    
    product = central_inventory[notification.product_id]
    old_stock = product.stock
    product.stock = max(0, product.stock - notification.quantity_sold)
    
    logger.info(f"Inventario actualizado - {product.name}: {old_stock} -> {product.stock}")

        # Ya no se reenvía la notificación a RabbitMQ
    
    return {
        "status": "received",
        "message": f"Venta registrada para {notification.quantity_sold} unidades",
        "updated_central_stock": product.stock
    }

@app.get("/sale-notifications", response_model=List[SaleNotification], tags=["Comunicación"])
async def get_sale_notifications():
    """
    Devuelve el historial de notificaciones de ventas recibidas desde sucursales.
    """
    return sale_notifications

@app.get("/sales/recent", response_model=List[SaleNotification], tags=["Comunicación"])
async def get_recent_sales():
    """
    Devuelve las ventas recientes (alias de sale-notifications para el frontend)
    """
    logger.info("Solicitud de ventas recientes recibida")
    return sale_notifications[-10:]  # Últimas 10 ventas

# --- RabbitMQ Consumer Background Task ---
def consume_sales_events():
    """Consumidor en segundo plano para recibir ventas vía RabbitMQ"""
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    logger.info(f"🐰 Iniciando consumidor RabbitMQ en {rabbitmq_host}...")
    
    # Esperar un poco a que RabbitMQ arranque si estamos en Docker
    import time
    time.sleep(10) 
    
    while True:
        try:
            params = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=5672,
                credentials=pika.PlainCredentials('ecomarket_user', 'ecomarket_password'),
                heartbeat=600,
                blocked_connection_timeout=300
            )
            connection = pika.BlockingConnection(params)
            channel = connection.channel()
            
            # Declarar Exchange Fanout (Idempotente)
            channel.exchange_declare(exchange='sales_events', exchange_type='fanout', durable=True)

            # Asegurar que la cola existe y vincularla al exchange
            channel.queue_declare(
                queue='sale_notifications', # Cola específica para Central API
                durable=True,
                arguments={
                    'x-message-ttl': 86400000,
                    'x-dead-letter-exchange': '',
                    'x-dead-letter-routing-key': 'sale_notifications_dlq'
                }
            )
            # Binding: Unir la cola al exchange
            channel.queue_bind(exchange='sales_events', queue='sale_notifications')
            
            def callback(ch, method, properties, body):
                try:
                    data = json.loads(body)
                    logger.info(f"📥 [RabbitMQ] Venta recibida: {data}")
                    
                    # Actualizar inventario
                    pid = data.get('product_id')
                    qty = data.get('quantity_sold')
                    
                    if pid in central_inventory:
                        old_stock = central_inventory[pid].stock
                        central_inventory[pid].stock = max(0, central_inventory[pid].stock - qty)
                        logger.info(f"📉 Stock actualizado: {central_inventory[pid].name} {old_stock} -> {central_inventory[pid].stock}")
                        
                        # Agregar a historial
                        sale_notifications.append(SaleNotification(
                            branch_id=data.get('branch_id', 'Unknown'),
                            product_id=pid,
                            quantity_sold=qty,
                            timestamp=datetime.fromisoformat(data.get('timestamp')),
                            sale_price=data.get('sale_price', 0.0)
                        ))
                    
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    
                except Exception as e:
                    logger.error(f"❌ Error procesando mensaje RabbitMQ: {e}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='sale_notifications', on_message_callback=callback)
            logger.info("🐰 Consumidor esperando mensajes en 'sale_notifications'...")
            channel.start_consuming()
            
        except AMQPConnectionError as e:
            logger.error(f"❌ Error de conexión RabbitMQ: {e}. Reintentando en 5s...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"❌ Error fatal en consumidor RabbitMQ: {e}. Reintentando en 5s...")
            time.sleep(5)

@app.on_event("startup")
async def startup_event():
    # Iniciar consumidor en hilo separado
    t = threading.Thread(target=consume_sales_events, daemon=True)
    t.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)