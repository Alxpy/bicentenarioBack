from pydantic import BaseModel
from typing import Optional
from datetime import date

class PresidenteDomain(BaseModel):
    id: Optional[int] = None
    id_usuario: Optional[int] = None
    nombre: str
    apellido: str
    imagen: str
    inicio_periodo: date
    fin_periodo: date
    bibliografia: str
    partido_politico: str
    principales_politicas: str
    