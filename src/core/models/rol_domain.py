from pydantic import BaseModel

class RolDomain(BaseModel):
    id: int
    nombre_rol: str
    descripcion: str