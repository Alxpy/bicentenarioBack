from src.core.models.agenda_personal_domain import AgendaPersonalDomain
from src.presentation.dto.agenda_personal_dto import AgendaPersonalDTO, AgendaPersonalUpdateDTO

def map_agenda_personal_domain_to_dto(agenda_personal: AgendaPersonalDomain) -> AgendaPersonalDTO:
    return AgendaPersonalDTO(
        id=0,
        id_usuario=agenda_personal.id_usuario,
        id_evento=agenda_personal.id_evento,
        recordatorio=agenda_personal.recordatorio,
        notas=agenda_personal.notas
    )