from pydantic import BaseModel
from typing import Optional

class MultimediaHistoriaDTO(BaseModel):
    id_multimedia: Optional[int] = None
    id_historia: Optional[int] = None
    
class MultimediaDatosHistoriaDTO(BaseModel):
    id_multimedia: Optional[int] = None
    id_historia: Optional[int] = None
    enlace: Optional[str] = None
    tipo: Optional[str] = None