from model.City import City
from model.State import State
from sqlalchemy import and_
from service.InfoService import InfoService
from typing import List

class CityService:
    def getCities(self) -> List[dict]:
        cities = City.query.all()
        return [city.json() for city in cities]

    def getCityById(self, cityId:int) -> dict:
        city = City.query.filter(City.id == cityId).first()
        return city.json()
    
    def getCity(self, uf:str, name:str) -> City:
        state = State.query.filter(State.abbreviation == uf).first()
        return City.query.filter(and_(City.name == name, City.state_id == state.id)).first()

