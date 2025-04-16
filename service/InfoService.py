import json
from model.City import City
from model.State import State
from sqlalchemy import desc, create_engine, func, or_
from sqlalchemy.orm import sessionmaker
from configuration.config import conn
import functools as ft

class InfoService:   
    def getCityInfo(self, cityId):
        info = {}
        return info
    