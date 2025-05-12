from flask_restful import Resource
from flask import request
from service import DemandService
from model import DemandLocation


demandService = DemandService()

class Demand(Resource):
    def get(self):
        return demandService.getAll()
    
    def post(self):
        data = request.get_json()
        demandLocation = DemandLocation(data['demand'], data['description'], data['observation'], data['cep'])
        return demandService.save(demandLocation)
    
class SingleDemand(Resource):
    def post(self):
        data = request.get_json()
        return demandService.saveDemand(data['title'], data['description'])