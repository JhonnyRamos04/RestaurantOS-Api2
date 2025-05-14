from flask import Blueprint
from src.controllers.order_controller import delete_order, get_orders, get_order_by_id, get_orders_by_table, get_orders_by_waiter, get_orders_by_status, get_order_with_details, create_order, update_order

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['GET'])
def all_orders():
    return get_orders()

@order_bp.route('/<int:id_order>', methods=['GET'])
def order_by_id(id_order):
    return get_order_by_id(id_order)

@order_bp.route('/table/<int:id_table>', methods=['GET'])
def orders_by_table(id_table):
    return get_orders_by_table(id_table)

@order_bp.route('/waiter/<int:id_walker>', methods=['GET'])
def orders_by_waiter(id_walker):
    return get_orders_by_waiter(id_walker)

@order_bp.route('/status/<int:id_status>', methods=['GET'])
def orders_by_status(id_status):
    return get_orders_by_status(id_status)

@order_bp.route('/<int:id_order>/details', methods=['GET'])
def order_with_details(id_order):
    return get_order_with_details(id_order)

@order_bp.route('/', methods=['POST'])
def add_order():
    return create_order()

@order_bp.route('/<int:id_order>', methods=['PUT'])
def modify_order(id_order):
    return update_order(id_order)

@order_bp.route('/<int:id_order>', methods=['DELETE'])
def remove_order(id_order):
    return delete_order(id_order)