from pydantic import BaseModel
from typing import Optional

class CulturaDomain(BaseModel):
    id: Optional[int] = None
    nombre: str
    imagen: str
    descripcion: str
    id_ubicacion: Optional[int] = None
    nombre_ubicacion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
