from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.dependency_injection.dependency_injection import build_usuario_service
from src.presentation.dto.user_dto import UsuarioDTO, UpdateDataUserDTO, NewPasswordDTO
from src.core.models.user_domain import UsuarioDomain
from src.resources.responses.response import Response


user_controller = APIRouter(prefix="/api/v1/user", tags=["user"])

@user_controller.post(
    "",
    summary="Register user",
    description="Creates a new user in the system.",
    response_model=Response[None]
)
async def register(
    user_data: UsuarioDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.create_usuario(user_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.get(
    "",
    summary="Get all users",
    description="Returns a list of all registered users.",
    response_model=Response[list[UsuarioDomain]]
)
async def get_users(
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.get_all_usuarios()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_controller.get(
    "/{userId}",
    summary="Get user by ID",
    description="Returns a single user based on the given ID.",
    response_model=Response[UsuarioDomain]
)
async def get_user_by_id(
    userId: int,
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.get_usuario(userId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.put(
    "/{userId}",
    summary="Update user data",
    description="Updates basic user information for the specified user ID.",
    response_model=Response[None]
)
async def update_user(
    userId: int,
    update_data: UpdateDataUserDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.update_usuario(userId, update_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_controller.put(
    "/change-password",
    summary="Change user password",
    description="Changes the user's password based on their email.",
    response_model=Response[None]
)
async def change_password(
    new_password_data: NewPasswordDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.change_password(
            new_password_data.correo,
            new_password_data.nueva_contrasena
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_controller.delete(
    "/{userId}",
    summary="Delete user",
    description="Deletes a user from the system by ID.",
    response_model=Response[None]
)
async def delete_user(
    userId: int,
    user_service: IUsuarioService = Depends(build_usuario_service)
):
    try:
        return await user_service.delete_usuario(userId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
