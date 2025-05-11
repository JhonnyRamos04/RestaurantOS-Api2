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