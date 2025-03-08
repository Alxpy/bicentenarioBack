from pydantic import BaseModel
from typing import Optional

class UsuarioDto(BaseModel):
    id: Optional[int]
    nome: str
    apellidoPaterno: str
    apellidoMaterno: str
    correo: str
    contrasena: str
    genero: str
    telefono: str
    pais: str
    ciudad: str
    estado:bool
    id_rol: int
