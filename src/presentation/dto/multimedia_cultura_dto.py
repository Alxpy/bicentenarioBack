from pydantic import BaseModel
from typing import Optional

class MultimediaCulturaDTO(BaseModel):
    id_multimedia: Optional[int] = None
    id_cultura: Optional[int] = None


class MultimediaDatosCulturaDTO(BaseModel):
    id_multimedia: Optional[int] = None
    id_cultura: Optional[int] = None
    enlace: Optional[str] = None
    tipo: Optional[str] = None