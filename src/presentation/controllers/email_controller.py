from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.email_service_abstract import IEmailServiceAbstract
from src.core.dependency_injection.dependency_injection import build_email_service
from src.presentation.dto.email_dto import EmailDTO
from src.presentation.responses.base_response import Response

email_controller = APIRouter(prefix="/api/v1/emails", tags=["emails"])

@email_controller.get("/verify/{email}", response_model=Response[None])
async def send_verification_email(
    email: str,
    emailService: IEmailServiceAbstract = Depends(build_email_service)
):
    """
    Sends an email to verify the user's email address.
    """
    try:
        return await emailService.sendEmail_to_verify_email(EmailDTO(email=email))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error sending verification email: {str(e)}"
        )


@email_controller.get("/notifyLogin/{email}", response_model=Response[None])
async def send_login_notification_email(
    email: str,
    emailService: IEmailServiceAbstract = Depends(build_email_service)
):
    """
    Sends an email to notify a new login.
    """
    try:
        return await emailService.sendEmail_to_notify_new_login(EmailDTO(email=email))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error sending login notification email: {str(e)}"
        )


@email_controller.get("/recoveryPassword/{email}", response_model=Response[None])
async def send_password_recovery_email(
    email: str,
    emailService: IEmailServiceAbstract = Depends(build_email_service)
):
    """
    Sends an email to recover the password.
    """
    try:
        return await emailService.sendEmail_to_change_password(EmailDTO(email=email))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error sending password recovery email: {str(e)}"
        )
