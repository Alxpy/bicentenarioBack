from pydantic import BaseModel
from typing import Optional

class UsuarioEventoDomain(BaseModel):
    id: Optional[int] = None
    id_usuario: int
    id_evento: int
    asistio: Optional[bool] = None


