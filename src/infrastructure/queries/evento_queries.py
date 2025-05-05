# evento_queries.py

GET_ALL_EVENTO = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
       e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
       e.id_tipo_evento, t.nombre_evento AS nombre_evento,
       e.id_usuario, us.nombre AS nombre_usuario,
       e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
"""

GET_EVENTO_BY_ID = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
           e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE e.id = %s
"""

GET_EVENTO_BY_NOMBRE = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
              e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE e.nombre = %s
"""

GET_EVENTO_BY_FECHA = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
              e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE DATE(e.fecha_inicio) = %s
"""

GET_EVENTO_BY_TIPO = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
              e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE t.nombre_evento = %s
"""

GET_EVENTO_BY_UBICACION = """
    SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
              e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE ub.nombre = %s
"""

GET_EVENTO_BY_ORGANIZADOR = """
SELECT e.id, e.nombre, e.descripcion, e.imagen, 
           e.fecha_inicio, e.fecha_fin, e.id_ubicacion, ub.nombre AS nombre_ubicacion,
           e.id_tipo_evento, t.nombre_evento AS nombre_evento,
           e.id_usuario, us.nombre AS nombre_usuario,
              e.id_organizador, o.nombre AS nombre_organizador
    FROM evento AS e
    INNER JOIN tipo_evento AS t ON e.id_tipo_evento = t.id
    INNER JOIN ubicacion AS ub ON e.id_ubicacion = ub.id
    INNER JOIN usuario AS us ON e.id_usuario = us.id
    INNER JOIN usuario AS o ON e.id_organizador = o.id
    WHERE o.nombre = %s
"""



CREATE_EVENTO = """
    INSERT INTO evento (nombre, descripcion, imagen, fecha_inicio, fecha_fin, id_tipo_evento, id_ubicacion, id_usuario, id_organizador)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

UPDATE_EVENTO = """
    UPDATE evento
    SET nombre = %s, descripcion = %s, imagen = %s, 
        fecha_inicio = %s, fecha_fin = %s, 
        id_ubicacion = %s, id_tipo_evento = %s
    WHERE id = %s
"""

DELETE_EVENTO = """
    DELETE FROM evento
    WHERE id = %s
"""
