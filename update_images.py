"""One-time script to update existing pizza records with image URLs."""
from app import create_app
from utils.db import db
from models.pizza import Pizza

app = create_app()

IMAGE_MAP = {
    'Margherita': 'margherita.png',
    'Farmhouse': 'farmhouse.png',
    'Peppy Paneer': 'paneer.png',
    'Mexican Green Wave': 'farmhouse.png',
    'Veg Extravaganza': 'farmhouse.png',
    'Pepper Barbecue Chicken': 'bbq_chicken.png',
    'Chicken Sausage': 'bbq_chicken.png',
    'Chicken Golden Delight': 'bbq_chicken.png',
    'Non Veg Supreme': 'bbq_chicken.png',
    'Chicken Fiesta': 'bbq_chicken.png',
}

with app.app_context():
    pizzas = Pizza.query.all()
    updated = 0
    for pizza in pizzas:
        img = IMAGE_MAP.get(pizza.name)
        if img and pizza.image_url != img:
            pizza.image_url = img
            updated += 1
    db.session.commit()
    print(f"Updated {updated} pizza image URLs.")
    for p in Pizza.query.all():
        print(f"  {p.name}: {p.image_url}")
