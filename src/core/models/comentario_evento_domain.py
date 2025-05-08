from pydantic import BaseModel
from typing import Optional

class ComentarioEventoDomain(BaseModel):
    id_comentario: Optional[int] = None
    id_evento: Optional[int] = None
    