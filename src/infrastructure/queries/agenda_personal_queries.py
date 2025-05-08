
GET_ALL_AGENDA_PERSONAL = """
SELECT ap.id, ap.id_usuario, ap.id_evento, e.nombre AS nombre_evento, ap.recordatorio, ap.notas
FROM agenda_personal ap
JOIN evento e ON ap.id_evento = e.id
"""

GET_AGENDA_PERSONAL_BY_USER = """
SELECT ap.id, ap.id_usuario, ap.id_evento, e.nombre AS nombre_evento, ap.recordatorio, ap.notas
FROM agenda_personal ap
JOIN evento e ON ap.id_evento = e.id
WHERE ap.id_usuario = %s
"""


GET_AGENDA_PERSONAL_BY_FECHA_USER = """
SELECT ap.id, ap.id_usuario, ap.id_evento, e.nombre AS nombre_evento, ap.recordatorio, ap.notas
FROM agenda_personal ap
JOIN evento e ON ap.id_evento = e.id
WHERE DATE(ap.fecha) = %s AND ap.id_usuario = %s
"""


CREATE_AGENDA_PERSONAL = """
INSERT INTO agenda_personal (id_usuario, id_evento, recordatorio, notas)
VALUES (%s, %s, %s, %s)
"""

UPDATE_AGENDA_PERSONAL = """
UPDATE agenda_personal
SET recordatorio = %s, notas = %s
WHERE id = %s
"""

DELETE_AGENDA_PERSONAL = """
DELETE FROM agenda_personal
WHERE id = %s
"""
