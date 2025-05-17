from typing import List
from model.DemandLocation import DemandLocation, DemandReq
from model.Demand import Demand
from sqlalchemy import and_
from configuration.config import mongo, ormDatabase as orm
from service.StreetService import StreetService
from service.DistrictService import DistrictService
from service.AddressService import AddressService

streetService = StreetService()
districtService = DistrictService()
addressService = AddressService()

class DemandService:
    def getAll(self) -> List[dict]:
        demandLocationList = self.__getAll__()
        return demandLocationList
    
    def getByCity(self, cityId:int) -> List[dict]:
        streets = streetService.getByCityId(int(cityId))
        streetIds = [street.id for street in streets]
        condition = {"streetId": {"$in": streetIds}}
        return self.__getAll__(condition)

    def save(self, demandReq: DemandReq) -> dict:
        address = addressService.saveAddressByObj(demandReq.getDictAddress())
        demand = self.saveDemand(demandReq.demand)
        demandLocation = DemandLocation(demand, address, demandReq.observation, demandReq.createDate)
        mongo.db.get_collection('demand_location').insert_one(demandLocation.json())
        return demandLocation.getRes()

    def saveDemand(self, demand: Demand) -> Demand:
        existedDemand = Demand.query.filter(and_(Demand.name == demand.name, Demand.description == demand.description)).first()
        if existedDemand:
            return existedDemand
        orm.session.add(demand)
        orm.session.commit()
        return Demand.query.filter(and_(Demand.name == demand.name, Demand.description == demand.description)).first()
    
    def __getAll__(self, condition:dict={}) -> List[dict]:
        results = list(mongo.db.get_collection('demand_location').find(condition))
        return [self.__setDemandLocation__(result) for result in results]

    def __getDemandByTitleAndDescription__(self, title:str, description:str) -> Demand:
        return Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()

    def __getDemandById__(self, demandId: int) -> Demand:
        return Demand.query.filter(Demand.id == demandId).first()
    
    def __setDemandLocation__(self, result: dict) -> dict:
        demand = self.__getDemandById__(int(result['demandId']))
        address = addressService.getAddressByStreetId(int(result['streetId']))
        demandLocation = DemandLocation(demand, address, result['observation'], result['createDate'])
        return demandLocation.getRes()