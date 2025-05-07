from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.evento_service_abstract import IEventoService
from src.core.dependency_injection.dependency_injection import build_evento_service
from src.presentation.dto.evento_dto import EventoPostDTO, EventoUpdateDTO
from src.presentation.responses.base_response import Response
from src.core.models.evento_domain import EventoDomain


evento_router = APIRouter(
    prefix="/api/v1/evento",
    tags=["Evento"]
)

@evento_router.post(
    "",
    response_model=Response[EventoDomain],
    summary="Create a new event",
    description="Adds a new event with its name, description, image, start date, end date, location, and associated category."
)
async def create_evento(
    evento: EventoPostDTO,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.create_evento(evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@evento_router.get(
    "",
    response_model=Response[list[EventoDomain]],
    summary="List all events",
    description="Retrieves a list of all events stored in the system."
)

async def get_eventos(
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_all_eventos()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@evento_router.get(
    "/{id}",
    response_model=Response[EventoDomain],
    summary="Get event by ID",
    description="Fetches a specific event using its unique identifier."
)
async def get_evento_by_id(
    id: int,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@evento_router.get(
    "/organizer/{organizador}",
    response_model=Response[EventoDomain],
    summary="Get event by organizer",
    description="Fetches a specific event using its organizer."
)
async def get_evento_by_organizador(
    organizador: str,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_organizador(organizador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@evento_router.get(
    "/name/{nombre}",
    response_model=Response[EventoDomain],
    summary="Get event by name",
    description="Fetches a specific event using its name."
)
async def get_evento_by_nombre(
    nombre: str,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_nombre(nombre)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@evento_router.get(
    "/date/{fecha}",
    response_model=Response[EventoDomain],
    summary="Get event by date",
    description="Fetches a specific event using its start date."
)
async def get_evento_by_fecha(
    fecha: str,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_fecha(fecha)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@evento_router.get(
    "/type/{tipo}",
    response_model=Response[EventoDomain],
    summary="Get event by type",
    description="Fetches a specific event using its type."
)
async def get_evento_by_tipo(
    tipo: str,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_tipo(tipo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@evento_router.get(
    "/location/{ubicacion}",
    response_model=Response[EventoDomain],
    summary="Get event by location",
    description="Fetches a specific event using its location."
)
async def get_evento_by_ubicacion(
    ubicacion: str,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.get_evento_by_ubicacion(ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@evento_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update an event",
    description="Updates an existing event with its name, description, image, start date, end date, location, and associated category."
)
async def update_evento(
    id: int,
    evento: EventoUpdateDTO,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.update_evento(id, evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@evento_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete an event",
    description="Removes an event from the system using its unique identifier."
)
async def delete_evento(
    id: int,
    evento_service: IEventoService = Depends(build_evento_service)
):
    try:
        return await evento_service.delete_evento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
