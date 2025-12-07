"""
EcoMarket Central API
Este es el servidor central que mantiene el inventario maestro 
y recibe notificaciones de todas las sucursales.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Depends, Header
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import logging
import os
import time
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app_config import settings

# Configurar logging para ver las comunicaciones entre servicios
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EcoMarket Central API",
    description="API central que gestiona el inventario maestro",
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

# Configurar estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ===== SECURITY CONFIG =====
# SECRET_KEY, ALGORITHM moved to settings
security = HTTPBearer()

# ===== DB CONNECTION =====
# DB params moved to settings

# Lista de réplicas de lectura disponibles
READ_REPLICAS = ["pg_replica1", "pg_replica2"]

def get_db_connection():
    """Conexión al nodo PRIMARIO (Escritura/Lectura crítica)"""
    conn = psycopg2.connect(
        host=settings.db_host,
        user=settings.db_user,
        password=settings.db_pass,
        database=settings.db_name
    )
    return conn

def get_read_db_connection():
    """
    Balanceador de Carga para Lectura (Round-Robin/Random)
    Intenta conectar a una réplica aleatoria. Si falla, hace fallback al primario.
    """
    replica_host = random.choice(READ_REPLICAS)
    try:
        logger.info(f"📖 Intentando leer desde réplica: {replica_host}")
        conn = psycopg2.connect(
            host=replica_host,
            user=settings.db_user,
            password=settings.db_pass,
            database=settings.db_name,
            connect_timeout=3
        )
        return conn
    except Exception as e:
        logger.warning(f"⚠️ Falló conexión a {replica_host} ({e}). Redirigiendo a PRIMARIO.")
        return get_db_connection()

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            # Create orders table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id bigserial PRIMARY KEY,
                    branch_id text,
                    product_id integer,
                    quantity_sold integer,
                    sale_price numeric,
                    timestamp timestamptz DEFAULT now()
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            logger.info("✅ Database initialized successfully")
            break
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            retries -= 1
            time.sleep(5)

@app.on_event("startup")
async def startup_event():
    init_db()

# ===== MODELOS DE DATOS =====

class Product(BaseModel):
    """Modelo que representa un producto en el inventario"""
    id: int
    name: str
    price: float
    stock: int

class ProductCreate(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    
class SaleNotification(BaseModel):
    """Notificación de venta enviada por las sucursales"""
    branch_id: str
    product_id: int
    quantity_sold: int
    timestamp: datetime
    sale_price: float

# ===== INVENTARIO CENTRAL =====
# En un sistema real, esto sería una base de datos
central_inventory: Dict[int, Product] = {
    1: Product(id=1, name="Manzanas Orgánicas", price=2.50, stock=100),
    2: Product(id=2, name="Pan Integral", price=1.80, stock=50),
    3: Product(id=3, name="Leche Deslactosada", price=3.20, stock=30),
    4: Product(id=4, name="Café Premium", price=8.90, stock=25),
    5: Product(id=5, name="Quinoa", price=12.50, stock=15)
}

# Historial de ventas centralizado
central_sales_history: List[SaleNotification] = []

# ===== ENDPOINTS PRINCIPALES =====

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verifica la validez del JWT (Firma y Expiración)"""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_algorithm],
            audience="ecomarket-api" # Debe coincidir con el 'aud' del Auth Service
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

@app.get("/", tags=["General"])
async def root():
    """Endpoint de salud del servicio"""
    return {
        "service": "EcoMarket Central API",
        "status": "operational",
        "timestamp": datetime.now(),
        "total_products": len(central_inventory)
    }

@app.get("/inventory", response_model=List[Product], tags=["Inventario"])
async def get_full_inventory():
    """Obtiene todo el inventario central"""
    logger.info("Solicitud de inventario completo recibida")
    return list(central_inventory.values())

@app.get("/inventario", response_model=List[Product], tags=["Inventario"])
async def get_full_inventory_alias():
    """Alias en español para el frontend"""
    return list(central_inventory.values())

