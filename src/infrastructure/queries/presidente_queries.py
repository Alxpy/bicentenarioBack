GET_ALL_PRESIDENTES = """
    SELECT p.id, p.nombre, p.apellido, p.imagen, p.inicio_periodo, p.fin_periodo, p.bibliografia, p.partido_politico, p.principales_politicas, p.id_usuario
    FROM presidente AS p
"""

GET_PRESIDENTE_BY_ID = """
    SELECT p.id, p.nombre, p.apellido, p.imagen, p.inicio_periodo, p.fin_periodo, p.bibliografia, p.partido_politico, p.principales_politicas, p.id_usuario
    FROM presidente AS p
    WHERE p.id = %s
"""

GET_PRESIDENTE_BY_NOMBRE = """
    SELECT p.id, p.nombre, p.apellido, p.imagen, p.inicio_periodo, p.fin_periodo, p.bibliografia, p.partido_politico, p.principales_politicas, p.id_usuario
    FROM presidente AS p
    WHERE p.nombre = %s
"""

CREATE_PRESIDENTE = """
    INSERT INTO presidente (nombre, apellido, imagen, inicio_periodo, fin_periodo, bibliografia, partido_politico, principales_politicas, id_usuario)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_PRESIDENTE = """
    UPDATE presidente
    SET nombre = %s, apellido = %s, imagen = %s, inicio_periodo = %s, fin_periodo = %s, bibliografia = %s, partido_politico = %s, principales_politicas = %s, id_usuario = %s
    WHERE id = %s
"""

DELETE_PRESIDENTE = """
    DELETE FROM presidente WHERE id = %s
"""
