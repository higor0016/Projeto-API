from app.extensions import db

class Autor(db.Model):
    __tablename__ = 'Autores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    biografia = db.Column(db.String(100))

    def __repr__(self):
        return f'<Autor {self.nome}'