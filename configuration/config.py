from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db
from flask_cors import CORS
from flask_pymongo import PyMongo
import os

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
BASE_URL = '/city-db-api'

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "city_database")

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"

app = Flask(__name__)
CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config["MONGO_URI"] = MONGO_URI


ormDatabase = SQLAlchemy(app)
mongo = PyMongo(app)
api = Api(app)