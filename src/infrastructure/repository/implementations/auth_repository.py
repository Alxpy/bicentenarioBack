import bcrypt
import jwt
import os
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from typing import Optional

class AuthRepository(IAuthRepositoryAbstract):
    def __init__(self, connection: object) -> None:
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist = set()

    async def login(self, auth_login_dto: AuthLoginDTO) -> Optional[str]:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE correo = %s", (auth_login_dto.correo,))
                result = cursor.fetchone()
                if result and bcrypt.checkpw(auth_login_dto.contrasena.encode('utf-8'), result["contrasena"].encode('utf-8')):
                    cursor.execute("UPDATE usuario SET estado = 1 WHERE id = %s", (result["id"],))
                    self.connection.commit()
                    token = jwt.encode({
                        "id": result["id"],
                        "rol": result["id_rol"],
                        "nombre": result["nombre"],
                        "correo": result["correo"]
                    }, self.secret, algorithm="HS256")
                    return token
                return None
        except (Exception, self.connection.Error) as e:
            print({"Error": str(e)})
            return None

    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> None:
        try:
            decoded_token = jwt.decode(auth_logout_dto.token, self.secret, algorithms=["HS256"])
            self.blacklist.add(auth_logout_dto.token)
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE usuario SET estado = 0 WHERE id = %s", (decoded_token["id"],))
                self.connection.commit()
        except jwt.ExpiredSignatureError:
            print("Token expirado")
        except jwt.InvalidTokenError:
            print("Token inválido")
        except (Exception, self.connection.Error) as e:
            print({"Error": str(e)})
