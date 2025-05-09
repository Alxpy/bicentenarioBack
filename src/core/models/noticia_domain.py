from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoticiaDomain(BaseModel):
    id: Optional[int] = None
    titulo: str
    resumen: str
    contenido: str
    imagen: Optional[str] = None
    id_Categoria: Optional[int] = None
    id_usuario: Optional[int] = None
    nombre_usuario: Optional[str] = None
    nombre_categoria: Optional[str] = None
    fecha_publicacion: Optional[datetime] = None
    

    

