import os
import uuid
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app_config import settings

# --- Configuración ---
# SECRET_KEY, ALGORITHM, etc. are now in settings
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Simulación de Base de Datos
fake_users_db: dict = {
    "user123": {
        "id": "user123",
        "email": "admin@ecomarket.com",
        "password": "password123", # En producción, usar hash!
        "role": "admin"
    },
    "user456": {
        "id": "user456",
        "email": "cliente@ecomarket.com",
        "password": "password123",
        "role": "cliente"
    }
}

# Almacenamiento de refresh tokens (en memoria para el ejemplo)
refresh_tokens_db = {}

# --- Modelos Pydantic ---
class Credenciales(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class RefreshTokenRequest(BaseModel):
    refresh_token: str

# --- Rate Limiting ---
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title="EcoMarket Auth API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS Configuration ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Funciones de Utilidad ---
def crear_token(usuario_id: str, rol: str, expires_delta: Optional[timedelta] = None):
    to_encode: dict = {
        "sub": usuario_id,
        "role": rol,
        "iss": "ecomarket-auth-service",
        "aud": "ecomarket-api",
        "jti": str(uuid.uuid4())
    }
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Actualizar payload con tiempos de expiración y emisión
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def crear_refresh_token(usuario_id: str):
    jti = str(uuid.uuid4())
    ahora = datetime.now(timezone.utc)
    expires = ahora + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": usuario_id,
        "jti": jti,
        "type": "refresh",
        "iat": ahora,
        "exp": expires
    }
    token = jwt.encode(payload, settings.jwt_refresh_secret, algorithm=settings.jwt_algorithm)
    
    # Guardar en "BD"
    refresh_tokens_db[jti] = {
        "usuario_id": usuario_id,
        "creado": ahora,
        "revocado": False,
        "expira": expires
    }
    return token

def autenticar_usuario(credenciales: Credenciales):
    # Buscar usuario por email
    user = next((u for u in fake_users_db.values() if u["email"] == credenciales.email), None)
    if not user:
        return None
    if user["password"] != credenciales.password:
        return None
    return user

# --- Dependencias de Seguridad ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def verificar_jwt(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret, 
            algorithms=[settings.jwt_algorithm],
            options={"verify_signature": True, "verify_aud": True, "verify_iss": True},
            audience="ecomarket-api",
            issuer="ecomarket-auth-service"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Endpoints ---

@app.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(request: Request, credenciales: Credenciales):
    user = autenticar_usuario(credenciales)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.jwt_expire_minutes)
    access_token = crear_token(
        usuario_id=user["id"], 
        rol=user["role"], 
        expires_delta=access_token_expires
    )
    refresh_token = crear_refresh_token(user["id"])
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer",
        "expires_in": settings.jwt_expire_minutes * 60
    }

@app.post("/refresh", response_model=Token)
async def refresh_access_token(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, settings.jwt_refresh_secret, algorithms=[settings.jwt_algorithm])
        
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Token inválido (no es refresh)")
            
        jti = payload.get("jti")
        if jti not in refresh_tokens_db:
             raise HTTPException(status_code=401, detail="Refresh token no encontrado")
             
        if refresh_tokens_db[jti]["revocado"]:
            raise HTTPException(status_code=401, detail="Refresh token revocado")
            
        usuario_id = payload["sub"]
        # En una app real, verificaríamos que el usuario aún existe y está activo
        user = fake_users_db.get(usuario_id)
        if not user:
             raise HTTPException(status_code=401, detail="Usuario no encontrado")

        # Rotación de refresh token (opcional pero recomendado): revocar el anterior y dar uno nuevo
        refresh_tokens_db[jti]["revocado"] = True
        
        new_access_token = crear_token(user["id"], user["role"], timedelta(minutes=settings.jwt_expire_minutes))
        new_refresh_token = crear_refresh_token(user["id"])
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.jwt_expire_minutes * 60
        }
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Refresh token inválido")

@app.post("/logout")
async def logout(request: RefreshTokenRequest):
    try:
        payload = jwt.decode(request.refresh_token, settings.jwt_refresh_secret, algorithms=[settings.jwt_algorithm])
        jti = payload.get("jti")
        if jti in refresh_tokens_db:
            refresh_tokens_db[jti]["revocado"] = True
        return {"message": "Logout exitoso"}
    except:
        return {"message": "Logout procesado (token inválido o ya expirado)"}

@app.get("/health", tags=["General"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a EcoMarket Auth API",
        "docs": "http://localhost:8000/docs",
        "login": "http://localhost:8000/login"
    }

# --- Endpoints Protegidos ---

@app.get("/productos")
async def listar_productos(token_payload: dict = Depends(verificar_jwt)):
    # Endpoint protegido, accesible para cualquier usuario autenticado
    return [
        {"id": 1, "nombre": "Laptop Eco", "precio": 1200},
        {"id": 2, "nombre": "Mouse Solar", "precio": 25}
    ]

@app.post("/productos")
async def crear_producto(producto: dict, token_payload: dict = Depends(verificar_jwt)):
    # Endpoint protegido, solo para admins
    if token_payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    
    return {"message": "Producto creado", "producto": producto, "creado_por": token_payload["sub"]}

@app.get("/users/me")
async def read_users_me(token_payload: dict = Depends(verificar_jwt)):
    user_id = token_payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en token")
        
    user = fake_users_db.get(str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"id": user["id"], "email": user["email"], "role": user["role"]}

if __name__ == "__main__":
    import uvicorn
    
    # Configuración HTTPS para desarrollo local
    ssl_key = "./certs/server.key"
    ssl_cert = "./certs/server.crt"
    
    if os.path.exists(ssl_key) and os.path.exists(ssl_cert) and os.getenv("USE_HTTPS_DEV") == "true":
        print("SECURE: Iniciando Auth Service en modo HTTPS (Puerto 8444)")
        uvicorn.run(app, host="0.0.0.0", port=8444, ssl_keyfile=ssl_key, ssl_certfile=ssl_cert)
    else:
        print("INSECURE: Iniciando Auth Service en modo HTTP (Puerto 8002)")
        # Ejecutamos en el puerto 8002 para evitar conflictos con la API de Sucursal (8001)
        uvicorn.run(app, host="0.0.0.0", port=8002)