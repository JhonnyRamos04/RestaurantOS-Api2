from flask import Blueprint
from src.controllers.detail_order_controller import delete_detail_order, get_detail_orders, get_detail_order_by_id, get_detail_orders_by_order, get_detail_orders_by_menu, create_detail_order, update_detail_order

detail_order_bp = Blueprint('detail_order', __name__)

@detail_order_bp.route('/', methods=['GET'])
def all_detail_orders():
    return get_detail_orders()

@detail_order_bp.route('/<int:id_detail_order>', methods=['GET'])
def detail_order_by_id(id_detail_order):
    return get_detail_order_by_id(id_detail_order)

@detail_order_bp.route('/orders/<int:id_order>', methods=['GET'])
def detail_orders_by_order(id_order):
    return get_detail_orders_by_order(id_order)

@detail_order_bp.route('/menus/<int:id_menu>', methods=['GET'])
def detail_orders_by_menu(id_menu):
    return get_detail_orders_by_menu(id_menu)

@detail_order_bp.route('/', methods=['POST'])
def add_detail_order():
    return create_detail_order()

@detail_order_bp.route('/detail-orders/<int:id_detail_order>', methods=['PUT'])
def modify_detail_order(id_detail_order):
    return update_detail_order(id_detail_order)

@detail_order_bp.route('/detail-orders/<int:id_detail_order>', methods=['DELETE'])
def remove_detail_order(id_detail_order):
    return delete_detail_order(id_detail_order)