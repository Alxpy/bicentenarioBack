import bcrypt
import jwt
import os
from datetime import datetime, timedelta
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from src.resources.responses.response import Response

class AuthRepository(IAuthRepositoryAbstract):

    def __init__(self, connection: object) -> None:
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist = set()

    def _fetch_user(self, email: str):
        """Consulta los datos del usuario por correo electrónico."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""
                SELECT u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, u.contrasena, u.genero, u.telefono, 
                u.pais, u.ciudad, u.estado, u.email_verified_at, u.ultimoIntentoFallido, u.codeValidacion, u.cantIntentos, u.imagen, GROUP_CONCAT(r.nombre_rol) AS roles
                FROM usuario AS u
                INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                INNER JOIN rol AS r ON r.id = ur.id_rol
                WHERE u.correo = %s
                GROUP BY u.id;
            """, (email,))
            return cursor.fetchone()

    def _update_user_status(self, user_id: int, status: int, reset_attempts=False):
        """Actualiza el estado del usuario y restablece intentos si es necesario."""
        with self.connection.cursor() as cursor:
            if reset_attempts:
                cursor.execute("UPDATE usuario SET estado = %s, cantIntentos = 0, ultimoIntentoFallido = NULL WHERE id = %s", (status, user_id))
            else:
                cursor.execute("UPDATE usuario SET estado = %s WHERE id = %s", (status, user_id))
            self.connection.commit()

    async def login(self, auth_login_dto: AuthLoginDTO) -> Response:
        try:
            user = self._fetch_user(auth_login_dto.email)
            print(user)
            if not user:
                return Response(status=401, success=False, message="Credenciales incorrectas.")
            
            now = datetime.now()
            if user["cantIntentos"] >= 3 and user["ultimoIntentoFallido"]:
                if (now - user["ultimoIntentoFallido"]).total_seconds() < 300:
                    return Response(status=403, success=False,message="Demasiados intentos. Inténtelo más tarde.")
                self._update_user_status(user["id"], 1, reset_attempts=True)
            
            if not bcrypt.checkpw(auth_login_dto.password.encode('utf-8'), user["contrasena"].encode('utf-8')):
                with self.connection.cursor() as cursor:
                    cursor.execute("UPDATE usuario SET cantIntentos = cantIntentos + 1, ultimoIntentoFallido = %s WHERE id = %s", (now, user["id"]))
                    self.connection.commit()
                return Response(status=401, success=False, message="Credenciales incorrectas.")
            
            if user["email_verified_at"] is None:
                return Response(status=403, success=False, message="Correo no verificado. Revise su bandeja de entrada.")
            
            if user["estado"] == 3:
                return Response(status=403, success=False, message="Cuenta bloqueada.")
            
            self._update_user_status(user["id"], 1, reset_attempts=True)
            token = jwt.encode({"id": user["id"], "roles": user["roles"], "nombre": user["nombre"], "correo": user["correo"]}, self.secret, algorithm="HS256")
            return Response(status=200, success=True, message="Inicio de sesión exitoso.", data={"token": token})
        except Exception as e:
            print(f"Error: {e}")
            return Response(status=500,success=False,message="Error."
            )
    
    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> Response:
        try:
            decoded_token = jwt.decode(auth_logout_dto.token, self.secret, algorithms=["HS256"])
            self.blacklist.add(auth_logout_dto.token)
            self._update_user_status(decoded_token["id"], 0)
            return Response(status=200, success=True, message="Cierre de sesión exitoso.")
        except jwt.ExpiredSignatureError:
            return Response(status=401, success=False, message="Token expirado.")
        except jwt.InvalidTokenError:
            return Response(status=401, success=False, message="Token inválido.")
        except Exception:
            return Response(status=500, success=False, message="Error.")
    
    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM usuario WHERE correo = %s AND codeValidacion = %s", (auth_verify.email, auth_verify.code))
                if cursor.fetchone():
                    return Response(status=200, success=True, message="Código válido.")
                return Response(status=400, success=False, message="Código inválido o correo incorrecto.")
        except Exception:
            return Response(status=500, success=False, message="Error.")

    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM usuario WHERE correo = %s AND codeValidacion = %s", (auth_verify.email, auth_verify.code))
                if cursor.fetchone():
                    cursor.execute("UPDATE usuario SET email_verified_at = %s WHERE correo = %s", (datetime.now(), auth_verify.email))
                    self.connection.commit()
                    return Response(status=200, success=True, message="Correo verificado correctamente.")
                return Response(status=400, success=False, message="Código inválido o correo incorrecto.")
        except Exception:
            return Response(status=500, success=False, message="Error.")
