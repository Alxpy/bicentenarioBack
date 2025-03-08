from pydantic import BaseModel
from typing import Optional

class UsuarioDTO(BaseModel):
    id: Optional[int]
    nombre: str
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

class UpdateDataUserDTO(BaseModel):
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    correo: str
    genero: str
    telefono: str
    pais: str
    ciudad: str
    estado:bool

class ChangeRoleUserDTO(BaseModel):
    id_rol: int

class ChangePasswordUserDTO(BaseModel):
    contrasena: str
    nueva_contrasena: str