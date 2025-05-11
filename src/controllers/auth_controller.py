from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    get_jwt_identity, jwt_required
)
from src.models.user import User, db
from src.models.role import Role
from datetime import datetime

def register_user():
    """Registrar un nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['name', 'username', 'password', 'id_role']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} es requerido"}), 400
        
        # Verificar si el usuario ya existe
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({"error": "El nombre de usuario ya existe"}), 409
        
        # Verificar si el rol existe
        role = Role.query.get(data['id_role'])
        if not role:
            return jsonify({"error": "El rol especificado no existe"}), 400
        
        # Crear nuevo usuario
        new_user = User(
            name=data['name'],
            username=data['username'],
            id_role=data['id_role'],
            id_solve=data.get('id_solve')
        )
        
        # Establecer contraseña hasheada
        new_user.set_password(data['password'])
        
        # Guardar en la base de datos
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def login_user():
    """Iniciar sesión y obtener tokens"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Se requiere nombre de usuario y contraseña"}), 400
        
        # Buscar usuario
        user = User.query.filter_by(username=data['username']).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if not user or not user.check_password(data['password']):
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Crear tokens
        access_token = create_access_token(identity=user.id_user)
        refresh_token = create_refresh_token(identity=user.id_user)
        
        return jsonify({
            "message": "Inicio de sesión exitoso",
            "user": user.to_dict(),
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required(refresh=True)
def refresh_token():
    """Renovar el token de acceso usando el token de actualización"""
    try:
        # Obtener identidad del usuario desde el token de actualización
        current_user_id = get_jwt_identity()
        
        # Crear nuevo token de acceso
        access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            "access_token": access_token
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
def get_current_user():
    """Obtener información del usuario actual"""
    try:
        # Obtener identidad del usuario desde el token
        current_user_id = get_jwt_identity()
        
        # Buscar usuario
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        return jsonify({
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@jwt_required()
def change_password():
    """Cambiar contraseña del usuario actual"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data or 'current_password' not in data or 'new_password' not in data:
            return jsonify({"error": "Se requiere contraseña actual y nueva"}), 400
        
        # Obtener identidad del usuario desde el token
        current_user_id = get_jwt_identity()
        
        # Buscar usuario
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        # Verificar contraseña actual
        if not user.check_password(data['current_password']):
            return jsonify({"error": "Contraseña actual incorrecta"}), 401
        
        # Establecer nueva contraseña
        user.set_password(data['new_password'])
        
        # Guardar en la base de datos
        db.session.commit()
        
        return jsonify({
            "message": "Contraseña cambiada exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
