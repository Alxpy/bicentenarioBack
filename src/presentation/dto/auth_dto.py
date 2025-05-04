from pydantic import BaseModel
from typing import List
from src.core.models.user_domain import UsuarioDomain

class AuthLoginDTO(BaseModel):
    email: str
    password: str
    
class AuthLogoutDTO(BaseModel):
    token: str

class AuthVerifyCodeDTO(BaseModel):
    email: str
    code: str

class AuthenticatedUserDTO(BaseModel):
    nombre: str
    correo: str
    roles: List[str]    

class AuthResponseDTO(BaseModel):
    token: str
    user: UsuarioDomain

