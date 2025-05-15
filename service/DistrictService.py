from model.District import District 
from model.City import City 
from model.State import State 
from typing import List
from sqlalchemy import and_
from configuration.config import ormDatabase as orm


class DistrictService:
    def get(self):
        districts =  District.query.all()
        return districts
       
    def getByCity(self, city:City):
        districts = District.query.filter(District.city_id==city.id).all()
        return districts
        
    def getByName(self, districtName:str, cityId:int) -> District:
        return District.query.filter(and_(District.name == districtName, District.city_id == cityId)).first()
        
    def getById(self, districtId:int) -> District:
        return District.query.filter(District.id == districtId).first()
    
    def saveMany(self, districts:List[District]):
        orm.session.add_all(districts)
        orm.session.commit()
        return districts
    
    def save(self, districtName:str, cityId:int) -> District:
        district = District(districtName, cityId)
        orm.session.add(district)
        orm.session.commit()
        return District.query.filter(District.name == districtName and District.city_id == cityId).first()
