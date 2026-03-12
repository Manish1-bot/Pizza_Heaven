from flask import Flask
from config import Config
from utils.db import db, bcrypt, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprints
    from routes.main_routes import main
    from routes.user_routes import user
    from routes.admin_routes import admin
    from routes.payment_routes import payment
    
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(payment, url_prefix='/payment')
    
    return app
