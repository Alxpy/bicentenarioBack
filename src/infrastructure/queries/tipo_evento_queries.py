GET_ALL_TIPO_EVENTO = """
    SELECT id, nombre_evento
    FROM tipo_evento
"""

GET_TIPO_EVENTO_BY_ID = """
    SELECT id, nombre_evento
    FROM tipo_evento
    WHERE id = %s
"""

CREATE_TIPO_EVENTO = """
    INSERT INTO tipo_evento (nombre_evento)
    VALUES (%s)
"""

UPDATE_TIPO_EVENTO = """
    UPDATE tipo_evento
    SET nombre_evento = %s
    WHERE id = %s
"""

DELETE_TIPO_EVENTO = """
    DELETE FROM tipo_evento
    WHERE id = %s
"""