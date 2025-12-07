# core/config.py
import os
from typing import Optional
from .contracts import IConfigService

class ConfigService(IConfigService):
    """Servicio de configuración que lee de variables de entorno"""
    
    def __init__(self):
        self._defaults = {
            "ECHO_HOST": "127.0.0.1",
            "ECHO_PORT": "5000",
            "UDP_PORT": "5001",
            "API_PORT": "8000",
            "TIMEOUT_SECONDS": "5.0",
            "MAX_MESSAGE_LENGTH": "1024"
        }
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return os.getenv(key, default or self._defaults.get(key))
    
    def get_int(self, key: str, default: int = 0) -> int:
        value = self.get(key, str(default))
        return int(value) if value else default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        value = self.get(key, str(default))
        return float(value) if value else default