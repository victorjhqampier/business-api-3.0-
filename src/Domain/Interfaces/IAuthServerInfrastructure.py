from abc import ABC, abstractmethod
from Domain.Entities.HttpResponseEntity import HttpResponseEntity

class IAuthServerInfrastructure(ABC):

    @abstractmethod
    async def post_async(self, url:str, data=None, params=None, headers=None) -> HttpResponseEntity:
        pass