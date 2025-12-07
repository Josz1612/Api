# tcp_server/server.py
import asyncio
import logging
import signal
from typing import Optional, Set
from core.contracts import ITcpEchoServer, IConfigService
from core.container import container

class TcpEchoServer(ITcpEchoServer):
    def __init__(self, config: Optional[IConfigService] = None):
        self.config = config or container.get(IConfigService)
        self.logger = logging.getLogger(__name__)
        self.active_connections: Set[asyncio.Task] = set()
        self.shutdown_event = asyncio.Event()
    
    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info('peername')
        self.logger.info("New connection from %s", addr)
        
        try:
            while not self.shutdown_event.is_set():
                try:
                    # Leer con timeout para permitir shutdown graceful
                    data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
                    if not data:
                        break
                    
                    message = data.decode('utf-8')
                    self.logger.debug("Received from %s: %s", addr, message[:100])
                    
                    # Echo back
                    writer.write(data)
                    await writer.drain()
                    
                except asyncio.TimeoutError:
                    # Timeout normal para permitir check de shutdown
                    continue
                except UnicodeDecodeError:
                    self.logger.warning("Invalid UTF-8 from %s", addr)
                    break
                    
        except ConnectionResetError:
            self.logger.info("Client %s disconnected abruptly", addr)
        except Exception as e:
            self.logger.error("Error handling client %s: %s", addr, e)
        finally:
            writer.close()
            await writer.wait_closed()
            self.logger.info("Connection %s closed", addr)
    
    async def run(self, port: int = 5000) -> None:
        server = await asyncio.start_server(
            self._handle_client, 
            '0.0.0.0', 
            port
        )
        
        addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
        self.logger.info("TCP server listening on %s", addrs)
        
        # Setup signal handlers para shutdown graceful
        loop = asyncio.get_running_loop()
        for sig in [signal.SIGTERM, signal.SIGINT]:
            try:
                loop.add_signal_handler(sig, self._shutdown)
            except NotImplementedError:
                self.logger.warning("Signal handlers not supported on this platform")
        
        try:
            async with server:
                await self.shutdown_event.wait()
        finally:
            self.logger.info("Shutting down server...")
            server.close()
            await server.wait_closed()
            
            # Esperar que terminen las conexiones activas
            if self.active_connections:
                self.logger.info("Waiting for %d active connections...", len(self.active_connections))
                await asyncio.gather(*self.active_connections, return_exceptions=True)
            
            self.logger.info("Server shutdown complete")
    
    def _shutdown(self):
        self.logger.info("Shutdown signal received")
        self.shutdown_event.set()

# Entry point con configuración completa
if __name__ == "__main__":
    import sys
    from core.config import ConfigService
    from core.logging_config import setup_logging
    from core.contracts import IConfigService
    
    setup_logging()
    container.register_singleton(IConfigService, ConfigService())
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    server = TcpEchoServer()
    
    try:
        asyncio.run(server.run(port))
    except KeyboardInterrupt:
        print("\nServer stopped by user")