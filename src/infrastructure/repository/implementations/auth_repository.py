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

    async def login(self, auth_login_dto: AuthLoginDTO) -> dict:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT 
                        u.id, 
                        u.nombre, 
                        u.correo, 
                        u.contrasena, 
                        u.cantIntentos, 
                        u.estado, 
                        u.email_verified_at, 
                        u.ultimoIntentoFallido, 
                        GROUP_CONCAT(ur.id_rol) AS roles
                    FROM usuario AS u
                    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
                    WHERE u.correo = %s
                    GROUP BY u.id;

                """, (auth_login_dto.email,))
                result = cursor.fetchone()
                
                if not result:
                    return {"success": False, "message": "Credenciales incorrectas."}
                
                now = datetime.now()
                
                if result["cantIntentos"] >= 3:
                    if result["ultimoIntentoFallido"]:
                        ultimo_intento = result["ultimoIntentoFallido"]
                        diferencia = now - ultimo_intento

                        if diferencia.total_seconds() < 300:
                            return {"success": False, "message": "Demasiados intentos. Inténtelo más tarde."}
                        else:
                            cursor.execute("UPDATE usuario SET cantIntentos = 0, ultimoIntentoFallido = NULL WHERE id = %s", (result["id"],))
                            self.connection.commit()

                if not bcrypt.checkpw(auth_login_dto.password.encode('utf-8'), result["contrasena"].encode('utf-8')):
                    cursor.execute("""
                        UPDATE usuario 
                        SET cantIntentos = cantIntentos + 1, ultimoIntentoFallido = %s 
                        WHERE id = %s
                    """, (now, result["id"]))
                    self.connection.commit()

                    if result["cantIntentos"] + 1 >= 3:
                        cursor.execute("UPDATE usuario SET estado = 3 WHERE id = %s", (result["id"],))
                        self.connection.commit()
                        return {"success": False, "message": "Cuenta bloqueada por intentos fallidos."}

                    return {"success": False, "message": "Credenciales incorrectas."}

                if result["email_verified_at"] is None:
                    return {"success": False, "message": "Correo no verificado. Revise su bandeja de entrada."}

                if result["estado"] == 2:
                    return {"success": False, "message": "Cuenta inactiva."}
                elif result["estado"] == 1:
                    return {"success": False, "message": "Cuenta activa."}
                elif result["estado"] == 3:
                    return {"success": False, "message": "Cuenta bloqueada."}

                cursor.execute("UPDATE usuario SET estado = 2, cantIntentos = 0, ultimoIntentoFallido = NULL WHERE id = %s", (result["id"],))
                self.connection.commit()

                try:
                    payload = {
                        "id": result["id"],
                        "roles": result["roles"],
                        "nombre": result["nombre"],
                        "correo": result["correo"]
                    }
                    token = jwt.encode(payload, self.secret, algorithm="HS256")
                except Exception as err:
                    print(f"Error: {err}")
                    return

                return {"success": True, "message": "Inicio de sesión exitoso.", "token": token}
        except Exception as err:
            print(f"Error: {err}")
            return {"success": False, "message": "Error interno del servidor."}

    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> dict:
        try:
            decoded_token = jwt.decode(auth_logout_dto.token, self.secret, algorithms=["HS256"])
            self.blacklist.add(auth_logout_dto.token)
            with self.connection.cursor() as cursor:
                cursor.execute("UPDATE usuario SET estado = 1 WHERE id = %s", (decoded_token["id"],))
                self.connection.commit()
            return {"success": True, "message": "Cierre de sesión exitoso."}
        except jwt.ExpiredSignatureError:
                return {"success": False, "message": "Token expirado."}
        except jwt.InvalidTokenError:
            return {"success": False, "message": "Token inválido."}
        except jwt.DecodeError:
            return {"success": False, "message": "Error en la decodificación del token."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}
        
    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> dict:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM usuario WHERE correo = %s AND codeValidacion = %s", (auth_verify.email, auth_verify.code))
                result = cursor.fetchone()
                if result:
                    return {"success": True, "message": "Código válido."}
                return {"success": False, "message": "Código inválido o correo incorrecto."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}

    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> dict:
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM usuario WHERE correo = %s AND codeValidacion = %s", (auth_verify.email, auth_verify.code))
                result = cursor.fetchone()
                if result:
                    cursor.execute("UPDATE usuario SET email_verified_at = %s WHERE correo = %s", (datetime.now(), auth_verify.email))
                    self.connection.commit()
                    return {"success": True, "message": "Correo verificado correctamente."}
                return {"success": False, "message": "Código inválido o correo incorrecto."}
        except Exception:
            return {"success": False, "message": "Error interno del servidor."}
