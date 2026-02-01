from typing import Optional
from Domain.Entities.AuhenticationServer.AuthServerFailEntity import AuthServerFailEntity
from Domain.Entities.AuhenticationServer.AuthServerSuccessEntity import AuthServerSuccessEntity
from pydantic import BaseModel

class AuthServerEntity (BaseModel):
    StatusCode:int
    StatusContent:bool
    Data: Optional[AuthServerSuccessEntity] = None
    Error: Optional[AuthServerFailEntity] = None
