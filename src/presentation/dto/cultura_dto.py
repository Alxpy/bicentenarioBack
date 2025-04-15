from pydantic import BaseModel
from typing import Optional

class CulturaDTO(BaseModel):    
    nombre: str
    imagen: str
    descripcion: str
    id_ubicacion: Optional[int] = None
    
