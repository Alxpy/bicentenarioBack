from pydantic import BaseModel
from typing import Optional, List

class PatrocinadorDomain(BaseModel):
    id: Optional[int] = None
    nombre: str
    imagen: str
    contacto: str