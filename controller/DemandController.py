from flask_restful import Resource
from flask import redirect, request, render_template, make_response
from service.DemandService import DemandService
from model.demands.DemandLocation import DemandLocation


demandService = DemandService()

class Demand(Resource):
    def get(self):
        return demandService.getAll()
    
    def post(self, demandLocation: DemandLocation):
        return demandService.save(demandLocation)