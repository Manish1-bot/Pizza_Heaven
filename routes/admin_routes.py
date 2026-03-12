import os
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required
from utils.db import db
from utils.helpers import admin_required, save_picture
from models.user import User
from models.pizza import Pizza
from models.order import Order
from forms.pizza_forms import PizzaForm

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    today = date.today()
    
    total_orders_today = Order.query.filter(db.func.date(Order.order_date) == today).count()
    revenue_query = db.session.query(db.func.sum(Order.total_amount)).filter(db.func.date(Order.order_date) == today).scalar()
    total_revenue = revenue_query if revenue_query else 0.0
    
    pending_orders = Order.query.filter_by(status='pending').count()
    total_customers = User.query.filter_by(is_admin=False).count()
    
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           total_orders_today=total_orders_today,
                           total_revenue=total_revenue,
                           pending_orders=pending_orders,
                           total_customers=total_customers,
                           recent_orders=recent_orders)

@admin.route('/pizzas')
@login_required
@admin_required
def manage_pizzas():
    pizzas = Pizza.query.all()
    return render_template('admin/manage_pizzas.html', pizzas=pizzas)

@admin.route('/pizza/new', methods=['GET', 'POST'])
@login_required
@admin_required
def add_pizza():
    form = PizzaForm()
    if form.validate_on_submit():
        pizza = Pizza(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            size_small_price=form.size_small_price.data,
            size_medium_price=form.size_medium_price.data,
            size_large_price=form.size_large_price.data,
            is_available=form.is_available.data
        )
        if form.image.data:
            picture_file = save_picture(form.image.data)
            pizza.image_url = picture_file
            
        db.session.add(pizza)
        db.session.commit()
        flash('Pizza has been created!', 'success')
        return redirect(url_for('admin.manage_pizzas'))
    return render_template('admin/add_pizza.html', title='New Pizza', form=form, legend='New Pizza')

@admin.route('/pizza/<int:pizza_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_pizza(pizza_id):
    pizza = Pizza.query.get_or_404(pizza_id)
    form = PizzaForm()
    if form.validate_on_submit():
        if form.image.data:
            picture_file = save_picture(form.image.data)
            pizza.image_url = picture_file
            
        pizza.name = form.name.data
        pizza.description = form.description.data
        pizza.category = form.category.data
        pizza.size_small_price = form.size_small_price.data
        pizza.size_medium_price = form.size_medium_price.data
        pizza.size_large_price = form.size_large_price.data
        pizza.is_available = form.is_available.data
        
        db.session.commit()
        flash('Pizza has been updated!', 'success')
        return redirect(url_for('admin.manage_pizzas'))
    elif request.method == 'GET':
        form.name.data = pizza.name
        form.description.data = pizza.description
        form.category.data = pizza.category
        form.size_small_price.data = pizza.size_small_price
        form.size_medium_price.data = pizza.size_medium_price
        form.size_large_price.data = pizza.size_large_price
        form.is_available.data = pizza.is_available
        
    return render_template('admin/edit_pizza.html', title='Edit Pizza', form=form, legend='Edit Pizza', pizza=pizza)

@admin.route('/pizza/<int:pizza_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_pizza(pizza_id):
    pizza = Pizza.query.get_or_404(pizza_id)
    db.session.delete(pizza)
    db.session.commit()
    flash('Pizza has been deleted!', 'success')
    return redirect(url_for('admin.manage_pizzas'))

@admin.route('/orders')
@login_required
@admin_required
def orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@admin.route('/order/<int:order_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def view_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if request.method == 'POST':
        new_status = request.form.get('status')
        if new_status in ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']:
            order.status = new_status
            db.session.commit()
            flash(f'Order status updated to {new_status}', 'success')
            
    return render_template('admin/view_order.html', order=order)
