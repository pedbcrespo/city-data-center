from flask_restful import Resource
from service import AddressService
from flask import request
from flask import jsonify
from urllib.parse import unquote

addressService = AddressService()

class Address(Resource):
    def get(self, cep):
        saved = addressService.saveCep(cep)
        return jsonify({'status': 'salvo com sucesso', 'data': saved.json()})

class AddressComplete(Resource):
    def post(self):
        data = request.get_json()
        return jsonify(addressService.saveAddressByObj(data))
    
class AddressName(Resource):
    def get(self, uf, city, street):
        # street = unquote(street)
        print(uf, city, street)
        addressList = addressService.saveAddress(street, city, uf)
        return jsonify([addrs.json() for addrs in addressList])