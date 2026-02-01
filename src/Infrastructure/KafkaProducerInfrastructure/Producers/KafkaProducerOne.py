from typing import Optional, Callable
from confluent_kafka import Producer
from Infrastructure.KafkaProducerInfrastructure.Services.KafkaProducerService import KafkaProducerService


class KafkaProducerOne(KafkaProducerService):
    def __init__(self, bootstrap_servers: str, *, default_topic: Optional[str] = None, delivery_cb: Optional[Callable] = None) -> None:
        self._bootstrap_servers = bootstrap_servers
        super().__init__(default_topic=default_topic, delivery_cb=delivery_cb)

    #---  funcion que debe implenenbtar si o si por cvada 
    def _create_producer(self) -> Producer:
        return Producer({"bootstrap.servers": self._bootstrap_servers})