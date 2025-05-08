GET_ALL_COMENTARIO_EVENTO = """
SELECT 
    ce.id_comentario,
    ce.id_evento,
    c.id_usuario,
    c.contenido,
    c.fecha_creacion
FROM 
    comentario_evento AS ce
JOIN 
    comentario AS c ON ce.id_comentario = c.id
"""

GET_COMENTARIO_EVENTO_BY_ID_EVENTO = """
SELECT 
    ce.id_comentario,
    ce.id_evento,
    c.id_usuario,
    c.contenido,
    c.fecha_creacion
FROM 
    comentario_evento AS ce
JOIN 
    comentario AS c ON ce.id_comentario = c.id
WHERE 
    ce.id_evento = %s
"""

CREATE_COMENTARIO_EVENTO = """
INSERT INTO comentario_evento (
    id_evento,
    id_comentario
) VALUES (%s, %s)
"""

DELETE_COMENTARIO_EVENTO = """
DELETE FROM comentario_evento
WHERE 
    id_evento = %s AND 
    id_comentario = %s
"""
