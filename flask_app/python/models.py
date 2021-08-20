from flask_app import db
from datetime import datetime

class Cars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelo = db.Column(db.String(100), unique=False, nullable=False)
    placa = db.Column(db.String(7), unique=True, nullable=False)
    ano = db.Column(db.Integer, unique=False, nullable=False)
    estado = db.Column(db.Boolean, default=True, nullable=False)
    alugado = db.Column(db.Boolean, default=True, nullable=False)
    inicio_aluguel = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable=True)
    termino_aluguel = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable=True)

    #time = db.Column(db.DateTime, default=datetime.utcnow, unique=False, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'placa': self.placa,
            'ano': self.ano,
            'estado': self.estado,
            'alugado': self.alugado,
            'inicio_aluguel': self.inicio_aluguel,
            'termino_aluguel': self.termino_aluguel,
        }