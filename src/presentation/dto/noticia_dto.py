from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticiaDTO(BaseModel):
    titulo: str
    resumen: str
    contenido: str
    imagen: Optional[str] = None
    id_Categoria: Optional[str] = None
    id_usuario: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
class NoticiaUpdateDTO(BaseModel):
    titulo: str
    resumen: str
    contenido: str
    imagen: Optional[str] = None
    id_Categoria: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None