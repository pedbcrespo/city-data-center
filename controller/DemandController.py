from flask_restful import Resource
from flask import request, jsonify
from service import DemandService
from model import DemandLocation


demandService = DemandService()

class Demand(Resource):
    def get(self):
        return jsonify(demandService.getAll())
    
    def post(self):
        data = request.get_json()
        demandLocation = DemandLocation(data['demandId'], data['streetId'], data['observation'], data['cep'])
        return jsonify(demandService.save(demandLocation))
    
class SingleDemand(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(demandService.saveDemand(data['title'], data['description']))