GET_ALL_USUARIO_ROL = """
SELECT 
    ur.id_usuario, 
    ur.id_rol, 
    u.nombre, 
    u.apellidoPaterno, 
    u.apellidoMaterno
FROM usuario_rol AS ur
JOIN usuario AS u ON ur.id_usuario = u.id
"""

GET_USUARIO_ROL_BY_ID_ROL = """
SELECT 
    ur.id_usuario, 
    ur.id_rol, 
    u.nombre, 
    u.apellidoPaterno, 
    u.apellidoMaterno
FROM usuario_rol AS ur
JOIN usuario AS u ON ur.id_usuario = u.id
WHERE ur.id_rol = %s
"""

CREATE_USUARIO_ROL = """
INSERT INTO usuario_rol (id_usuario, id_rol)
VALUES (%s, %s)
"""

DELETE_USUARIO_ROL = """
DELETE FROM usuario_rol
WHERE id_usuario = %s
"""
