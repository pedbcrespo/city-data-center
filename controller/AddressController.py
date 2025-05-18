from flask_restful import Resource
from service import AddressService
from flask import request
from flask import jsonify
from flasgger import swag_from

addressService = AddressService()

class AddressCep(Resource):
    @swag_from({
        'tags': ['Address'],
        'parameters': [
            {
                'name': 'cep',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'CEP para buscar o endereço'
            }
        ],
        'responses': {
            200: {
                'description': 'Endereço salvo com sucesso',
                'examples': {
                    'application/json': {
                        'status': 'salvo com sucesso',
                        'data': {
                            'street': 'Rua A',
                            'district': 'Centro',
                            'city': 'Rio de Janeiro',
                            'state': 'RJ'
                        }
                    }
                }
            }
        }
    })
    def get(self, cep):
        saved = addressService.saveCep(cep)
        return jsonify({'status': 'salvo com sucesso', 'data': saved.json()})

class AddressComplete(Resource):
    @swag_from({
        'tags': ['Address'],
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
                        'street': {'type': 'string'}
                    },
                    'required': ['uf', 'city', 'district', 'street']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Endereço salvo com sucesso',
                'examples': {
                    'application/json': {
                        'street': 'Rua A',
                        'district': 'Centro',
                        'city': 'Rio de Janeiro',
                        'state': 'RJ'
                    }
                }
            }
        }
    })
    def post(self):
        data = request.get_json()
        return jsonify(addressService.saveAddressByObj(data).json())
    
class AddressName(Resource):
    @swag_from({
        'tags': ['Address'],
        'parameters': [
            {
                'name': 'uf',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Unidade Federativa (UF)'
            },
            {
                'name': 'city',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nome da cidade'
            },
            {
                'name': 'street',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nome da rua'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de endereços encontrados',
                'examples': {
                    'application/json': [
                        {
                            'street': 'Rua A',
                            'district': 'Centro',
                            'city': 'Rio de Janeiro',
                            'state': 'RJ'
                        },
                        {
                            'street': 'Rua B',
                            'district': 'Copacabana',
                            'city': 'Rio de Janeiro',
                            'state': 'RJ'
                        }
                    ]
                }
            }
        }
    })
    def get(self, uf, city, street): 
        print(uf, city, street)
        addressList = addressService.saveAddress(street, city, uf)
        return jsonify([addrs.json() for addrs in addressList]) 