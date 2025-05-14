from flask import Blueprint
from src.controllers.role_controller import delete_role, get_roles, get_role_by_id, create_role, update_role

role_bp = Blueprint('role', __name__)

@role_bp.route('/', methods=['GET'])
def all_roles():
    return get_roles()

@role_bp.route('/<int:id_role>', methods=['GET'])
def role_by_id(id_role):
    return get_role_by_id(id_role)

@role_bp.route('/', methods=['POST'])
def add_role():
    return create_role()

@role_bp.route('/<int:id_role>', methods=['PUT'])
def modify_role(id_role):
    return update_role(id_role)

@role_bp.route('/<int:id_role>', methods=['DELETE'])
def remove_role(id_role):
    return delete_role(id_role)
