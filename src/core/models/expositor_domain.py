from pydantic import BaseModel
from typing import Optional

class ExpositorDomain(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
