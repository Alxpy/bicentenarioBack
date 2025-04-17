from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.auth_service_abstract import IAuthServiceAbstract
from src.core.dependency_injection.dependency_injection import build_auth_service
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO,AuthResponseDTO
from src.resources.responses.response import Response

auth_router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@auth_router.post(
    "/login",
    summary="Login",
    description="Allows the user to log in and obtain a JWT access token.",
    response_model=Response[AuthResponseDTO]
)
async def login(
    auth_login_dto: AuthLoginDTO,
    auth_service: IAuthServiceAbstract = Depends(build_auth_service)
):
    return await auth_service.login(auth_login_dto)

@auth_router.put(
    "/logout",
    summary="Logout",
    description="Logs out the user and invalidates the current token.",
    response_model=Response[None]
)
async def logout(
    auth_logout_dto: AuthLogoutDTO,
    auth_service: IAuthServiceAbstract = Depends(build_auth_service)
):
    return await auth_service.logout(auth_logout_dto)

@auth_router.get(
    "/login/verifyCode/{email}/{code}",
    summary="Verify Login Code",
    description="Verifies the login authentication code sent to the user's email.",
    response_model=Response[None]
)
async def verify_login_code(
    email: str,
    code: str,
    auth_service: IAuthServiceAbstract = Depends(build_auth_service)
):
    return await auth_service.verify_code_login(AuthVerifyCodeDTO(email=email, code=code))

