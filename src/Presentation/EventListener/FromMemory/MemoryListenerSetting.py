from Domain.Commons.CoreServices import CoreServices as Services
from Presentation.EventListener.FromMemory.Queries.MicroserviceCallMemoryListener import MicroserviceCallMemoryListener
from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue

class MemoryListenerSetting:
    
    @staticmethod
    async def add_services():
        # Inicializar la cola en memoria
        Services.add_singleton_instance(MicroserviceCallMemoryQueue(capacity=1500))

        # Inicializar y arrancar el listener
        listener = MicroserviceCallMemoryListener()
        await listener.start_async()
        return listener