from Application.Adpaters.ExampleAdapters.ExampleRequestAdaper import ExampleRequestAdaperValidator
from Application.Adpaters.ExampleAdapters.CreateExampleAdapter import CreateExampleAdapter
from Application.Internals.Executors.EasyResult import EasyResult
from Application.Internals.Adapters.TraceIdentifierAdapter import TraceIdentifierAdapterValidator
from Application.Internals.Executors.FluentValidationExecutor import FluentValidationExecutor
from Application.Internals.Adapters.TraceIdentifierAdapter import TraceIdentifierAdapter
from Application.Internals.Adapters.ValidationResultAdapter import ValidationResultAdapter
import asyncio
import random
from Application.Adpaters.ExampleAdapters.ExampleRequestAdaper import ExampleRequestAdaper
from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Interfaces.IFakeApiInfrastructure import IFakeApiInfrastructure

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : Example usecase Class to standardize success and failure responses
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 31/01/2026
# * 
# **********************************************************************************************************

class ExampleUsecase:
    def __init__(self) -> None:
        self.__fake_api:IFakeApiInfrastructure = Services.get_dependency(IFakeApiInfrastructure)

    async def get_data_async(self,trace:TraceIdentifierAdapter, example_request:ExampleRequestAdaper) -> EasyResult:
        # Validar trace identifier
        trace_validation_errors: list[ValidationResultAdapter] = FluentValidationExecutor.execute(trace, lambda obj: TraceIdentifierAdapterValidator(obj))
        if trace_validation_errors:
            return EasyResult.failure(422, trace_validation_errors)

        # Validar request
        request_validation_errors: list[ValidationResultAdapter] = FluentValidationExecutor.execute(example_request, lambda obj: ExampleRequestAdaperValidator(obj))
        if request_validation_errors:
            return EasyResult.failure(422, request_validation_errors)
        
        # Ejemplo de llamada en paralelo
        result_1_task = self.__fake_api.get_user_async(random.randint(1, 10))
        result_2_task = self.__fake_api.get_user_async(random.randint(1, 10))
        result_1, result_2  = await asyncio.gather(result_1_task, result_2_task)

        if not result_1 or not result_2 :
            return EasyResult.empty()
        
        # Send to Kafka
        # Kafka = Services.get_dependency(IExampleKafkaProduInfraestruture)
        # Kafka.send_message(result_1.title, result_2.title)
        
        return EasyResult.success(
            CreateExampleAdapter(
                name=result_1.title,
                age=5,
                email=result_2.title
            )
        )        