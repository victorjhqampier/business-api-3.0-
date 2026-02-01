from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, Optional
from confluent_kafka import Producer, KafkaError

# ********************************************************************************************************          
# * Copyright © 2025 Arify Labs - All rights reserved.   
# * 
# * Info                  : Base for KAFKA Producer.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 01/06/2025
# * 
# **********************************************************************************************************

class KafkaProducerService(ABC):    
    def __init__(self, *, default_topic: Optional[str] = None, delivery_cb: Optional[Callable] = None) -> None:
        self._producer = self._create_producer()
        self._default_topic = default_topic
        self._delivery_cb = delivery_cb or self._default_delivery_cb

    @abstractmethod
    # Método abstracto que las clases derivadas deben implementar si o si para crear su propia instancia de Producer
    def _create_producer(self) -> Producer:        
        pass

    # ──────────────── API pública ────────────────
    def send(self, payload: Dict[str, Any], *, topic: Optional[str] = None, key: str | None = None) -> None:        
        topic = topic or self._default_topic
        if topic is None:
            raise ValueError("Topic no especificado")

        self._producer.produce(
            topic=topic,
            key=key,
            value=json.dumps(payload),
            callback=self._delivery_cb,
        )
        # Procesa acks y reintentos sin bloquear; 0 = inmediato
        self._producer.poll(0)
        self._producer.flush()        

    # ──────────────── Callbacks ────────────────
    @staticmethod
    def _default_delivery_cb(err: KafkaError | None, msg) -> None:  # noqa: D401
        if err is not None:
            print(f"[Kafka] Error entregando mensaje: {err}")
        else:
            print(
                f"[Kafka] topic {msg.topic()} "
                f"[part {msg.partition()}] offset {msg.offset()}"
            )