from typing import List
from model.DemandLocation import DemandLocation, DemandReq
from model.Demand import Demand
from model.Street import Street
from model.District import District
from model.City import City
from model.State import State
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from configuration.config import mongo, ormDatabase as orm
from flask import jsonify
from service.StreetService import StreetService
from service.DistrictService import DistrictService
from service.AddressService import AddressService

streetService = StreetService()
districtService = DistrictService()
addressService = AddressService()

class DemandService:
    def getAll(self) -> List[dict]:
        demandLocationList = self.__get__()
        return demandLocationList
    
    def getByCity(self, cityId:int) -> List[dict]:
        streets = streetService.getByCityId(int(cityId))
        streetIds = [street.id for street in streets]
        condition = {"streetId": {"$in": streetIds}}
        return self.__get__(condition)

    def saveOld(self, demandLocation: DemandLocation) -> dict: 
        address = addressService.saveCep(demandLocation.cep)
        demand = self.__getDemandById__(demandLocation.demandId)
        if not demand:
            return None
        mongo.db.get_collection('demand_location').insert_one(demandLocation.json())
        return demandLocation.getRes(demand, address['street'], address['district'], address['city'], address['state'])

    def save(self, demandReq: DemandReq):
        address = addressService.saveAddressByObj(demandReq.getAddress())


    def saveDemand(self, title:str, description:str) -> Demand:
        demand = Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()
        if not demand:
            demand = Demand(title, description)
            orm.session.add(demand)
            orm.session.commit()
        return Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()
    
    def __get__(self, condition=None) -> List[dict]:
        results = []
        if not condition:
            results = list(mongo.db.get_collection('demand_location').find())
        return [self.__setDemandLocation__(result) for result in results]

    def __getDemandByTitleAndDescription__(self, title:str, description:str) -> Demand:
        return Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()

    def __getDemandById__(self, demandId: int) -> Demand:
        return Demand.query.filter(Demand.id == demandId).first()
    
    def __setDemandLocation__(self, result: dict) -> dict:
        demand = self.__getDemandById__(int(result['demandId']))
        address = addressService.getAddressByStreetId(int(result['streetId']))
        demandLocation = DemandLocation(result['demandId'], result['streetId'], result['observation'])
        return demandLocation.getRes(demand, address['street'], address['district'], address['city'], address['state'], result['createDate'])