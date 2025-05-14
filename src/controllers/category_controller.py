from flask import jsonify, request
from src.models.category import Category, db

def get_categories():
    """Get all categories"""
    try:
        all_categories = Category.query.all()
        categories_list = [c.to_dict() for c in all_categories]
        return jsonify(categories_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_category_by_id(id_category):
    """Get a category by ID"""
    try:
        category = Category.query.get(id_category)
        if category:
            return jsonify(category.to_dict())
        return jsonify({"message": "Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ==================== Category POST Controller ====================
def create_category():
    """Create a new category"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({"error": "Name is required"}), 400
            
        # Create new category
        new_category = Category(
            name=data['name'],
            description=data.get('description'),
            image_url=data.get('image_url')
        )
        
        # Add to database
        db.session.add(new_category)
        db.session.commit()
        
        return jsonify({
            "message": "Category created successfully",
            "category": new_category.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Category PUT Controller ====================

def update_category(id_category):
    """Update an existing category"""
    try:
        category = Category.query.get(id_category)
        if not category:
            return jsonify({"error": "Category not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        if 'image_url' in data:
            category.image_url = data['image_url']
            
        db.session.commit()
        
        return jsonify({
            "message": "Category updated successfully",
            "category": category.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Category DELETE Controller ====================

def delete_category(id_category):
    """Delete a category"""
    try:
        category = Category.query.get(id_category)
        if not category:
            return jsonify({"error": "Category not found"}), 404
            
        # Check if category is being used
        if category.menus:
            return jsonify({"error": "Cannot delete category that has menu items"}), 400
            
        db.session.delete(category)
        db.session.commit()
        
        return jsonify({
            "message": "Category deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500