from configuration.config import ormDatabase as orm
from datetime import datetime
from model.Demand import Demand
from model.Address import Address

class DemandLocation:
    def __init__(self, demand: Demand, address: Address, observation: str, createDate:datetime = None):
        self.demand = demand
        self.address = address
        self.observation = observation
        if isinstance(createDate, str):
            try:
                createDate = datetime.strptime(createDate, "%Y-%m-%dT%H:%M:%S.%f")
            except ValueError:
                createDate = datetime.strptime(createDate, "%Y-%m-%dT%H:%M:%S")
        self.createDate = datetime.now() if not createDate else createDate

    def json(self) -> dict:
        return {
            'demandId': self.demand.id,
            'streetId': self.address.street.id,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
        }
    
    def getRes(self) -> dict:
        return {
            'state': self.address.state.name,
            'city': self.address.city.name,
            'district': self.address.district.name,
            'street': self.address.street.name,
            'demand': self.demand.name,
            'description': self.demand.description,
            'observation': self.observation,
            'createDate': self.createDate.isoformat()
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

    def getDictAddress(self) -> dict[str, str]:
        return {
            'uf': self.uf,
            'city': self.city,
            'district': self.district,
            'street': self.street
        }
