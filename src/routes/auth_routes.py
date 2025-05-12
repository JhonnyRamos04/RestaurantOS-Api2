from flask import Blueprint
from flask_cors import cross_origin
from src.controllers.auth_controller import (
    register_user, login_user, refresh_token, 
    get_current_user, change_password
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ==================== Auth Routes ====================
@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user()

@auth_bp.route('/login', methods=['POST'])
@cross_origin(origins=["http://localhost:3000", "https://tuaplicacion.com"])
def login():
    return login_user()

# Ruta para renovar token
@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    return refresh_token()

@auth_bp.route('/me', methods=['GET'])
def me():
    return get_current_user()

@auth_bp.route('/change-password', methods=['POST'])
def change_pass():
    return change_password()
