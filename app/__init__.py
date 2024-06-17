from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": ['http://localhost:5173']}}, supports_credentials=True)
    app.config.from_object(config_class)
    db.init_app(app)
    jwt = JWTManager(app)
    
    from app import routes, models
    app.register_blueprint(routes.bp)
        
    with app.app_context():
        db.create_all()

    return app
