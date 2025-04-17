from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_cultura_service_abstract import IMultimediaCulturaService
from src.core.dependency_injection.dependency_injection import build_multimedia_cultura_service
from src.presentation.dto.multimedia_cultura_dto import MultimediaCulturaDTO, MultimediaDatosCulturaDTO
from src.presentation.responses.base_response import Response

multimedia_cultura_router = APIRouter(
    prefix="/api/v1/multimedia_cultura",
    tags=["multimedia_cultura"]
)

@multimedia_cultura_router.post("", response_model=Response[None], summary="Create multimedia entry for culture")
async def create_multimedia_cultura(
    multimedia_cultura: MultimediaCulturaDTO,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    """
    Creates a new multimedia entry associated with a cultural element.
    """
    try:
        return await multimedia_cultura_service.create_multimedia_cultura(multimedia_cultura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_cultura_router.get("", response_model=Response[list[MultimediaDatosCulturaDTO]], summary="Get all multimedia for culture")
async def get_all_multimedia_cultura(
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    """
    Retrieves all multimedia entries related to culture.
    """
    try:
        return await multimedia_cultura_service.get_all_multimedia_cultura()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_cultura_router.get("/byCulturaId/{id}", response_model=Response[list[MultimediaDatosCulturaDTO]], summary="Get multimedia by culture ID")
async def get_multimedia_cultura_by_id(
    id: int,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    """
    Retrieves all multimedia entries associated with a specific culture by its ID.
    """
    try:
        return await multimedia_cultura_service.get_multimedia_cultura_by_id_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_cultura_router.delete("/{id}", response_model=Response[None], summary="Delete multimedia entry by ID")
async def delete_multimedia_cultura(
    id: int,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    """
    Deletes a multimedia entry by its ID.
    """
    try:
        return await multimedia_cultura_service.delete_multimedia_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
