from datetime import datetime
from utils.db import db

class Payment(db.Model):
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50)) # e.g., razorpay
    transaction_id = db.Column(db.String(100), unique=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') # pending, successful, failed
    
    def __repr__(self):
        return f'<Payment {self.id} for Order {self.order_id}>'
