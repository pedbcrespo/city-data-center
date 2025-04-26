from configuration.config import ormDatabase as orm
 
class Region(orm.Model):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(45))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"({self.id}, {self.name})"

    def json(self):
        return {'id': self.id, 'name': self.name}