from flask import Blueprint
from src.controllers.payment_method_controller import delete_payment_method, get_payment_methods, get_payment_method_by_id, get_active_payment_methods, create_payment_method, update_payment_method

payment_method_bp = Blueprint('payment_method', __name__)

@payment_method_bp.route('/', methods=['GET'])
def all_payment_methods():
    return get_payment_methods()

@payment_method_bp.route('/<int:id_payment_method>', methods=['GET'])
def payment_method_by_id(id_payment_method):
    return get_payment_method_by_id(id_payment_method)

@payment_method_bp.route('/active', methods=['GET'])
def active_payment_methods():
    return get_active_payment_methods()

@payment_method_bp.route('/', methods=['POST'])
def add_payment_method():
    return create_payment_method()

@payment_method_bp.route('/<int:id_payment_method>', methods=['PUT'])
def modify_payment_method(id_payment_method):
    return update_payment_method(id_payment_method)

@payment_method_bp.route('/<int:id_payment_method>', methods=['DELETE'])
def remove_payment_method(id_payment_method):
    return delete_payment_method(id_payment_method)