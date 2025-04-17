from pydantic import BaseModel
from typing import Optional
from datetime import date

class HistoriaPostDTO(BaseModel):
    titulo: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: date
    imagen: str
    id_ubicacion: Optional[int] = None
    id_categoria: Optional[int] = None

class HistoriaDTO(BaseModel):
    titulo: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: date
    imagen: str
    id_ubicacion: Optional[int] = None
    nombre_ubicacion: Optional[str] = None
    id_categoria: Optional[int] = None
    nombre_categoria: Optional[str] = None

class HistoriaUpdateDTO(BaseModel):
    titulo: str
    descripcion: str
    fecha_inicio: date
    fecha_fin: date
    imagen: str
    id_ubicacion: Optional[int] = None
    id_categoria: Optional[int] = None
