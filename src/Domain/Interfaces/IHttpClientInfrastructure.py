from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue
from abc import ABC, abstractmethod
from typing import Dict, Optional

from Domain.Entities.HttpResponseEntity import HttpResponseEntity

class IHttpClientInfrastructure(ABC):
    @abstractmethod
    def http(self, base_url: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def endpoint(self, endpoint: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def header(self, key: str, value: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def authorization(self, key: str, value: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def headers(self, headers: Dict[str, str]) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def param(self, key: str, value: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def params(self, params: Dict[str, str]) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def query(self, key: str, value: str) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    def queries(self, queries: Dict[str, str]) -> "IHttpClientInfrastructure":
        pass

    @abstractmethod
    async def get(self) -> HttpResponseEntity:
        pass

    @abstractmethod
    async def post(self, body: Optional[dict] = None) -> HttpResponseEntity:
        pass

    @abstractmethod
    async def put(self, body: Optional[dict] = None) -> HttpResponseEntity:
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Cierra la conexión interna (AsyncClient o Session).
        Debe llamarse cuando no se use más la instancia.
        """
        pass

    @abstractmethod
    def with_memory_queue(self, container: MicroserviceCallMemoryQueue, operation_name: str, keyword:str = None) -> "IHttpClientInfrastructure":
        pass