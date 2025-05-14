from flask import jsonify, request
from src.models.status import Status, db

def get_status():
    """Get all status records"""
    try:
        all_status = Status.query.all()
        status_list = [s.to_dict() for s in all_status]
        return jsonify(status_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_status_by_id(id_status):
    """Get a status by ID"""
    try:
        status = Status.query.get(id_status)
        if status:
            return jsonify(status.to_dict())
        return jsonify({"message": "Status not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Status POST Controller ====================
def create_status():
    """Create a new status"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new status
        new_status = Status(
            name=data['name'],
            description=data.get('description')
        )
        
        # Add to database
        db.session.add(new_status)
        db.session.commit()
        
        return jsonify({
            "message": "Status created successfully",
            "status": new_status.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Status PUT Controller ====================

def update_status(id_status):
    """Update an existing status"""
    try:
        status = Status.query.get(id_status)
        if not status:
            return jsonify({"error": "Status not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            status.name = data['name']
        if 'description' in data:
            status.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            "message": "Status updated successfully",
            "status": status.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# ==================== Status DELETE Controller ====================
def delete_status(id_status):
    """Delete a status"""
    try:
        status = Status.query.get(id_status)
        if not status:
            return jsonify({"error": "Status not found"}), 404
            
        # Check if status is being used
        if status.menus or status.tables or status.orders:
            return jsonify({"error": "Cannot delete status that is in use"}), 400
            
        db.session.delete(status)
        db.session.commit()
        
        return jsonify({
            "message": "Status deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500