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
    estado:Optional[int] = None
    roles: Optional[list[str]] = None
    email_verified_at: Optional[datetime] = None
    codeValidacion: Optional[str] = None
    cantIntentos: Optional[int] = None
    ultimoIntentoFallido: Optional[datetime] = None

    
    

