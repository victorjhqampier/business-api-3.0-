from Application.Adpaters.ExampleAdapters.CreateExampleAdapter import CreateExampleAdapter
from Presentation.BusinessApi.Helpers.EasyBianResponseHelper import EasyBianResponseHelper
from Application.Internals.Executors.EasyResult import EasyResult
from Domain.Commons.CancelationToken import CancelationToken
from Domain.Commons.CoreServices import CoreServices as Services
from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue
from Application.Internals.Adapters.TraceIdentifierAdapter import TraceIdentifierAdapter
from Application.Adpaters.ExampleAdapters.ExampleRequestAdaper import ExampleRequestAdaper
from Application.Usecases.ExampleCase.ExampleUsecase import ExampleUsecase
from Presentation.BusinessApi.Models.RequestInputModel import RequestInputModel
from Presentation.BusinessApi.Handlers.CognitoAuthorizer import CognitoAuthorizer
from Presentation.BusinessApi.BusinessApiLogger import BusinessApiLogger
from Presentation.BusinessApi.Handlers.MicroserviceTraceHandler import MicroserviceTraceHandler
from fastapi import APIRouter, Security, Depends, Header, Path, Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import asyncio
import traceback
import logging

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : Example Controller Class to standardize success and failure responses
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991714
# *
# * Creation date         : 31/01/2026
# * 
# **********************************************************************************************************

class BianExampleController:
    def __init__(self) -> None:
        # ** Tener cuidado con el constructor, solo se llama una vez, es decir está en singlenthon **
        self.ApiRouter = APIRouter(tags=["BIAN Example"])
        self._logger: logging.Logger = BusinessApiLogger.set_logger().getChild(__name__)
        self.__my_routes()
    
    def __my_routes(self) -> None:
        self.ApiRouter.post("/{customer_id}/create", response_model=CreateExampleAdapter)(self.get_basic_data_async)
        self.ApiRouter.post("/new/create", response_model=CreateExampleAdapter)(self.get_secury_data_async)
    
    async def get_basic_data_async(
        self,
        http_request: Request,
        body: ExampleRequestAdaper,
        customer_id:str = Path(..., title="Cod cliente", description="Token de autenticación"),
        device_identifier: str = Header(..., title="Cod Dispositivo", description="Token de autenticación"),
        message_identifier: str = Header(..., title="Cod Mensaje", description="Token de autenticación"),
        channel_identifier: str = Header(..., title="Cod Canal", description="Token de autenticación"),
        example_usecase: ExampleUsecase = Depends(ExampleUsecase)
    ) -> JSONResponse:
        # Start components
        ctx:CancelationToken = CancelationToken(seconds=9.0)
        queue_sender: MicroserviceTraceHandler = MicroserviceTraceHandler(Services.get_instance(MicroserviceCallMemoryQueue))
        request_model = RequestInputModel(
            request=http_request,
            operation_name="obtener-cliente",
            keyword=customer_id
        )        
        trace_model = TraceIdentifierAdapter(
            DeviceIdentifier= device_identifier,
            MessageIdentifier= message_identifier,
            ChannelIdentifier= channel_identifier
        )        
        try:
            async with asyncio.timeout(ctx.remaining()):
                #await asyncio.sleep(9)
                result: EasyResult = await example_usecase.get_data_async(trace_model, body)
                await queue_sender.push_success(request_model, response=result, status_code=result.status)          
            
            if result.status == 204:
                return JSONResponse(status_code=204, content=None)
            
            if not result.is_success:
                return JSONResponse(
                    status_code=result.status,
                    content=jsonable_encoder(EasyBianResponseHelper.easy_warning_respond(result.validation_values), exclude_none=True)
                )
            
            return JSONResponse(
                status_code=result.status,
                content=jsonable_encoder(EasyBianResponseHelper.easy_success_respond(result.success_value), exclude_none=True)
            )
        
        except TimeoutError:
            #await queue_sender.push_error(request_data, error=Exception("SLA_TIMEOUT"))
            return JSONResponse(status_code=408, content=None)
        
        except Exception as e:        
            self._logger.error(str(e) + " in "+traceback.format_exc().replace('\n',' ').strip())
            await queue_sender.push_error(request_model, error=e)
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder(EasyBianResponseHelper.easy_error_respond("99","No es de tu lado, es nuestro error"),exclude_none=True)
            )

    async def get_secury_data_async (
        self,        
        http_request: Request,
        body: ExampleRequestAdaper,
        device_identifier: str = Header(..., title="Cod Dispositivo", description="Token de autenticación"),
        message_identifier: str = Header(..., title="Cod Mensaje", description="Token de autenticación"),
        channel_identifier: str = Header(..., title="Cod Canal", description="Token de autenticación"),        
        example_usecase: ExampleUsecase = Depends(ExampleUsecase),
        _: dict = Security(CognitoAuthorizer(), scopes=["openid"])
    ) -> JSONResponse:
        # Start components
        ctx:CancelationToken = CancelationToken(seconds=9.0)
        queue_sender: MicroserviceTraceHandler = MicroserviceTraceHandler(Services.get_instance(MicroserviceCallMemoryQueue))
        request_model = RequestInputModel(
            request=http_request,
            operation_name="obtener-cliente",
            keyword="None"
        )        
        trace_model = TraceIdentifierAdapter(
            DeviceIdentifier= device_identifier,
            MessageIdentifier= message_identifier,
            ChannelIdentifier= channel_identifier
        )        
        try:
            async with asyncio.timeout(ctx.remaining()):
                #await asyncio.sleep(8)
                result: EasyResult = await example_usecase.get_data_async(trace_model, body)
                await queue_sender.push_success(request_model, response=result, status_code=result.status)
            
            if result.status == 204:
                return JSONResponse(status_code=204, content=None)
            
            if not result.is_success:
                return JSONResponse(
                    status_code=result.status,
                    content=jsonable_encoder(EasyBianResponseHelper.easy_warning_respond(result.validation_values), exclude_none=True)
                )            
            
            return JSONResponse(
                status_code=result.status,
                content=jsonable_encoder(EasyBianResponseHelper.easy_success_respond(result.success_value), exclude_none=True)
            )
        
        except TimeoutError:
            #await queue_sender.push_error(request_data, error=Exception("SLA_TIMEOUT"))
            return JSONResponse(status_code=408, content=None)
        
        except Exception as e:        
            self._logger.error(str(e) + " in "+traceback.format_exc().replace('\n',' ').strip())
            await queue_sender.push_error(request_model, error=e)
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder(EasyBianResponseHelper.easy_error_respond("99","No es de tu lado, es nuestro error"),exclude_none=True)
            )
