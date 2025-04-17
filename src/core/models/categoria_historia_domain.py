from pydantic import BaseModel
from typing import Optional

class CategoriaHistoriaDomain(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str