from pydantic import BaseModel

class AuthLoginDTO(BaseModel):
    email: str
    password: str
    
class AuthLogoutDTO(BaseModel):
    token: str

class AuthVerifyCodeDTO(BaseModel):
    email: str
    code: str