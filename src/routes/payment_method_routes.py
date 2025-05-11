from flask import Blueprint
from src.controllers.payment_method_controller import get_payment_methods, get_payment_method_by_id, get_active_payment_methods, create_payment_method

payment_method_bp = Blueprint('payment_method', __name__)

@payment_method_bp.route('/payment-methods', methods=['GET'])
def all_payment_methods():
    return get_payment_methods()

@payment_method_bp.route('/payment-methods/<int:id_payment_method>', methods=['GET'])
def payment_method_by_id(id_payment_method):
    return get_payment_method_by_id(id_payment_method)

@payment_method_bp.route('/payment-methods/active', methods=['GET'])
def active_payment_methods():
    return get_active_payment_methods()

@payment_method_bp.route('/payment-methods', methods=['POST'])
def add_payment_method():
    return create_payment_method()