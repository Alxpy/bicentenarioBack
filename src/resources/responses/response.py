from pydantic import BaseModel
from typing import Optional

class Response(BaseModel):
    status: int # 200, 400, 404, 500
    success: bool # True, False
    message: str # "Success", "Bad Request", "Not Found", "Internal Server Error", other
    data: Optional[object] = None # regresa los datos solicitados por el usuario
    