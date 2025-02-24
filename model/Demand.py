class Demand:
    def __init__(self, demand, description):
        self.demand = demand
        self.description = description
    
    def getJson(self):
        return {"demand": self.demand, "description": self.description}