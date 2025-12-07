from fastapi import FastAPI
import os
import socket

app = FastAPI()

INSTANCE_ID = os.getenv("INSTANCE_ID", "unknown")
HOSTNAME = socket.gethostname()

@app.get("/")
async def root():
    return {
        "message": "Hello from EcoMarket User Service",
        "instance_id": INSTANCE_ID,
        "hostname": HOSTNAME
    }

@app.get("/users")
async def get_users():
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Charlie"}
        ],
        "served_by": INSTANCE_ID
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "instance_id": INSTANCE_ID}