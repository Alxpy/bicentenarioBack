from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.patrosinador_service_abstrac import IPatrocinadorServiceAbstract
from src.core.dependency_injection.dependency_injection import build_patrocinador_service
from src.presentation.dto.patrocinador_dto import PatrocinadorCreateDTO
from src.core.models.patrocinador_domain import PatrocinadorDomain
from src.presentation.responses.base_response import Response

patrocinador_router = APIRouter(
    prefix="/api/v1/patrocinadores",
    tags=["Patrocinadores"],
    responses={404: {"description": "Patrocinador not found"}}
)

@patrocinador_router.post(
    "",
    response_model=Response[PatrocinadorDomain],
    summary="Crear patrocinador",
    description="Crea un nuevo patrocinador en la base de datos."
)
async def create_patrocinador(patrocinador: PatrocinadorCreateDTO, patrocinador_service: IPatrocinadorServiceAbstract = Depends(build_patrocinador_service)):
    try:
        return await patrocinador_service.create(patrocinador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@patrocinador_router.get(
    "",
    response_model=Response[list[PatrocinadorDomain]],
    summary="Listar patrocinadores",
    description="Obtiene una lista de todos los patrocinadores."
)
async def get_patrocinadores(patrocinador_service: IPatrocinadorServiceAbstract = Depends(build_patrocinador_service)):
    try:
        return await patrocinador_service.get_all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    