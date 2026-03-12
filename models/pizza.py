from datetime import datetime
from utils.db import db

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(20), nullable=False) # 'veg' or 'non-veg'
    size_small_price = db.Column(db.Float, nullable=False)
    size_medium_price = db.Column(db.Float, nullable=False)
    size_large_price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), default='default_pizza.png')
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Pizza {self.name}>'

class Topping(db.Model):
    __tablename__ = 'toppings'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Topping {self.name}>'
