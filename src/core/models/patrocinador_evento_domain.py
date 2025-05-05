from pydantic import BaseModel

class PatrocinadorEvento(BaseModel):
    id_evento: int
    id_patrocinador: int