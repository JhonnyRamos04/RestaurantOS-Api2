from src.db.connection import db

class Order(db.Model):
    __tablename__ = 'orders'
    id_order = db.Column(db.Integer, primary_key=True)
    id_table = db.Column(db.Integer, db.ForeignKey('tables.id_table'), nullable=False)
    id_walker = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    items_count = db.Column(db.Integer, nullable=False)
    id_status = db.Column(db.Integer, db.ForeignKey('status.id_status'), nullable=False)
    order_type = db.Column(db.String(50))
    
    # Relaciones
    details = db.relationship('DetailOrder', backref='order', lazy=True)
    sale = db.relationship('Sale', backref='order', lazy=True, uselist=False)

    def __repr__(self):
        return f'<Order id={self.id_order}, total={self.total}, date={self.date}>'
    
    def to_dict(self):
        return {
            'id_order': self.id_order,
            'id_table': self.id_table,
            'id_walker': self.id_walker,
            'date': self.date.isoformat() if self.date else None,
            'total': float(self.total) if self.total else None,
            'items_count': self.items_count,
            'id_status': self.id_status,
            'order_type': self.order_type
        }