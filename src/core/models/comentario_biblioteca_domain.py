from pydantic import BaseModel
from typing import Optional

class ComentarioBibliotecaDomain(BaseModel):
    id_comentario: Optional[int] = None
    id_biblioteca: Optional[int] = None
    

