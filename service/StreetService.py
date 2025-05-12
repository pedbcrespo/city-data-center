from model.Street import Street 
from model.District import District 
from model.City import City 
from model.State import State 
from typing import List
from sqlalchemy import and_
from configuration.config import ormDatabase as orm


class StreetService:
    def get(self):
        districts =  Street.query.all()
        return districts
    
    def getByName(self, streetName:str, districtId:int, cityId: int) -> Street:
        return Street.query.filter(and_(Street.name == streetName, Street.district_id == districtId, Street.city_id == cityId)).first()
    
    def save(self, streetName:str, districtId:int, cityId: int) -> Street:
        street = Street(streetName, districtId, cityId)
        orm.session.add(street)
        orm.session.commit()
        return Street.query.filter(Street.name == streetName and Street.district_id == districtId).first()
