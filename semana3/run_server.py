# run_server.py
import sys
import asyncio
import uvicorn
from core.config import ConfigService
from core.logging_config import setup_logging
from core.container import container
from core.contracts import IConfigService
from tcp_server.server import TcpEchoServer
from udp_server.server import UdpEchoServer

def run_tcp():
    setup_logging()
    container.register_singleton(IConfigService, ConfigService())
    config = container.get(IConfigService)
    port = config.get_int("ECHO_PORT", 5000)
    server = TcpEchoServer()
    print(f"Starting TCP Server on port {port}...")
    try:
        asyncio.run(server.run(port))
    except KeyboardInterrupt:
        print("\nServer stopped by user")

def run_udp():
    setup_logging()
    container.register_singleton(IConfigService, ConfigService())
    config = container.get(IConfigService)
    port = config.get_int("UDP_PORT", 5001)
    server = UdpEchoServer()
    print(f"Starting UDP Server on port {port}...")
    try:
        asyncio.run(server.run(port))
    except KeyboardInterrupt:
        print("\nServer stopped by user")

def run_api():
    setup_logging()
    # Uvicorn handles its own loop and logging config mostly, but we setup ours for the app
    # We can just run uvicorn programmatically
    container.register_singleton(IConfigService, ConfigService())
    config = container.get(IConfigService)
    port = config.get_int("API_PORT", 8000)
    print(f"Starting API on port {port}...")
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_server.py [tcp|udp|api]")
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    if mode == "tcp":
        run_tcp()
    elif mode == "udp":
        run_udp()
    elif mode == "api":
        run_api()
    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python run_server.py [tcp|udp|api]")
        sys.exit(1)