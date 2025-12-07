# core/exceptions.py
class SocketError(Exception):
    """Base exception para errores de socket"""
    pass

class ConnectionTimeoutError(SocketError):
    """Error por timeout de conexión"""
    pass

class MessageTooLongError(SocketError):
    """Mensaje excede límites"""
    pass

class ServerNotAvailableError(SocketError):
    """Servidor no disponible"""
    pass