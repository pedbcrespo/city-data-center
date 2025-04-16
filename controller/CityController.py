from flask_restful import Resource
from flask import redirect, request, render_template, make_response
from configuration.config import api
from configuration.dev_configuration import BASE_URL
from service.CityService import CityService
from service.InfoService import InfoService
from service.StateService import StateService

cityService = CityService()
stateService = StateService()
infoService = InfoService()

class Initial(Resource):
    def get(self):
        return make_response(render_template('index.html'))

class RedirectToCities(Resource):
    def get(self):
        return redirect(BASE_URL)

class Cities(Resource):
    def get(self):
        return cityService.getAllCities()

class City(Resource):
    def get(self, city_id):
        info = infoService.getCityInfo(city_id)
        return info

    
    
api.add_resource(RedirectToCities, "/")
api.add_resource(Initial, BASE_URL)
api.add_resource(Cities, f"{BASE_URL}/cities")
api.add_resource(City, f"{BASE_URL}/city/info/<int:city_id>")
