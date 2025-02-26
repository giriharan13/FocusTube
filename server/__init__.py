from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():

    app = Flask(__name__)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    app.config['DEBUG'] = os.getenv("FLASK_DEBUG")
    app.config['SQLALCHEMY_ECHO'] = os.getenv("SQLALCHEMY_ECHO")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .models import User

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix="/auth")

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix="/main")
    

    return app

