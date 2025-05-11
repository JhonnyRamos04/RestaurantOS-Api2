from src.db.connection import db

class Role(db.Model):
    __tablename__ = 'roles'
    id_role = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    
    # Relaciones
    users = db.relationship('User', backref='role', lazy=True)

    def __repr__(self):
        return f'<Role id={self.id_role}, name={self.name}>'
    
    def to_dict(self):
        return {
            'id_role': self.id_role,
            'name': self.name,
            'description': self.description
        }