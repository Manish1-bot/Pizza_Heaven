import json
from datetime import datetime
from utils.db import db

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, preparing, ready, delivered, cancelled
    payment_method = db.Column(db.String(20), default='online') # online, cod
    payment_status = db.Column(db.String(20), default='pending') # pending, completed, failed
    delivery_address = db.Column(db.Text, nullable=False)
    special_instructions = db.Column(db.Text)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    payment = db.relationship('Payment', backref='order', uselist=False, lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id} for User {self.user_id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    size = db.Column(db.String(10), nullable=False) # small, medium, large
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    toppings = db.Column(db.Text) # Stored as JSON string
    
    pizza = db.relationship('Pizza')
    
    @property
    def toppings_list(self):
        if self.toppings:
            return json.loads(self.toppings)
        return []

    def set_toppings(self, toppings_list):
        self.toppings = json.dumps(toppings_list)
