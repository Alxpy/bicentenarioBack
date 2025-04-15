from pydantic import BaseModel
from typing import Optional
from datetime import date

class BibliotecaDomain(BaseModel):
    id: Optional[int] = None
    titulo:str
    autor:str
    imagen: Optional[str] = None
    fecha_publicacion: Optional[date] = None
    edicion:str
    id_usuario: Optional[int] = None
    id_tipo:Optional[int] = None
    tipo:Optional[str] = None
    fuente:str
    enlace:str