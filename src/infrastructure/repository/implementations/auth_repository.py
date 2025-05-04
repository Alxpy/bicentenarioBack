import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Set, Optional
import logging
from mysql.connector import Error as MySQLError

from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO, AuthResponseDTO, AuthenticatedUserDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.auth_queries import *
from src.infrastructure.config.auth_config import *
from src.core.models.user_domain import UsuarioDomain

logger = logging.getLogger(__name__)

class AuthRepository(IAuthRepositoryAbstract):
    def __init__(self, connection):
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist: Set[str] = set()


    def _generate_token(self, user_data: dict) -> str:
        """Genera un token JWT para el usuario"""
        payload = {
            "sub": user_data["correo"],
            "user_id": user_data["id"],
            "nombre": user_data["nombre"],
            "roles": user_data["roles"],
            "exp": datetime.utcnow() + timedelta(days=30)
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    async def _execute_query(self, query: str, params: tuple = None, fetch_all: bool = False) -> Optional[dict]:
        """Ejecuta una consulta y retorna los resultados"""
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall() if fetch_all else cursor.fetchone()
        except MySQLError as e:
            logger.error(f"Error en consulta SQL: {str(e)}")

    async def _execute_update(self, query: str, params: tuple = None) -> int:
        """Ejecuta una consulta de actualización"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params or ())
                self.connection.commit()
                return cursor.rowcount
        except MySQLError as e:
            logger.error(f"Error en actualización SQL: {str(e)}")

    async def login(self, auth_login: AuthLoginDTO) -> Response:
        """Autentica un usuario y genera un token JWT"""
        try:
            # Obtener usuario por email
            user = await self._execute_query(GET_USER_BY_EMAIL, (auth_login.email,))
            if not user:
                logger.info(f"Intento de login con email no registrado: {auth_login.email}")
                return error_response(INVALID_CREDENTIALS_MSG)

            # Verificar contraseña
            if not bcrypt.checkpw(auth_login.password.encode(), user["contrasena"].encode()):
                logger.info(f"Contraseña incorrecta para usuario: {auth_login.email}")
                return error_response(INVALID_CREDENTIALS_MSG)
            logger.info(user)
            # Obtener roles del usuario
            roles_result = await self._execute_query(GET_USER_ROLES, (user['id'],), fetch_all=True)
            roles = [row["nombre_rol"] for row in roles_result] if roles_result else []
            user["roles"] = roles
            logger.info(user)
            # Generar token JWT
            token = self._generate_token(user)
            response_dto = AuthResponseDTO(
                token=token,
                user=UsuarioDomain(**user)
            )

            logger.info(f"Login exitoso para usuario: {response_dto}")
            return success_response(
                data=response_dto, 
                message=LOGIN_SUCCESS_MSG
            )

        except MySQLError as e:
            logger.error(f"Error de base de datos en login: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error inesperado en login: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> Response:
        """Invalida el token JWT y actualiza el estado del usuario"""
        try:
            # Verificar y decodificar token
            decoded_token = jwt.decode(
                auth_logout_dto.token,
                self.secret,
                algorithms=[JWT_ALGORITHM]
            )
            user_id = decoded_token["user_id"]

            # Agregar token a la lista negra
            self.blacklist.add(auth_logout_dto.token)

            # Actualizar estado del usuario
            await self._execute_update(UPDATE_USER_STATUS, (0, user_id))

            logger.info(f"Logout exitoso para usuario ID: {user_id}")
            return success_response(message=LOGOUT_SUCCESS_MSG)

        except jwt.ExpiredSignatureError as e:
            logger.warning(f"Token expirado en logout: {str(e)}")
            return error_response(
                message=TOKEN_EXPIRED_MSG,
                status=HTTP_401_UNAUTHORIZED
            )
        except (jwt.InvalidTokenError, KeyError) as e:
            logger.warning(f"Token inválido en logout: {str(e)}")
            return error_response(
                message=INVALID_TOKEN_MSG,
                status=HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(f"Error en logout: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        """Verifica un código de autenticación para login"""
        try:
            result = await self._execute_query(
                VERIFY_CODE_LOGIN,
                (auth_verify.email, auth_verify.code)
            )

            if result:
                logger.info(f"Código válido para usuario: {auth_verify.email}")
                return success_response(message=VALID_CODE_MSG)
            
            logger.info(f"Código inválido para usuario: {auth_verify.email}")
            return error_response(
                message=INVALID_CODE_MSG,
                status=HTTP_400_BAD_REQUEST
            )

        except MySQLError as e:
            logger.error(f"Error de base de datos en verify_code_login: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error inesperado en verify_code_login: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )

    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        """Verifica un código de autenticación para email"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    VERIFY_EMAIL,
                    (datetime.now(), auth_verify.email, auth_verify.code)
                )
                self.connection.commit()

                if cursor.rowcount > 0:
                    logger.info(f"Email verificado: {auth_verify.email}")
                    return success_response(message=EMAIL_VERIFIED_MSG)
                
                logger.info(f"Código inválido para verificación de email: {auth_verify.email}")
                return error_response(
                    message=INVALID_CODE_MSG,
                    status=HTTP_400_BAD_REQUEST
                )

        except MySQLError as e:
            logger.error(f"Error de base de datos en verify_code_email: {str(e)}")
            return error_response(
                message=INTERNAL_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Error inesperado en verify_code_email: {str(e)}", exc_info=True)
            return error_response(
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}",
                status=HTTP_500_INTERNAL_SERVER_ERROR
            )