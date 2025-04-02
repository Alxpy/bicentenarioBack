from pydantic import BaseModel
from typing import Optional

class TipoDocumentoDTO(BaseModel):
    tipo: str
