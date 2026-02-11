from pydantic import BaseModel

class FakeApiEntity (BaseModel):
    userId:int
    id:int
    title:str
    completed:bool
