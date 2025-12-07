"""
EcoMarket Sucursal API
Esta API implementa el principio de AUTONOMÍA: puede operar 
independientemente del servidor central.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import httpx
import logging
import os
import pika
import json
import asyncio
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EcoMarket Sucursal API",
    description="API de sucursal autónoma",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar templates
templates = Jinja2Templates(directory="templates")

# ===== CONFIGURACIÓN =====
BRANCH_ID = "sucursal-001"
CENTRAL_API_URL = os.getenv("CENTRAL_API_URL", "http://localhost:8000")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "guest")

# Estado Global
CURRENT_NOTIFY_METHOD = "http"  # Options: http, http_retry, http_backoff, rabbitmq

# ===== MODELOS =====

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str

class ProductUpdate(BaseModel):
    stock: Optional[int] = None
    price: Optional[float] = None

class ProductCreate(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str

class SaleRequest(BaseModel):
    product_id: int
    quantity: int
    customer_info: Optional[str] = None

class SaleResponse(BaseModel):
    sale_id: str
    product_name: str
    quantity_sold: int
    total_amount: float
    timestamp: datetime
    status: str

# ===== INVENTARIO LOCAL (AUTONOMÍA) =====
local_inventory: Dict[int, Product] = {
    1: Product(id=1, name="Manzanas Orgánicas", price=2.50, stock=25, category="food"),
    2: Product(id=2, name="Pan Integral", price=1.80, stock=15, category="food"),
    3: Product(id=3, name="Leche Deslactosada", price=3.20, stock=8, category="drink"),
    4: Product(id=4, name="Café Premium", price=8.90, stock=6, category="drink"),
    5: Product(id=5, name="Quinoa", price=12.50, stock=3, category="food")
}

sales_history: List[SaleResponse] = []

# ===== ENDPOINTS =====

@app.get("/", tags=["General"])
async def root():
    return {
        "service": f"EcoMarket Sucursal",
        "branch_id": BRANCH_ID,
        "status": "operational - AUTONOMOUS",
        "notification_method": CURRENT_NOTIFY_METHOD,
        "local_inventory_items": len(local_inventory)
    }

@app.get("/inventory", response_model=List[Product], tags=["Inventario"])
async def get_local_inventory():
    logger.info("🏪 Consultando inventario LOCAL")
    return list(local_inventory.values())

@app.put("/products/{product_id}", tags=["Inventario"])
async def update_product_stock(product_id: int, product_update: ProductUpdate):
    if product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product = local_inventory[product_id]
    if product_update.stock is not None:
        product.stock = product_update.stock
    if product_update.price is not None:
        product.price = product_update.price
        
    return {"message": "Producto actualizado", "product": product}

@app.post("/products", tags=["Inventario"])
async def create_product(product: ProductCreate):
    if product.id in local_inventory:
        raise HTTPException(status_code=400, detail="Producto ya existe en esta sucursal")
    local_inventory[product.id] = Product(**product.dict())
    return {"message": "Producto agregado a sucursal", "product": local_inventory[product.id]}

@app.delete("/products/{product_id}", tags=["Inventario"])
async def delete_product(product_id: int):
    if product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del local_inventory[product_id]
    return {"message": "Producto eliminado de sucursal"}

@app.post("/set-method", tags=["Config"])
async def set_notification_method(method: str = Form(...)):
    global CURRENT_NOTIFY_METHOD
    if method in ["http", "http_retry", "http_backoff", "rabbitmq"]:
        CURRENT_NOTIFY_METHOD = method
        logger.info(f"🔄 Método de notificación cambiado a: {method}")
    return RedirectResponse(url="/dashboard", status_code=303)

@app.post("/sales", response_model=SaleResponse, tags=["Ventas"])
async def process_sale(sale_request: SaleRequest, background_tasks: BackgroundTasks):
    # PASO 1: Verificación local
    if sale_request.product_id not in local_inventory:
        raise HTTPException(status_code=404, detail="Producto no disponible")
    
    product = local_inventory[sale_request.product_id]
    
    if product.stock < sale_request.quantity:
        raise HTTPException(status_code=400, detail=f"Stock insuficiente. Disponible: {product.stock}")
    
    # PASO 2: Procesar venta
    product.stock -= sale_request.quantity
    sale_timestamp = datetime.now()
    total_amount = product.price * sale_request.quantity
    
    sale_response = SaleResponse(
        sale_id=f"{BRANCH_ID}_{sale_timestamp.isoformat()}",
        product_name=product.name,
        quantity_sold=sale_request.quantity,
        total_amount=total_amount,
        timestamp=sale_timestamp,
        status="completed"
    )
    
    sales_history.append(sale_response)
    
    # PASO 3: Notificar según método configurado
    background_tasks.add_task(
        dispatch_notification,
        sale_request.product_id,
        sale_request.quantity,
        sale_timestamp,
        total_amount
    )
    
    return sale_response

@app.get("/sales", response_model=List[SaleResponse], tags=["Ventas"])
async def get_sales_history():
    return sales_history

@app.get("/sales/stats", tags=["Ventas"])
async def get_sales_stats():
    if not sales_history:
        return {"total_sales": 0, "total_revenue": 0}
    total_revenue = sum(sale.total_amount for sale in sales_history)
    return {
        "total_sales": len(sales_history),
        "total_revenue": round(total_revenue, 2),
        "average_sale": round(total_revenue / len(sales_history), 2)
    }

@app.get("/dashboard", tags=["Frontend"])
async def dashboard(request: Request):
    return templates.TemplateResponse("sucursal_dashboard.html", {
        "request": request,
        "notify_method": CURRENT_NOTIFY_METHOD
    })

# ===== LÓGICA DE NOTIFICACIÓN =====

async def dispatch_notification(p_id, qty, ts, amount):
    notification = {
        "branch_id": BRANCH_ID,
        "product_id": p_id,
        "quantity_sold": qty,
        "timestamp": ts.isoformat(),
        "sale_price": amount
    }
    
    logger.info(f"📤 Iniciando notificación usando método: {CURRENT_NOTIFY_METHOD}")
    
    if CURRENT_NOTIFY_METHOD == "rabbitmq":
        notify_via_rabbitmq(notification)
    elif CURRENT_NOTIFY_METHOD == "http_retry":
        await notify_via_http_retry(notification)
    elif CURRENT_NOTIFY_METHOD == "http_backoff":
        await notify_via_http_backoff(notification)
    else:
        await notify_via_http_simple(notification)

def notify_via_rabbitmq(notification):
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='sales_queue', durable=True)
        
        channel.basic_publish(
            exchange='',
            routing_key='sales_queue',
            body=json.dumps(notification),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        connection.close()
        logger.info("🐰 [RabbitMQ] Notificación enviada a la cola")
    except Exception as e:
        logger.error(f"❌ [RabbitMQ] Error: {e}")

async def notify_via_http_simple(notification):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{CENTRAL_API_URL}/sale-notification", json=notification)
            if resp.status_code == 200:
                logger.info("✅ [HTTP] Notificación enviada")
            else:
                logger.warning(f"⚠️ [HTTP] Falló con status {resp.status_code}")
    except Exception as e:
        logger.error(f"❌ [HTTP] Error de conexión: {e}")

async def notify_via_http_retry(notification, retries=3):
    for i in range(retries):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(f"{CENTRAL_API_URL}/sale-notification", json=notification)
                if resp.status_code == 200:
                    logger.info(f"✅ [HTTP Retry] Enviado en intento {i+1}")
                    return
        except Exception as e:
            logger.warning(f"⚠️ [HTTP Retry] Intento {i+1} falló: {e}")
            await asyncio.sleep(1)
    logger.error("❌ [HTTP Retry] Todos los intentos fallaron")

async def notify_via_http_backoff(notification, retries=5):
    delay = 1
    for i in range(retries):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.post(f"{CENTRAL_API_URL}/sale-notification", json=notification)
                if resp.status_code == 200:
                    logger.info(f"✅ [HTTP Backoff] Enviado en intento {i+1}")
                    return
        except Exception as e:
            logger.warning(f"⚠️ [HTTP Backoff] Intento {i+1} falló. Esperando {delay}s...")
            await asyncio.sleep(delay)
            delay *= 2  # Exponential backoff
    logger.error("❌ [HTTP Backoff] Todos los intentos fallaron")