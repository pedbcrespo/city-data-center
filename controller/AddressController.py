from flask_restful import Resource
from service import AddressService
from flask import request
from flask import jsonify
addressService = AddressService()

class Address(Resource):
    def get(self, cep):
        addressService.saveCep(cep)
        return jsonify({'status': 'salvo com sucesso'})
