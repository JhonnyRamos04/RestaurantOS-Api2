from src.db.connection import db

class DetailOrder(db.Model):
    __tablename__ = 'detail_order'
    id_detail_order = db.Column(db.Integer, primary_key=True)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), nullable=False)
    id_menu = db.Column(db.Integer, db.ForeignKey('menu.id_menu'), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Numeric(5, 2))
    total = db.Column(db.Numeric(10, 2), nullable=False)
    database = db.Column(db.String(50))  # Nota: propósito no claro

    def __repr__(self):
        return f'<DetailOrder id={self.id_detail_order}, order={self.id_order}, menu={self.id_menu}>'
    
    def to_dict(self):
        return {
            'id_detail_order': self.id_detail_order,
            'id_order': self.id_order,
            'id_menu': self.id_menu,
            'price': float(self.price) if self.price else None,
            'quantity': self.quantity,
            'discount': float(self.discount) if self.discount else None,
            'total': float(self.total) if self.total else None,
            'database': self.database
        }