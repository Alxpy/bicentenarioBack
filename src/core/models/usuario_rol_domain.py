from pydantic import BaseModel
from typing import Optional

class UsuarioRolDomain(BaseModel):
    id_usuario: Optional[bool] = None
    id_rol: Optional[int] = None