# tests/test_tcp.py
import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from tcp_client.client import TcpEchoClient
from core.exceptions import ConnectionTimeoutError, MessageTooLongError

@pytest.mark.asyncio
class TestTcpEchoClient:
    
    async def test_successful_echo(self, mock_config):
        """Test eco exitoso"""
        client = TcpEchoClient(mock_config)
        
        # Mock asyncio.open_connection
        mock_reader = AsyncMock()
        mock_writer = AsyncMock()
        mock_reader.read.return_value = b"hello"
        
        with patch('asyncio.open_connection', return_value=(mock_reader, mock_writer)):
            with patch('asyncio.wait_for', side_effect=[
                (mock_reader, mock_writer),  # Primera llamada (conexión)
                b"hello"  # Segunda llamada (lectura)
            ]):
                result = await client.echo("127.0.0.1", 5000, "hello")
                
                assert result == "hello"
                mock_writer.write.assert_called_once_with(b"hello")
                mock_writer.drain.assert_called_once()
    
    async def test_connection_timeout(self, mock_config):
        """Test timeout de conexión"""
        client = TcpEchoClient(mock_config)
        
        with patch('asyncio.wait_for', side_effect=asyncio.TimeoutError()):
            with pytest.raises(ConnectionTimeoutError):
                await client.echo("127.0.0.1", 5000, "hello", timeout=1.0)
    
    async def test_message_too_long(self, mock_config):
        """Test mensaje demasiado largo"""
        mock_config.get_int.return_value = 10  # Límite muy bajo
        client = TcpEchoClient(mock_config)
        
        with pytest.raises(MessageTooLongError):
            await client.echo("127.0.0.1", 5000, "mensaje muy largo", timeout=1.0)
    
    async def test_connection_refused(self, mock_config):
        """Test servidor no disponible"""
        client = TcpEchoClient(mock_config)
        
        with patch('asyncio.wait_for', side_effect=ConnectionRefusedError()):
            with pytest.raises(ConnectionRefusedError):
                await client.echo("127.0.0.1", 5000, "hello")
    
    async def test_cleanup_on_error(self, mock_config):
        """Test que se cierre la conexión aún con error"""
        client = TcpEchoClient(mock_config)
        
        mock_reader = AsyncMock()
        mock_writer = AsyncMock()
        
        with patch('asyncio.open_connection', return_value=(mock_reader, mock_writer)):
            with patch('asyncio.wait_for', side_effect=[
                (mock_reader, mock_writer),  # Conexión exitosa
                Exception("Error de prueba")  # Error en lectura
            ]):
                with pytest.raises(Exception):
                    await client.echo("127.0.0.1", 5000, "hello")
                
                # Verificar que se cerró la conexión
                mock_writer.close.assert_called_once()
                mock_writer.wait_closed.assert_called_once()