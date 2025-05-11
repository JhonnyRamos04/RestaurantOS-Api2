from src.db.connection import db

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    id_payment_method = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    active = db.Column(db.Boolean, nullable=False)
    
    # Relaciones
    sales = db.relationship('Sale', backref='payment_method', lazy=True)

    def __repr__(self):
        return f'<PaymentMethod id={self.id_payment_method}, name={self.name}>'
    
    def to_dict(self):
        return {
            'id_payment_method': self.id_payment_method,
            'name': self.name,
            'description': self.description,
            'active': self.active
        }