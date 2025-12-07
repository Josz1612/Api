# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import logging
from typing import Optional
from core.contracts import ITcpEchoClient, IConfigService
from core.container import container
from core.exceptions import ConnectionTimeoutError, MessageTooLongError
from core.logging_config import setup_logging
from core.config import ConfigService
from tcp_client.client import TcpEchoClient

# Configurar aplicación
setup_logging()
container.register_singleton(IConfigService, ConfigService())
container.register_factory(ITcpEchoClient, lambda: TcpEchoClient())

app = FastAPI(
    title="SocketsPy Pro Echo API",
    description="API robusta para eco TCP con DI y logging",
    version="2.0.0"
)

logger = logging.getLogger(__name__)

# Modelos Pydantic
class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, description="Mensaje a enviar")
    timeout: Optional[float] = Field(5.0, ge=0.1, le=30.0, description="Timeout en segundos")

class EchoResponse(BaseModel):
    echoed: str
    message_length: int
    success: bool = True

class ErrorResponse(BaseModel):
    error: str
    detail: str
    success: bool = False

# Dependency injection para FastAPI
def get_tcp_client() -> ITcpEchoClient:
    return container.get(ITcpEchoClient)

def get_config() -> IConfigService:
    return container.get(IConfigService)

@app.post("/echo", response_model=EchoResponse, responses={
    400: {"model": ErrorResponse, "description": "Mensaje inválido"},
    503: {"model": ErrorResponse, "description": "Servicio no disponible"},
    408: {"model": ErrorResponse, "description": "Timeout"}
})
async def echo_message(
    request: EchoRequest,
    client: ITcpEchoClient = Depends(get_tcp_client),
    config: IConfigService = Depends(get_config)
):
    """Envía un mensaje al servidor TCP y retorna el eco"""
    
    host = config.get("ECHO_HOST", "127.0.0.1") or "127.0.0.1"
    port = config.get_int("ECHO_PORT", 5000)
    
    logger.info("Processing echo request: %s chars to %s:%d", 
                len(request.message), host, port)
    
    try:
        # Ensure timeout is not None (Pydantic default handles this, but type checker needs help)
        timeout_val = request.timeout if request.timeout is not None else 5.0
        echoed = await client.echo(host, port, request.message, timeout_val)
        
        logger.info("Echo successful: %s chars returned", len(echoed))
        
        return EchoResponse(
            echoed=echoed,
            message_length=len(echoed)
        )
        
    except ConnectionTimeoutError as e:
        logger.error("Timeout error: %s", str(e))
        raise HTTPException(
            status_code=408, 
            detail={"error": "timeout", "detail": str(e), "success": False}
        )
    
    except MessageTooLongError as e:
        logger.error("Message too long: %s", str(e))
        raise HTTPException(
            status_code=400, 
            detail={"error": "message_too_long", "detail": str(e), "success": False}
        )
    
    except ConnectionRefusedError:
        logger.error("TCP server not available at %s:%d", host, port)
        raise HTTPException(
            status_code=503, 
            detail={"error": "server_unavailable", "detail": f"Cannot connect to {host}:{port}", "success": False}
        )
    
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise HTTPException(
            status_code=500, 
            detail={"error": "internal_error", "detail": "Internal server error", "success": False}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SocketsPy Pro API"}

@app.get("/config")
async def get_configuration(config: IConfigService = Depends(get_config)):
    """Retorna configuración actual (sin datos sensibles)"""
    return {
        "echo_host": config.get("ECHO_HOST"),
        "echo_port": config.get_int("ECHO_PORT"),
        "max_message_length": config.get_int("MAX_MESSAGE_LENGTH")
    }

# Ejecutar con: uvicorn api.main:app --reload --port 8000