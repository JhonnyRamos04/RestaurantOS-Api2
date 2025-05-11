from flask import jsonify, request
from src.models.detail_order import DetailOrder, db
from src.models.order import Order

def get_detail_orders():
    """Get all order details"""
    try:
        all_details = DetailOrder.query.all()
        details_list = [d.to_dict() for d in all_details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_detail_order_by_id(id_detail_order):
    """Get an order detail by ID"""
    try:
        detail = DetailOrder.query.get(id_detail_order)
        if detail:
            return jsonify(detail.to_dict())
        return jsonify({"message": "Order detail not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_detail_orders_by_order(id_order):
    """Get details for a specific order"""
    try:
        details = DetailOrder.query.filter_by(id_order=id_order).all()
        details_list = [d.to_dict() for d in details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_detail_orders_by_menu(id_menu):
    """Get order details for a specific menu item"""
    try:
        details = DetailOrder.query.filter_by(id_menu=id_menu).all()
        details_list = [d.to_dict() for d in details]
        return jsonify(details_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Detail Order POST Controller ====================
def create_detail_order():
    """Create a new order detail"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id_order', 'id_menu', 'price', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Calculate total
        total = data['price'] * data['quantity']
        if 'discount' in data:
            total -= data['discount']
            
        # Create new detail order
        new_detail = DetailOrder(
            id_order=data['id_order'],
            id_menu=data['id_menu'],
            price=data['price'],
            quantity=data['quantity'],
            discount=data.get('discount'),
            total=total,
            database=data.get('database')
        )
        
        # Add to database
        db.session.add(new_detail)
        
        # Update order total and items_count
        order = Order.query.get(data['id_order'])
        if order:
            order.total = db.session.query(db.func.sum(DetailOrder.total)).filter_by(id_order=data['id_order']).scalar() or 0
            order.items_count = db.session.query(db.func.sum(DetailOrder.quantity)).filter_by(id_order=data['id_order']).scalar() or 0
            
        db.session.commit()
        
        return jsonify({
            "message": "Order detail created successfully",
            "detail": new_detail.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500