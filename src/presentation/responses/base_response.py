from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Response(BaseModel, Generic[T]):
    status: int
    success: bool
    message: str
    data: Optional[T] = None
