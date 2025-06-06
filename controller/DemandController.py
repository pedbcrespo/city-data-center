from flask_restful import Resource
from flask import request, jsonify
from service import DemandService
from model import DemandReq, Demand as ModelDemand
from flasgger import swag_from

demandService = DemandService()
  
class SingleDemand(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(demandService.saveDemand(ModelDemand(data['title'], data['description'])))
    
class Demand(Resource):
    @swag_from({
        'tags': ['Demand'],
        'responses': {
            200: {
                'description': 'Lista todas as demandas',
                'examples': {
                    'application/json': [
                        {
                            'state': 'RJ',
                            'city': 'Rio de Janeiro',
                            'district': 'Centro',
                            'street': 'Rua A',
                            'demand': 'Iluminação',
                            'description': 'Poste apagado',
                            'observation': 'Em frente ao número 123',
                            'location': {'x': -43.182365, 'y': -22.971964},
                            'createDate': '2025-05-17T17:48:30'
                        }
                    ]
                }
            }
        }
    })
    def get(self):
        return jsonify(demandService.getAll())

    @swag_from({
        'tags': ['Demand'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'uf': {'type': 'string'},
                        'city': {'type': 'string'},
                        'district': {'type': 'string'},
                        'street': {'type': 'string'},
                        'title': {'type': 'string'},
                        'description': {'type': 'string'},
                        'location': {'type': 'object'},
                        'observation': {'type': 'string'},
                    },
                    'required': ['uf', 'city', 'district', 'street', 'title', 'description', 'location']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Salva uma demanda de uma determinada localidade.',
                'examples': {
                    'application/json': {
                        'state': 'RJ',
                        'city': 'Rio de Janeiro',
                        'district': 'Centro',
                        'street': 'Rua A',
                        'demand': 'Iluminação',
                        'description': 'Poste apagado',
                        'observation': 'Em frente ao número 123',
                        'location': {'x': -43.182365, 'y': -22.971964},
                        'createDate': '2025-05-17T17:48:30'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        demandReq = DemandReq(data)
        return jsonify(demandService.save(demandReq))