from flask_restful import Resource
from service import StateService

service = StateService()
class States(Resource):
    def get(self):
        return service.getStates()

class State(Resource):
    def get(self, stateAb):
        return service.getState(stateAb)



