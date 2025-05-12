#========== lib imports ===========
from flask import Flask
from flask_cors import CORS

# ============ app imports ========
from src.config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from src.db.connection import init_db
from src.routes.auth_routes import auth_bp
from src.routes.protected_routes import protected_bp
from src.routes.status_routes import status_bp
from src.routes.role_routes import role_bp
from src.routes.category_routes import category_bp
from src.routes.menu_routes import menu_bp
from src.routes.allergen_routes import allergen_bp
from src.routes.table_routes import table_bp
from src.routes.order_routes import order_bp
from src.routes.detail_order_routes import detail_order_bp
from src.routes.payment_method_routes import payment_method_bp
from src.routes.sale_routes import sale_bp
from src.routes.user_routes import user_bp
from src.config.cors_config import get_cors_config
from src.jwt.jwt import init_jwt
import os

def create_app():
    app = Flask(__name__)
    env = os.environ.get('FLASK_ENV', 'development')

    if env == 'production':
        app.config.from_object(ProductionConfig)
    elif env == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    init_db(app)
    init_jwt(app)

    CORS(app, resources=get_cors_config(env))

    with app.app_context():
        # Registrar rutas
        from .routes.routes import main, app_route
        app.register_blueprint(main)
        app.register_blueprint(status_bp, url_prefix='/status')
        app.register_blueprint(role_bp, url_prefix='/roles')
        app.register_blueprint(category_bp, url_prefix='/categories')
        app.register_blueprint(menu_bp, url_prefix='/menus')
        app.register_blueprint(allergen_bp, url_prefix='/allergens')
        app.register_blueprint(table_bp, url_prefix='/tables')
        app.register_blueprint(order_bp, url_prefix='/orders')
        app.register_blueprint(detail_order_bp, url_prefix='/detail-orders')
        app.register_blueprint(payment_method_bp, url_prefix='/payment-methods')
        app.register_blueprint(sale_bp, url_prefix='/sales')
        app.register_blueprint(user_bp, url_prefix='/users')
        app.register_blueprint(protected_bp)
        app.register_blueprint(auth_bp)

    return app
