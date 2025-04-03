from pydantic import BaseModel
from typing import Optional

class TipoDocumentoDomain(BaseModel):
    id_tipo: Optional[int] = None
    tipo: str