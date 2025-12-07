"""
Ejemplo mínimo de API en FastAPI.
Instrucciones: crear un entorno y ejecutar `uvicorn example_fastapi:app --reload`.
Este código es un ejemplo didáctico, no incluye persistencia real (usa memoria).
"""
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

app = FastAPI(title="API Productos ejemplo")

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    price: float = Field(..., ge=0)
    currency: str = Field(...)
    tags: Optional[List[str]] = []

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    createdAt: datetime

# almacenamiento en memoria (solo ejemplo)
DB = {}

def format_response(data=None, error=None, meta=None):
    return {"data": data, "error": error, "meta": meta or {}}

@app.post('/api/v1/products', status_code=201)
def create_product(payload: ProductCreate):
    pid = str(uuid4())
    now = datetime.utcnow()
    product = Product(id=pid, createdAt=now, **payload.dict())
    DB[pid] = product
    return format_response(data=product.dict())

@app.get('/api/v1/products')
def list_products():
    items = [p.dict() for p in DB.values()]
    return format_response(data=items)

@app.get('/api/v1/products/{id}')
def get_product(id: str):
    p = DB.get(id)
    if not p:
        raise HTTPException(status_code=404, detail="No encontrado")
    return format_response(data=p.dict())

@app.put('/api/v1/products/{id}')
def update_product(id: str, payload: ProductCreate):
    p = DB.get(id)
    if not p:
        raise HTTPException(status_code=404, detail="No encontrado")
    updated = p.copy(update=payload.dict())
    DB[id] = updated
    return format_response(data=updated.dict())

@app.delete('/api/v1/products/{id}', status_code=204)
def delete_product(id: str):
    if id in DB:
        del DB[id]
        return
    raise HTTPException(status_code=404, detail="No encontrado")