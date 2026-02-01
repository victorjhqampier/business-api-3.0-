from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TransactionEntity(BaseModel):
    transaction_id: str = Field(..., description="ID único de la transacción")
    timestamp: datetime = Field(default_factory=datetime.now(), description="Fecha y hora de la transacción")
    buyer: str = Field(..., description="Nombre o ID del comprador")
    item: str = Field(..., description="Descripción del bien adquirido")
    amount: float = Field(..., description="Monto de la transacción")
    currency: str = Field(..., description="Moneda de la transacción (por ejemplo, USD, EUR)")
    metadata: Optional[dict] = Field(None, description="Información adicional sobre la transacción (opcional)")
