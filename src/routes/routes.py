from flask import Blueprint, jsonify
from src.controllers.user_controller import get_users, create_user
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

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Bienvenido a la API organizada de RestaurantOS"})

@main.route('/state')
def status():
    return jsonify({"status": "OK", "message": "La API está funcionando correctamente"})

# Registrar los blueprints
app_route = Blueprint('app_route', __name__)
