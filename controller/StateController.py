from flask_restful import Resource
from service import StateService
from flask import jsonify
from flasgger import swag_from

service = StateService()
class States(Resource):
    @swag_from({
        'responses': {
            200: {
                'description': 'Lista todas os Estados',
                'examples': {
                    'application/json': [
                        {
                            'id': 1,
                            'name': 'Rio de Janeiro',
                            'abbreviation': 'RJ',
                        }
                    ]
                }
            }
        }
    })
    def get(self):
        return jsonify(service.getStates())

class State(Resource):
    @swag_from({
        'parameters': [
            {
                'name': 'uf',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Abreviação do Estado'
            },
        ],
        'responses': {
            200: {
                'description': 'Busca informações mais detalhadas de determinado Estado',
                'examples': {
                    'application/json':
                        {
                            'id': 1,
                            'name': 'Rio de Janeiro',
                            'abbreviation': 'RJ',
                        }
                }
            }
        }
    })
    def get(self, uf):
        return jsonify(service.getStateByUf(uf).json())



