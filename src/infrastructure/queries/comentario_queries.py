GET_ALL_COMENTARIOS = """
SELECT 
    c.id,
    c.id_usuario,
    u.nombre, 
    u.apellidoPaterno, 
    u.apellidoMaterno,
    c.contenido,
    c.fecha_creacion
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id
"""

GET_COMENTARIO_BY_ID = """
SELECT 
    c.id,
    c.id_usuario,
    u.nombre, 
    u.apellidoPaterno, 
    u.apellidoMaterno,
    c.contenido,
    c.contenido,
    c.fecha_creacion
FROM comentario c
WHERE c.id = %s
"""

CREATE_COMENTARIO = """
INSERT INTO comentario (id_usuario, contenido, fecha_creacion)
VALUES (%s, %s, %s)
"""

UPDATE_COMENTARIO = """
UPDATE comentario
SET contenido = %s,
    fecha_creacion = %s
WHERE id = %s
"""

DELETE_COMENTARIO = """
DELETE FROM comentario
WHERE id = %s
"""
