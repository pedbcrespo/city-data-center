from configuration.config import ormDatabase as orm

class Street(orm.Model):
    id = orm.Column(orm.BigInteger, primary_key=True)
    name = orm.Column(orm.String(200))
    district_id = orm.Column(orm.BigInteger, orm.ForeignKey('district.id'), nullable=True, default=None)
    city_id = orm.Column(orm.BigInteger, orm.ForeignKey('city.id'), nullable=True, default=None)
    
    def __init__(self, name, district_id, city_id):
        self.name = name
        self.district_id = district_id
        self.city_id = city_id
                    
    def __repr__(self):
        return f"({self.id}, {self.name}, {self.district_id})"
    
    def json(self):
        result = {'id': self.id, 'name': self.name, 'district_id':self.district_id}
        return result