GET_USER_BY_EMAIL = """
    SELECT u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, 
    u.contrasena, u.genero, u.telefono, u.pais, u.ciudad, u.estado, 
    u.email_verified_at, u.ultimoIntentoFallido, u.codeValidacion, 
    u.cantIntentos, u.imagen, GROUP_CONCAT(r.nombre_rol) AS roles
    FROM usuario AS u
    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
    INNER JOIN rol AS r ON r.id = ur.id_rol
    WHERE u.correo like %s
    GROUP BY u.id;
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