from model.Street import Street
from model.District import District
from model.City import City
from model.State import State

class Address:
    def __init__(self, street: Street, district: District, city: City, state: State):
        self.street = street
        self.district = district
        self.city = city
        self.state = state

    def json(self) -> dict[str, str]:
        return {
            'street': self.street.name,
            'district': self.district.name,
            'city': self.city.name,
            'state': self.state.name
        }
    