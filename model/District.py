from config.baseConfig import ormDatabase
orm = ormDatabase

class District(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(20))
    city_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('city.id'))