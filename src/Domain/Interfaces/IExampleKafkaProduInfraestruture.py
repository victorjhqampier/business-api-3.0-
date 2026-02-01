from abc import ABC, abstractmethod

from Domain.Entities.CoreLoggerEntity import CoreLoggerEntity

class IExampleKafkaProduInfraestruture(ABC):
    
    @abstractmethod
    def send_message(self, text_1:str,text_2:str) -> None:
        pass