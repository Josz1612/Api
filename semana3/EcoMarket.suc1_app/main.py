from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
import httpx
from typing import List

app = FastAPI(
    title="EcoMarket Sucursal 1 API",
    description="API Sucursal 1: Inventario local y notificación asíncrona de ventas a la central."
)

class Venta(BaseModel):
    producto_id: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=1)
    sucursal: str

inventario = {
    1: {"nombre": "Manzana", "stock": 100},
    2: {"nombre": "Leche", "stock": 50},
    3: {"nombre": "Pan", "stock": 80}
}

async def notificar_central(venta: Venta):
    async with httpx.AsyncClient() as client:
        try:
            # Envía una lista de ventas (aunque sea solo una)
            await client.post(
                "http://127.0.0.1:8001/ventas/notificacion",
                json=[venta.dict()],
                timeout=5
            )
        except httpx.RequestError:
            print("No se pudo notificar a la central.")

@app.post("/venta")
async def registrar_venta(ventas: List[Venta], background_tasks: BackgroundTasks):
    resultados = []
    for venta in ventas:
        if venta.producto_id not in inventario or inventario[venta.producto_id]["stock"] < venta.cantidad:
            resultados.append({"producto_id": venta.producto_id, "error": "Stock insuficiente"})
            continue
        inventario[venta.producto_id]["stock"] -= venta.cantidad
        background_tasks.add_task(notificar_central, venta)
        resultados.append({"producto_id": venta.producto_id, "msg": "Venta registrada y notificada"})
    return resultados

@app.get("/inventario")
async def get_inventario():
    return inventario