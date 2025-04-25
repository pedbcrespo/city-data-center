from configuration.config import ormDatabase as orm
from datetime import datetime
from model.demands.Demand import Demand
from model.State import State
from model.City import City
from model.District import District
from model.Street import Street

class DemandLocation:
    def __init__(self, demand: str, description: str, observation: str, cep:str):
        self.cep = cep.replace('-', '')
        self.demand = demand
        self.description = description
        self.observation = observation
        self.createDate = datetime.now()

    def completeInfo(self, streetId:int, demandId:int):
        self.streetId = streetId
        self.demandId = demandId

    def get(self):
        return {
            'demand': self.demand,
            'cep': self.cep,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
        }

    def json(self):
        return {
            'demandId': self.demandId,
            'streetId': self.streetId,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
        }
    
    def getRes(self, demand:Demand, street: Street, district: District, city: City, state: State):
        return {
            'state': state.name,
            'city': city.name,
            'district': district.name,
            'street': street.name,
            'demand': demand.name,
            'description': demand.description,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
        }