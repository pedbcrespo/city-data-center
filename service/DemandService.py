from typing import List
from model.DemandByAddress import DemandByAddress, DemandReq
from model.Demand import Demand
from sqlalchemy import and_
from configuration.config import mongo, ormDatabase as orm
from service.StreetService import StreetService
from service.DistrictService import DistrictService
from service.AddressService import AddressService
from configuration.config import DEMAND_BY_ADDRESS_COLLECTION
streetService = StreetService()
districtService = DistrictService()
addressService = AddressService()

class DemandService:
    def getAll(self) -> List[dict]:
        demandByAddressList = self.__getAll__()
        return demandByAddressList
    
    def getByCity(self, cityId:int) -> List[dict]:
        streets = streetService.getByCityId(int(cityId))
        streetIds = [street.id for street in streets]
        condition = {"streetId": {"$in": streetIds}}
        return self.__getAll__(condition)

    def save(self, demandReq: DemandReq) -> dict:
        address = addressService.saveAddressByObj(demandReq.getDictAddress())
        demand = self.saveDemand(demandReq.demand)
        demandByAddress = DemandByAddress(demand, address, demandReq.observation, demandReq.createDate, demandReq.location)
        mongo.db.get_collection(DEMAND_BY_ADDRESS_COLLECTION).insert_one(demandByAddress.json())
        return demandByAddress.getRes()

    def saveDemand(self, demand: Demand) -> Demand:
        existedDemand = Demand.query.filter(and_(Demand.name == demand.name, Demand.description == demand.description)).first()
        if existedDemand:
            return existedDemand
        orm.session.add(demand)
        orm.session.commit()
        return Demand.query.filter(and_(Demand.name == demand.name, Demand.description == demand.description)).first()
    
    def __getAll__(self, condition:dict={}) -> List[dict]:
        results = list(mongo.db.get_collection(DEMAND_BY_ADDRESS_COLLECTION).find(condition))
        return [self.__setDemandByAddress__(result) for result in results]

    def __getDemandByTitleAndDescription__(self, title:str, description:str) -> Demand:
        return Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()

    def __getDemandById__(self, demandId: int) -> Demand:
        return Demand.query.filter(Demand.id == demandId).first()
    
    def __setDemandByAddress__(self, result: dict) -> dict:
        demand = self.__getDemandById__(int(result['demandId']))
        address = addressService.getAddressByStreetId(int(result['streetId']))
        demandByAddress = DemandByAddress(demand, address, result['observation'], result['createDate'])
        return demandByAddress.getRes()