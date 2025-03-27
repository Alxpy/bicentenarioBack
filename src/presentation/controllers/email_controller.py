from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.email_service_abstract import IEmailServiceAbstract
from src.core.dependency_injection.dependency_injection import build_email_service
from src.presentation.dto.email_dto import EmailDTO
from fastapi.responses import JSONResponse

email_controller = APIRouter(prefix="/api/v1", tags=["email"])

@email_controller.get("/send_email/vetify_email/{email}")
async def send_email(
    email: str, 
    email_service: IEmailServiceAbstract = Depends(build_email_service)):
    """
    Endpoint para enviar un correo electrónico y verificar.
    """
    try:
        return await email_service.sendEmail_to_verify_email(EmailDTO(email=email))        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al enviar el email: {str(e)}"
       )
    
@email_controller.get("/send_email/vetify_login/{email}")
async def send_email(
    email_dto: str, 
    email_service: IEmailServiceAbstract = Depends(build_email_service)):
    """
    Endpoint para enviar un correo electrónico y verificar el login.
    """
    try:
        return await email_service.sendEmail_to_notify_new_login(EmailDTO(email=email_dto))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al enviar el email: {str(e)}"
       )
        
@email_controller.get("/send_email/recovery_password/{email}")
async def send_email(
    email: str, 
    email_service: IEmailServiceAbstract = Depends(build_email_service)):
    """
    Endpoint para enviar un correo electrónico y recuperar la contraseña.
    """
    try:
        return await email_service.sendEmail_to_change_password(EmailDTO(email=email))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al enviar el email: {str(e)}"
       )