from flask_restful import Resource
from flask import redirect, render_template, make_response
from configuration.config import api, BASE_URL
from controller.CityController import Cities, City
from controller.StateController import States, State
from controller.DemandController import Demand, SingleDemand
from controller.AddressController import AddressCep, AddressComplete, AddressName


class Initial(Resource):
    def get(self):
        return make_response(render_template('index.html'))

class RedirectToCities(Resource):
    def get(self):
        return redirect(BASE_URL)


api.add_resource(RedirectToCities, "/")
api.add_resource(Initial, BASE_URL)
api.add_resource(Cities, f"{BASE_URL}/cities")
api.add_resource(City, f"{BASE_URL}/city/info/<int:city_id>")
api.add_resource(States, f"{BASE_URL}/states")
api.add_resource(State, f"{BASE_URL}/state/<uf>")
api.add_resource(Demand, f"{BASE_URL}/demand/")
api.add_resource(SingleDemand, f"{BASE_URL}/single-demand/")
api.add_resource(AddressCep, f"{BASE_URL}/address/<string:cep>")
api.add_resource(AddressComplete, f"{BASE_URL}/address")
api.add_resource(AddressName, f"{BASE_URL}/address-list/<string:uf>/<string:city>/<string:street>")