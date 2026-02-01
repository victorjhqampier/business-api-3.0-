from typing import Optional
from pydantic import BaseModel

class HttpResponseEntity (BaseModel):
    StatusCode:int
    StatusContent:bool
    Content:Optional[dict] = None
    Headers:Optional[dict] = None
    Url:str

    