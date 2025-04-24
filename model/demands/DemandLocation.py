from configuration.config import ormDatabase as orm
from datetime import datetime

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
            'createDate': self.createDate
        }

    def json(self):
        return {
            'demandId': self.demandId,
            'streetId': self.streetId,
            'observation': self.observation,
            'createDate': self.createDate
        }