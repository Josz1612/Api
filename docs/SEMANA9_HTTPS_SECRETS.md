# 📘 Semana 9: HTTPS/TLS y Gestión de Secrets

## 🎯 Objetivos de la Semana

- ✅ Implementar HTTPS con certificados SSL/TLS
- ✅ Gestión segura de secrets con pydantic-settings
- ✅ Configuración de entorno (development/production)
- ✅ Generación de certificados autofirmados
- ✅ Redirección HTTP → HTTPS

## 📂 Archivos Principales

- `config.py` - Gestión centralizada de configuración
- `generar_certificados.py` - Script para generar certificados SSL
- `certs/` - Directorio con certificados (cert.pem, key.pem)
- `.env` - Variables de entorno (NO versionar)
- `.env.example` - Plantilla de variables
- `SEMANA9_COMPLETADA.md` - Documentación detallada
- `semana9.html` - Guía oficial

## 🔐 Arquitectura de Seguridad

```
┌──────────────┐
│   Cliente    │
└──────┬───────┘
       │ HTTP request
       ▼
┌──────────────┐
│ Middleware   │ ─────▶ Redirect a HTTPS
└──────┬───────┘
       │ HTTPS request
       ▼
┌──────────────┐
│     API      │ ─────▶ Valida certificado
│   (Port      │        Lee secrets de .env
│    8443)     │
└──────────────┘
```

## 🔒 Certificados SSL/TLS

### Generación de Certificados

```python
# generar_certificados.py
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta
import os

def generar_certificados():
    """
    Genera certificados autofirmados para desarrollo
    RSA 4096 bits, válido por 365 días
    """
    # Generar clave privada RSA
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    
    # Crear certificado
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "MX"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CDMX"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Ciudad de Mexico"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "EcoMarket"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
            x509.DNSName("127.0.0.1"),
            x509.DNSName("ecomarket.local"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Guardar certificados
    os.makedirs("certs", exist_ok=True)
    
    # Guardar clave privada
    with open("certs/key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Guardar certificado público
    with open("certs/cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print("✅ Certificados generados exitosamente")
    print("   📄 certs/cert.pem (certificado público)")
    print("   🔑 certs/key.pem (clave privada)")
```

### Características del Certificado

- **Algoritmo**: RSA 4096 bits
- **Hash**: SHA-256
- **Validez**: 365 días
- **SANs**: localhost, 127.0.0.1, ecomarket.local
- **Uso**: Desarrollo (autofirmado)

## ⚙️ Gestión de Configuración con Pydantic

### config.py

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import Literal

