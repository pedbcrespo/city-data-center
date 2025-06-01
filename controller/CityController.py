from flask_restful import Resource
from flasgger import swag_from
from service import CityService

cityService = CityService()

class Cities(Resource):
    @swag_from({
        'tags': ['City'],
        'responses': {
            200: {
                'description': 'Lista todas as cidades',
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'name': 'Rio de Janeiro',
                            'stateId': 1,
                            'ibgeId': 1,
                        }
                    ]
                }
            }
        }
    })
    def get(self):
        return cityService.getCities()

class City(Resource):
    @swag_from({
        'tags': ['City'],
        'parameters': [
            {
                'name': 'cityId',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Identificador da cidade'
            },
        ],
        'responses': {
            200: {
                'description': 'Busca informações mais detalhadas de determinada cidade',
                'examples': {
                    'application/json':
                        {
                            'id': 1,
                            'name': 'Rio de Janeiro',
                            'stateId': 1,
                            'ibgeId': 1,
                        }
                }
            }
        }
    })
    def get(self, cityId):
        city = cityService.getById(cityId)
        return city.json()

