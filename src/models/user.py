from werkzeug.security import generate_password_hash, check_password_hash
from src.db.connection import db

class User(db.Model):
    __tablename__ = 'users'
    id_user = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('roles.id_role'), nullable=False)
    id_solve = db.Column(db.Integer)
    
    # Relaciones
    tables_assigned = db.relationship('Table', backref='waiter', lazy=True, foreign_keys='Table.id_walker')
    orders_taken = db.relationship('Order', backref='waiter', lazy=True, foreign_keys='Order.id_walker')
    sales_processed = db.relationship('Sale', backref='cashier', lazy=True)

    def __repr__(self):
        return f'<User id={self.id_user}, username={self.username}>'
    
    def set_password(self, password):
        """Establece la contraseña hasheada para el usuario"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica si la contraseña proporcionada coincide con la almacenada"""
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id_user': self.id_user,
            'name': self.name,
            'username': self.username,
            'id_role': self.id_role,
            'id_solve': self.id_solve
        }