# 📘 Semana 8: Autenticación y Autorización con JWT

## 🎯 Objetivos de la Semana

- ✅ Implementar autenticación con JWT
- ✅ Sistema de roles y permisos
- ✅ Protección de endpoints sensibles
- ✅ Refresh tokens
- ✅ Demostración visual interactiva

## 📂 Archivos Principales

- `semana8_jwt/` - Módulo de autenticación
- `main.py` - Endpoints de auth integrados
- `semana 8.html` - Guía de JWT
- `config.py` - Configuración de secrets

## 🔐 Arquitectura de Seguridad

```
┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │ 1. Login (user/pass)
       ▼
┌─────────────┐
│     API     │───▶ Valida credenciales
└──────┬──────┘
       │ 2. Retorna JWT
       ▼
┌─────────────┐
│   Cliente   │───▶ Guarda token
└──────┬──────┘
       │ 3. Request + JWT en header
       ▼
┌─────────────┐
│     API     │───▶ Valida JWT + verifica rol
└──────┬──────┘
       │ 4. Response (si autorizado)
       ▼
┌─────────────┐
│   Cliente   │
└─────────────┘
```

## 🔑 Sistema de JWT

### Estructura del Token

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "usuario123",
    "role": "admin",
    "exp": 1733328000,
    "iat": 1733324400
  },
  "signature": "..."
}
```

### Generación de Token

```python
import jwt
from datetime import datetime, timedelta
from config import get_settings

settings = get_settings()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_refresh_secret,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
```

## 👥 Sistema de Roles

### Roles Implementados

| Rol | Permisos |
|-----|----------|
| **admin** | ✅ Todo: crear, leer, actualizar, eliminar productos |
| **vendedor** | ✅ Crear y leer productos<br>❌ Eliminar productos |
| **cliente** | ✅ Solo leer productos y comprar<br>❌ Crear/editar/eliminar |

### Base de Datos de Usuarios

```python
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # En producción: hash con bcrypt
        "role": "admin",
        "email": "admin@ecomarket.com"
    },
    "vendedor": {
        "username": "vendedor",
        "password": "vend123",
        "role": "vendedor",
        "email": "vendedor@ecomarket.com"
    },
    "cliente": {
        "username": "cliente",
        "password": "cli123",
        "role": "cliente",
        "email": "cliente@ecomarket.com"
    }
}
```

## 🔌 Endpoints de Autenticación

### 1. Login
```python
@app.post("/api/auth/login")
async def login(credentials: LoginCredentials):
    """
    Autenticar usuario y retornar tokens
    """
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    access_token = create_access_token({"sub": user.username, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "username": user.username,
            "role": user.role,
            "email": user.email
        }
    }
```

### 2. Refresh Token
```python
@app.post("/api/auth/refresh")
async def refresh(refresh_token: str):
    """
    Generar nuevo access token usando refresh token
    """
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_refresh_secret,
            algorithms=[settings.jwt_algorithm]
        )
        username = payload.get("sub")
        user = get_user(username)
        
        new_access_token = create_access_token({
            "sub": user.username,
            "role": user.role
        })
        
        return {"access_token": new_access_token}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
