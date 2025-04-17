from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.cultura_service_abstract import ICulturaService
from src.core.dependency_injection.dependency_injection import build_cultura_service
from src.presentation.dto.cultura_dto import CulturaDTO
from src.core.models.cultura_domain import CulturaDomain
from src.presentation.responses.base_response import Response

culture_controller = APIRouter(prefix="/api/v1/cultures", tags=["cultures"])

@culture_controller.post("", response_model=Response[None])
async def create_culture(
    culture_dto: CulturaDTO,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.create_cultura(culture_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.get("", response_model=Response[list[CulturaDomain]])
async def get_all_cultures(
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_all_culturas()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.get("/{id}", response_model=Response[CulturaDomain])
async def get_culture_by_id(
    id: int,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.get("/byName/{name}", response_model=Response[CulturaDomain])
async def get_culture_by_name(
    name: str,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_nombre(name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.get("/byLocation/{location}", response_model=Response[CulturaDomain])
async def get_culture_by_location(
    location: str,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.get_cultura_by_ubicacion(location)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.put("/{id}", response_model=Response[None])
async def update_culture(
    id: int,
    culture_dto: CulturaDTO,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.update_cultura(id, culture_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@culture_controller.delete("/{id}", response_model=Response[None])
async def delete_culture(
    id: int,
    culture_service: ICulturaService = Depends(build_cultura_service)
):
    try:
        return await culture_service.delete_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
