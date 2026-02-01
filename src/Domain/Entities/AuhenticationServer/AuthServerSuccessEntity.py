from typing import Optional
from pydantic import BaseModel

class AuthServerSuccessEntity (BaseModel):
    ExpireIn:int
    AccessToken:str
    IdToken:Optional[str] = None
    TokenType:Optional[str] = None
