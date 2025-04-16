GET_ALL_MULTIMEDIA_HISTORIA = """
    SELECT mh.id_multimedia, mh.id_historia, m.enlace, m.tipo
    FROM multimedia_historia mh
    INNER JOIN multimedia m ON mh.id_multimedia = m.id
"""


GET_MULTIMEDIA_HISTORIA_BY_ID_HISTORIA = """
    SELECT mh.id_multimedia, mh.id_historia, m.enlace, m.tipo
    FROM multimedia_historia mh
    INNER JOIN multimedia m ON mh.id_multimedia = m.id
    WHERE mh.id_historia = %s
"""

CREATE_MULTIMEDIA_HISTORIA = """
    INSERT INTO multimedia_historia (id_multimedia, id_historia)
    VALUES (%s, %s)
"""

DELETE_MULTIMEDIA_HISTORIA = """
    DELETE FROM multimedia_historia
    WHERE id_historia = %s
"""

