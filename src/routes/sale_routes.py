from flask import Blueprint
from src.controllers.sale_controller import create_sale, get_sales, get_sale_by_id, get_sales_by_order, get_sales_by_cashier, get_sales_by_payment_method, get_sales_summary

sale_bp = Blueprint('sale', __name__)

@sale_bp.route('/sales', methods=['GET'])
def all_sales():
    return get_sales()

@sale_bp.route('/sales/<int:id_sale>', methods=['GET'])
def sale_by_id(id_sale):
    return get_sale_by_id(id_sale)

@sale_bp.route('/orders/<int:id_order>/sales', methods=['GET'])
def sales_by_order(id_order):
    return get_sales_by_order(id_order)

@sale_bp.route('/users/<int:id_casher>/sales', methods=['GET'])
def sales_by_cashier(id_casher):
    return get_sales_by_cashier(id_casher)

@sale_bp.route('/payment-methods/<int:id_payment_method>/sales', methods=['GET'])
def sales_by_payment_method(id_payment_method):
    return get_sales_by_payment_method(id_payment_method)

@sale_bp.route('/sales/summary', methods=['GET'])
def sales_summary():
    return get_sales_summary()

@sale_bp.route('/sales', methods=['POST'])
def add_sale():
    return create_sale()