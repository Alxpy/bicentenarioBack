from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class ComentarioDomain(BaseModel):
    id: Optional[int] = None
    id_usuario: int
    nombre:Optional[str] = None
    apellidoPaterno:Optional[str] = None
    apellidoMaterno:Optional[str] = None
    contenido: str
    fecha_creacion: date

    

