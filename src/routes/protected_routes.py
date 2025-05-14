from flask import Blueprint
from flask_jwt_extended import jwt_required

#========= App Imports =========
from src.controllers.allergen_controller import create_allergen, delete_allergen, update_allergen
from src.controllers.category_controller import create_category
from src.controllers.payment_method_controller import create_payment_method
from src.controllers.sale_controller import create_sale, delete_sale, update_sale
from src.controllers.table_controller import create_table, delete_table, update_table
from src.middlewares.auth import admin_required, role_required
from src.controllers.status_controller import create_status
from src.controllers.order_controller import create_order
from src.controllers.detail_order_controller import create_detail_order
from src.controllers.role_controller import create_role
from src.controllers.menu_controller import create_menu, delete_menu, update_menu


protected_bp = Blueprint('protected', __name__)

# Rutas que requieren autenticación básica
@protected_bp.route('/orders', methods=['POST'])
@jwt_required()
def add_order():
    return create_order()

@protected_bp.route('/detail-orders', methods=['POST'])
@jwt_required()
def add_detail_order():
    return create_detail_order()

# Rutas que requieren rol de administrador
@protected_bp.route('/status', methods=['POST'])
@admin_required()
def add_status():
    return create_status()

@protected_bp.route('/roles', methods=['POST'])
@admin_required()
def add_role():
    return create_role()

@protected_bp.route('/categories', methods=['POST'])
@admin_required()
def add_category():
    return create_category()

@protected_bp.route('/payment-methods', methods=['POST'])
@admin_required()
def add_payment_method():
    return create_payment_method()

# Rutas que requieren roles específicos (admin o gerente)
@protected_bp.route('/menus', methods=['POST'])
@role_required([1, 2])  # Asumiendo que 1 es admin y 2 es gerente
def add_menu():
    return create_menu()

@protected_bp.route('/allergens', methods=['POST'])
@role_required([1, 2])
def add_allergen():
    return create_allergen()

@protected_bp.route('/tables', methods=['POST'])
@role_required([1, 2])
def add_table():
    return create_table()

@protected_bp.route('/sales', methods=['POST'])
@role_required([1, 2, 3])  # Asumiendo que 3 es cajero
def add_sale():
    return create_sale()

# PUT routes
@protected_bp.route('/menus/<int:id_menu>', methods=['PUT'])
@role_required([1, 2])
def modify_menu(id_menu):
    return update_menu(id_menu)

@protected_bp.route('/allergens/<int:id_allergen>', methods=['PUT'])
@role_required([1, 2])
def modify_allergen(id_allergen):
    return update_allergen(id_allergen)

@protected_bp.route('/tables/<int:id_table>', methods=['PUT'])
@role_required([1, 2])
def modify_table(id_table):
    return update_table(id_table)

@protected_bp.route('/sales/<int:id_sale>', methods=['PUT'])
@role_required([1, 2, 3])
def modify_sale(id_sale):
    return update_sale(id_sale)

# DELETE routes
@protected_bp.route('/menus/<int:id_menu>', methods=['DELETE'])
@role_required([1, 2])
def remove_menu(id_menu):
    return delete_menu(id_menu)

@protected_bp.route('/allergens/<int:id_allergen>', methods=['DELETE'])
@role_required([1, 2])
def remove_allergen(id_allergen):
    return delete_allergen(id_allergen)

@protected_bp.route('/tables/<int:id_table>', methods=['DELETE'])
@role_required([1, 2])
def remove_table(id_table):
    return delete_table(id_table)

@protected_bp.route('/sales/<int:id_sale>', methods=['DELETE'])
@role_required([1, 2])
def remove_sale(id_sale):
    return delete_sale(id_sale)

