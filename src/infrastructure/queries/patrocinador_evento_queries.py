GET_PATROCINADOR_EVENTO_BY_EVENTO = """
    SELECT p.id, p.nombre, p.imagen, p.contacto, pe.id_evento, pe.id_patrocinador
    FROM patrosinador_evento pe
    JOIN patrosinador p ON pe.id_patrocinador = p.id
    WHERE pe.id_evento = %s
"""

GET_PATROCINADOR_EVENTO_BY_PATROCINADOR = """

    SELECT e.id, e.nombre, e.fecha_inicio, e.fecha_fin
    FROM patrosinador_evento pe
    WHERE pe.id_patrocinador = %s
"""

CREATE_PATROCINADOR_EVENTO = """
    INSERT INTO patrosinador_evento (id_evento, id_patrocinador)
    VALUES (%s, %s)
"""