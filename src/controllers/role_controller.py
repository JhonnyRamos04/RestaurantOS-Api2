from flask import jsonify, request
from src.models.role import Role, db

def get_roles():
    """Get all roles"""
    try:
        all_roles = Role.query.all()
        roles_list = [r.to_dict() for r in all_roles]
        return jsonify(roles_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_role_by_id(id_role):
    """Get a role by ID"""
    try:
        role = Role.query.get(id_role)
        if role:
            return jsonify(role.to_dict())
        return jsonify({"message": "Role not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Role POST Controller ====================
def create_role():
    """Create a new role"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new role
        new_role = Role(
            name=data['name'],
            description=data.get('description')
        )
        
        # Add to database
        db.session.add(new_role)
        db.session.commit()
        
        return jsonify({
            "message": "Role created successfully",
            "role": new_role.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500