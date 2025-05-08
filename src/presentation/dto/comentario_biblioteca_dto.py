from pydantic import BaseModel
from typing import Optional
from datetime import date

class ComentarioBibliotecaDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_biblioteca: Optional[int] = None


class ComentarioDatosBibliotecaDTO(BaseModel):
    id_comentario: Optional[int] = None
    id_biblioteca: Optional[int] = None
    id_usuario: Optional[int] = None
    contenido: Optional[str] = None
    fecha_creacion: Optional[date] = None

    