from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.email_service_abstract import IEmailServiceAbstract
from src.core.dependency_injection.dependency_injection import build_email_service
from src.presentation.dto.email_dto import EmailDTO
from src.presentation.responses.base_response import Response

email_router = APIRouter(
    prefix="/api/v1/emails",
    tags=["Email Notifications"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid request or email sending failure"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)

@email_router.post(
    "/verification",
    response_model=Response[None],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send verification email",
    description="Sends an email with a verification link to confirm the user's email address."
)
async def send_verification_email(
    email_data: EmailDTO,
    email_service: IEmailServiceAbstract = Depends(build_email_service)
):
    try:
        return await email_service.send_verification_email(email_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send verification email: {str(e)}"
        )

@email_router.post(
    "/loginNotification",
    response_model=Response[None],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send login notification",
    description="Sends a security notification email when a new login is detected for the account."
)
async def send_login_notification(
    email_data: EmailDTO,
    email_service: IEmailServiceAbstract = Depends(build_email_service)
):
    try:
        return await email_service.send_login_notification(email_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send login notification: {str(e)}"
        )

@email_router.post(
    "/passwordRecovery",
    response_model=Response[None],
    status_code=status.HTTP_202_ACCEPTED,
    summary="Send password recovery",
    description="Sends an email with instructions to reset the account password."
)
async def send_password_recovery(
    email_data: EmailDTO,
    email_service: IEmailServiceAbstract = Depends(build_email_service)
):
    try:
        return await email_service.send_password_recovery(email_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to send password recovery email: {str(e)}"
        )