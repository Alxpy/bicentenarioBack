from pydantic import BaseModel
from typing import Optional

class UsuarioEventoDTO(BaseModel):
    id_usuario: int
    id_evento: int
    asistio: Optional[bool] = None

class UsuarioEventoData(BaseModel):
    nombre: str
    apellidoPaterno:str 
    apellidoMaterno:str
    nombre_evento: str
    asistio: Optional[bool] = None
class UpdateAsistioUsuarioEventoDTO(BaseModel):
    asistio: bool

