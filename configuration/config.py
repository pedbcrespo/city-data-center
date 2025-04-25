from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db
from flask_cors import CORS
from flask_pymongo import PyMongo
from configuration.args import args
import os

DB_USER = db.user if args.dev else os.getenv('DB_USER')
DB_PASS = db.password if args.dev else os.getenv('DB_PASS')
DB_HOST = db.host if args.dev else os.getenv('DB_HOST')
DB_NAME = db.database if args.dev else os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
BASE_URL = '/city-db-api'

MONGO_HOST = db.mongoHost if args.dev else os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = db.mongoPort if args.dev else os.getenv("MONGO_PORT", "27017")
MONGO_DB = db.mongoDB if args.dev else os.getenv("MONGO_DB", "city_database")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["MONGO_URI"] = MONGO_URI


ormDatabase = SQLAlchemy(app)
mongo = PyMongo(app)
api = Api(app)
