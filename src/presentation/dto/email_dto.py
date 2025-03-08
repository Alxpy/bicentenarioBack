from pydantic import BaseModel

class EmailDTO(BaseModel):
    email: str
    
