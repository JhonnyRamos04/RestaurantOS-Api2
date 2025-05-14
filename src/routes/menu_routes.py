from flask import Blueprint
from src.controllers.menu_controller import delete_menu, get_menus, get_menu_by_id, get_menus_by_category, get_available_menus, get_popular_menus, create_menu, update_menu

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def all_menus():
    return get_menus()

@menu_bp.route('/<int:id_menu>', methods=['GET'])
def menu_by_id(id_menu):
    return get_menu_by_id(id_menu)

@menu_bp.route('/category/<int:id_category>', methods=['GET'])
def menus_by_category(id_category):
    return get_menus_by_category(id_category)

@menu_bp.route('/available', methods=['GET'])
def available_menus():
    return get_available_menus()

@menu_bp.route('/popular', methods=['GET'])
def popular_menus():
    return get_popular_menus()

@menu_bp.route('/', methods=['POST'])
def add_menu():
    return create_menu()

@menu_bp.route('/<int:id_menu>', methods=['PUT'])
def modify_menu(id_menu):
    return update_menu(id_menu)

@menu_bp.route('/<int:id_menu>', methods=['DELETE'])
def remove_menu(id_menu):
    return delete_menu(id_menu)
