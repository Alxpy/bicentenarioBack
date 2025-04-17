from pydantic import BaseModel
from typing import Optional

class UsuarioDTO(BaseModel):
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    correo: str
    contrasena: str
    genero: str
    telefono: str
    pais: str
    ciudad: str

class UpdateDataUserDTO(BaseModel):
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    correo: str
    genero: str
    telefono: str
    pais: str
    ciudad: str

class ChangeRoleUserDTO(BaseModel):
    id_rol: int

class ChangePasswordUserDTO(BaseModel):
    contrasena: str
    nueva_contrasena: str

class NewPasswordDTO(BaseModel):
    correo: str
    code: str
    nueva_contrasena: str