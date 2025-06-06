from pydantic import BaseModel
from typing import Optional
from datetime import date

class ComentarioEventoDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_evento: Optional[int] = None

class ComentarioDatosEventoDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_evento: Optional[int] = None
    id_usuario: Optional[int] = None
    nombre: Optional[str] = None
    contenido: Optional[str] = None
    fecha_creacion: Optional[date] = None