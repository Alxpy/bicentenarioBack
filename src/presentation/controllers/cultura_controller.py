from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.cultura_service_abstract import ICulturaService
from src.core.dependency_injection.dependency_injection import build_cultura_service
from src.presentation.dto.cultura_dto import CulturaDTO
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.responses.base_response import Response

culture_router = APIRouter(
    prefix="/api/v1/cultures",
    tags=["Cultural"],
    responses={404: {"description": "Cultural item not found"}}
)

@culture_router.post(
    "",
    response_model=Response[None],
    summary="Create cultural record",
    description="Adds a new cultural item to the database with all relevant information."
)
async def create_culture(
    culture_dto: CulturaDTO,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.create_cultura(culture_dto)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create cultural record: {str(e)}"
        )

@culture_router.get(
    "",
    response_model=Response[list[CulturaDomain]],
    summary="List all cultural items",
    description="Retrieves a complete catalog of all cultural records in the system."
)
async def get_all_cultures(
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_all_culturas()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to retrieve cultural records: {str(e)}"
        )

@culture_router.get(
    "/{id}",
    response_model=Response[CulturaDomain],
    summary="Get cultural item by ID",
    description="Retrieves detailed information about a specific cultural item using its unique identifier."
)
async def get_culture_by_id(
    id: int,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_id(id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cultural item with ID {id} not found: {str(e)}"
        )

@culture_router.get(
    "/by-name/{name}",
    response_model=Response[CulturaDomain],
    summary="Find culture by name",
    description="Searches for a cultural item by its exact name (case-sensitive)."
)
async def get_culture_by_name(
    name: str,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_nombre(name)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Cultural item named '{name}' not found: {str(e)}"
        )

@culture_router.get(
    "/by-location/{location}",
    response_model=Response[CulturaDomain],
    summary="Find cultures by location",
    description="Retrieves cultural items associated with a specific geographic location."
)
async def get_culture_by_location(
    location: str,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_ubicacion(location)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"No cultural items found for location '{location}': {str(e)}"
        )

@culture_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update cultural record",
    description="Modifies the information of an existing cultural item. All fields are optional (partial updates supported)."
)
async def update_culture(
    id: int,
    culture_dto: CulturaDTO,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.update_cultura(id, culture_dto)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to update cultural record: {str(e)}"
        )

@culture_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete cultural record",
    description="Permanently removes a cultural item from the system. Requires administrative privileges."
)
async def delete_culture(
    id: int,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.delete_cultura(id)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete cultural record: {str(e)}"
        )