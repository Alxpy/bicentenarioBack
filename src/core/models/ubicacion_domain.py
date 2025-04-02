from pydantic import BaseModel
from typing import Optional

class UbicacionDomain(BaseModel):
    id: Optional[int] = None
    nombre: str
    latitud: float
    longitud: float
    imagen: str
    descripcion: str
    
