from pydantic import BaseModel
from typing import Optional

class MultimediaDomain(BaseModel):
    id: Optional[int] = None
    enlace : str
    tipo: str
