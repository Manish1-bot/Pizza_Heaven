from app import create_app
from utils.db import db, bcrypt
from models.user import User
from models.pizza import Pizza

app = create_app()

def init_db():
    # Helper to initialize DB with sample data
    db.create_all()
    
    # Check if admin exists
    admin_user = User.query.filter_by(email='admin@pizza.com').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(username='Admin', email='admin@pizza.com', password_hash=hashed_password, is_admin=True)
        db.session.add(admin)
        print("Admin user created: admin@pizza.com / admin123")
        
    # Check if we have pizzas
        sample_pizzas = [
            Pizza(name='Margherita', description='Classic delight with 100% real mozzarella cheese.', category='veg', size_small_price=99, size_medium_price=199, size_large_price=399, image_url='margherita.png'),
            Pizza(name='Farmhouse', description='Delightful combination of onion, capsicum, tomato & grilled mushroom.', category='veg', size_small_price=199, size_medium_price=399, size_large_price=599, image_url='farmhouse.png'),
            Pizza(name='Peppy Paneer', description='Flavorful trio of juicy paneer, crisp capsicum with spicy red paprika.', category='veg', size_small_price=229, size_medium_price=419, size_large_price=619, image_url='paneer.png'),
            Pizza(name='Mexican Green Wave', description='A pizza loaded with crunchy onions, crisp capsicum, juicy tomatoes and jalapeno.', category='veg', size_small_price=229, size_medium_price=419, size_large_price=619, image_url='farmhouse.png'),
            Pizza(name='Pepper Barbecue Chicken', description='Pepper barbecue chicken for that extra zing.', category='non-veg', size_small_price=229, size_medium_price=429, size_large_price=629, image_url='bbq_chicken.png'),
            Pizza(name='Chicken Sausage', description='American classic! Spicy, herbed chicken sausage on pizza.', category='non-veg', size_small_price=169, size_medium_price=319, size_large_price=499, image_url='bbq_chicken.png'),
            Pizza(name='Chicken Golden Delight', description='Double pepper barbecue chicken, golden corn and extra cheese.', category='non-veg', size_small_price=249, size_medium_price=459, size_large_price=659, image_url='bbq_chicken.png'),
            Pizza(name='Non Veg Supreme', description='Supreme combination of black olives, onion, capsicum, grilled mushroom, pepper barbecue chicken, local sausage.', category='non-veg', size_small_price=319, size_medium_price=579, size_large_price=839, image_url='bbq_chicken.png'),
            Pizza(name='Veg Extravaganza', description='Black olives, capsicum, onion, grilled mushroom, corn, tomato, jalapeno & extra cheese.', category='veg', size_small_price=269, size_medium_price=479, size_large_price=679, image_url='farmhouse.png'),
            Pizza(name='Chicken Fiesta', description='Grilled chicken rashers, peri-peri chicken, onion & capsicum.', category='non-veg', size_small_price=249, size_medium_price=459, size_large_price=659, image_url='bbq_chicken.png')
        ]
        db.session.bulk_save_objects(sample_pizzas)
        print("Sample pizzas created.")
        
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
        
    app.run(debug=True)
