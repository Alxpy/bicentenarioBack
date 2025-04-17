from pydantic import BaseModel
from typing import Optional


class MultimediaCulturaDomain(BaseModel):
    id_multimedia: Optional[int] = None
    id_cultura: Optional[int] = None
    