```

### 3. Logout
```python
@app.post("/api/auth/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    """
    Invalidar token (agregar a blacklist)
    """
    # En producción: agregar token a Redis blacklist
    blacklist.add(token)
    return {"message": "Logout exitoso"}
```

## 🛡️ Protección de Endpoints

### Dependency de Autenticación

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extraer y validar usuario desde JWT
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )
        username: str = payload.get("sub")
        role: str = payload.get("role")
        
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        return {"username": username, "role": role}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar el token")
```

### Verificación de Roles

```python
def require_role(required_role: str):
    """
    Decorator para verificar rol específico
    """
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Se requiere rol '{required_role}'"
            )
        return current_user
    return role_checker

def require_any_role(allowed_roles: list):
    """
    Verificar si usuario tiene alguno de los roles permitidos
    """
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Se requiere uno de estos roles: {allowed_roles}"
            )
        return current_user
    return role_checker
```

### Endpoints Protegidos

```python
# Solo admin puede crear productos
@app.post("/api/productos", dependencies=[Depends(require_role("admin"))])
async def crear_producto(producto: ProductoInput):
    # ...
    pass

# Admin y vendedor pueden ver todos los productos
@app.get("/api/productos", dependencies=[Depends(require_any_role(["admin", "vendedor"]))])
async def listar_productos():
    # ...
    pass

# Cualquier usuario autenticado puede ver su perfil
@app.get("/api/perfil")
async def ver_perfil(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}
```

## 🎨 Demostración Visual Interactiva

### Página `/jwt-demo`

Características de la demo:
- 🎮 **Selección de Usuario**: admin, vendedor, cliente
- 🔐 **Login Visual**: Muestra el token generado
- 📊 **Decodificación JWT**: Visualiza payload del token
- 🔒 **Prueba de Endpoints**: Intenta crear producto con diferentes roles
- ❌ **Visualización de Errores**: Muestra error 403 para cliente

```html
<div class="jwt-demo">
    <h2>🔐 Demostración JWT</h2>
    
    <!-- Seleccionar usuario -->
    <select id="userSelect">
        <option value="admin">Admin (puede crear productos)</option>
        <option value="vendedor">Vendedor (puede crear productos)</option>
        <option value="cliente">Cliente (NO puede crear)</option>
    </select>
    
    <!-- Login -->
    <button onclick="loginDemo()">🔑 Login</button>
    
    <!-- Mostrar token -->
    <div id="tokenDisplay" style="display:none;">
        <h3>Token JWT:</h3>
        <pre id="tokenValue"></pre>
        <h3>Payload Decodificado:</h3>
        <pre id="tokenPayload"></pre>
    </div>
    
    <!-- Probar crear producto -->
    <button onclick="crearProductoDemo()">➕ Intentar Crear Producto</button>
    
    <!-- Resultado -->
    <div id="resultado"></div>
</div>

<script>
let currentToken = null;

async function loginDemo() {
    const user = document.getElementById('userSelect').value;
    
    const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: user,
            password: user + '123'
        })
    });
    
    const data = await response.json();
    currentToken = data.access_token;
    
    // Mostrar token
    document.getElementById('tokenValue').textContent = currentToken;
    
    // Decodificar y mostrar payload
    const payload = JSON.parse(atob(currentToken.split('.')[1]));
    document.getElementById('tokenPayload').textContent = JSON.stringify(payload, null, 2);
    
    document.getElementById('tokenDisplay').style.display = 'block';
}

async function crearProductoDemo() {
    if (!currentToken) {
        alert('Primero debes hacer login');
        return;
    }
    
    const response = await fetch('/api/productos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${currentToken}`
        },
        body: JSON.stringify({
            nombre: 'Producto de Prueba',
            categoria: 'Test',
            precio: 10.0,
            stock: 100
        })
    });
    
    const resultado = document.getElementById('resultado');
    
    if (response.ok) {
        resultado.innerHTML = `
            <div class="success">
                ✅ ¡Producto creado exitosamente!
                <p>Tu rol tiene permisos suficientes.</p>
            </div>
        `;
    } else {
        const error = await response.json();
        resultado.innerHTML = `
            <div class="error">
                ❌ Error ${response.status}: ${error.detail}
                <p>Tu rol NO tiene permisos para crear productos.</p>
                <p><strong>¡Así funciona JWT!</strong></p>
            </div>
        `;
    }
}
</script>
```

## ✨ Características Implementadas

- ✅ JWT con HS256
- ✅ Access tokens (30 min)
- ✅ Refresh tokens (7 días)
- ✅ Sistema de roles (admin, vendedor, cliente)
- ✅ Protección por rol de endpoints
- ✅ Demo visual interactiva
- ✅ Manejo de tokens expirados
- ✅ Logout con blacklist

## 🔒 Seguridad

### Mejores Prácticas Implementadas

1. ✅ **Secrets en variables de entorno** (.env)
2. ✅ **JWT_SECRET de 32+ caracteres**
3. ✅ **Algoritmo HS256** (simétrico, rápido)
4. ✅ **Tokens con expiración**
5. ✅ **Refresh tokens separados**
6. ✅ **Validación de roles en servidor**

### Pendientes para Producción

- ⏳ Hash de passwords con bcrypt
- ⏳ Rate limiting en /login
- ⏳ Blacklist de tokens en Redis
- ⏳ HTTPS obligatorio
- ⏳ CORS restrictivo
- ⏳ Rotación de secrets

## 🚀 Cómo Probar

### 1. Configurar Secrets
```bash
# Crear .env
echo "JWT_SECRET=$(openssl rand -hex 32)" > .env
echo "JWT_REFRESH_SECRET=$(openssl rand -hex 32)" >> .env
echo "JWT_ALGORITHM=HS256" >> .env
echo "JWT_EXPIRE_MINUTES=30" >> .env
```

### 2. Ejecutar API
```bash
python main.py
```

### 3. Probar Demo Visual
```
http://localhost:8000/jwt-demo
```

### 4. Probar con cURL

```bash
# Login como admin
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Guardar token
TOKEN="eyJhbGc..."

# Crear producto (exitoso con admin)
curl -X POST http://localhost:8000/api/productos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":"Test","precio":10,"stock":100}'

# Login como cliente
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"cliente","password":"cli123"}'

# Intentar crear producto (fallará con 403)
curl -X POST http://localhost:8000/api/productos \
  -H "Authorization: Bearer $CLIENTE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","categoria":"Test","precio":10,"stock":100}'
```

## 🎓 Conceptos Clave

- **JWT**: JSON Web Token para autenticación stateless
- **Bearer Token**: Token enviado en header Authorization
- **Claims**: Datos dentro del JWT (sub, role, exp, etc.)
- **Signature**: Garantiza que el token no fue modificado
- **Access Token**: Token de corta duración para acceso
- **Refresh Token**: Token de larga duración para renovar access
- **Role-Based Access Control (RBAC)**: Permisos basados en roles

## 📈 Flujo Completo

```
1. Usuario → Login (username + password)
2. API → Valida credenciales
3. API → Genera access_token + refresh_token
4. Usuario → Guarda tokens (localStorage/cookie)
5. Usuario → Request con Authorization: Bearer <token>
6. API → Valida token y extrae rol
7. API → Verifica permisos del rol
8. API → Response (200 OK o 403 Forbidden)
9. Token expira → Usuario usa refresh_token
10. API → Genera nuevo access_token
```
