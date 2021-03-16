from flask import Flask
from flask_minify import minify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin

from app.config import ProductionConfig, DevelopmentConfig
from app.admin import CustomAdminIndexView, AdminModelView, MainIndexLink

from werkzeug.security import generate_password_hash, check_password_hash

import logging
#import meinheld
import os

# Extensions declaration
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name='WizeTher',
              index_view=CustomAdminIndexView())

# Application factory init
def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        gunicorn_logger = logging.getLogger('gunicorn.error')
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)
        
        app.logger.info('Minifying')
        minify(app=app, html=True, js=False, cssless=True)
        app.logger.info('Starting with ProductionConfig')
        app.config.from_object(ProductionConfig)
    else:
        app.logger.info('Starting with DevelopmentConfig')
        app.config.from_object(DevelopmentConfig)

    app.logger.info('Using database connection:' + app.config['SQLALCHEMY_DATABASE_URI'])
    app.logger.info('Using redis connection:' + app.config['REDIS_URL'])
    app.url_map.strict_slashes = True

    # Init extensions
    init_extensions(app)

    # Adding the views app
    from app.views.landing import landing_bp
    from app.views.dashboard import dashboard_bp
    from app.views.auth import auth_bp
    from app.views.api import api_bp

    app.register_blueprint(landing_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    return app


# Init extensions
def init_extensions(app):
    # Start Flask-SQLAlchemy
    db.init_app(app)

    # Start Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.models import User
    from app import admin

    # Start Flask-Admin
    admin.init_app(app)
    admin.add_view(AdminModelView(User, db.session))
    admin.add_link(MainIndexLink(name='WizeTher Dashboard'))

    try:
        with app.app_context():
            # Create database models
            db.create_all()

            # Create admin user on startup
            admin_email = app.config['ADMIN_EMAIL']
            admin_name = app.config['ADMIN_NAME']
            admin_pass = app.config['ADMIN_PASSWORD']

            app.logger.info('Admin account: {} <----> {}'.format(admin_email, admin_pass))

            admin = User.query.filter_by(email=admin_email).first()
            if admin is None:
                passw = generate_password_hash(admin_pass, method='sha256')
                new_user = User(email=admin_email,
                                name=admin_name,
                                #password=admin_pass,
                                role='admin')
                new_user.set_password(admin_pass)

                db.session.add(new_user)
                db.session.commit()
                app.logger.info('Added admin user to dabatase')
            else:
                # Checking if password has been changed
                admin_hash = generate_password_hash(admin_pass, method='sha256')

                if not check_password_hash(admin_hash, admin.password):
                    # Updating password on database
                    admin.password = admin_hash
                    
                    db.session.add(admin)
                    db.session.commit()
                    #app.logger.info('Updated admin password')
                
            app.logger.info('Database working')

    except Exception as e:
        app.logger.error('Exception Found: ' + str(e))
        app.logger.error('Database not found. Please read README.md to create the db.')

    app.logger.info('Done. Flask extensions started.')