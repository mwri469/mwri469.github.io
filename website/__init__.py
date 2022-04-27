from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Initialise data base
db = SQLAlchemy()
DBName = "database.db"

def create_app():
    """ Creates our application
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'martinwright' # Website key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DBName}'
    db.init_app(app)

    # Import and register the blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Stock

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    """ Checks if database is created, and creates it if not
    """
    if not path.exists('website/' + DBName):
        db.create_all(app = app)
        print('Database created')

