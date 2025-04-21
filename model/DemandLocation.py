from configuration.config import ormDatabase as orm
from datetime import datetime

class DemandLocation:
    def __init__(self, state: str, city: str, district: str, street: str, demand: str):
        self.state = state
        self.city = city
        self.district = district
        self.street = street
        self.demand = demand
        self.createDate = datetime.now()

    def completeInfo(self, streetId:int, demandId:int):
        self.streetId = streetId
        self.demandId = demandId

    def get(self):
        return {
            'state': self.state,
            'city': self.city,
            'district': self.district,
            'street': self.street,
            'demand': self.demand,
            'createDate': self.createDate
        }

    def json(self):
        return {
            'demandId': self.demandId,
            'streetId': self.streetId,
            'createDate': self.createDate
        }