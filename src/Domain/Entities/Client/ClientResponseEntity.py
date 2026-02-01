from Domain.Entities.Client.ClientNiubizEntity import ClientNiubizEntity
from Application.Adpaters.GlobalErrorCoreAdapter import GlobalErrorCoreAdapter
from pydantic import BaseModel

class ClientResponseEntity (BaseModel):
    errors:list[GlobalErrorCoreAdapter] | None
    data:ClientNiubizEntity | None