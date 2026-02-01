from __future__ import annotations
import asyncio
import logging
from typing import Any, TypeVar, Generic, Optional, Union, List
from Infrastructure.KafkaProducerInfrastructure2.Services.KafkaProducerBuilder import KafkaProducerBuilder
from Infrastructure.KafkaProducerInfrastructure2.Services.KafkaProducerLogger import KafkaProducerLogger

T = TypeVar('T')

class KafkaProducerService(Generic[T]):   
    def __init__(self) -> None:
        self.__bootstrap: str | None = None
        self.__topic: str | None = None
        self.__value_serializer: Optional[callable] = None
        self.__client_id: str | None = None
        self.__producer = None
        self._started = False
        self._lock = asyncio.Lock()
        self._logger = KafkaProducerLogger.set_logger().getChild(self.__class__.__name__)

    def with_bootstrap_servers(self, bootstrap: str) -> 'KafkaProducerService[T]':
        self.__bootstrap = bootstrap
        return self

    def with_topic(self, topic: str) -> 'KafkaProducerService[T]':
        self.__topic = topic
        return self

    def with_value_serializer(self, serializer: callable) -> 'KafkaProducerService[T]':
        self.__value_serializer = serializer
        return self

    def with_client_id(self, client_id: str) -> 'KafkaProducerService[T]':
        self.__client_id = client_id
        return self

    def _validate(self) -> None:
        if not self.__bootstrap:
            raise ValueError("Bootstrap servers are required")
        if not self.__topic:
            raise ValueError("Topic is required")

    async def start(self) -> None:
        async with self._lock:
            if self._started:
                return

            self._validate()
            self.__producer = KafkaProducerBuilder(
                bootstrap_servers=self.__bootstrap,
                value_serializer=self.__value_serializer
            ).build()

            await self.__producer.start()
            self._started = True
            self._logger.info("KafkaProducer conectado a %s", self.__producer.client_id)

    async def stop(self) -> None:
        async with self._lock:
            if not self._started:
                return
            await self.__producer.stop()
            self._started = False
            self._logger.info("KafkaProducer [%s] cerrado", self.__producer.client_id)

    async def send(
        self,
        value: T,
        key: bytes | None = None,
        headers: list[tuple[str, bytes]] | None = None,
        partition: int | None = None,
    ) -> None:
        """
        Publica un mensaje y espera a la confirmación (`await`).

        - `value` puede ser dict/list/str… se serializa a JSON por default.
        """
        if not self._started:
            raise RuntimeError("Producer aún no está iniciado")

        try:
            await self.__producer.send_and_wait(
                topic=self.__topic,
                value=value,
                key=key,
                headers=headers,
                partition=partition,
            )
            self._logger.debug("Enviado a %s: %s", self.__topic, value)
        except Exception as e:
            self._logger.exception("Fallo enviando mensaje a %s", self.__topic)
            raise e