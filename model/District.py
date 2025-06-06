from configuration.config import ormDatabase as orm

class District(orm.Model):
    id = orm.Column(orm.BigInteger, primary_key=True)
    name = orm.Column(orm.String(200))
    city_id = orm.Column(orm.BigInteger, orm.ForeignKey('city.id'), nullable=True, default=None)
    def __init__(self, name, cityId):
        self.name = name
        self.city_id = cityId
        
    def json(self):
        return {'id': self.id, 'name': self.name}