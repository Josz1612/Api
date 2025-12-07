# tests/conftest.py
import pytest
import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock
from core.container import DIContainer
from core.contracts import ITcpEchoClient, IConfigService
from core.config import ConfigService

# Configurar logging para tests
logging.basicConfig(level=logging.DEBUG)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_config():
    """Mock de configuración para tests"""
    config = MagicMock(spec=IConfigService)
    config.get.side_effect = lambda key, default=None: {
        "ECHO_HOST": "127.0.0.1",
        "ECHO_PORT": "5000",
        "TIMEOUT_SECONDS": "5.0",
        "MAX_MESSAGE_LENGTH": "1024"
    }.get(key, default)
    config.get_int.side_effect = lambda key, default=0: int(config.get(key, str(default)))
    config.get_float.side_effect = lambda key, default=0.0: float(config.get(key, str(default)))
    return config

@pytest.fixture
def container_with_mocks(mock_config):
    """Contenedor DI con mocks para testing"""
    container = DIContainer()
    container.register_singleton(IConfigService, mock_config)
    return container