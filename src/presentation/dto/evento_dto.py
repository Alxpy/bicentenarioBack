from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventoPostDTO(BaseModel):
    nombre: str
    descripcion: str
    imagen: str
    fecha_inicio: datetime
    fecha_fin: datetime
    id_tipo_evento: Optional[int] = None
    id_ubicacion: Optional[int] = None
    id_usuario: Optional[int] = None
    id_organizador: Optional[int] = None
    categoria: Optional[str] = None
    enlace: Optional[str] = None
    precio: Optional[float] = None

class EventoDTO(BaseModel):
    id: Optional[int] = None
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

class EventoUpdateDTO(BaseModel):
    nombre: str
    descripcion: str
    imagen: str
    fecha_inicio: datetime
    fecha_fin: datetime
    id_tipo_evento: Optional[int] = None
    id_ubicacion: Optional[int] = None
    id_usuario: Optional[int] = None