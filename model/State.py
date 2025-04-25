from configuration.config import ormDatabase as orm

class State(orm.Model):
    id = orm.Column(orm.BigInteger, primary_key=True)
    ibge_id = orm.Column(orm.Integer) 
    name = orm.Column(orm.String(100))
    abbreviation = orm.Column(orm.String(2))
    region_id = orm.Column(orm.BigInteger, orm.ForeignKey('region.id'))
    
    def __init__(self, name, abbreviation, region_id):
        self.name = name
        self.abbreviation = abbreviation
        self.region_id = region_id

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.abbreviation}, {self.region_id}, {self.ibge_id})"

    def json(self):
        return {'id': self.id, 'name': self.name, 'abbreviation': self.abbreviation, 'region_id': self.region_id, 'ibge_id': self.ibge_id}