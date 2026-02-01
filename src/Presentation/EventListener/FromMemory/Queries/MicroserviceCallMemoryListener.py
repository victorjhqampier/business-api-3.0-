import random
import asyncio
import logging
from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue
from Domain.Entities.Internals.MicroserviceCallTraceEntity import MicroserviceCallTraceEntity
from Presentation.EventListener.EventListenerLogger import EventListenerLogger

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : Background Task equivalente a BackgroundService de C#.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 02/01/2026
# * 
# **********************************************************************************************************

class MicroserviceCallMemoryListener:    
    def __init__(self) -> None:
        self._container: MicroserviceCallMemoryQueue = Services.get_instance(MicroserviceCallMemoryQueue)
        self._logger = EventListenerLogger.set_logger().getChild(self.__class__.__name__)
        self._task: asyncio.Task = None
        self._is_running = False
    
    # Inicia el background service
    async def start_async(self) -> None:
        if self._is_running:
            return
            
        self._is_running = True
        self._task = asyncio.create_task(self._execute_async())
    
    # Detiene el background service
    async def stop_async(self) -> None:
        if not self._is_running:
            return
            
        self._is_running = False
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
    # LLamar aqui a los casos de uso para procesar los eventos
    # Método principal equivalente a ExecuteAsync de BackgroundService en C#.
    async def _execute_async(self) -> None:
        while self._is_running:
            try:
                # Leer eventos de la cola en lotes (mejor práctica)
                events = await self._container.read_all_async(batch_size=10, timeout=1.0)
                
                if events:
                    # Procesar cada evento del lote
                    for event in events:
                        # Aquí debe llamar a un caso de uso para procesar el evento
                        # ***** public Task SaveEventAsync(MicroserviceApiEventEntity microserviceEvent) ****
                        
                        # TODO: Implementar llamada al caso de uso
                        # use_case = Services.get_instance(ISaveEventUseCase)
                        # await use_case.save_event_async(event)

                        await asyncio.sleep(random.randint(0, 2))
                        
                        self._logger.warning(f"IDENTITY>> {event.Identity} START>> {event.RequestDatetime} END>> {event.ResponseDatetime}")
                    
            except Exception as e:
                self._logger.error(f"Error procesando eventos: {e}")
                # Continuar el loop en caso de error