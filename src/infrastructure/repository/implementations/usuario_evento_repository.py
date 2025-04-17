

class UsuarioEventoRepository:
    def __init__(self, db):
        self.db = db

    def add_evento(self, evento):
        self.db.session.add(evento)
        self.db.session.commit()

    def get_eventos_by_usuairo(self, usuario_id):
        return self.db.session.query(Evento).filter_by(usuario_id=usuario_id).all()

    def get_evento_by_evento(self, evento_id):
        return self.db.session.query(Evento).get(evento_id)

    def delete_evento(self, evento_id):
        evento = self.db.session.query(Evento).get(evento_id)
        if evento:
            self.db.session.delete(evento)
            self.db.session.commit()



