from flask_restful import Resource
from flask import request, jsonify
from service import DemandService
from model import DemandLocation, DemandReq


demandService = DemandService()
  
class SingleDemand(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(demandService.saveDemand(data['title'], data['description']))
    

class Demand(Resource):
    def get(self):
        return jsonify(demandService.getAll())
    
    def post(self):
        data = request.get_json()
        demandReq = DemandReq(data)
        return jsonify(demandService.save(demandReq))
