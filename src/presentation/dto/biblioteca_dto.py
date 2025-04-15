from pydantic import BaseModel
from typing import Optional
from datetime import date

class BibliotecaDTO(BaseModel):
    titulo:str
    autor:str
    imagen: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    edicion:str
    id_tipo:Optional[int] = None
    id_usuario: Optional[int] = None
    fuente:str
    enlace:str

class BibliotecaUpdateDTO(BaseModel):
    titulo:str
    autor:str
    imagen: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    edicion:str
    id_tipo:Optional[int] = None
    id_usuario: Optional[int] = None
    fuente:str
    enlace:str

