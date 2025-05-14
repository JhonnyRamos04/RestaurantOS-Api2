from flask import jsonify, request
from src.models.payment_method import PaymentMethod, db

def get_payment_methods():
    """Get all payment methods"""
    try:
        all_methods = PaymentMethod.query.all()
        methods_list = [m.to_dict() for m in all_methods]
        return jsonify(methods_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_payment_method_by_id(id_payment_method):
    """Get a payment method by ID"""
    try:
        method = PaymentMethod.query.get(id_payment_method)
        if method:
            return jsonify(method.to_dict())
        return jsonify({"message": "Payment method not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_active_payment_methods():
    """Get all active payment methods"""
    try:
        methods = PaymentMethod.query.filter_by(active=True).all()
        methods_list = [m.to_dict() for m in methods]
        return jsonify(methods_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Payment Method POST Controller ====================

def create_payment_method():
    """Create a new payment method"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'active']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Create new payment method
        new_method = PaymentMethod(
            name=data['name'],
            description=data.get('description'),
            active=data['active']
        )
        
        # Add to database
        db.session.add(new_method)
        db.session.commit()
        
        return jsonify({
            "message": "Payment method created successfully",
            "payment_method": new_method.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Payment Method PUT Controller ====================

def update_payment_method(id_payment_method):
    """Update an existing payment method"""
    try:
        method = PaymentMethod.query.get(id_payment_method)
        if not method:
            return jsonify({"error": "Payment method not found"}), 404
            
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Update fields if provided
        if 'name' in data:
            method.name = data['name']
        if 'description' in data:
            method.description = data['description']
        if 'active' in data:
            method.active = data['active']
            
        db.session.commit()
        
        return jsonify({
            "message": "Payment method updated successfully",
            "payment_method": method.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ==================== Payment Method DELETE Controller ====================

def delete_payment_method(id_payment_method):
    """Delete a payment method"""
    try:
        method = PaymentMethod.query.get(id_payment_method)
        if not method:
            return jsonify({"error": "Payment method not found"}), 404
            
        # Check if payment method is being used in sales
        if method.sales:
            return jsonify({"error": "Cannot delete payment method that is used in sales"}), 400
            
        db.session.delete(method)
        db.session.commit()
        
        return jsonify({
            "message": "Payment method deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500