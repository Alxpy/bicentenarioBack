GET_ALL_MULTIMEDIA_CULTURA = """
     SELECT mc.id_multimedia, mc.id_cultura, m.enlace, m.tipo
    FROM multimedia_cultura mc
    INNER JOIN multimedia m ON mc.id_multimedia = m.id;
"""

GET_MULTIMEDIA_CULTURA_BY_ID_CULTURA = """
    SELECT mc.id_multimedia, mc.id_cultura, m.enlace, m.tipo
    FROM multimedia_cultura mc
    INNER JOIN multimedia m ON mc.id_multimedia = m.id
    WHERE mc.id_cultura = %s
"""


CREATE_MULTIMEDIA_CULTURA = """
    INSERT INTO multimedia_cultura (id_multimedia, id_cultura)
    VALUES (%s, %s)
"""

DELETE_MULTIMEDIA_CULTURA = """
    DELETE FROM multimedia_cultura
    WHERE id_cultura = %s
"""
