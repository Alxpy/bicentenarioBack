from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.role_service_abstract import IRolSerice
from src.core.dependency_injection.dependency_injection import build_rol_service

rol_controller = APIRouter(prefix="/api/v1/rol", tags=["rol"])

@rol_controller.get("/")
async def get_all_roles(
    rol_service: IRolSerice = Depends(build_rol_service)
):
    try:
        return await rol_service.get_all_roles()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))