from Infrastructure.HttpClientHelper.HttpClientBuilder import HttpClientBuilder
from Infrastructure.HttpClientHelper.HttpClientConnector import HttpClientConnector
from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue
from typing import Optional
from Domain.Entities.ExampleFakeApi.FakeApiEntity import FakeApiEntity
from Domain.Interfaces.IFakeApiInfrastructure import IFakeApiInfrastructure
from Domain.Entities.HttpResponseEntity import HttpResponseEntity
from Infrastructure.ExampleFakeApiInfra.ExampleFakeStartting import _exampleFakeStartting as ExampleFakeStartting
from Infrastructure.InfrastructureLogger import InfrastructureLogger
from Domain.Commons.CoreServices import CoreServices as Services

class FakeApiCommand (IFakeApiInfrastructure):
    def __init__(self) -> None:
        self._queue: MicroserviceCallMemoryQueue = Services.get_instance(MicroserviceCallMemoryQueue)     
        self._http_connector:HttpClientConnector = Services.get_instance(HttpClientConnector) 
        self._logger = InfrastructureLogger.set_logger().getChild(self.__class__.__name__)
        
    async def get_user_async(self,id:int) -> Optional[FakeApiEntity]:
        http_client = HttpClientBuilder(self._http_connector, self._logger)
        (
            http_client.http(ExampleFakeStartting.EXAMPLE_HOST_BASE.value)            
            .endpoint(f"todos/{id}")
            .with_memory_queue(self._queue, "FakeApiCommand.get_user_async", keyword="my_user_id") # Solo con esto debes dejar traza
        )
        
        result:HttpResponseEntity = await http_client.get()

        if result.StatusCode == 500:
            self._logger.error(f"[{result.StatusCode}] [{result.Url}] : {str(result.Content)}")
            return None

        if result.StatusCode != 200 or not result.Content:
            self._logger.warning(f"[{result.StatusCode}] [{result.Url}] - {str(result.Content)}")
            return None        

        return FakeApiEntity(
                userId = result.Content.get("userId", 0),
                id = result.Content.get("id", 0),
                title = result.Content.get("title", "No Title"),
                completed = result.Content.get("completed", False)
        )
    
    async def get_title_async(self,id:int) -> Optional[FakeApiEntity]:
        http_client = HttpClientBuilder(self._http_connector, self._logger)
        (
            http_client.http(ExampleFakeStartting.EXAMPLE_TITLE_BASE.value)
            .endpoint(f"products/{id}")
            #.with_memory_queue(self._queue, "FakeApiCommand.get_title_async", keyword="my_title_id") # Solo con esto debes dejar traza
        )
        
        result:HttpResponseEntity = await http_client.get()

        if result.StatusCode == 500:
            self._logger.error(f"[{result.StatusCode}] [{result.Url}] : {str(result.Content)}")
            return None

        if result.StatusCode != 200 or not result.Content:
            self._logger.warning(f"[{result.StatusCode}] [{result.Url}] - {str(result.Content)}")
            return None        

        return FakeApiEntity(
                userId = 0,
                id = result.Content.get("id", 0),
                title = result.Content.get("title", "No Title"),
                completed = True
        )