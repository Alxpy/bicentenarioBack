from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.auth_service_abstract import IAuthServiceAbstract
from src.core.dependency_injection.dependency_injection import build_auth_service
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO
from fastapi.responses import JSONResponse

auth_controller = APIRouter(prefix="/api/v1", tags=["auth"])

@auth_controller.post("/login")
async def login(auth_login_dto: AuthLoginDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para realizar el login. Si las credenciales son correctas, se genera un JWT token.
    """
    token = await auth_service.login(auth_login_dto)
    if token:
        return JSONResponse(content={"access_token": token}, status_code=status.HTTP_200_OK)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
    )

@auth_controller.post("/logout")
async def logout(auth_logout_dto: AuthLogoutDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para realizar el logout. El token se agrega a la lista negra para invalidarlo.
    """
    try:
        await auth_service.logout(auth_logout_dto)
        return JSONResponse(content={"detail": "Logout exitoso"}, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error en el logout: {str(e)}"
        )