class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación
    Lee automáticamente desde:
    1. Variables de entorno del sistema
    2. Archivo .env
    """
    
    # JWT Configuration
    jwt_secret: str
    jwt_refresh_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Application
    environment: Literal["development", "production"] = "development"
    debug: bool = True
    
    # Database (opcional)
    database_url: str | None = None
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8443
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_secrets()
    
    def _validate_secrets(self):
        """Validaciones de seguridad"""
        if len(self.jwt_secret) < 32:
            raise ValueError("JWT_SECRET debe tener al menos 32 caracteres")
        
        if self.jwt_secret == self.jwt_refresh_secret:
            raise ValueError("JWT_SECRET y JWT_REFRESH_SECRET deben ser diferentes")
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

@lru_cache()
def get_settings() -> Settings:
    """
    Singleton: Una sola instancia de Settings
    Cachea la configuración en memoria
    """
    return Settings()
```

### Archivo .env

```bash
# .env (NO versionar en Git)

# JWT Secrets (generar con: openssl rand -hex 32)
JWT_SECRET=a7f2c9e1b4d8f3e6c9a2d5e8f1b4c7d0e3f6a9b2c5d8e1f4a7b0c3d6e9f2a5b8
JWT_REFRESH_SECRET=f5e8d1c4b7a0e3f6d9c2b5a8e1d4c7b0f3e6d9c2b5a8e1d4c7b0f3e6d9c2b5a8
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# Database (opcional)
# DATABASE_URL=postgresql://user:pass@localhost:5432/ecomarket

# Server
HOST=0.0.0.0
PORT=8443
```

### Archivo .env.example

```bash
# .env.example (SÍ versionar en Git)
# Plantilla para crear .env

# JWT Secrets - GENERAR NUEVOS CON: openssl rand -hex 32
JWT_SECRET=your_secret_here_min_32_chars
JWT_REFRESH_SECRET=different_secret_here_min_32_chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=development
DEBUG=true

# Database (opcional)
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname

# Server
HOST=0.0.0.0
PORT=8443
```

## 🚀 Configuración del Servidor HTTPS

### main.py - Inicio con SSL

```python
import uvicorn
from config import get_settings
import os

settings = get_settings()

if __name__ == "__main__":
    # Verificar si existen certificados
    cert_exists = os.path.exists("certs/cert.pem") and os.path.exists("certs/key.pem")
    
    if cert_exists:
        print("=" * 70)
        print("🔒 Iniciando EcoMarket API con HTTPS (TLS/SSL)")
        print("=" * 70)
        print(f"📍 URL: https://localhost:{settings.port}")
        print(f"📄 Documentación: https://localhost:{settings.port}/docs")
        print(f"🔐 Certificado: certs/cert.pem")
        print("⚠️  Advertencia: Certificado autofirmado (solo desarrollo)")
        print("   Los navegadores mostrarán advertencia - es normal")
        print("=" * 70)
        
        uvicorn.run(
            "main:app",
            host=settings.host,
            port=settings.port,
            ssl_keyfile="./certs/key.pem",
            ssl_certfile="./certs/cert.pem",
            reload=settings.debug
        )
    else:
        print("⚠️  Certificados no encontrados. Generando...")
        from generar_certificados import generar_certificados
        generar_certificados()
        print("\n✅ Certificados creados. Ejecuta nuevamente para iniciar con HTTPS")
```

## 🔄 Middleware de Redirección HTTP → HTTPS

```python
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from config import get_settings

settings = get_settings()

# Solo en producción
if settings.is_production:
    app.add_middleware(HTTPSRedirectMiddleware)
```

### Comportamiento

- **Development**: Permite HTTP y HTTPS
- **Production**: Redirige automáticamente HTTP → HTTPS

## 📊 Panel Visual de Seguridad

### Homepage con Indicadores de Seguridad

```html
<div class="security-panel">
    <h2>🔒 Estado de Seguridad</h2>
    
    <div class="security-item">
        <span class="icon">✅</span>
        <span class="label">HTTPS/TLS Activo</span>
        <span class="value">Puerto 8443</span>
    </div>
    
    <div class="security-item">
        <span class="icon">✅</span>
        <span class="label">JWT Configurado</span>
        <span class="value">HS256</span>
    </div>
    
    <div class="security-item">
        <span class="icon">✅</span>
        <span class="label">Secrets Protegidos</span>
        <span class="value">.env</span>
    </div>
    
    <div class="security-item">
        <span class="icon">✅</span>
        <span class="label">Certificado</span>
        <span class="value">RSA 4096</span>
    </div>
</div>

<script>
async function verificarSeguridad() {
    const response = await fetch('/api/security-status');
    const data = await response.json();
    
    console.log('🔒 Estado de Seguridad:', data);
    // {
    //   "https_enabled": true,
    //   "jwt_configured": true,
    //   "environment": "development",
    //   "certificate": {
    //     "exists": true,
    //     "algorithm": "RSA",
    //     "bits": 4096,
    //     "valid_until": "2025-12-04"
    //   }
    // }
}
</script>
```

## ✨ Características Implementadas

- ✅ HTTPS con certificados SSL/TLS
- ✅ Generación automática de certificados
- ✅ Configuración con pydantic-settings
- ✅ Secrets en .env (no versionados)
- ✅ Validación de secrets (longitud, diferencia)
- ✅ Redirección HTTP → HTTPS (producción)
- ✅ Panel visual de seguridad
- ✅ Singleton pattern para config
- ✅ Type hints completos

## 🔧 Setup Inicial

```bash
# 1. Instalar dependencias
pip install pydantic-settings cryptography

# 2. Crear archivo .env desde plantilla
cp .env.example .env

# 3. Generar secrets
echo "JWT_SECRET=$(openssl rand -hex 32)" >> .env
echo "JWT_REFRESH_SECRET=$(openssl rand -hex 32)" >> .env

# 4. Generar certificados
python generar_certificados.py

# 5. Ejecutar API con HTTPS
python main.py

# 6. Acceder
# https://localhost:8443
```

## 🔒 Seguridad en Producción

### Checklist

- ✅ Usar certificados de CA confiable (Let's Encrypt)
- ✅ JWT_SECRET de 64+ caracteres
- ✅ Environment=production
- ✅ Debug=false
- ✅ Secrets en secrets manager (AWS Secrets Manager, Azure Key Vault)
- ✅ Firewall configurado (solo 443)
- ✅ Rate limiting
- ✅ CORS restrictivo

### Obtener Certificado Let's Encrypt

```bash
# Usando certbot
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com

# Certificados en:
# /etc/letsencrypt/live/yourdomain.com/fullchain.pem
# /etc/letsencrypt/live/yourdomain.com/privkey.pem
```

## 🎓 Conceptos Clave

- **HTTPS**: HTTP sobre TLS/SSL (encriptación)
- **SSL/TLS**: Protocolos de seguridad en capa de transporte
- **Certificado**: Archivo que prueba identidad del servidor
- **CA**: Certificate Authority (autoridad certificadora)
- **Self-Signed**: Certificado autofirmado (desarrollo)
- **Secrets Management**: Gestión segura de credenciales
- **Environment Variables**: Variables de configuración del sistema

## 📈 Comparación HTTP vs HTTPS

| Característica | HTTP | HTTPS |
|---------------|------|-------|
| Encriptación | ❌ No | ✅ Sí (TLS) |
| Puerto | 80 | 443 |
| Integridad | ❌ No | ✅ Sí |
| Autenticación | ❌ No | ✅ Sí |
| SEO | 🔴 Penalizado | 🟢 Favorecido |
| Confianza | 🔴 Baja | 🟢 Alta |

## 🐛 Troubleshooting

### Certificado no confiable en navegador

**Normal en desarrollo (autofirmado)**

Soluciones:
1. Click en "Avanzado" → "Continuar de todas formas"
2. Agregar certificado a confiables del sistema
3. Usar `curl -k` (inseguro, solo desarrollo)

### Error "JWT_SECRET muy corto"

```bash
# Generar secret de 32+ caracteres
openssl rand -hex 32
```

### Error "No se puede leer .env"

```bash
# Verificar que existe
ls -la .env

# Verificar permisos
chmod 600 .env

# Verificar contenido
cat .env
```

### Puerto 8443 en uso

```bash
# Windows
netstat -ano | findstr :8443
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8443
kill -9 <PID>
```

## 📝 Mejores Prácticas

1. **NUNCA versionar .env** en Git (.gitignore)
2. **Rotar secrets** periódicamente
3. **Usar secrets manager** en producción
4. **Certificados de CA** en producción (Let's Encrypt gratis)
5. **HSTS header** para forzar HTTPS
6. **Auditar configuración** regularmente
7. **Logging de accesos** a secrets

## 🚀 Próximos Pasos

- 🔄 Renovación automática de certificados
- 📊 Monitoring de certificados (expiración)
- 🔐 Mutual TLS (mTLS)
- 🌐 CDN con SSL (Cloudflare, etc.)
- 📦 Secrets rotation automática
- 🔍 Auditoría de seguridad
