import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

load_dotenv()

class Settings(BaseSettings):
    # Base de datos
    database_url: str # URL de conexión completa requerida
    
    # JWT
    jwt_secret: str
    jwt_refresh_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Entorno
    environment: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Validación al importar
try:
    settings = get_settings()
    
    # Verificación explícita
    if len(settings.jwt_secret) < 32:
        raise ValueError("JWT_SECRET debe tener al menos 32 caracteres")
    if settings.jwt_secret == settings.jwt_refresh_secret:
        raise ValueError("JWT_SECRET y JWT_REFRESH_SECRET deben ser diferentes")
except Exception as e:
    print(f"Error cargando configuración: {e}")
    # For development, we might want to allow it to fail, but for now let's re-raise
    raise e