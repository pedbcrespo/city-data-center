from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from configuration import dev_configuration as db
from flask_cors import CORS
import os

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
BASE_URL = '/city-db-api'

app = Flask(__name__)
CORS(app, origins='*')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

ormDatabase = SQLAlchemy(app)
api = Api(app)