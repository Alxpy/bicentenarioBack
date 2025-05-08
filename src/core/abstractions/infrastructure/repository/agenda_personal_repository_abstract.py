from abc import ABC, abstractmethod
from src.core.models.agenda_personal_domain import AgendaPersonalDomain
from src.presentation.dto.agenda_personal_dto import *
from src.resources.responses.response import Response

class IAgendaPersonalRepository(ABC):
    @abstractmethod
    async def get_agenda_personal_by_user(self, id: int) -> Response:
        """Retrieve a personal agenda entry by its ID."""
        pass

    @abstractmethod
    async def get_all_agendas_personales(self) -> Response:
        """Retrieve all personal agenda entries."""
        pass

    @abstractmethod
    async def agenda_personal_by_fecha_user(self, fecha: str, id: int) -> Response:
        """Retrieve a personal agenda entry by date and user ID."""
        pass

    @abstractmethod
    async def create_agenda_personal(self, agenda_personal: AgendaPersonalDTO) -> None:
        """Create a new personal agenda entry."""
        pass

    @abstractmethod
    async def update_agenda_personal(self, id: int, agenda_personal: AgendaPersonalUpdateDTO) -> None:
        """Update an existing personal agenda entry."""
        pass

    @abstractmethod
    async def delete_agenda_personal(self, id: int) -> None:
        """Delete a personal agenda entry by its ID."""
        pass