from Domain.Entities.Blockchain.TransactionEntity import TransactionEntity
from pydantic import BaseModel, Field, Optional
from typing import List
from datetime import datetime

class BlockEntity(BaseModel):
    index: int = Field(..., description="Número del bloque en la cadena")
    timestamp: datetime = Field(default_factory=datetime.now(), description="Fecha y hora de creación del bloque")
    transactions: Optional[TransactionEntity] = Field(..., description="Lista de transacciones incluidas en el bloque")
    previous_hash: str = Field(..., description="Hash del bloque anterior")
    nonce: int = Field(..., description="Número utilizado para la prueba de trabajo")
    hash: str = Field(..., description="Hash del bloque actual")