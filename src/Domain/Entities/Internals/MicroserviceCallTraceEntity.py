from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class MicroserviceCallTraceEntity (BaseModel):
    Identity: str
    TraceId: str
    ChannelId: str
    DeviceId:str
    Keyword: Optional[str] = None
    Method: Optional[str] = None
    MicroserviceName: str = "BusinessAPI2.0"  # This Project
    OperationName: str  # Transfer.GetBalance.execute
    RequestUrl: str
    RequestPayload: Optional[str] = None
    RequestDatetime: datetime = datetime.now()
    ResponseStatusCode: int = 0
    ResponsePayload: Optional[str] = None
    ResponseDatetime: datetime = datetime.now()