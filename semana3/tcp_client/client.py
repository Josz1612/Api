import asyncio
import logging
from typing import Optional
from core.contracts import ITcpEchoClient, IConfigService
from core.exceptions import ConnectionTimeoutError, MessageTooLongError
from core.container import container

class TcpEchoClient(ITcpEchoClient):
    def __init__(self, config: Optional[IConfigService] = None):
        self.config = config or container.get(IConfigService)
        self.logger = logging.getLogger(__name__)
        self.max_message_length = self.config.get_int("MAX_MESSAGE_LENGTH", 1024)
    
    async def echo(self, host: str, port: int, message: str, timeout: float = 5.0) -> str:
        if len(message.encode('utf-8')) > self.max_message_length:
            raise MessageTooLongError(f"Message too long: {len(message)} bytes")
        
        self.logger.info("Connecting to %s:%d", host, port)
        
        writer = None
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), 
                timeout=timeout
            )
            
            # Enviar mensaje
            writer.write(message.encode('utf-8'))
            await writer.drain()
            
            # Leer respuesta con timeout
            data = await asyncio.wait_for(
                reader.read(1024), 
                timeout=timeout
            )
            
            response = data.decode('utf-8')
            self.logger.info("Received echo: %s", response[:50] + "..." if len(response) > 50 else response)
            
            return response
            
        except asyncio.TimeoutError:
            self.logger.error("Connection timeout to %s:%d after %fs", host, port, timeout)
            raise ConnectionTimeoutError(f"Timeout connecting to {host}:{port}")
        except ConnectionRefusedError:
            self.logger.error("Connection refused by %s:%d", host, port)
            raise
        except Exception as e:
            self.logger.error("Unexpected error: %s", str(e))
            raise
        finally:
            if writer:
                writer.close()
                await writer.wait_closed()

# CLI con DI
if __name__ == "__main__":
    import sys
    from core.config import ConfigService
    from core.logging_config import setup_logging
    from core.contracts import IConfigService
    
    setup_logging()
    container.register_singleton(IConfigService, ConfigService())
    
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
    msg = sys.argv[3] if len(sys.argv) > 3 else "hola"
    
    client = TcpEchoClient()
    echo = asyncio.run(client.echo(host, port, msg))
    print(f"[CLI] Echo: {echo}")