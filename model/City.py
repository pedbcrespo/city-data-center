from config.baseConfig import ormDatabase
orm = ormDatabase

class City(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(20))
    state_id = ormDatabase.Column(ormDatabase.Integer, ormDatabase.ForeignKey('state.id'))