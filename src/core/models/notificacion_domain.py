from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificacionDomain(BaseModel):
    titulo: str
    mensaje: str
    fecha_envio: datetime
    id_evento: Optional[int] = None
    nombre_evento: Optional[str] = None
    id_usuario: Optional[int] = None
    