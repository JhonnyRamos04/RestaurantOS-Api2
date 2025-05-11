from flask import Blueprint
from src.controllers.allergen_controller import get_allergens, get_allergen_by_id, get_menu_allergens, create_allergen

allergen_bp = Blueprint('allergen', __name__)

@allergen_bp.route('/', methods=['GET'])
def all_allergens():
    return get_allergens()

@allergen_bp.route('/<int:id_allergen>', methods=['GET'])
def allergen_by_id(id_allergen):
    return get_allergen_by_id(id_allergen)

@allergen_bp.route('/menus/<int:id_menu>', methods=['GET'])
def menu_allergens(id_menu):
    return get_menu_allergens(id_menu)

@allergen_bp.route('/', methods=['POST'])
def add_allergen():
    return create_allergen()
