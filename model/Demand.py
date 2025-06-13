from configuration.config import ormDatabase as orm
from datetime import datetime

class DemandType(orm.Model):
    __tablename__ = 'demand_type'
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(200))

class Demand(orm.Model):
    id = orm.Column(orm.BigInteger, primary_key=True)
    name = orm.Column(orm.String(200))
    description = orm.Column(orm.String(500))
    type_id = orm.Column(orm.Integer, orm.ForeignKey('demand_type.id'))
    creationDate = orm.Column(orm.DateTime, nullable=False, default=datetime.now())
    def __init__(self, name:str, description:str, demandType: DemandType):
        self.name = name
        self.description = description
        self.demandType = demandType
        self.creationDate = datetime.now()
        
    def __repr__(self):
        return f"({self.id}, {self.demandType.name}, {self.name}, {self.description}, {self.creationDate.isoformat()})"
    
    def json(self):
        return {'id': self.id, 'type': self.demandType.name,'name': self.name, 'description': self.description, 'creationDate': self.creationDate.isoformat() }