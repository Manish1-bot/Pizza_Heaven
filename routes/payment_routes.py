import razorpay
from flask import Blueprint, render_template, request, session, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from utils.db import db
from models.order import Order, OrderItem
from models.payment import Payment

payment = Blueprint('payment', __name__)

@payment.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.menu'))
        
    subtotal = sum(item['price'] * item['quantity'] for item in cart.values())
    tax = subtotal * 0.05
    total = subtotal + tax
    
    if request.method == 'POST':
        delivery_address = request.form.get('address')
        special_instructions = request.form.get('special_instructions')
        
        # Create Order
        new_order = Order(
            user_id=current_user.id,
            total_amount=total,
            delivery_address=delivery_address,
            special_instructions=special_instructions,
            payment_method='online'
        )
        db.session.add(new_order)
        db.session.flush() # Get the new_order.id
        
        # Create Order Items
        for item_key, item in cart.items():
            order_item = OrderItem(
                order_id=new_order.id,
                pizza_id=item['pizza_id'],
                size=item['size'],
                quantity=item['quantity'],
                unit_price=item['price']
            )
            db.session.add(order_item)
            
        db.session.commit()
        
        # Clear cart but store order id for payment
        session['cart'] = {}
        session['current_order_id'] = new_order.id
        
        return redirect(url_for('payment.process_payment'))
        
    return render_template('checkout.html', cart=cart, subtotal=subtotal, tax=tax, total=total)

@payment.route('/process_payment')
@login_required
def process_payment():
    order_id = session.get('current_order_id')
    if not order_id:
        return redirect(url_for('main.index'))
        
    order = Order.query.get_or_404(order_id)
    
    # Initialize Razorpay Client
    client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
    
    # Create Razorpay Order
    # Amount is in paise (INR * 100)
    data = {
        "amount": int(order.total_amount * 100),
        "currency": "INR",
        "receipt": f"receipt_order_{order.id}",
        "payment_capture": 1
    }
    
    try:
        razorpay_order = client.order.create(data=data)
        
        # Store razorpay order id
        session['razorpay_order_id'] = razorpay_order['id']
        
        return render_template('payment.html', order=order, razorpay_order=razorpay_order, 
                              key_id=current_app.config['RAZORPAY_KEY_ID'])
    except Exception as e:
        flash(f'Error creating payment order: {str(e)}', 'danger')
        return redirect(url_for('main.index'))

@payment.route('/payment_success', methods=['POST'])
@login_required
def payment_success():
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    razorpay_order_id = request.form.get('razorpay_order_id')
    razorpay_signature = request.form.get('razorpay_signature')
    
    order_id = session.get('current_order_id')
    if not order_id:
        return redirect(url_for('main.index'))
        
    order = Order.query.get_or_404(order_id)
    
    client = razorpay.Client(auth=(current_app.config['RAZORPAY_KEY_ID'], current_app.config['RAZORPAY_KEY_SECRET']))
    
    try:
        # Verify Payment Signature
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        
        # Payment is successful
        order.payment_status = 'completed'
        order.status = 'confirmed'
        
        new_payment = Payment(
            order_id=order.id,
            amount=order.total_amount,
            payment_method='razorpay',
            transaction_id=razorpay_payment_id,
            status='successful'
        )
        db.session.add(new_payment)
        db.session.commit()
        
        # Remove session variables
        session.pop('current_order_id', None)
        session.pop('razorpay_order_id', None)
        
        flash('Payment Successful! Your order has been placed.', 'success')
        return redirect(url_for('payment.receipt', order_id=order.id))
        
    except razorpay.errors.SignatureVerificationError:
        order.payment_status = 'failed'
        db.session.commit()
        flash('Payment Verification Failed.', 'danger')
        return redirect(url_for('main.index'))

@payment.route('/receipt/<int:order_id>')
@login_required
def receipt(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('main.index'))
        
    return render_template('receipt.html', order=order)
