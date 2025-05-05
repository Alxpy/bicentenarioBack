from abc import ABC, abstractmethod
from src.presentation.dto.patrocinador_dto import PatrocinadorCreateDTO
from src.presentation.responses.base_response import Response
class IPatrocinadorServiceAbstract(ABC):
    
    @abstractmethod
    async def create(self, patrocinador: PatrocinadorCreateDTO) -> Response:
        pass
    
    @abstractmethod
    async def get_all(self)-> Response:
        pass
    
    