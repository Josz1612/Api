from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(title="EcoMarket Products API")

class Product(BaseModel):
    id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)

products_db = [
    Product(id=1, name="Manzana", price=10.5, stock=100),
    Product(id=2, name="Leche", price=22.0, stock=50),
    Product(id=3, name="Pan", price=8.0, stock=80),
]

@app.get("/products", response_model=List[Product])
def get_products():
    return products_db

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    for product in products_db:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail={"error": "Producto no encontrado"})

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    if any(p.id == product.id for p in products_db):
        raise HTTPException(status_code=400, detail={"error": "ID ya existe"})
    products_db.append(product)
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product: Product):
    for idx, p in enumerate(products_db):
        if p.id == product_id:
            products_db[idx] = product
            return product
    raise HTTPException(status_code=404, detail={"error": "Producto no encontrado"})

@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int):
    for idx, p in enumerate(products_db):
        if p.id == product_id:
            del products_db[idx]
            return
    raise HTTPException(status_code=404, detail={"error": "Producto no encontrado"})