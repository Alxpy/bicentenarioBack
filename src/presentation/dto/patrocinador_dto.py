from pydantic import BaseModel
from typing import Optional

class PatrocinadorCreateDTO(BaseModel):
    nombre: str
    imagen: str
    contacto: str
    
