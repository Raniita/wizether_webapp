import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'flask-template')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    QUEUES = ["default"]

    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'example@mail.es')
    ADMIN_NAME = os.environ.get('ADMIN_NAME', 'admin')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', '654321')

    SESSION_COOKIE_SECURE = True

    INFLUX_ORG = os.environ.get('INFLUX_ORG', 'wize_org')
    INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET', 'wize_data')
    INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN', '')

    # Api folder
    if not os.path.exists('api_tmp'):
        os.makedirs('api_tmp')

class ProductionConfig(Config):
    DB_USER = os.environ.get('MYSQL_USER', 'root')
    DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'root')
    DB_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    DB_DATABASE = os.environ.get('MYSQL_DATABASE', 'db')

    SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USER + ':' + DB_PASSWORD + '@' + DB_HOST + '/' + DB_DATABASE

    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
    REDIS_PORT = os.environ.get('REDIS_HOST_PORT', '6379')
    REDIS_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT

    INFLUX_HOST = os.environ.get('INFLUX_HOST', 'influxdb')
    INFLUX_PORT = os.environ.get('INFLUX_PORT', '8086')
    INFLUX_URL = 'http://' + INFLUX_HOST + ':' + INFLUX_PORT + '/'

class DevelopmentConfig(Config):
    DEBUG = True

    ## SQLAlchemy folder
    if not os.path.exists(os.path.join(basedir, 'db')):
        os.makedirs(os.path.join(basedir, 'db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app.sqlite')

    REDIS_URL = 'redis://localhost:6379'

    INFLUX_URL = "http://10.0.0.3:8086/"

    #SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    DEBUG = True

    ## SQLAlchemy folder
    if not os.path.exists(os.path.join(basedir, 'db')):
        os.makedirs(os.path.join(basedir, 'db'))

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'app_testing.sqlite')

    REDIS_URL = 'redis://localhost:6379'

    #SESSION_COOKIE_SECURE = True