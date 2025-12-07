# core/contracts.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
import logging

class ITcpEchoServer(ABC):
    @abstractmethod
    async def run(self, port: int) -> None: ...

class ITcpEchoClient(ABC):
    @abstractmethod
    async def echo(self, host: str, port: int, message: str, timeout: float = 5.0) -> str: ...

class ILogger(ABC):
    @abstractmethod
    def info(self, message: str, **kwargs) -> None: ...
    
    @abstractmethod
    def error(self, message: str, **kwargs) -> None: ...
    
    @abstractmethod
    def warning(self, message: str, **kwargs) -> None: ...

class IConfigService(ABC):
    @abstractmethod
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]: ...
    
    @abstractmethod
    def get_int(self, key: str, default: int = 0) -> int: ...
    
    @abstractmethod
    def get_float(self, key: str, default: float = 0.0) -> float: ...