import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from typing import Set, Optional

from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from src.resources.responses.response import Response
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.messages import *
from src.infrastructure.queries.auth_queries import *
from src.infrastructure.config.auth_config import *

class AuthRepository(IAuthRepositoryAbstract):
    def __init__(self, connection):
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist: Set[str] = set()

    async def generate_token(self, user: dict, roles: list):
        print(user)
        token_payload = {
            "id": user["id"],
            "roles": roles,
            "nombre": user["nombre"],
            "correo": user["correo"],
            "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MINUTES),
            "iss": "bicentenario",    
        }
    
        return jwt.encode(token_payload, self.secret, algorithm=JWT_ALGORITHM)

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

    async def login(self, auth_login_dto: AuthLoginDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(GET_USER_BY_EMAIL, (auth_login_dto.email,))
                user = cursor.fetchone()
                
            if not user:
                return Response(
                    status=HTTP_401_UNAUTHORIZED,
                    success=False,
                    message=INVALID_CREDENTIALS_MSG
                )
                
            now = datetime.now()
                
            # 2. Verificar intentos fallidos
            if user["cantIntentos"] >= MAX_LOGIN_ATTEMPTS and user["ultimoIntentoFallido"]:
                block_time = timedelta(minutes=LOGIN_BLOCK_TIME_MINUTES)
                if (now - user["ultimoIntentoFallido"]) < block_time:
                    return Response(
                        status=HTTP_403_FORBIDDEN,
                        success=False,
                        message=TOO_MANY_ATTEMPTS_MSG
                    )
                await self._update_user_status(user["id"], 1, reset_attempts=True)
                
            # 3. Verificar contraseña
            if not bcrypt.checkpw(auth_login_dto.password.encode('utf-8'), user["contrasena"].encode('utf-8')):
                with self.connection.cursor() as cursor:
                    cursor.execute(INCREMENT_LOGIN_ATTEMPTS, (now, user["id"]))
                    self.connection.commit()
                return Response(
                    status=HTTP_401_UNAUTHORIZED,
                    success=False,
                    message=INVALID_CREDENTIALS_MSG
                )
                
                # 4. Verificar estado de cuenta
            if user["email_verified_at"] is None:
                return Response(
                    status=HTTP_403_FORBIDDEN,
                    success=False,
                    message=UNVERIFIED_EMAIL_MSG
                )
                
            if user["estado"] == 3:
                return Response(
                    status=HTTP_403_FORBIDDEN,
                    success=False,
                    message=ACCOUNT_LOCKED_MSG
                )
                
            await self._update_user_status(user["id"], 1, reset_attempts=True)                
            roles = user['roles'].split(',') if isinstance(user['roles'], str) else user['roles']
        
            token = await self.generate_token(user, roles)
                
            return Response(
                status=HTTP_200_OK,
                success=True,
                message=LOGIN_SUCCESS_MSG,
                data={
                    "token": token,
                    "user": {
                        "nombre": user["nombre"],
                        "correo": user["correo"],
                        "roles": roles
                    }
                }
            )
                
        except Exception as e:
            print(e)
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )


    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> Response:
        try:
            decoded_token = jwt.decode(
                auth_logout_dto.token,
                self.secret,
                algorithms=[JWT_ALGORITHM]
            )
            self.blacklist.add(auth_logout_dto.token)
            self._update_user_status(decoded_token["id"], 0)
            return Response(
                status=HTTP_200_OK,
                success=True,
                message=LOGOUT_SUCCESS_MSG
            )
        except jwt.ExpiredSignatureError:
            return Response(
                status=HTTP_401_UNAUTHORIZED,
                success=False,
                message=TOKEN_EXPIRED_MSG
            )
        except jwt.InvalidTokenError:
            return Response(
                status=HTTP_401_UNAUTHORIZED,
                success=False,
                message=INVALID_TOKEN_MSG
            )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )

    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    VERIFY_CODE_LOGIN,
                    (auth_verify.email, auth_verify.code)
                )
                if cursor.fetchone():
                    return Response(
                        status=HTTP_200_OK,
                        success=True,
                        message="Código válido."
                    )
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    success=False,
                    message=INVALID_CODE_MSG
                )
        except Exception as e:
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if self.connection:
                self.connection.close()

    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(
                    VERIFY_EMAIL,
                    (datetime.now(), auth_verify.email, auth_verify.code)
                )
                self.connection.commit()
                
                if cursor.rowcount > 0:
                    return Response(
                        status=HTTP_200_OK,
                        success=True,
                        message=EMAIL_VERIFIED_MSG
                    )
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    success=False,
                    message=INVALID_CODE_MSG
                )
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=f"{INTERNAL_ERROR_MSG} Detalles: {str(e)}"
            )
        finally:
            if self.connection:
                self.connection.close()