from configuration.config import ormDatabase as orm
from datetime import datetime

class Demand(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    description = orm.Column(orm.String(500))
    createDate = orm.Column(orm.DateTime)
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.createDate = datetime.now()
        
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.description}, {self.createDate.isoformat()})"
    
    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'createDate': self.createDate.isoformat() }