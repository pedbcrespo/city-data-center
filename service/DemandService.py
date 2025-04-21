from model.DemandLocation import DemandLocation
from model.Demand import Demand
from model.Street import Street
from model.District import District
from model.City import City
from model.State import State
from sqlalchemy.orm import aliased
from configuration.config import mongo, ormDatabase as orm
from flask import jsonify

class DemandService:
    def getAll(self):
        results = list(mongo.db.get_collection('demand_location').find())
        return jsonify(results)
    
    def save(self, demand: DemandLocation):
        registerDemand = Demand.query.filter(Demand.name == demand.demand).first()
        
        if not registerDemand:
            orm.session.add(Demand(demand.demand, demand.description))
            orm.session.commit()
        
        demand.completeInfo()
        mongo.db.get_collection('demand_location').insert_one(demand.json())
        return demand
    

    def __getStreet__(self, demand: DemandLocation):
        district_alias = aliased(District)
        city_alias = aliased(City)
        state_alias = aliased(State)

        result = (orm.session.query(Street)
        .join(district_alias, Street.district_id == district_alias.id)
        .join(city_alias, district_alias.city_id == city_alias.id)
        .join(state_alias, city_alias.state_id == state_alias.id)
        .filter(Street.name == demand.street)
        .filter(district_alias.name == demand.district)
        .filter(city_alias.name == demand.city)
        .filter(state_alias.name == demand.state)
        .one())

        return result