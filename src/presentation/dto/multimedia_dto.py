from pydantic import BaseModel
from typing import Optional

class MultimediaDTO(BaseModel):
    enlace: str
    tipo: str

