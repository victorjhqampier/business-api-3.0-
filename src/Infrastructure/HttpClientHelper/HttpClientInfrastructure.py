from Infrastructure.InfrastructureLogger import InfrastructureLogger
from uuid import uuid4
from datetime import datetime
from typing import Dict, Optional, Any
import json
from Domain.Entities.Internals.MicroserviceCallTraceEntity import MicroserviceCallTraceEntity
from Domain.Containers.MemoryEvents.MicroserviceCallMemoryQueue import MicroserviceCallMemoryQueue
from Domain.Entities.HttpResponseEntity import HttpResponseEntity
from Domain.Interfaces.IHttpClientInfrastructure import IHttpClientInfrastructure
from Infrastructure.HttpClientHelper.HttpClientConnector import HttpClientConnector
from Domain.Commons.CoreServices import CoreServices as Services

# ********************************************************************************************************          
# * Copyright © 2025 Arify Labs - All rights reserved.   
# * 
# * Info                  : Build a http request Handler.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991*14
# *
# * Creation date         : 03/01/2026
# * 
# **********************************************************************************************************

class HttpClientInfrastructure(IHttpClientInfrastructure):
    def __init__(self):
        self.__ApiClient: HttpClientConnector = Services.get_instance(HttpClientConnector)
        self.__base_url: str = ''
        self.__endpoint: str = ''
        self.__headers: dict = {}
        self.__params: dict = {}
        self.__query: dict = {}
        # In memory event - optimized attributes
        self.__memory_enabled: bool = False
        self.__container: Optional[MicroserviceCallMemoryQueue] = None
        self.__operation_name: str = ''
        self.__start_datetime: datetime = datetime.utcnow()
        self._logger = InfrastructureLogger.set_logger().getChild(self.__class__.__name__)

    def timeout(self, timeout: int) -> "HttpClientInfrastructure":
        # No está en la interfaz, pero es adicional si lo deseas
        self.__ApiClient.timeout_sec = timeout
        return self

    def http(self, base_url: str) -> "HttpClientInfrastructure":
        self.__base_url = base_url.rstrip('/')
        return self

    def endpoint(self, endpoint: str) -> "HttpClientInfrastructure":
        self.__endpoint = endpoint.lstrip('/')
        return self

    def header(self, key: str, value: str) -> "HttpClientInfrastructure":
        self.__headers[key] = value
        return self

    def authorization(self, key: str, value: str) -> "HttpClientInfrastructure":
        # Método adicional, no en la interfaz
        self.__headers['Authorization'] = f"{key} {value}"
        return self

    def headers(self, headers: Dict[str, str]) -> "HttpClientInfrastructure":
        self.__headers.update(headers)
        return self

    def param(self, key: str, value: str) -> "HttpClientInfrastructure":
        self.__params[key] = value
        return self

    def params(self, params: Dict[str, str]) -> "HttpClientInfrastructure":
        self.__params.update(params)
        return self

    def query(self, key: str, value: str) -> "HttpClientInfrastructure":
        self.__query[key] = value
        return self

    def queries(self, queries: Dict[str, str]) -> "HttpClientInfrastructure":
        self.__query.update(queries)
        return self

    def _build_final_url(self) -> str:
        path = f"{self.__base_url}/{self.__endpoint}"
        if self.__query:
            qs = '&'.join(f"{k}={v}" for k, v in self.__query.items())
            return f"{path}?{qs}"
        return path

    def _ensure_default_headers(self) -> None:
        if not self.__headers:
            self.__headers['Content-Type'] = 'application/json'

    async def get(self) -> HttpResponseEntity:
        self._ensure_default_headers()
        final_url = self._build_final_url()
        
        try:
            response = await self.__ApiClient.get_async(
                url=final_url, 
                params=self.__params,
                headers=self.__headers
            )
            # Capturar evento completo (request + response)
            await self._capture_complete_trace("GET", None, response)
            return response
        except Exception as e:
            # Capturar traza de error
            await self._capture_error_trace("GET", None, str(e))
            raise  # Re-lanzar la excepción

    async def post(self, body: Optional[dict] = None) -> HttpResponseEntity:
        self._ensure_default_headers()
        final_url = self._build_final_url()
        
        try:
            response = await self.__ApiClient.post_async(
                url=final_url,
                data=body,
                params=self.__params,
                headers=self.__headers
            )
            # Capturar evento completo (request + response)
            await self._capture_complete_trace("POST", body, response)
            return response
        except Exception as e:
            # Capturar traza de error
            await self._capture_error_trace("POST", body, str(e))
            raise  # Re-lanzar la excepción

    async def put(self, body: Optional[dict] = None) -> HttpResponseEntity:
        self._ensure_default_headers()
        final_url = self._build_final_url()
        
        try:
            response = await self.__ApiClient.put_async(
                url=final_url,
                data=body,
                params=self.__params,
                headers=self.__headers
            )
            # Capturar evento completo (request + response)
            await self._capture_complete_trace("PUT", body, response)
            return response
        except Exception as e:
            # Capturar traza de error
            await self._capture_error_trace("PUT", body, str(e))
            raise  # Re-lanzar la excepción

    async def close(self) -> None:
        await self.__ApiClient.close()
    
     # Memory queue functionality - optimized implementation
    def with_memory_queue(self, queue: MicroserviceCallMemoryQueue, operation_name: str, keyword: Optional[str] = None) -> "HttpClientInfrastructure":
        self.__memory_enabled = True
        self.__container = queue
        self.__operation_name = operation_name
        self.__keyword = keyword
        return self

    # Resetea el estado de memory queue para reutilizar la instancia. Útil para optimizar recursos cuando se reutiliza el cliente.
    def _reset_memory_state(self) -> "HttpClientInfrastructure":
        self.__memory_enabled = False
        self.__container = None
        self.__operation_name = ''
        self.__keyword = None
        self.__identity = ''
        return self
   
    def _serialize_payload(self, payload: Any) -> Optional[str]:
        if payload is None:
            return None
        
        try:
            if isinstance(payload, (dict, list)):
                return json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
            return str(payload)
        except (TypeError, ValueError):
            return str(payload)

    async def _capture_complete_trace(self, method: str, body: Optional[dict], response: HttpResponseEntity) -> None:
        if not self.__memory_enabled or self.__container is None:
            return

        trace_entity = MicroserviceCallTraceEntity(
            Identity=str(uuid4()),
            TraceId=self.__headers.get("message-identification", ""),
            ChannelId=self.__headers.get("channel-identification", ""),
            DeviceId=self.__headers.get("device-identification", ""),
            Keyword=self.__keyword or "",
            Method=method,
            MicroserviceName="BusinessAPI2.0",
            OperationName=self.__operation_name,
            RequestUrl=self._build_final_url(),
            RequestPayload=self._serialize_payload(body),
            RequestDatetime=self.__start_datetime,
            ResponseStatusCode=response.StatusCode,
            ResponsePayload=self._serialize_payload(response.Content),
            ResponseDatetime=datetime.utcnow()
        )

        # Usar try_push para evitar bloqueos
        if not await self.__container.try_push(trace_entity):
            self._logger.error(f"[QUEUE FULL], Trace: {trace_entity.TraceId} {trace_entity.RequestUrl} {trace_entity.ResponsePayload}")

    async def _capture_error_trace(self, method: str, body: Optional[dict], error_message: str) -> None:
        if not self.__memory_enabled or self.__container is None:
            return

        trace_entity = MicroserviceCallTraceEntity(
            Identity=str(uuid4()),
            TraceId=self.__headers.get("message-identification", ""),
            ChannelId=self.__headers.get("channel-identification", ""),
            DeviceId=self.__headers.get("device-identification", ""),
            Keyword=self.__keyword or "",
            Method=method,
            MicroserviceName="BusinessAPI2.0",
            OperationName=self.__operation_name,
            RequestUrl=self._build_final_url(),
            RequestPayload=self._serialize_payload(body),
            RequestDatetime=self.__start_datetime,
            ResponseStatusCode=408,  # Timeout o error de conexión
            ResponsePayload=f"ERROR: {error_message}",
            ResponseDatetime=datetime.utcnow()
        )

        # Usar try_push para evitar bloqueos
        if not await self.__container.try_push(trace_entity):
            self._logger.error(f"[QUEUE FULL], Trace: {trace_entity.TraceId} {trace_entity.RequestUrl} {trace_entity.ResponsePayload}")