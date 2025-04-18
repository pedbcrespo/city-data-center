from configuration.config import ormDatabase as orm

class DemandLocation:
    def __init__(self, demand_id, street_id):
        self.demand_id = demand_id
        self.street_id = street_id

    def json(self):
        return {
            'demand_id': self.demand_id,
            'street_id': self.street_id
        }