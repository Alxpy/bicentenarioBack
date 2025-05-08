from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgendaPersonalDTO(BaseModel):
    id_usuario: Optional[int] = None
    id_evento: Optional[int] = None
    recordatorio: datetime
    notas:str

class AgendaPersonalUpdateDTO(BaseModel):
    recordatorio: datetime
    notas:str
    
