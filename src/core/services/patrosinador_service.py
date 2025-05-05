from src.core.abstractions.infrastructure.repository.patrosinador_repository_abstrac import IPatrocinadorRepositoryAbstract
from src.core.abstractions.services.patrosinador_service_abstrac import IPatrocinadorServiceAbstract
from src.presentation.dto.patrocinador_dto import PatrocinadorCreateDTO



class PatrocinadorService(IPatrocinadorServiceAbstract):
    
    def __init__(self, patrocinador_repository: IPatrocinadorRepositoryAbstract):
        self.patrocinador_repository = patrocinador_repository

    async def create(self, patrocinador: PatrocinadorCreateDTO):
        return await self.patrocinador_repository.create(patrocinador)
    
    
    async def get_all(self):
        return await self.patrocinador_repository.get_all()
    
    