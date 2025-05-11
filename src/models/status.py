from src.db.connection import db

class Status(db.Model):
    __tablename__ = 'status'
    id_status = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # Relaciones
    menus = db.relationship('Menu', backref='status', lazy=True)
    tables = db.relationship('Table', backref='status', lazy=True)
    orders = db.relationship('Order', backref='status', lazy=True)

    def __repr__(self):
        return f'<Status id={self.id_status}, name={self.name}, description={self.description}>'
    
    def to_dict(self):
        return {
            'id_status': self.id_status,
            'name': self.name,
            'description': self.description
        }