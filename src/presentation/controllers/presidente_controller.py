from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.presidente_service_abstract import IPresidenteService
from src.core.dependency_injection.dependency_injection import build_presidente_service
from src.presentation.dto.presidente_dto import PresidenteDTO
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.responses.base_response import Response

president_router = APIRouter(
    prefix="/api/v1/president",
    tags=["president"]
)

@president_router.post("", response_model=Response[None])
async def create_president(
    president: PresidenteDTO,
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Create a new president.
    """
    try:
        return await president_service.create_presidente(president)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@president_router.get("", response_model=Response[list[PresidenteDomain]])
async def get_all_presidents(
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Retrieve a list of all presidents.
    """
    try:
        return await president_service.get_all_presidentes()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@president_router.get("/{id}", response_model=Response[PresidenteDomain])
async def get_president_by_id(
    id: int,
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Retrieve a president by their ID.
    """
    try:
        return await president_service.get_presidente_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@president_router.get("/ByName/{name}", response_model=Response[PresidenteDomain])
async def get_president_by_name(
    name: str,
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Retrieve a president by their name.
    """
    try:
        return await president_service.get_presidente_by_nombre(name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@president_router.put("/{id}", response_model=Response[None])
async def update_president(
    id: int,
    president: PresidenteDTO,
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Update an existing president by ID.
    """
    try:
        return await president_service.update_presidente(id, president)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@president_router.delete("/{id}", response_model=Response[None])
async def delete_president(
    id: int,
    president_service: IPresidenteService = Depends(build_presidente_service)
):
    """
    Delete a president by ID.
    """
    try:
        return await president_service.delete_presidente(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
