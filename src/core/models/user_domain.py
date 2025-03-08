# Domain Model
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuarioDomain(BaseModel):
    id: Optional[int] = None
    nombre: str
    apellidoPaterno: str
    apellidoMaterno: str
    correo: str
    contrasena: Optional[str] = None
    genero: str
    telefono: str
    pais: str
    ciudad: str
    estado:int
    id_rol: Optional[int] = None
    email_verfied_at: datetime
    codeValidation: Optional[str] = None
    cantIntentos: Optional[int] = None


    
    

