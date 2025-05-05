from flask import Flask
from model import *
from configuration.config import app, ENV
from controller import *

if __name__ == '__main__':
    if not ENV:
        app.run()
    else:
        app.run(host="0.0.0.0", port=5000)
