from typing import List, Optional
import asyncio
import threading
from Domain.Entities.Internals.MicroserviceCallTraceEntity import MicroserviceCallTraceEntity

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : Cola en memoria basada en el concepto de channels de C#.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 02/01/2026
# * 
# **********************************************************************************************************

class MicroserviceCallMemoryQueue:
    def __init__(self, capacity: int = 1000) -> None:
        self._capacity = capacity
        self._queue = asyncio.Queue(maxsize=capacity)
        self._completed = False
        self._lock = asyncio.Lock()
        self._length = 0
        self._length_lock = threading.Lock()

    # ---- Enqueue (async) con backpressure
    # Bloquea si la cola está llena hasta que haya espacio disponible
    async def push_async(self, item: MicroserviceCallTraceEntity, timeout: Optional[float] = 3.0) -> bool:        
        if self._completed:
            return False
        
        try:
            await asyncio.wait_for(self._queue.put(item), timeout=timeout)
            self._increment_length()
            return True
        except asyncio.TimeoutError:
            return False

    # Intenta añadir un elemento sin bloquear, Usar esto cuando no se quiera esperar. Riesgo de pérdida de datos
    async def try_push(self, item: MicroserviceCallTraceEntity) -> bool:
        if self._completed:
            return False
            
        try:
            self._queue.put_nowait(item)
            self._increment_length()
            return True
        except asyncio.QueueFull:
            return False
    
    # ---- Dequeue (una unidad)
    # Extrae un elemento de la cola de forma asíncrona
    async def pop_async(self, timeout: Optional[float] = None) -> Optional[MicroserviceCallTraceEntity]:        
        if self._completed and self._queue.empty():
            return None
            
        try:
            item = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            self._decrement_length()
            self._queue.task_done()
            return item
        except asyncio.TimeoutError:
            return None

    # Intenta extraer un elemento sin bloquear
    async def try_pop(self) -> Optional[MicroserviceCallTraceEntity]:
        try:
            item = self._queue.get_nowait()
            self._decrement_length()
            self._queue.task_done()
            return item
        except asyncio.QueueEmpty:
            return None

    # ---- Consumo continuo (para BackgroundTask)
    # Lee múltiples elementos de la cola en lotes
    async def read_all_async(self, batch_size: int = 10, timeout: Optional[float] = None) -> List[MicroserviceCallTraceEntity]:        
        items: list[MicroserviceCallTraceEntity] = []
        
        # Esperar por el primer elemento
        first_item: MicroserviceCallTraceEntity | None = await self.pop_async(timeout)
        if first_item is None:
            return items
            
        items.append(first_item)
        
        # Leer elementos adicionales sin bloquear
        for _ in range(batch_size - 1):
            item: MicroserviceCallTraceEntity | None = await self.try_pop()
            if item is None:
                break
            items.append(item)
            
        return items

    # ---- Control de estado
    def complete(self) -> None:
        self._completed = True

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def is_empty(self) -> bool:
        return self._queue.empty()

    @property
    def is_full(self) -> bool:
        return self._queue.full()

    @property
    def approx_length(self) -> int:
        with self._length_lock:
            return self._length

    @property
    def capacity(self) -> int:
        return self._capacity

    # ---- Métodos de utilidtarios privados
    # Incrementa el contador de longitud de forma thread-safe
    def _increment_length(self) -> None:
        with self._length_lock:
            self._length += 1

    # Decrementa el contador de longitud de forma thread-safe
    def _decrement_length(self) -> None:
        with self._length_lock:
            if self._length > 0:
                self._length -= 1

    # ---- Context manager support
    async def __aenter__(self):
        return self

    async def __aexit__(self):
        self.complete()
        # Esperar a que se procesen los elementos pendientes
        await self._queue.join()

    # Retorna la longitud aproximada de la cola
    def __len__(self) -> int:
        return self.approx_length

    # Retorna True si la cola no está vacía
    def __bool__(self) -> bool:
        return not self.is_empty