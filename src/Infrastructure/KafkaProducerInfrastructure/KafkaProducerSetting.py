from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Interfaces.IExampleKafkaProduInfraestruture import IExampleKafkaProduInfraestruture
from Infrastructure.KafkaProducerInfrastructure.Commands.ExampleKafkaProducer import ExampleKafkaProducer
from Infrastructure.KafkaProducerInfrastructure.Producers.KafkaProducerOne import KafkaProducerOne
from Infrastructure.KafkaProducerInfrastructure.Services.KafkaProducerService import KafkaProducerService

class KafkaProducerSetting():
    @staticmethod
    def add_services() -> None:
        Services.add_singleton_instance(
            KafkaProducerOne(
                bootstrap_servers="10.5.81.14:9092",
                default_topic="vcaxi-topic"
            )
        )

        Services.add_singleton_dependency(IExampleKafkaProduInfraestruture, ExampleKafkaProducer)