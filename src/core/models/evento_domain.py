from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class EventoDomain(BaseModel):
    id: Optional[int]=None
    nombre: str
    descripcion: str
    imagen: str
    fecha_inicio: datetime
    fecha_fin: datetime
    id_tipo_evento: Optional[int] = None
    nombre_evento: Optional[str] = None
    id_ubicacion: Optional[int] = None
    nombre_ubicacion: Optional[str] = None
    id_usuario: Optional[int] = None
    nombre_usuario: Optional[str] = None
