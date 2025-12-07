import asyncio
import logging
import signal
from typing import Optional
from core.contracts import IConfigService
from core.container import container

class EchoProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.transport = None
        self.message_count = 0
    
    def connection_made(self, transport):
        self.transport = transport
        sockname = transport.get_extra_info('sockname')
        self.logger.info("UDP server listening on %s", sockname)
    
    def datagram_received(self, data, addr):
        self.message_count += 1
        try:
            message = data.decode('utf-8')
            self.logger.debug("Message #%d from %s: %s", self.message_count, addr, message[:100])
            if self.transport:
                self.transport.sendto(data, addr)
        except UnicodeDecodeError:
            self.logger.warning("Invalid UTF-8 datagram from %s", addr)
        except Exception as e:
            self.logger.error("Error processing datagram from %s: %s", addr, e)
    
    def error_received(self, exc):
        self.logger.error("UDP error received: %s", exc)

class UdpEchoServer:
    def __init__(self, config: Optional[IConfigService] = None):
        self.config = config or container.get(IConfigService)
        self.logger = logging.getLogger(__name__)
        self.shutdown_event = asyncio.Event()
    
    async def run(self, port: int = 5001) -> None:
        loop = asyncio.get_running_loop()
        
        # Setup signal handlers
        for sig in [signal.SIGTERM, signal.SIGINT]:
            try:
                loop.add_signal_handler(sig, self._shutdown)
            except NotImplementedError:
                self.logger.warning("Signal handlers not supported on this platform")
        
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: EchoProtocol(), 
            local_addr=('0.0.0.0', port)
        )
        
        try:
            await self.shutdown_event.wait()
        finally:
            self.logger.info("Shutting down UDP server...")
            transport.close()
            self.logger.info("UDP server shutdown complete")
    
    def _shutdown(self):
        self.logger.info("UDP shutdown signal received")
        self.shutdown_event.set()

if __name__ == "__main__":
    import sys
    from core.config import ConfigService
    from core.logging_config import setup_logging
    from core.contracts import IConfigService
    
    setup_logging()
    container.register_singleton(IConfigService, ConfigService())
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5001
    server = UdpEchoServer()
    
    try:
        asyncio.run(server.run(port))
    except KeyboardInterrupt:
        print("\nUDP Server stopped by user")