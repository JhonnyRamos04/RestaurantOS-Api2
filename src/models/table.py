from src.db.connection import db

class Table(db.Model):
    __tablename__ = 'tables'
    id_table = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False, unique=True)
    capacity = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50))
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'), nullable=False)
    id_walker = db.Column(db.Integer, db.ForeignKey('users.id_user'))
    guests = db.Column(db.Integer)
    occupied_at = db.Column(db.DateTime)
    
    # Relaciones
    orders = db.relationship('Order', backref='table', lazy=True)

    def __repr__(self):
        return f'<Table id={self.id_table}, number={self.number}, capacity={self.capacity}>'
    
    def to_dict(self):
        return {
            'id_table': self.id_table,
            'number': self.number,
            'capacity': self.capacity,
            'section': self.section,
            'id_status': self.id_status,
            'id_walker': self.id_walker,
            'guests': self.guests,
            'occupied_at': self.occupied_at.isoformat() if self.occupied_at else None
        }