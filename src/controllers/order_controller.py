from flask import jsonify, request
from src.models.order import Order, db
from src.models.detail_order import DetailOrder
from datetime import datetime

def get_orders():
    """Get all orders"""
    try:
        all_orders = Order.query.all()
        orders_list = [o.to_dict() for o in all_orders]
        return jsonify(orders_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_order_by_id(id_order):
    """Get an order by ID"""
    try:
        order = Order.query.get(id_order)
        if order:
            return jsonify(order.to_dict())
        return jsonify({"message": "Order not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_orders_by_table(id_table):
    """Get orders for a specific table"""
    try:
        orders = Order.query.filter_by(id_table=id_table).all()
        orders_list = [o.to_dict() for o in orders]
        return jsonify(orders_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_orders_by_waiter(id_walker):
    """Get orders taken by a specific waiter"""
    try:
        orders = Order.query.filter_by(id_walker=id_walker).all()
        orders_list = [o.to_dict() for o in orders]
        return jsonify(orders_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_orders_by_status(id_status):
    """Get orders by status ID"""
    try:
        orders = Order.query.filter_by(id_status=id_status).all()
        orders_list = [o.to_dict() for o in orders]
        return jsonify(orders_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_order_with_details(id_order):
    """Get an order with its details"""
    try:
        order = Order.query.get(id_order)
        if not order:
            return jsonify({"message": "Order not found"}), 404
            
        order_dict = order.to_dict()
        details = DetailOrder.query.filter_by(id_order=id_order).all()
        details_list = [d.to_dict() for d in details]
        
        order_dict['details'] = details_list
        return jsonify(order_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Order POST Controller ====================
def create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id_table', 'id_walker', 'items_count', 'id_status']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Create new order
        new_order = Order(
            id_table=data['id_table'],
            id_walker=data['id_walker'],
            date=datetime.now(),
            total=data.get('total', 0),
            items_count=data['items_count'],
            id_status=data['id_status'],
            order_type=data.get('order_type')
        )
        
        # Add to database
        db.session.add(new_order)
        db.session.commit()
        
        # Handle order details if provided
        if 'details' in data and isinstance(data['details'], list):
            total = 0
            for detail in data['details']:
                if not all(k in detail for k in ['id_menu', 'price', 'quantity']):
                    continue
                    
                detail_total = detail['price'] * detail['quantity']
                if 'discount' in detail:
                    detail_total -= detail['discount']
                    
                new_detail = DetailOrder(
                    id_order=new_order.id_order,
                    id_menu=detail['id_menu'],
                    price=detail['price'],
                    quantity=detail['quantity'],
                    discount=detail.get('discount'),
                    total=detail_total,
                    database=detail.get('database')
                )
                db.session.add(new_detail)
                total += detail_total
                
            # Update order total
            new_order.total = total
            db.session.commit()
        
        return jsonify({
            "message": "Order created successfully",
            "order": new_order.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500