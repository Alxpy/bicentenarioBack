from pydantic import BaseModel
from typing import Optional

class UsuarioRolDTO(BaseModel):
    id_usuario: int
    id_rol: int
    
class UsuarioRolDataDTO(BaseModel):
    id_usuario: int
    id_rol: int
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str