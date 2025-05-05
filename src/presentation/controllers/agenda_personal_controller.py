from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.agenda_personal_service_abstract import IAgendaPersonalService
from src.core.dependency_injection.dependency_injection import build_agenda_personal_service
from src.presentation.dto.agenda_personal_dto import AgendaPersonalDTO, AgendaPersonalUpdateDTO
from src.core.models.agenda_personal_domain import AgendaPersonalDomain
from src.presentation.responses.base_response import Response


agenda_personal_router = APIRouter(
    prefix="/api/v1/agenda_personal",
    tags=["Agenda Personal"],
    responses={404: {"description": "Not found"}}
)

@agenda_personal_router.post(
    "",
    response_model=Response[None],
    summary="Crear agenda personal",
    description="Crea una nueva entrada en la agenda personal."
)
async def create_agenda_personal(
    agenda_personal_dto: AgendaPersonalDTO,
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.create_agenda_personal(agenda_personal_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@agenda_personal_router.get(
    "",
    response_model=Response[list[AgendaPersonalDomain]],
    summary="Listar todas las agendas personales",
    description="Obtiene una lista completa de todas las entradas en la agenda personal."
)
async def get_all_agendas_personales(
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.get_all_agendas_personales()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@agenda_personal_router.get(
    "/{id}",
    response_model=Response[AgendaPersonalDomain],
    summary="Obtener agenda personal por ID",
    description="Obtiene información detallada sobre una entrada específica en la agenda personal utilizando su identificador único."
)
async def get_agenda_personal_by_user(
    id: int,
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.get_agenda_personal_by_user(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@agenda_personal_router.get(
    "/fecha/{fecha}",
    response_model=Response[AgendaPersonalDomain],
    summary="Obtener agenda personal por fecha y usuario",
    description="Obtiene una entrada específica en la agenda personal utilizando su fecha y el ID del usuario."
)
async def get_agenda_personal_by_fecha_user(
    fecha: str,
    id: int,
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.agenda_personal_by_fecha_user(fecha, id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@agenda_personal_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Actualizar agenda personal",
    description="Modifica una entrada existente en la agenda personal."
)
async def update_agenda_personal(
    id: int,
    agenda_personal_dto: AgendaPersonalUpdateDTO,
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.update_agenda_personal(id, agenda_personal_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@agenda_personal_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Eliminar agenda personal",
    description="Elimina una entrada específica en la agenda personal utilizando su identificador único."
)
async def delete_agenda_personal(
    id: int,
    agenda_personal_service: IAgendaPersonalService = Depends(build_agenda_personal_service)
):
    try:
        return await agenda_personal_service.delete_agenda_personal(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    