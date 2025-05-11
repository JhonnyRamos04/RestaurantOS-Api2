from src.db.connection import db

class Sale(db.Model):
    __tablename__ = 'sales'
    id_sale = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2))
    list = db.Column(db.JSON)  # JSONB en PostgreSQL
    items_count = db.Column(db.Integer, nullable=False)
    id_payment_method = db.Column(db.Integer, db.ForeignKey('payment_methods.id_payment_method'), nullable=False)
    id_order = db.Column(db.Integer, db.ForeignKey('orders.id_order'), nullable=False)
    id_casher = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    database = db.Column(db.String(50))  # Nota: propósito no claro

    def __repr__(self):
        return f'<Sale id={self.id_sale}, total={self.total}>'
    
    def to_dict(self):
        return {
            'id_sale': self.id_sale,
            'total': float(self.total) if self.total else None,
            'discount': float(self.discount) if self.discount else None,
            'list': self.list,
            'items_count': self.items_count,
            'id_payment_method': self.id_payment_method,
            'id_order': self.id_order,
            'id_casher': self.id_casher,
            'database': self.database
        }

