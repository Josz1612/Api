from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="EcoMarket Central API",
    description="API Central: Inventario global y recepción de notificaciones de ventas de sucursales."
)

class Venta(BaseModel):
    producto_id: int
    cantidad: int
    sucursal: str

inventario_global = {
    1: {"nombre": "Manzana", "stock": 1000},
    2: {"nombre": "Leche", "stock": 500},
    3: {"nombre": "Pan", "stock": 800}
}
notificaciones = []  # Historial de notificaciones

@app.post(
    "/ventas/notificacion",
    include_in_schema=False
)
async def recibir_notificacion(ventas: List[Venta]):
    resultados = []
    for venta in ventas:
        if venta.producto_id in inventario_global:
            inventario_global[venta.producto_id]["stock"] -= venta.cantidad
            mensaje = (
                f"Notificación recibida de {venta.sucursal}: "
                f"Producto {venta.producto_id}, cantidad {venta.cantidad}. "
                f"Inventario global actualizado."
            )
            notificaciones.append({
                "sucursal": venta.sucursal,
                "producto_id": venta.producto_id,
                "cantidad": venta.cantidad,
                "mensaje": mensaje
            })
            print(mensaje)
            resultados.append({
                "msg": mensaje,
                "inventario_actual": inventario_global[venta.producto_id]["stock"]
            })
        else:
            mensaje = f"Producto {venta.producto_id} no existe en inventario global."
            notificaciones.append({
                "sucursal": venta.sucursal,
                "producto_id": venta.producto_id,
                "cantidad": venta.cantidad,
                "mensaje": mensaje
            })
            print(mensaje)
            resultados.append({"msg": mensaje})
    return resultados

@app.get("/inventario")
async def get_inventario():
    return inventario_global

@app.get("/notificaciones")
async def get_notificaciones():
    return notificaciones