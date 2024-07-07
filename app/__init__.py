# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['WTF_CSRF_CHECK_DEFAULT'] = False


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    csrf.init_app(app)
    # Disable CSRF protection for all routes
    # csrf.init_app(app, exempt_methods=['POST', 'PUT', 'PATCH', 'DELETE'])
  
    # Register blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app


# Enable CSRF protection for all non-exempted methods
csrf.exempt_views = []  # Ensure all views are protected by default