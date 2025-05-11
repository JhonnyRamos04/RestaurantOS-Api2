from src.db.connection import db

class Category(db.Model):
    __tablename__ = 'categories'
    id_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    # Relaciones
    menus = db.relationship('Menu', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category id={self.id_category}, name={self.name}>'
    
    def to_dict(self):
        return {
            'id_category': self.id_category,
            'name': self.name,
            'description': self.description,
            'image_url': self.image_url
        }