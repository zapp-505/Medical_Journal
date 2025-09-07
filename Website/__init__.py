from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    '''connects Flask app and SQLAlchemy db to Flask-Migrate and 
    enables to run flask db commands from terminal to manage schema'''
    migrate = Migrate(app, db)

    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.gett(int(user_id))

    from .auth import auth
    app.register_blueprint(views,url_prefix='/')

    return app
