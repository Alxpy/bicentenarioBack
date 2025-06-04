GET_USUARIO_EVENTO_BY_ID_USUARIO = """
    SELECT uv.id,uv.id_usuario,uv.id_evento,uv.asistio
    FROM usuario_evento uv
    WHERE uv.id_usuario = %s
"""

GET_USUARIO_EVENTOS_BY_ID_EVENTO = """
    SELECT uv.id,uv.id_usuario,uv.id_evento,uv.asistio
    FROM usuario_evento uv
    WHERE uv.id_evento = %s
"""

GET_ALL_USUARIO_EVENTOS = """
    SELECT uv.id,uv.id_usuario,uv.id_evento,uv.asistio
    FROM usuario_evento uv
""" 

CREATE_USUARIO_EVENTO = """
    INSERT INTO usuario_evento (id_usuario, id_evento, asistio)
    VALUES (%s, %s, %s)
"""

UPDATE_ASISTIO_USUARIO_EVENTO = """
    UPDATE usuario_evento
    SET asistio = %s
    WHERE id_usuario = %s
"""

DELETE_USUARIO_EVENTO = """
    DELETE FROM usuario_evento
    WHERE id = %s
"""

GET_DATA_USUARIO_EVENTO = """
    SELECT u.nombre, u.apellidoPaterno, u.apellidoMaterno, e.nombre AS nombre_evento, ue.asistio 
    FROM usuario_evento ue
    JOIN usuario u ON ue.id_usuario = u.id
    JOIN evento e ON ue.id_evento = e.id
"""
