from pydantic import BaseModel

# class FakeApiEntity (BaseModel):
#     statusCode:int
#     errors:list[GlobalErrorCoreAdapter] | None
#     data: Optional["FakeApiSuccess"]

class FakeApiEntity (BaseModel):
    userId:int
    id:int
    title:str
    completed:bool
