from model.demands.DemandLocation import DemandLocation
from model.demands.Demand import Demand
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
    
    def getByCity(self, cityId:int):
        districts = list(District.query.filter(District.city_id == cityId))
        streets = list(Street.query.filter(Street.district_id in [district.id for district in districts]))
        results = list(mongo.db.get_collection('demand_location').find({"streetId": { "$in": [street.id for street in streets] }})) 
        return jsonify(results)
    
    def save(self, demand: DemandLocation):
        registerDemand = Demand.query.filter(Demand.name == demand.demand).first()
        street = self.__getStreet__(demand)

        if not registerDemand:
            orm.session.add(Demand(demand.demand, demand.description))
            orm.session.commit()
        
        streetId = None if not street else street.id

        demand.completeInfo(streetId, registerDemand.id)
        mongo.db.get_collection('demand_location').insert_one(demand.json())
        return demand
    

    def __getStreet__(self, demand: DemandLocation):
        district_alias = aliased(District)
        city_alias = aliased(City)
        state_alias = aliased(State)
        try:
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
        except:
            return None