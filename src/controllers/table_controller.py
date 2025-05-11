from flask import jsonify, request
from src.models.table import Table, db

def get_tables():
    """Get all tables"""
    try:
        all_tables = Table.query.all()
        tables_list = [t.to_dict() for t in all_tables]
        return jsonify(tables_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_table_by_id(id_table):
    """Get a table by ID"""
    try:
        table = Table.query.get(id_table)
        if table:
            return jsonify(table.to_dict())
        return jsonify({"message": "Table not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_tables_by_status(id_status):
    """Get tables by status ID"""
    try:
        tables = Table.query.filter_by(id_status=id_status).all()
        tables_list = [t.to_dict() for t in tables]
        return jsonify(tables_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_available_tables():
    """Get all available tables"""
    try:
        # Assuming status ID 1 is 'Available'
        # You should replace this with the actual status ID for available tables
        available_status_id = 1  
        tables = Table.query.filter_by(id_status=available_status_id).all()
        tables_list = [t.to_dict() for t in tables]
        return jsonify(tables_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_tables_by_waiter(id_walker):
    """Get tables assigned to a specific waiter"""
    try:
        tables = Table.query.filter_by(id_walker=id_walker).all()
        tables_list = [t.to_dict() for t in tables]
        return jsonify(tables_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ==================== Table POST Controller ====================
def create_table():
    """Create a new table"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['number', 'capacity', 'id_status']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Check if table number already exists
        existing_table = Table.query.filter_by(number=data['number']).first()
        if existing_table:
            return jsonify({"error": "Table number already exists"}), 409
            
        # Create new table
        new_table = Table(
            number=data['number'],
            capacity=data['capacity'],
            section=data.get('section'),
            id_status=data['id_status'],
            id_walker=data.get('id_walker'),
            guests=data.get('guests'),
            occupied_at=data.get('occupied_at')
        )
        
        # Add to database
        db.session.add(new_table)
        db.session.commit()
        
        return jsonify({
            "message": "Table created successfully",
            "table": new_table.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
