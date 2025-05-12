from configuration.config import ormDatabase as orm
from datetime import datetime

class Demand(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))
    description = orm.Column(orm.String(500))
    creationDate = orm.Column(orm.DateTime, nullable=False, default=datetime.now())
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.creationDate = datetime.now()
        
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.description}, {self.creationDate.isoformat()})"
    
    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'creationDate': self.creationDate.isoformat() }