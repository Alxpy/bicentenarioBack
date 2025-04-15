GET_USER_BY_EMAIL = """
    SELECT u.*, 
       (SELECT GROUP_CONCAT(r.nombre_rol) 
        FROM usuario_rol ur 
        JOIN rol r ON ur.id_rol = r.id 
        WHERE ur.id_usuario = u.id) AS roles
FROM usuario u
WHERE u.correo LIKE %s;

"""

UPDATE_USER_STATUS = """
    UPDATE usuario 
    SET estado = %s, 
        cantIntentos = %s, 
        ultimoIntentoFallido = %s 
    WHERE id = %s
"""

UPDATE_USER_STATUS_RESET = """
    UPDATE usuario 
    SET estado = %s, cantIntentos = %s, ultimoIntentoFallido = %s 
    WHERE id = %s
"""
INCREMENT_LOGIN_ATTEMPTS = """
    UPDATE usuario 
    SET cantIntentos = cantIntentos + 1, 
        ultimoIntentoFallido = %s 
    WHERE id = %s
"""

VERIFY_CODE_LOGIN = """
    SELECT id 
    FROM usuario 
    WHERE correo = %s AND codeValidacion = %s
"""

VERIFY_EMAIL = """
    UPDATE usuario 
    SET email_verified_at = %s 
    WHERE correo = %s AND codeValidacion = %s
"""