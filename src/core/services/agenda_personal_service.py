from src.core.abstractions.infrastructure.repository.agenda_personal_repository_abstract import IAgendaPersonalRepository
from src.core.abstractions.services.agenda_personal_service_abstract import IAgendaPersonalService
from src.core.models.agenda_personal_domain import AgendaPersonalDomain
from src.presentation.dto.agenda_personal_dto import AgendaPersonalDTO, AgendaPersonalUpdateDTO
from src.resources.responses.response import Response

class AgendaPersonalService(IAgendaPersonalService):

    def __init__(self, agenda_personal_repository: IAgendaPersonalRepository):
        self.agenda_personal_repository = agenda_personal_repository
    
    async def get_agenda_personal_by_user(self, id: int) -> Response:
        return await self.agenda_personal_repository.get_agenda_personal_by_user(id)
    
    async def get_all_agendas_personales(self) -> Response:
        return await self.agenda_personal_repository.get_all_agendas_personales()
    
    async def agenda_personal_by_fecha_user(self, fecha: str, id: int) -> Response:
        return await self.agenda_personal_repository.agenda_personal_by_fecha_user(fecha, id)
    
    async def create_agenda_personal(self, agenda_personal: AgendaPersonalDTO) -> None:
        return await self.agenda_personal_repository.create_agenda_personal(agenda_personal)
    
    async def update_agenda_personal(self, id: int, agenda_personal: AgendaPersonalUpdateDTO) -> None:
        return await self.agenda_personal_repository.update_agenda_personal(id, agenda_personal)
    
    async def delete_agenda_personal(self, id: int) -> None:
        return await self.agenda_personal_repository.delete_agenda_personal(id)