@app.post("/products", tags=["Inventario"], dependencies=[Depends(verify_token)])
async def create_product(product: ProductCreate):
    if product.id in central_inventory:
        raise HTTPException(status_code=400, detail="Producto ya existe")
    central_inventory[product.id] = Product(**product.dict())
    return {"message": "Producto creado", "product": central_inventory[product.id]}

@app.put("/products/{product_id}", tags=["Inventario"], dependencies=[Depends(verify_token)])
async def update_product(product_id: int, product: ProductUpdate):
    if product_id not in central_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    current = central_inventory[product_id]
    if product.name is not None: current.name = product.name
    if product.price is not None: current.price = product.price
    if product.stock is not None: current.stock = product.stock
    
    return {"message": "Producto actualizado", "product": current}

@app.delete("/products/{product_id}", tags=["Inventario"], dependencies=[Depends(verify_token)])
async def delete_product(product_id: int):
    if product_id not in central_inventory:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del central_inventory[product_id]
    return {"message": "Producto eliminado"}

@app.get("/sales/recent", tags=["Ventas"])
async def get_recent_sales():
    try:
        # Usar conexión de lectura (Réplica)
        conn = get_read_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM orders ORDER BY timestamp DESC LIMIT 10")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error fetching recent sales: {e}")
        return []

@app.get("/sales", tags=["Ventas"])
async def get_all_sales():
    """Obtiene el historial completo de ventas"""
    try:
        # Usar conexión de lectura (Réplica)
        conn = get_read_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM orders ORDER BY timestamp DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        logger.error(f"Error fetching sales: {e}")
        return []

@app.post("/sale-notification", tags=["Comunicación"])
async def receive_sale_notification(notification: SaleNotification):
    """
    CONCEPTO CLAVE: Comunicación asíncrona
    
    Este endpoint recibe notificaciones de venta de las sucursales
    y actualiza el inventario central. Nota que las sucursales
    NO esperan una respuesta para completar su venta.
    """
    logger.info(f"📦 Notificación de venta recibida: {notification}")
    
    # Verificar que el producto existe
    if notification.product_id not in central_inventory:
        raise HTTPException(
            status_code=404, 
            detail=f"Producto {notification.product_id} no encontrado"
        )
    
    # Actualizar el inventario central
    product = central_inventory[notification.product_id]
    old_stock = product.stock
    product.stock = max(0, product.stock - notification.quantity_sold)
    
    # Registrar venta en DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (branch_id, product_id, quantity_sold, sale_price, timestamp) VALUES (%s, %s, %s, %s, %s)",
            (notification.branch_id, notification.product_id, notification.quantity_sold, notification.sale_price, notification.timestamp)
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving sale to DB: {e}")
    
    logger.info(
        f"📊 Inventario actualizado - {product.name}: "
        f"{old_stock} → {product.stock}"
    )
    
    return {
        "status": "received",
        "message": f"Venta registrada para {notification.quantity_sold} unidades",
        "updated_central_stock": product.stock
    }

@app.get("/dashboard", tags=["Frontend"])
async def dashboard(request: Request):
    """Renderiza el dashboard de administración central"""
    return templates.TemplateResponse("central_dashboard.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    
    # Configuración HTTPS para desarrollo local
    ssl_key = "./certs/server.key"
    ssl_cert = "./certs/server.crt"
    
    # Verificar si existen certificados y si se solicita HTTPS explícitamente o estamos en local
    # Nota: En Docker, usualmente Nginx maneja el SSL, así que esto es para ejecución directa
    if os.path.exists(ssl_key) and os.path.exists(ssl_cert) and os.getenv("USE_HTTPS_DEV") == "true":
        print("SECURE: Iniciando servidor en modo HTTPS (Puerto 8443)")
        uvicorn.run(app, host="0.0.0.0", port=8443, ssl_keyfile=ssl_key, ssl_certfile=ssl_cert)
    else:
        print("INSECURE: Iniciando servidor en modo HTTP (Puerto 8000)")
        uvicorn.run(app, host="0.0.0.0", port=8000)