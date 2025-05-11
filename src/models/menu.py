from src.db.connection import db

class Menu(db.Model):
    __tablename__ = 'menu'
    id_menu = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categories.id_category'), nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    cost = db.Column(db.Numeric(10, 2))
    popularity = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    
    # Relaciones
    allergens = db.relationship('Allergen', secondary='menu_allegers', backref=db.backref('menus', lazy=True))
    order_details = db.relationship('DetailOrder', backref='menu_item', lazy=True)

    def __repr__(self):
        return f'<Menu id={self.id_menu}, name={self.name}, price={self.price}>'
    
    def to_dict(self):
        return {
            'id_menu': self.id_menu,
            'name': self.name,
            'id_category': self.id_category,
            'id_status': self.id_status,
            'price': float(self.price) if self.price else None,
            'description': self.description,
            'cost': float(self.cost) if self.cost else None,
            'popularity': self.popularity,
            'stock': self.stock,
            'availability': self.availability
        }
    
# Tabla de unión para la relación muchos a muchos entre Menu y Allergen
class MenuAllergen(db.Model):
    __tablename__ = 'menu_allegers'
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id_menu'), primary_key=True)
    id_allegers = db.Column(db.Integer, db.ForeignKey('allegers.id_allegers'), primary_key=True)
