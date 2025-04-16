from model.City import City
from model.State import State
from service.InfoService import InfoService
from typing import List

class CityService:
    def getCities(self):
        cities = City.query.all()
        return [city.json() for city in cities]

    def getCityById(self, cityId:int):
        city = City.query.filter(City.id == cityId).first()
        return city.json()