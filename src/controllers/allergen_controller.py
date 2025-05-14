from flask import jsonify, request
from src.models.allergen import Allergen, db
from src.models.menu import Menu


def get_allergens():
    """Get all allergens"""
    try:
        all_allergens = Allergen.query.all()
        allergens_list = [a.to_dict() for a in all_allergens]
        return jsonify(allergens_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_allergen_by_id(id_allergen):
    """Get an allergen by ID"""
    try:
        allergen = Allergen.query.get(id_allergen)
        if allergen:
            return jsonify(allergen.to_dict())
        return jsonify({"message": "Allergen not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_menu_allergens(id_menu):
    """Get allergens for a specific menu item"""
    try:
        menu = Menu.query.get(id_menu)
        if not menu:
            return jsonify({"message": "Menu item not found"}), 404
            
        allergens = menu.allergens
        allergens_list = [a.to_dict() for a in allergens]
        return jsonify(allergens_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Allergen POST Controller ====================

def create_allergen():
    """Create a new allergen"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new allergen
        new_allergen = Allergen(
            name=data['name'],
            description=data.get('description')
        )
        
        # Add to database
        db.session.add(new_allergen)
        db.session.commit()
        
        return jsonify({
            "message": "Allergen created successfully",
            "allergen": new_allergen.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Allergen PUT Controller ====================

def update_allergen(id_allergen):
    """Update an existing allergen"""
    try:
        allergen = Allergen.query.get(id_allergen)
        if not allergen:
            return jsonify({"error": "Allergen not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            allergen.name = data['name']
        if 'description' in data:
            allergen.description = data['description']
            
        db.session.commit()
        
        return jsonify({
            "message": "Allergen updated successfully",
            "allergen": allergen.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Allergen DELETE Controller ====================

def delete_allergen(id_allergen):
    """Delete an allergen"""
    try:
        allergen = Allergen.query.get(id_allergen)
        if not allergen:
            return jsonify({"error": "Allergen not found"}), 404
            
        # Check if allergen is being used in menu items
        if allergen.menus:
            return jsonify({"error": "Cannot delete allergen that is used in menu items"}), 400
            
        # Remove menu associations
        Menu.query.filter_by(id_allegers=id_allergen).delete()
        
        # Delete allergen
        db.session.delete(allergen)
        db.session.commit()
        
        return jsonify({
            "message": "Allergen deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500