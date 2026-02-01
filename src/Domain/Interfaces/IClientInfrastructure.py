from abc import ABC, abstractmethod
from Domain.Entities.Client.ClientResponseEntity import ClientResponseEntity

class IClientInfrastructure(ABC):
    
    @abstractmethod
    async def get_client(self, CustomerCardIdentifier:int, CustomerCardNumber:str) -> ClientResponseEntity:
        pass