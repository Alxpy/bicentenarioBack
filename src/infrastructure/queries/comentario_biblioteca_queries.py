GET_ALL_COMENTARIO_BIBLIOTECA = """
SELECT 
    cb.id_comentario,
    cb.id_biblioteca,
    c.id_usuario,
    c.contenido,
    c.fecha_creacion
FROM 
    comentario_biblioteca AS cb
JOIN 
    comentario AS c ON cb.id_comentario = c.id
"""

GET_COMENTARIO_BIBLIOTECA_BY_ID_BIBLIOTECA = """
SELECT 
    cb.id_comentario,
    cb.id_biblioteca,
    c.id_usuario,
    c.contenido,
    c.fecha_creacion
FROM 
    comentario_biblioteca AS cb
JOIN 
    comentario AS c ON cb.id_comentario = c.id
WHERE 
    cb.id_biblioteca = %s
"""

CREATE_COMENTARIO_BIBLIOTECA = """
INSERT INTO comentario_biblioteca (
    id_biblioteca,
    id_comentario
) VALUES (%s, %s)
"""

DELETE_COMENTARIO_BIBLIOTECA = """
DELETE FROM comentario_biblioteca
WHERE 
    id_biblioteca = %s AND 
    id_comentario = %s
"""
