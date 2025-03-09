from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.auth_service_abstract import IAuthServiceAbstract
from src.core.dependency_injection.dependency_injection import build_auth_service
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from fastapi.responses import JSONResponse

auth_controller = APIRouter(prefix="/api/v1", tags=["auth"])

@auth_controller.post("/login")
async def login(auth_login_dto: AuthLoginDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para realizar el login. Si las credenciales son correctas, se genera un JWT token.
    """
    token = await auth_service.login(auth_login_dto)
    return JSONResponse(content={"response": token}, status_code=status.HTTP_200_OK)

@auth_controller.put("/logout")
async def logout(auth_logout_dto: AuthLogoutDTO, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para realizar el logout. El token se agrega a la lista negra para invalidarlo.
    """
    try:
        response = await auth_service.logout(auth_logout_dto)
        return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"response": f"Error en el logout: {str(e)}"}, status_code=status.HTTP_400_BAD_REQUEST)

@auth_controller.get("/log/vr/{email}/{code}")
async def verify_code_login(email: str, code: str, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para verificar el código de autenticación enviado por email.
    """
    response = await auth_service.verify_code_login(AuthVerifyCodeDTO(email=email, code=code))
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)

@auth_controller.get("/verify/email/{email}/{code}")
async def verify_code_email(email: str, code: str, auth_service: IAuthServiceAbstract = Depends(build_auth_service)):
    """
    Endpoint para verificar el código de autenticación enviado por email.
    """
    response = await auth_service.verify_code_email(AuthVerifyCodeDTO(email=email, code=code))
    return JSONResponse(content={"response": response}, status_code=status.HTTP_200_OK)
