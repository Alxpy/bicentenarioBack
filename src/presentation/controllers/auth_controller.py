from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.auth_service_abstract import IAuthServiceAbstract
from src.core.dependency_injection.dependency_injection import build_auth_service
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from src.resources.responses.response import Response

auth_controller = APIRouter(prefix="/api/v1", tags=["auth"])

@auth_controller.post("/login")
async def login(auth_login_dto: AuthLoginDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para iniciar sesión y obtener un JWT.
    """
    response: Response = await auth_service.login(auth_login_dto)
    return response

@auth_controller.put("/logout")
async def logout(auth_logout_dto: AuthLogoutDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para cerrar sesión. El token se invalida.
    """
    response = await auth_service.logout(auth_logout_dto)
    return response

@auth_controller.get("/log/vr/{email}/{code}")
async def verify_code_login(email: str, code: str, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para verificar el código de autenticación del login.
    """
    response = await auth_service.verify_code_login(AuthVerifyCodeDTO(email=email, code=code))
    return response

@auth_controller.get("/verify/email/{email}/{code}")
async def verify_code_email(email: str, code: str, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para verificar el código de validación de email.
    """
    response = await auth_service.verify_code_email(AuthVerifyCodeDTO(email=email, code=code))
    return response
