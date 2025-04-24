from pydantic import BaseModel
from typing import Optional

class UbicacionDTO(BaseModel):
    nombre: str
    latitud: float
    longitud: float
    imagen: str
    descripcion: str
    
class ResponseUbicacionCreateDTO(BaseModel):
    id: int