from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db

def get_users():
    """Get all users"""
    try:
        all_users = User.query.all()
        users_list = [u.to_dict() for u in all_users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_user_by_id(id_user):
    """Get a user by ID"""
    try:
        user = User.query.get(id_user)
        if user:
            return jsonify(user.to_dict())
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_users_by_role(id_role):
    """Get users by role ID"""
    try:
        users = User.query.filter_by(id_role=id_role).all()
        users_list = [u.to_dict() for u in users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ==================== User POST Controller ====================
@jwt_required()
def create_user():
    """Create a new user"""
    try:
        # Verificar si el usuario actual tiene permisos (asumiendo rol de admin es 1)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.id_role != 1:
            return jsonify({"error": "No tienes permisos para crear usuarios"}), 403
        
        data = request.get_json()
        
        # Validar required fields
        required_fields = ['name', 'username', 'password', 'id_role']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Check if username already exists
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 409
            
        # Create new user
        new_user = User(
            name=data['name'],
            username=data['username'],
            id_role=data['id_role'],
            id_solve=data.get('id_solve')
        )
        
        # Set hashed password
        new_user.set_password(data['password'])
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "User created successfully",
            "user": new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@jwt_required()
def update_user(id_user):
    """Update an existing user"""
    try:
        # Verificar si el usuario actual tiene permisos o es el mismo usuario
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or (current_user.id_role != 1 and current_user.id_user != id_user):
            return jsonify({"error": "No tienes permisos para actualizar este usuario"}), 403
        
        user = User.query.get(id_user)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        data = request.get_json()
        
        # Update fields if provided
        if 'name' in data:
            user.name = data['name']
            
        if 'username' in data and data['username'] != user.username:
            # Check if new username already exists
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                return jsonify({"error": "Username already exists"}), 409
            user.username = data['username']
            
        if 'password' in data:
            user.set_password(data['password'])
            
        # Only admin can change role
        if 'id_role' in data and current_user.id_role == 1:
            user.id_role = data['id_role']
            
        if 'id_solve' in data:
            user.id_solve = data['id_solve']
            
        db.session.commit()
        
        return jsonify({
            "message": "User updated successfully",
            "user": user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@jwt_required()
def delete_user(id_user):
    """Delete a user"""
    try:
        # Verificar si el usuario actual tiene permisos (solo admin)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if not current_user or current_user.id_role != 1:
            return jsonify({"error": "No tienes permisos para eliminar usuarios"}), 403
        
        user = User.query.get(id_user)
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            "message": "User deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500