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
    
class StreetDetails(orm.Model):
    id = orm.Column(orm.BigInteger, primary_key=True)
    street_id = orm.Column(orm.BigInteger, orm.ForeignKey('district.id'))
    lenght = orm.Column(orm.Float)
    width = orm.Column(orm.Float)
    isDeadEnd = orm.Column(orm.Boolean)

    def __init__(self, streetId: int, lenght:float=None, width:float=None, isDeadEnd:bool=False):
        self.street_id = streetId
        self.lenght = lenght
        self.width = width
        self.isDeadEnd = isDeadEnd

    def json(self):
        return {
            'lenght': self.lenght,
            'width': self.width,
            'isDeadEnd': self.isDeadEnd
        }