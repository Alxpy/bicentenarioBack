from pydantic import BaseModel
from typing import Optional, List
from src.core.models.patrocinador_domain import PatrocinadorDomain

class PatrocinadorEventoByEvento(BaseModel):
    id_evento: int
    id_patrocinador: int
    nombre: str
    imagen: str
    contacto: str