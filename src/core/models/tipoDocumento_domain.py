from pydantic import BaseModel
from typing import Optional

class TipoDocumentoDomain(BaseModel):
    id: Optional[int] = None
    tipo: str