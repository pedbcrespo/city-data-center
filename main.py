from flask import Flask
from configuration.config import app, ormDatabase
from controller.StateController import *
from controller.CityController import *

if __name__ == '__main__':
    with app.app_context():
        ormDatabase.create_all()
    app.run(host="0.0.0.0", port=5000)
