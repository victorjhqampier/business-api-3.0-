from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Interfaces.IExampleKafkaProduInfraestruture import IExampleKafkaProduInfraestruture
from Infrastructure.KafkaProducerInfrastructure.Producers.KafkaProducerOne import KafkaProducerOne

class ExampleKafkaProducer(IExampleKafkaProduInfraestruture):
    def __init__(self) -> None:
        self.__myProducer = Services.get_instance(KafkaProducerOne)

    def send_message(self, text_1:str,text_2:str) -> None:
        mess = {
            'code': text_1,
            'message': text_2
        }
        try:
            self.__myProducer.send(mess)
        except BufferError as ex:
            print(str(ex))