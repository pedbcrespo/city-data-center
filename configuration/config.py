from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_migrate import Migrate
from flasgger import Swagger
import os

ENV = os.getenv('FLASK_ENV', None)

DB_USER = os.getenv('DB_USER', db.user)
DB_PASS = os.getenv('DB_PASS', db.password)
DB_HOST = os.getenv('DB_HOST', db.host)
DB_NAME = os.getenv('DB_NAME', db.database)

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
BASE_URL = '/city-db-api'

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "city_database")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["MONGO_URI"] = MONGO_URI
swagger = Swagger(app)


ormDatabase = SQLAlchemy(app)
mongo = PyMongo(app)
api = Api(app)
migrate = Migrate(app, ormDatabase)