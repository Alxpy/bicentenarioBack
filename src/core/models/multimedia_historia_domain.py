from pydantic import BaseModel
from typing import Optional

class  MultimediaHistoriaDomain(BaseModel):
    id_multimedia: Optional[int] = None
    id_historia: Optional[int] = None
    