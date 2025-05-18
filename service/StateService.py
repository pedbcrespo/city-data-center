from model.State import State
from typing import List

class StateService:
    def getStates(self):
        states = State.query.all()
        return [state.json() for state in states]
    
    def getStateByUf(self, uf: str) -> State:
        return State.query.filter(State.abbreviation == uf).first()
    
    def getById(self, stateId: int) -> State:
        return State.query.filter(State.id == stateId).first()