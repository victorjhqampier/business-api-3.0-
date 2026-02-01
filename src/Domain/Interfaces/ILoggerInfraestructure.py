from abc import ABC, abstractmethod

from Domain.Entities.CoreLoggerEntity import CoreLoggerEntity

class ILoggerInfraestructure(ABC):
    
    @abstractmethod
    async def open_log(self,cApi:str, cOperation:str, cJsonRequest:str) -> str:
        pass

    @abstractmethod
    async def close_log(self,id:str, cJsonResponse:str) -> None:
        pass

    @abstractmethod
    async def close_with_error_log(self,id:str, cJsonResponse:str) -> None:
        pass
    
    @abstractmethod
    async def get_log(self,id:str) -> CoreLoggerEntity | None:
        pass