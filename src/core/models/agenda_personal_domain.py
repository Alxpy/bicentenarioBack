from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgendaPersonalDomain(BaseModel):
    id: Optional[int] = None
    id_usuario: Optional[int] = None
    id_evento: Optional[int] = None
    nombre_evento:str
    recordatorio: datetime
    notas:str


