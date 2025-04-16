import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Set, Optional
import logging
logger = logging.getLogger(__name__)
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO, AuthResponseDTO, AuthenticatedUserDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.auth_queries import *
from src.infrastructure.config.auth_config import *

class AuthRepository(IAuthRepositoryAbstract):
    def __init__(self, connection):
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist: Set[str] = set()

    def _generate_token(self, user_data: dict) -> str:
        payload = {
            "sub": user_data["correo"],
            "user_id": user_data["id"],  
            "nombre": user_data["nombre"],
            "roles": user_data["roles"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def _fetch_user(self, email: str) -> Optional[dict]:
        """Consulta los datos del usuario usando el context manager"""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(GET_USER_BY_EMAIL, (email,))
            return cursor.fetchone()

    async def _update_user_status(self, user_id: int, status: int, reset_attempts: bool = False) -> None:
        """Actualiza el estado del usuario en una sola conexión"""
        with self.connection.cursor() as cursor:
            query = UPDATE_USER_STATUS_RESET if reset_attempts else UPDATE_USER_STATUS
            params = (status, user_id) if not reset_attempts else (status, 0, None, user_id)
            cursor.execute(query, params)
            self.connection.commit()

    async def login(self, auth_login: AuthLoginDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
            
                cursor.execute(GET_USER_BY_EMAIL, (auth_login.email,))
                user = cursor.fetchone()
                if not user:
                    return error_response(INVALID_CREDENTIALS_MSG)

                if not bcrypt.checkpw(auth_login.password.encode(), user["contrasena"].encode()):
                    return error_response(INVALID_CREDENTIALS_MSG)

                cursor.execute(GET_USER_ROLES, (auth_login.email,))
                roles = [row["rol"] for row in cursor.fetchall()]
                user["roles"] = roles

                token = self._generate_token(user)
                response_dto = AuthResponseDTO(
                    token=token,
                    user=AuthenticatedUserDTO(
                        nombre=user["nombre"],
                        correo=user["correo"],
                        roles=roles
                    )
                )

                return success_response(data=response_dto, message="Inicio de sesión exitoso")

        except Exception as e:
            logger.error("Error en login: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )



    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> Response:
        try:
            decoded_token = jwt.decode(
                auth_logout_dto.token,
                self.secret,
                algorithms=[JWT_ALGORITHM]
            )
            user_id = decoded_token["user_id"]
            self.blacklist.add(auth_logout_dto.token)
            await self._update_user_status(user_id, 0)
            return success_response(message=LOGOUT_SUCCESS_MSG)
        except jwt.ExpiredSignatureError as e:
            logger.error("Token expirado: %s", e)
            return error_response(
                message=TOKEN_EXPIRED_MSG,
                status=HTTP_401_UNAUTHORIZED
            )
        except (jwt.InvalidTokenError, KeyError) as e:
            logger.error("Token inválido o falta claim: %s", e)
            return error_response(
                message=INVALID_TOKEN_MSG,
                status=HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error("Error en logout: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    VERIFY_CODE_LOGIN,
                    (auth_verify.email, auth_verify.code)
                )
                result = cursor.fetchone()
                if result:
                    return success_response(message="Código válido.")
                return error_response(
                    message=INVALID_CODE_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error("Error en verify_code_login: %s", e)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    VERIFY_EMAIL,
                    (datetime.now(), auth_verify.email, auth_verify.code)
                )
                self.connection.commit()
                
                if cursor.rowcount > 0:
                    return success_response(message=EMAIL_VERIFIED_MSG)
                return error_response(
                    message=INVALID_CODE_MSG,
                    status=HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            logger.error("Error en verify_code_email: %s", e)
            if self.connection:
                self.connection.rollback()
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )