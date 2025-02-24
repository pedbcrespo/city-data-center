from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from config import dev_configuration as db
from flask_cors import CORS

postgres_conn = f"postgresql+psycopg2://{db.user}:{db.password}@{db.host}/{db.database}"
mongo_conn = f"mongodb://{db.mongo_url}"

app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = postgres_conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ormDatabase = SQLAlchemy(app)

app.config["MONGO_URI"] = mongo_conn
mongo = PyMongo(app)

api = Api(app)


