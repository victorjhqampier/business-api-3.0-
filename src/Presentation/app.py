from Presentation.BusinessApi.Controllers.NonBianExample.NoBianExampleController import NoBianExampleController
from Presentation.BusinessApi.Controllers.BianExample.BianExampleController import BianExampleController
from Application.CoreApplicationSetting import CoreApplicationSetting
# from Presentation.EventListener.FromExternal.KafkaConsumerSetting import KafkaConsumerSetting
from Presentation.EventListener.FromMemory.MemoryListenerSetting import MemoryListenerSetting
from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

# ********************************************************************************************************          
# * Copyright © 2026 Arify Labs - All rights reserved.   
# * 
# * Info                  : Business started for SaaS.
# *
# * By                    : Victor Jhampier Caxi Maquera
# * Email/Mobile/Phone    : victorjhampier@gmail.com | 968991*14
# *
# * Creation date         : 01/01/2026
# * 
# **********************************************************************************************************

# ----- Start Coroutine -----
@asynccontextmanager
async def lifespan(app: FastAPI):    
    # Add Memory listener
    await MemoryListenerSetting.add_services()

    # Add Application layer
    CoreApplicationSetting()

    # Add Kafka consumer
    # my_consumers = KafkaConsumerSetting()
    # await my_consumers.add_services()
    
    try:
        yield
    finally:
        pass
        # await my_consumers.stop_services()

app = FastAPI(docs_url="/docs/openapi", redoc_url="/docs/reopenapi", lifespan=lifespan)
app.title = "Arify Business API"
app.version = "3.0"

@app.get("/")
def default() -> dict[str, str]:
    return {"Info":"Arify Labs All rights reserved" }

@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/health/ready")
def readiness() -> dict[str, str]:
    return {"status": "ready"}

@app.get("/health")
def health() -> dict[str, str]:
    # TODO:
    # Debe llamarse a un caso de uso que verifique la salud de las dependencias
    return {"status": "ok"}

# Add Example APIs
app.include_router(BianExampleController().ApiRouter, prefix="/business-api-b/v1/bian")
app.include_router(NoBianExampleController().ApiRouter, prefix="/business-api-b/v1/no-bian")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")