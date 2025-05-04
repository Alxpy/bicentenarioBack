from pydantic import BaseModel
from typing import Optional

class TipoEventoDomain(BaseModel):
    id: Optional[int] = None
    nombre_evento: str