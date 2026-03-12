import json
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.pizza import Pizza
from models.order import OrderItem

main = Blueprint('main', __name__)

@main.route('/')
def index():
    featured_pizzas = Pizza.query.filter_by(is_available=True).limit(6).all()
    return render_template('index.html', pizzas=featured_pizzas)

@main.route('/menu')
def menu():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Pizza.query.filter_by(is_available=True)
    
    if category and category in ['veg', 'non-veg']:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Pizza.name.ilike(f'%{search}%'))
        
    pizzas = query.all()
    return render_template('menu.html', pizzas=pizzas)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/cart')
def cart_view():
    cart = session.get('cart', {})
    cart_items = []
    subtotal = 0
    
    for item_key, item in cart.items():
        pizza = Pizza.query.get(item['pizza_id'])
        if pizza:
            item_total = item['price'] * item['quantity']
            subtotal += item_total
            cart_items.append({
                'key': item_key,
                'pizza': pizza,
                'size': item['size'],
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item_total
            })
            
    tax = subtotal * 0.05 # 5% tax
    total = subtotal + tax
    
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal, tax=tax, total=total)

@main.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pizza_id = request.form.get('pizza_id')
    size = request.form.get('size')
    quantity = int(request.form.get('quantity', 1))
    
    pizza = Pizza.query.get_or_404(pizza_id)
    
    # Determine price based on size
    price = 0
    if size == 'small':
        price = pizza.size_small_price
    elif size == 'medium':
        price = pizza.size_medium_price
    elif size == 'large':
        price = pizza.size_large_price
        
    # Create unique key for cart item
    cart = session.get('cart', {})
    item_key = f"{pizza_id}_{size}"
    
    if item_key in cart:
        cart[item_key]['quantity'] += quantity
    else:
        cart[item_key] = {
            'pizza_id': pizza.id,
            'size': size,
            'quantity': quantity,
            'price': price,
            'name': pizza.name
        }
        
    session['cart'] = cart
    flash(f'{pizza.name} added to cart!', 'success')
    return redirect(request.referrer or url_for('main.menu'))

@main.route('/update_cart', methods=['POST'])
def update_cart():
    item_key = request.form.get('item_key')
    action = request.form.get('action')
    
    cart = session.get('cart', {})
    
    if item_key in cart:
        if action == 'increase':
            cart[item_key]['quantity'] += 1
        elif action == 'decrease':
            cart[item_key]['quantity'] -= 1
            if cart[item_key]['quantity'] <= 0:
                del cart[item_key]
        elif action == 'remove':
            del cart[item_key]
            
    session['cart'] = cart
    return redirect(url_for('main.cart_view'))
