from configuration.config import ormDatabase
from model.District import District
orm = ormDatabase

class Street(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    district_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('district.id'))
    
    def __init__(self, name, district_id):
        self.name = name
        self.district_id = district_id
                    
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.state_id})"
    
    def json(self):
        result = {'id': self.id, 'name': self.name, 'district_id':self.district_id}
        return result