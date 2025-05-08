from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class ComentarioDTO(BaseModel):
    id: Optional[int] = None
    id_usuario: int
    contenido: str
    fecha_creacion: date


class ComentarioUpdateDTO(BaseModel):    
    contenido: str
    fecha_creacion: date

class ComentarioResponseCreate(BaseModel):
    id: int
