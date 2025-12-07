# core/logging_config.py
import logging
import logging.config
import json
import os
from typing import Dict, Any

def setup_logging(config_path: str = "config/logging.json") -> None:
    """Configura el sistema de logging de la aplicación"""
    
    # Configuración por defecto si no existe el archivo
    default_config = {
        "version": 1,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
            },
            "simple": {
                "format": "%(levelname)s - %(message)s"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file": {
                "class": "logging.FileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": "app.log",
                "mode": "a"
            }
        },
        "loggers": {
            "tcp_server": {"level": "DEBUG"},
            "tcp_client": {"level": "DEBUG"},
            "api": {"level": "INFO"}
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file"]
        }
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = default_config
        # Crear directorio config si no existe
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    logging.config.dictConfig(config)