from abc import ABC, abstractmethod

class IExampleKafkaConsumerInfrastructure(ABC):
    @abstractmethod
    def consume_message(self) -> None:
        pass 