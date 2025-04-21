from model.DemandLocation import DemandLocation
from configuration.config import mongo
from flask import jsonify

class DemandService:
    def getAll(self):
        results = list(mongo.db.get_collection('demand_location').find())
        return jsonify(results)
    
    def save(self, demand: str, location: DemandLocation): 
        mongo.db.get_collection('demand_location').insert_one(demand.json())
        return True