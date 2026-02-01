from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CoreLoggerEntity (BaseModel):
    idLogger:str | None = None
    idPadre:Optional[str]
    cApi:str
    cOperation:str
    dFechaRequest:datetime = datetime.now()
    cJsonRequest:str
    dFechaResponse:datetime | None
    cJsonResponse:str | None
    lIsSuccess:bool = False
    