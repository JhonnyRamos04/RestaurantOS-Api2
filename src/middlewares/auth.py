from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from src.models.user import User

def admin_required():
    """
    Decorador para requerir que el usuario sea administrador
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                # Verificar token
                verify_jwt_in_request()
                
                # Obtener identidad del usuario
                current_user_id = get_jwt_identity()
                
                # Buscar usuario
                user = User.query.get(current_user_id)
                
                # Verificar si es administrador
                if not user or user.id_role != 1:
                    return jsonify({"error": "Se requieren privilegios de administrador"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401
        return decorator
    return wrapper

def role_required(allowed_roles):
    """
    Decorador para requerir que el usuario tenga uno de los roles permitidos
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                # Verificar token
                verify_jwt_in_request()
                
                # Obtener identidad del usuario
                current_user_id = get_jwt_identity()
                
                # Buscar usuario
                user = User.query.get(current_user_id)
                
                # Verificar si tiene un rol permitido
                if not user or user.id_role not in allowed_roles:
                    return jsonify({"error": "No tienes permisos para acceder a este recurso"}), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({"error": str(e)}), 401
        return decorator
    return wrapper
