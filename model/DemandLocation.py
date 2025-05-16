from configuration.config import ormDatabase as orm
from datetime import datetime
from model.Demand import Demand
from model.State import State
from model.City import City
from model.District import District
from model.Street import Street

class DemandLocation:
    def __init__(self, demandId: int, streetId: int, observation: str, cep:str = None):
        self.cep = cep.replace('-', '')
        self.demandId = demandId
        self.streetId = streetId
        self.observation = observation
        self.createDate = datetime.now()

    def json(self):
        return {
            'demandId': self.demandId,
            'streetId': self.streetId,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
        }
    
    def getRes(self, demand:Demand, street: Street, district: District, city: City, state: State, createDate=None):
        return {
            'state': state.name,
            'city': city.name,
            'district': district.name,
            'street': street.name,
            'demand': demand.name,
            'description': demand.description,
            'observation': self.observation,
            'createDate': self.createDate.isoformat() if not createDate else createDate
        }
    
class DemandReq:
    def __init__(self, data: dict):
        self.uf = data['uf']
        self.city = data['city']
        self.district = data['district']
        self.street = data['street']
        self.demand = Demand(data['title'], data['description'])
        self.observation = data['observation']
        self.createDate = datetime.now()

    def getAddress(self) -> dict[str, str]:
        return {
            'uf': self.uf,
            'city': self.city,
            'district': self.district,
            'street': self.street
        }