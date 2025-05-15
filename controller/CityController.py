from flask_restful import Resource
from flask import redirect, render_template, make_response
from service import CityService, StateService, InfoService

cityService = CityService()
stateService = StateService()
infoService = InfoService()

class Cities(Resource):
    def get(self):
        return cityService.getCities()

class City(Resource):
    def get(self, city_id):
        return cityService.getById(city_id)

