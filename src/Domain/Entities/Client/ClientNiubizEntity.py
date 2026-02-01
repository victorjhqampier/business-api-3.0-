from typing import Optional
from pydantic import BaseModel

class ClientNiubizEntity (BaseModel):
    CustomerIdentifier:str
    CustomerName:str
    CustomerEmail:str
    CustomerPhoneNumber:str
    RegistrationDate:str
    DaysSinceRegistration:int