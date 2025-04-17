from configuration.config import ormDatabase as orm

class DemandLocation(orm.Model):
    __tablename__ = 'demand_location'
    
    id = orm.Column(orm.Integer, primary_key=True)
    demand_id = orm.Column(orm.Integer, orm.ForeignKey('demand.id'))
    district_id = orm.Column(orm.Integer, orm.ForeignKey('district.id'))
    occurrence = orm.Column(orm.Integer)
    
    def __init__(self, demand_id, district_id):
        self.demand_id = demand_id
        self.district_id = district_id
        self.occurrence = 0
        
    def __repr__(self):
        return f"({self.id}, {self.demand_id}, {self.district_id})"
    
    def json(self):
        return {'id': self.id, 'demand_id': self.name}