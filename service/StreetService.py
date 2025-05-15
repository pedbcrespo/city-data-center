from model.Street import Street 
from model.District import District 
from model.City import City 
from model.State import State 
from typing import List
from sqlalchemy import and_
from configuration.config import ormDatabase as orm


class StreetService:
    def get(self) -> List[Street]:
        streets =  Street.query.all()
        return streets
    
    def getByName(self, streetName:str, districtId:int, cityId: int) -> Street:
        return Street.query.filter(and_(Street.name == streetName, Street.district_id == districtId, Street.city_id == cityId)).first()
    
    def getById(self, streetId: int) -> Street:
        return Street.query.filter(Street.id == streetId).first()
    
    def getByCityId(self, cityId:int) -> List[Street]:
        return Street.query.filter(Street.city_id == cityId).all()
    
    def save(self, streetName:str, districtId:int, cityId: int) -> Street:
        street = Street(streetName, districtId, cityId)
        orm.session.add(street)
        orm.session.commit()
        return Street.query.filter(Street.name == streetName and Street.district_id == districtId).first()
