from pydantic import BaseModel
from typing import Optional

class CategoriaNoticiaDomain(BaseModel):
    id: Optional[int] = None
    nombre_categoria: str
    