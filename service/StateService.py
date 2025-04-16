from model.State import State
from typing import List

class StateService:
    def getStates(self):
        states = State.query.all()
        return [state.json() for state in states]
    
    def getState(self, uf: str):
        state = State.query.filter(State.abbreviation == uf).first()
        return state.json()