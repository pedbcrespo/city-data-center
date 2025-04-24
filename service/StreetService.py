from model.Street import Street 
from model.District import District 
from model.City import City 
from model.State import State 
from typing import List
from configuration.config import ormDatabase as orm


class StreetService:
    def get(self):
        districts =  Street.query.all()
        return districts
    
    def save(self, streetName:str, districtId:int) -> Street:
        street = Street(streetName, districtId)
        orm.session.add(street)
        orm.session.commit()
        return Street.query.filter(Street.name == streetName and Street.district_id == districtId).first()
