from flask_restful import Resource
from configuration.config import api, BASE_URL
from service.StateService import StateService

service = StateService()
class States(Resource):
    def get(self):
        return service.getStates()

class State(Resource):
    def get(self, stateAb):
        return service.getState(stateAb)


api.add_resource(States, f"{BASE_URL}/states")
api.add_resource(State, f"{BASE_URL}/state/<uf>")
