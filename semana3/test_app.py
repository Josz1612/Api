import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product_success():
    response = client.get("/products/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_product_not_found():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert "error" in response.json()["detail"]

def test_post_product_success():
    new_product = {"id": 10, "name": "Queso", "price": 30, "stock": 5}
    response = client.post("/products", json=new_product)
    assert response.status_code == 201
    assert response.json()["name"] == "Queso"

def test_post_product_duplicate_id():
    duplicate = {"id": 1, "name": "Repetido", "price": 10, "stock": 1}
    response = client.post("/products", json=duplicate)
    assert response.status_code == 400
    assert "error" in response.json()["detail"]

def test_put_product_success():
    update = {"id": 1, "name": "Manzana Roja", "price": 12, "stock": 90}
    response = client.put("/products/1", json=update)
    assert response.status_code == 200
    assert response.json()["name"] == "Manzana Roja"

def test_put_product_not_found():
    update = {"id": 999, "name": "Nada", "price": 1, "stock": 1}
    response = client.put("/products/999", json=update)
    assert response.status_code == 404
    assert "error" in response.json()["detail"]

def test_delete_product_success():
    response = client.delete("/products/2")
    assert response.status_code == 204

def test_delete_product_not_found():
    response = client.delete("/products/999")
    assert response.status_code == 404
    assert "error" in response.json()["detail"]