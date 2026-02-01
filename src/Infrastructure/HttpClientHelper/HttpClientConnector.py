from Domain.Entities.HttpResponseEntity import HttpResponseEntity
import httpx
from typing import Optional

class HttpClientConnector:
    #*** Mantiene un solo AsyncClient para evitar abrir/cerrar conexiones constantemente.
    def __init__(self, timeout_sec: int = 28):        
        self.timeout_sec = timeout_sec
        # Configuración optimizada para conexiones HTTPS
        self._client = httpx.AsyncClient(
            timeout=self.timeout_sec,            
            http2=False, # Habilitar multiplexación      
            verify=True,# Configuración de SSL optimizada            
            limits=httpx.Limits(# Pool de conexiones
                max_keepalive_connections=5,  # Mantener hasta 5 conexiones vivas
                keepalive_expiry=30.0,       # Mantener conexiones por 30 segundos
                max_connections=10           # Máximo de conexiones simultáneas
            ),
            # Configuración de reintentos
            transport=httpx.AsyncHTTPTransport(
                verify=True,
                retries=2  # Reintentos automáticos
            )
        )

    #*** Cierra el AsyncClient, liberando recursos de red y sockets
    async def close(self):        
        await self._client.aclose()

    async def get_async(self, url: str, params=None, headers=None) -> HttpResponseEntity:
        response = await self._client.get(url, params=params, headers=headers)
        return self._build_response(response)

    async def post_async(self, url: str, data=None, params=None, headers=None) -> HttpResponseEntity:
        response = await self._client.post(url, json=data, params=params, headers=headers)
        return self._build_response(response)

    async def put_async(self, url: str, data=None, params=None, headers=None) -> HttpResponseEntity:
        response = await self._client.put(url, json=data, params=params, headers=headers)
        return self._build_response(response)

    #*** Convierte un httpx.Response en un HttpResponseEntity
    def _build_response(self, response: httpx.Response) -> HttpResponseEntity:
        try:
            content = response.json()
        except Exception:
            content = None

        return HttpResponseEntity(
            StatusCode=response.status_code,
            StatusContent=(content is not None),
            Content=content,
            Headers=response.headers,
            Url=str(response.url),
        )
