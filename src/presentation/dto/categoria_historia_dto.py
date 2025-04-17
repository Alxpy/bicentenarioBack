from pydantic import BaseModel
from typing import Optional

class CategoriaHistoriaDTO(BaseModel):
    nombre: str
    descripcion: str
