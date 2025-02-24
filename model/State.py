from config.baseConfig import ormDatabase
orm = ormDatabase

class State(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(100), nullable=False)
    code = orm.Column(orm.String(10), unique=True, nullable=False)