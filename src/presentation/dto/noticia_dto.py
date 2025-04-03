from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticiaDTO(BaseModel):
    titulo: str
    resumen: str
    contenido: str
    imagen: Optional[str] = None
    idCategoria: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    

