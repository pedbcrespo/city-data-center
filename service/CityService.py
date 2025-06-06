from model.City import City
from model.State import State
from sqlalchemy import and_
from service.InfoService import InfoService
from configuration.config import ormDatabase as orm
from typing import List

class CityService:
    def getCities(self) -> List[dict]:
        cities = City.query.all()
        return [city.json() for city in cities]

    def getById(self, cityId:int) -> City:
        city = City.query.filter(City.id == cityId).first()
        return city
    
    def getCity(self, uf:str, name:str) -> City:
        state = State.query.filter(State.abbreviation == uf).first()
        return City.query.filter(and_(City.name == name, City.state_id == state.id)).first()

    def save(self, name:str, stateId:int) -> City:
        city = City.query.filter(and_(City.name == name, City.state_id == stateId)).first()
        if city:
            return city
        city = City(name, stateId)
        orm.session.add(city)
        orm.session.commit()
        return City.query.filter(and_(City.name == name, City.state_id == stateId)).first()

