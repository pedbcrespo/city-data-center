from flask import Flask
from configuration.config import app, ormDatabase as orm
from controller.Controller import *
from configuration.args import args

if __name__ == '__main__':
    with app.app_context():
        orm.create_all()
    if args.dev:
        app.run()
    else:
        app.run(host="0.0.0.0", port=5000)
