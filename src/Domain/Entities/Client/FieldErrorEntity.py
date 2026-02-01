from typing import Optional
from pydantic import BaseModel

class FieldErrorEntity(BaseModel):
    code:str
    message:str
    field:Optional[str]