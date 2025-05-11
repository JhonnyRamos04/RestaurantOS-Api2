from flask import Blueprint
from src.controllers.user_controller import (
    get_users, get_user_by_id, get_users_by_role,
    create_user, update_user, delete_user
)

user_bp = Blueprint('users', __name__)

# ==================== User Routes ====================
@user_bp.route('', methods=['GET'])
def all_users():
    return get_users()

@user_bp.route('/<int:id_user>', methods=['GET'])
def user_by_id(id_user):
    return get_user_by_id(id_user)

@user_bp.route('/role/<int:id_role>', methods=['GET'])
def users_by_role(id_role):
    return get_users_by_role(id_role)

# Rutas para gestionar usuarios (protegidas)
@user_bp.route('', methods=['POST'])
def add_user():
    return create_user()

@user_bp.route('/<int:id_user>', methods=['PUT'])
def modify_user(id_user):
    return update_user(id_user)

@user_bp.route('/<int:id_user>', methods=['DELETE'])
def remove_user(id_user):
    return delete_user(id_user)