from flask import Blueprint
from src.controllers.category_controller import get_categories, get_category_by_id, create_category

category_bp = Blueprint('category', __name__)

@category_bp.route('/', methods=['GET'])
def all_categories():
    return get_categories()

@category_bp.route('/<int:id_category>', methods=['GET'])
def category_by_id(id_category):
    return get_category_by_id(id_category)

@category_bp.route('/', methods=['POST'])
def add_category():
    return create_category()
