from flask import jsonify, request
from src.models.menu import Menu, db, MenuAllergen

def get_menus():
    """Get all menu items"""
    try:
        all_menus = Menu.query.all()
        menus_list = [m.to_dict() for m in all_menus]
        return jsonify(menus_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_menu_by_id(id_menu):
    """Get a menu item by ID"""
    try:
        menu = Menu.query.get(id_menu)
        if menu:
            return jsonify(menu.to_dict())
        return jsonify({"message": "Menu item not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_menus_by_category(id_category):
    """Get menu items by category ID"""
    try:
        menus = Menu.query.filter_by(id_category=id_category).all()
        menus_list = [m.to_dict() for m in menus]
        return jsonify(menus_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_available_menus():
    """Get all available menu items"""
    try:
        menus = Menu.query.filter_by(availability=True).all()
        menus_list = [m.to_dict() for m in menus]
        return jsonify(menus_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_popular_menus(limit=10):
    """Get most popular menu items"""
    try:
        menus = Menu.query.order_by(Menu.popularity.desc()).limit(limit).all()
        menus_list = [m.to_dict() for m in menus]
        return jsonify(menus_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Menu POST Controller ====================

def create_menu():
    """Create a new menu item"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'id_category', 'id_status', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Create new menu item
        new_menu = Menu(
            name=data['name'],
            id_category=data['id_category'],
            id_status=data['id_status'],
            price=data['price'],
            description=data.get('description'),
            cost=data.get('cost'),
            popularity=data.get('popularity', 0),
            stock=data.get('stock'),
            availability=data.get('availability', True)
        )
        
        # Add to database
        db.session.add(new_menu)
        db.session.commit()
        
        # Handle allergens if provided
        if 'allergens' in data and isinstance(data['allergens'], list):
            for allergen_id in data['allergens']:
                menu_allergen = MenuAllergen(
                    id_menu=new_menu.id_menu,
                    id_allegers=allergen_id
                )
                db.session.add(menu_allergen)
            db.session.commit()
        
        return jsonify({
            "message": "Menu item created successfully",
            "menu": new_menu.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# ==================== Menu PUT Controller ====================

def update_menu(id_menu):
    """Update an existing menu item"""
    try:
        menu = Menu.query.get(id_menu)
        if not menu:
            return jsonify({"error": "Menu item not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            menu.name = data['name']
        if 'id_category' in data:
            menu.id_category = data['id_category']
        if 'id_status' in data:
            menu.id_status = data['id_status']
        if 'price' in data:
            menu.price = data['price']
        if 'description' in data:
            menu.description = data['description']
        if 'cost' in data:
            menu.cost = data['cost']
        if 'popularity' in data:
            menu.popularity = data['popularity']
        if 'stock' in data:
            menu.stock = data['stock']
        if 'availability' in data:
            menu.availability = data['availability']
            
        # Handle allergens if provided
        if 'allergens' in data and isinstance(data['allergens'], list):
            # Remove existing allergens
            MenuAllergen.query.filter_by(id_menu=id_menu).delete()
            
            # Add new allergens
            for allergen_id in data['allergens']:
                menu_allergen = MenuAllergen(
                    id_menu=id_menu,
                    id_allegers=allergen_id
                )
                db.session.add(menu_allergen)
                
        db.session.commit()
        
        return jsonify({
            "message": "Menu item updated successfully",
            "menu": menu.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Menu DELETE Controller ====================

def delete_menu(id_menu):
    """Delete a menu item"""
    try:
        menu = Menu.query.get(id_menu)
        if not menu:
            return jsonify({"error": "Menu item not found"}), 404
            
        # Check if menu is being used in orders
        if menu.order_details:
            return jsonify({"error": "Cannot delete menu item that is used in orders"}), 400
            
        # Remove allergen associations
        MenuAllergen.query.filter_by(id_menu=id_menu).delete()
        
        # Delete menu item
        db.session.delete(menu)
        db.session.commit()
        
        return jsonify({
            "message": "Menu item deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500