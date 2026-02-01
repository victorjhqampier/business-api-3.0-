from __future__ import annotations
import uuid
import json
from typing import Any, Callable, Dict, List, Union
from Presentation.Queues.Services.KafkaDefaultConfig import KafkaDefaultConfig
from aiokafka import AIOKafkaProducer

class KafkaProducerBuilder:
    def __init__(
        self,
        *,
        bootstrap_servers: str | None = None,
        value_serializer: Callable[[Any], bytes] | None = None,
        **extra_conf: Dict[str, Any],
    ) -> None:
        self.__producer_default = KafkaDefaultConfig()
        self._config: Dict[str, Any] = {
            "bootstrap_servers": bootstrap_servers or self.__producer_default.bootstrap_servers,
            "value_serializer": value_serializer or (lambda v: json.dumps(v).encode()),
            "client_id": f"{self.__producer_default.client_id_prefix}-{uuid.uuid4()}",
            "acks": "all",          # garantiza *at-least-once* en el broker
            "linger_ms": 10,        # un poco de batching
        }
        self._config.update(extra_conf)

        if self.__producer_default.ssl_enabled:
            self._config.update(
                security_protocol="SSL",
                ssl_cafile=self.__producer_default.ssl_cafile,
                ssl_certfile=self.__producer_default.ssl_certfile,
                ssl_keyfile=self.__producer_default.ssl_keyfile,
            )

    # ----- Devuelve la instancia, sin iniciar el `start()`
    def build(self) -> AIOKafkaProducer:        
        return AIOKafkaProducer(**self._config)