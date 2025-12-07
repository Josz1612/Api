# Guía de Integración: Seguridad en EcoMarket

Esta guía explica cómo integrar el **Servicio de Autenticación (Semana 8)** con los servicios existentes (como la **Central API de la Semana 3**).

## Arquitectura Objetivo

*   **Auth Service (Puerto 8001)**: Emite tokens JWT.
*   **Resource Service (Puerto 8000)**: Valida tokens antes de dar acceso a datos.

## Paso 1: Preparar el Servicio de Autenticación

Edita `Semana8/app.py` para que corra en un puerto diferente (ej. 8001) para no chocar con la API Central.

```python
# Al final de Semana8/app.py
if __name__ == "__main__":
    import uvicorn
    # Cambiar puerto a 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

## Paso 2: Proteger la API Central (Semana 3)

Debes modificar `Semana3/central_api.py` agregando la validación de tokens.

### 2.1. Agregar Importaciones
```python
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
```

### 2.2. Configurar la Seguridad (Misma Clave Secreta)
Copia esto en `central_api.py`. Es CRÍTICO que la `SECRET_KEY` sea la misma que en `Semana8/app.py`.

```python
# Configuración de Seguridad
SECRET_KEY = "secreto_super_seguro_para_desarrollo" # ¡DEBE SER IGUAL AL DE SEMANA 8!
ALGORITHM = "HS256"

# Indica dónde obtener el token (apunta al servicio de auth)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8001/login")

async def validar_token_central(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience="ecomarket-api")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

### 2.3. Proteger Endpoints Críticos
Agrega la dependencia `validar_token_central` a los endpoints que quieras proteger (ej. crear o borrar productos).

```python
# Ejemplo: Proteger la creación de productos
@app.post("/products", response_model=Product, tags=["Inventario"])
async def create_product(
    product: Product, 
    token_data: dict = Depends(validar_token_central) # <--- ESTO PROTEGE EL ENDPOINT
):
    # Opcional: Verificar rol de admin
    if token_data.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
        
    # ... resto del código original ...
```

## Paso 3: Flujo de Prueba Completo

1.  **Iniciar Auth Service**: `python Semana8/app.py` (en puerto 8001).
2.  **Iniciar Central API**: `python Semana3/central_api.py` (en puerto 8000).
3.  **Obtener Token**:
    ```bash
    curl -X POST http://localhost:8001/login -d '{"email":"admin@ecomarket.com", "password":"password123"}'
    ```
4.  **Usar Token en Central API**:
    ```bash
    curl -X POST http://localhost:8000/products \
         -H "Authorization: Bearer <TU_TOKEN>" \
         -d '{"id": 99, "name": "Producto Seguro", "price": 100, "stock": 10}'
    ```