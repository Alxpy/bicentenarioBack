from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.ubicacion_service_abstract import IUbicacionService
from src.core.dependency_injection.dependency_injection import build_ubicacion_service
from src.presentation.dto.ubicacion_dto import UbicacionDTO
from src.core.models.ubicacion_domain import UbicacionDomain
from src.presentation.responses.base_response import Response

location_router = APIRouter(
    prefix="/api/v1/location",
    tags=["location"]
)

@location_router.post("", response_model=Response[None], summary="Create a new location")
async def create_location(
    location: UbicacionDTO,
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Creates a new location entry in the database.
    """
    try:
        return await location_service.create_ubicacion(location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@location_router.get("", response_model=Response[list[UbicacionDomain]], summary="Get all locations")
async def get_all_locations(
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Retrieves a list of all registered locations.
    """
    try:
        return await location_service.get_all_ubicaciones()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@location_router.get("/{id}", response_model=Response[UbicacionDomain], summary="Get location by ID")
async def get_location_by_id(
    id: int,
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Retrieves a specific location by its ID.
    """
    try:
        return await location_service.get_ubicacion_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@location_router.get("/byName/{name}", response_model=Response[UbicacionDomain], summary="Get location by name")
async def get_location_by_name(
    name: str,
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Retrieves a specific location by its name.
    """
    try:
        return await location_service.get_ubicacion_by_name(name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@location_router.put("/{id}", response_model=Response[None], summary="Update a location by ID")
async def update_location(
    id: int,
    location_update: UbicacionDTO,
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Updates the details of a location based on its ID.
    """
    try:
        return await location_service.update_ubicacion(id, location_update)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@location_router.delete("/{id}", response_model=Response[None], summary="Delete a location by ID")
async def delete_location(
    id: int,
    location_service: IUbicacionService = Depends(build_ubicacion_service)):
    """
    Deletes a location based on its ID.
    """
    try:
        return await location_service.delete_ubicacion(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
