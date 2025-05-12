from flask_restful import Resource
from service import AddressService
from flask import request
from flask import jsonify
addressService = AddressService()

class Address(Resource):
    def post(self):
        data = request.get_json()
        addressService.saveAddress(data)
        return jsonify({'status': 'salvo com sucesso!'})
