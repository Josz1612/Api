# core/container.py
from typing import TypeVar, Type, Dict, Any, Callable
import logging

T = TypeVar('T')

class DIContainer:
    def __init__(self):
        self._services: Dict[type, Any] = {}
        self._factories: Dict[type, Callable] = {}
        
    def register_singleton(self, interface: Type[T], implementation: T) -> None:
        """Registra una instancia única (singleton)"""
        self._services[interface] = implementation
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """Registra una factory para crear nuevas instancias"""
        self._factories[interface] = factory
    
    def get(self, interface: Type[T]) -> T:
        """Resuelve una dependencia"""
        if interface in self._services:
            return self._services[interface]
        
        if interface in self._factories:
            return self._factories[interface]()
            
        raise ValueError(f"Servicio {interface.__name__} no registrado")
    
    def get_logger(self, name: str) -> logging.Logger:
        """Factory method para loggers"""
        return logging.getLogger(name)

# Instancia global del contenedor
container = DIContainer()