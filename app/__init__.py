from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.customers import customers
    from app.routes.vehicles import vehicles
    from app.routes.renewals import renewals
    from app.routes.employees import employees

    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(customers)
    app.register_blueprint(vehicles)
    app.register_blueprint(renewals)
    app.register_blueprint(employees)

    from app import models

    from app.models import Employee

    @login_manager.user_loader
    def load_user(user_id):
        return Employee.query.get(int(user_id))

    return app