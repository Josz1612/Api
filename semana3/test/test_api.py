# tests/test_api.py
import pytest
from typing import Any, cast
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, MagicMock
from api.main import app, get_tcp_client, get_config
from core.exceptions import ConnectionTimeoutError, MessageTooLongError

@pytest.mark.asyncio
class TestEchoAPI:
    
    async def test_successful_echo_endpoint(self):
        """Test endpoint /echo exitoso"""
        mock_client = AsyncMock()
        mock_client.echo.return_value = "hello world"
        
        mock_config = MagicMock()
        mock_config.get.return_value = "127.0.0.1"
        mock_config.get_int.return_value = 5000
        
        app.dependency_overrides[get_tcp_client] = lambda: mock_client
        app.dependency_overrides[get_config] = lambda: mock_config
        
        try:
            async with AsyncClient(transport=ASGITransport(app=cast(Any, app)), base_url="http://test") as client:
                response = await client.post("/echo", json={
                    "message": "hello world",
                    "timeout": 5.0
                })
                
                assert response.status_code == 200
                data = response.json()
                assert data["echoed"] == "hello world"
                assert data["message_length"] == 11
                assert data["success"] is True
        finally:
            app.dependency_overrides = {}
    
    async def test_echo_timeout_error(self):
        """Test manejo de timeout en API"""
        mock_client = AsyncMock()
        mock_client.echo.side_effect = ConnectionTimeoutError("Timeout")
        
        mock_config = MagicMock()
        mock_config.get.return_value = "127.0.0.1"
        mock_config.get_int.return_value = 5000
        
        app.dependency_overrides[get_tcp_client] = lambda: mock_client
        app.dependency_overrides[get_config] = lambda: mock_config
        
        try:
            async with AsyncClient(transport=ASGITransport(app=cast(Any, app)), base_url="http://test") as client:
                response = await client.post("/echo", json={
                    "message": "test",
                    "timeout": 1.0
                })
                
                assert response.status_code == 408
                data = response.json()["detail"]
                assert data["error"] == "timeout"
                assert data["success"] is False
        finally:
            app.dependency_overrides = {}
    
    async def test_echo_message_too_long(self):
        """Test mensaje demasiado largo"""
        mock_client = AsyncMock()
        mock_client.echo.side_effect = MessageTooLongError("Too long")
        
        mock_config = MagicMock()
        mock_config.get.return_value = "127.0.0.1"
        mock_config.get_int.return_value = 5000
        
        app.dependency_overrides[get_tcp_client] = lambda: mock_client
        app.dependency_overrides[get_config] = lambda: mock_config
        
        try:
            async with AsyncClient(transport=ASGITransport(app=cast(Any, app)), base_url="http://test") as client:
                response = await client.post("/echo", json={
                    "message": "test message",
                    "timeout": 5.0
                })
                
                assert response.status_code == 400
                data = response.json()["detail"]
                assert data["error"] == "message_too_long"
        finally:
            app.dependency_overrides = {}
    
    async def test_health_endpoint(self):
        """Test endpoint de salud"""
        async with AsyncClient(transport=ASGITransport(app=cast(Any, app)), base_url="http://test") as client:
            response = await client.get("/health")
            
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    async def test_config_endpoint(self):
        """Test endpoint de configuración"""
        mock_config = MagicMock()
        mock_config.get.return_value = "127.0.0.1"
        mock_config.get_int.return_value = 5000
        
        app.dependency_overrides[get_config] = lambda: mock_config
        
        try:
            async with AsyncClient(transport=ASGITransport(app=cast(Any, app)), base_url="http://test") as client:
                response = await client.get("/config")
                
                assert response.status_code == 200
                data = response.json()
                assert "echo_host" in data
                assert "echo_port" in data
        finally:
            app.dependency_overrides = {}

# Ejecutar con: pytest tests/test_api.py -v