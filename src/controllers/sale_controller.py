from flask import jsonify, request
from src.models.sale import Sale, db
from src.models.payment_method import PaymentMethod
from src.models.order import Order

def get_sales():
    """Get all sales"""
    try:
        all_sales = Sale.query.all()
        sales_list = [s.to_dict() for s in all_sales]
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sale_by_id(id_sale):
    """Get a sale by ID"""
    try:
        sale = Sale.query.get(id_sale)
        if sale:
            return jsonify(sale.to_dict())
        return jsonify({"message": "Sale not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sales_by_order(id_order):
    """Get sales for a specific order"""
    try:
        sales = Sale.query.filter_by(id_order=id_order).all()
        sales_list = [s.to_dict() for s in sales]
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sales_by_cashier(id_casher):
    """Get sales processed by a specific cashier"""
    try:
        sales = Sale.query.filter_by(id_casher=id_casher).all()
        sales_list = [s.to_dict() for s in sales]
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sales_by_payment_method(id_payment_method):
    """Get sales by payment method"""
    try:
        sales = Sale.query.filter_by(id_payment_method=id_payment_method).all()
        sales_list = [s.to_dict() for s in sales]
        return jsonify(sales_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_sales_summary():
    """Get a summary of all sales"""
    try:
        # Total sales
        total_sales = db.session.query(db.func.sum(Sale.total)).scalar() or 0
        
        # Count of sales
        sales_count = Sale.query.count()
        
        # Sales by payment method
        payment_methods = PaymentMethod.query.all()
        sales_by_payment = []
        
        for method in payment_methods:
            method_total = db.session.query(db.func.sum(Sale.total))\
                .filter(Sale.id_payment_method == method.id_payment_method).scalar() or 0
            
            sales_by_payment.append({
                'payment_method': method.name,
                'total': float(method_total)
            })
        
        return jsonify({
            'total_sales': float(total_sales),
            'sales_count': sales_count,
            'sales_by_payment_method': sales_by_payment
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==================== Sale POST Controller ====================
def create_sale():
    """Create a new sale"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id_order', 'id_payment_method', 'id_casher', 'items_count']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
                
        # Get order to calculate total if not provided
        if 'total' not in data:
            order = Order.query.get(data['id_order'])
            if not order:
                return jsonify({"error": "Order not found"}), 404
            total = order.total
        else:
            total = data['total']
            
        # Create new sale
        new_sale = Sale(
            total=total,
            discount=data.get('discount'),
            list=data.get('list'),
            items_count=data['items_count'],
            id_payment_method=data['id_payment_method'],
            id_order=data['id_order'],
            id_casher=data['id_casher'],
            database=data.get('database')
        )
        
        # Add to database
        db.session.add(new_sale)
        
        # Update order status if needed
        if 'update_order_status' in data and data['update_order_status']:
            order = Order.query.get(data['id_order'])
            if order:
                # Assuming status ID 3 is 'Completed' or 'Paid'
                order.id_status = data.get('new_status_id', 3)
                
        db.session.commit()
        
        return jsonify({
            "message": "Sale created successfully",
            "sale": new_sale.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
