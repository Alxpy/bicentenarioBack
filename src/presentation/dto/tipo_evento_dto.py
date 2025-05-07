from pydantic import BaseModel
from typing import Optional

class TipoEventoDTO(BaseModel):
    id: Optional[int]
    nombre_evento: str