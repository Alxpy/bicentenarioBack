GET_USER_BY_ID = """
    SELECT u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, u.contrasena, 
    u.genero, u.telefono, u.pais, u.ciudad, u.estado, u.email_verified_at, 
    u.ultimoIntentoFallido, u.codeValidacion, u.cantIntentos, u.imagen, 
    GROUP_CONCAT(r.nombre_rol) AS roles
    FROM usuario AS u
    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
    INNER JOIN rol AS r ON r.id = ur.id_rol
    WHERE u.id = %s
    GROUP BY u.id;
"""

GET_ALL_USERS = """
    SELECT u.id, u.nombre, u.apellidoPaterno, u.apellidoMaterno, u.correo, 
    u.contrasena, u.cantIntentos, u.estado, u.email_verified_at, 
    u.ultimoIntentoFallido, u.genero, u.telefono, u.pais, u.ciudad,
    GROUP_CONCAT(r.nombre_rol) AS roles
    FROM usuario AS u
    INNER JOIN usuario_rol AS ur ON ur.id_usuario = u.id
    INNER JOIN rol AS r ON r.id = ur.id_rol
    GROUP BY u.id;
"""

CREATE_USER = """
    INSERT INTO usuario 
    (nombre, apellidoPaterno, apellidoMaterno, correo, contrasena, genero, telefono, pais, ciudad)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

CREATE_USER_CODE = """
   UPDATE usuario SET codeValidacion = %s 
    WHERE correo = %s
"""

ASSIGN_DEFAULT_ROLE = """
    INSERT INTO usuario_rol (id_usuario, id_rol)
    SELECT LAST_INSERT_ID(), r.id
    FROM rol r
    WHERE r.nombre_rol LIKE 'usuario'
"""

UPDATE_USER = """
    UPDATE usuario 
    SET nombre = %s, apellidoPaterno = %s, apellidoMaterno = %s, correo = %s, 
    genero = %s, telefono = %s, pais = %s, ciudad = %s
    WHERE id = %s
"""

UPDATE_CODE_VALIDATION = """
    UPDATE usuario 
    SET codeValidacion = %s 
    WHERE correo = %s
"""

UPDATE_PASSWORD = "UPDATE usuario SET contrasena = %s WHERE correo = %s"

REMOVE_CODE_VALIDATION = "UPDATE usuario SET codeValidacion = NULL WHERE correo = %s"

DELETE_USER = "UPDATE usuario SET estado = 3 WHERE id = %s"