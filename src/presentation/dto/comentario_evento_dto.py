from pydantic import BaseModel
from typing import Optional

class ComentarioEventoDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_evento: Optional[int] = None

class ComentarioDatosEventoDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_evento: Optional[int] = None
    id_usuario: Optional[int] = None
    contenido: Optional[str] = None
    fecha_creacion: Optional[str] = None