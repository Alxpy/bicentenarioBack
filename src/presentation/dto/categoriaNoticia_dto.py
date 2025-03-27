from pydantic import BaseModel
from typing import Optional

class CategoriaNoticiaDTO(BaseModel):
    nombre_categoria: str