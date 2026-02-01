from abc import ABC, abstractmethod
from typing import Optional
from Domain.Entities.ExampleFakeApi.FakeApiEntity import FakeApiEntity

class IFakeApiInfrastructure(ABC):
    
    @abstractmethod
    async def get_user_async(self,id:int) -> Optional[FakeApiEntity]:
        pass