from typing import Optional
from pydantic import BaseModel, Field

class CreateExampleAdapter(BaseModel):
    name:str = Field(..., title="Name", description="Name of the example")
    age:int = Field(..., title="Age", description="Age of the example")
    email:Optional[str] = Field(..., title="Email", description="Email of the example")