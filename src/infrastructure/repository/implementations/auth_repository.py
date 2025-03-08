import bcrypt
import jwt
import os
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from datetime import datetime
from typing import Optional, Tuple

class AuthRepository(IAuthRepositoryAbstract):
    def __init__(self, connection: object) -> None:
        self.connection = connection
        self.secret = os.getenv("JWT_SECRET", "default_secret")
        self.blacklist = set()

    async def login(self, auth_login_dto: AuthLoginDTO) -> Tuple[Optional[str], str]:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT id, id_rol, nombre, correo, contrasena, cantIntentos, estado, email_verified_at, ultimoIntentoFallido
                    FROM usuario WHERE correo = %s
                """, (auth_login_dto.correo,))
                result = cursor.fetchone()

                if not result:
                    return None, "Correo no registrado."

                now = datetime.now()

                if result["cantIntentos"] >= 3:
                    if result["ultimoIntentoFallido"]:
                        ultimo_intento = result["ultimoIntentoFallido"]
                        diferencia = now - ultimo_intento

                        if diferencia.total_seconds() < 300:
                            return None, "Demasiados intentos fallidos. Intenta de nuevo en unos minutos."
                        else:
                            cursor.execute("UPDATE usuario SET cantIntentos = 0, ultimoIntentoFallido = NULL WHERE id = %s", 
                                        (result["id"],))
                            self.connection.commit()

                if not bcrypt.checkpw(auth_login_dto.contrasena.encode('utf-8'), result["contrasena"].encode('utf-8')):
                    
                    cursor.execute("""
                        UPDATE usuario 
                        SET cantIntentos = cantIntentos + 1, ultimoIntentoFallido = %s 
                        WHERE id = %s
                    """, (now, result["id"]))
                    self.connection.commit()
                    return None, "Contraseña incorrecta."

                if result["email_verified_at"] is None:
                    return None, "Correo electrónico no verificado. Por favor, revisa tu bandeja de entrada."

                if result["estado"] != 1:
                    return None, "Cuenta activa."

                cursor.execute("UPDATE usuario SET estado = 1, cantIntentos = 0, ultimoIntentoFallido = NULL WHERE id = %s", 
                            (result["id"],))
                self.connection.commit()

                token = jwt.encode({
                    "id": result["id"],
                    "rol": result["id_rol"],
                    "nombre": result["nombre"],
                    "correo": result["correo"]
                }, self.secret, algorithm="HS256")

                return token, "Inicio de sesión exitoso."
        except Exception as e:
            print({"Error": str(e)})  
            return None, "Error interno del servidor."

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
    
    
    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> bool:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE correo = %s AND codigo = %s", (auth_verify.email, auth_verify.code))
                result = cursor.fetchone()
                if result:
                    return True
                return False
        except (Exception, self.connection.Error) as e:
            print({"Error": str(e)})
            return False
    
    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> bool:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM usuario WHERE correo = %s AND codeValidacion = %s", (auth_verify.email, auth_verify.code))
                result = cursor.fetchone()
                if result:
                    cursor.execute("UPDATE usuario SET email_verified_at = %s WHERE correo = %s", (datetime.now(), auth_verify.email))
                    self.connection.commit()
                    return True
                return False
        except (Exception, self.connection.Error) as e:
            print({"Error": str(e)})
            return False
            
    
