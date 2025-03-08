from pydantic import BaseModel

class AuthLoginDTO(BaseModel):
    correo: str
    contrasena: str
    
class AuthLogoutDTO(BaseModel):
    token: str

class AuthVerifyCodeDTO(BaseModel):
    email: str
    code: str