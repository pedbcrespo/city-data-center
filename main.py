from flask import Flask
from flask_migrate import Migrate
from configuration.config import app, ormDatabase as orm
from controller.Controller import *
from configuration.args import args


migrate = Migrate(app, orm)
if __name__ == '__main__':
    if args.dev:
        app.run()
    else:
        app.run(host="0.0.0.0", port=5000)
