from src.db.connection import db

class Allergen(db.Model):
    __tablename__ = 'allegers'  # Nota: hay un error de ortografía en el esquema original
    id_allegers = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Allergen id={self.id_allegers}, name={self.name}>'
    
    def to_dict(self):
        return {
            'id_allegers': self.id_allegers,
            'name': self.name,
            'description': self.description
        }