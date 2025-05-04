from pydantic import BaseModel
from typing import Optional

class TipoEventoDTO(BaseModel):
    nombre_evento: str