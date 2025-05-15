from flask_restful import Resource
from service import StateService
from flask import jsonify
service = StateService()
class States(Resource):
    def get(self):
        return service.getStates()

class State(Resource):
    def get(self, stateAb):
        return jsonify(service.getState(stateAb).json())



