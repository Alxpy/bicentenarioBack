from pydantic import BaseModel
from typing import Optional

class ExpositorCreate(BaseModel):
    nombre: Optional[str] = None
