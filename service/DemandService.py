from model.demands.DemandLocation import DemandLocation
from model.demands.Demand import Demand
from model.Street import Street
from model.District import District
from model.City import City
from model.State import State
from sqlalchemy.orm import aliased
from sqlalchemy import and_
from configuration.config import mongo, ormDatabase as orm
from flask import jsonify
from service.StreetService import StreetService
from service.DistrictService import DistrictService

import requests

streetService = StreetService()
districtService = DistrictService()

class DemandService:
    def getAll(self):
        results = list(mongo.db.get_collection('demand_location').find())
        return jsonify(results)
    
    def getByCity(self, cityId:int):
        districts = list(District.query.filter(District.city_id == cityId))
        streets = list(Street.query.filter(Street.district_id in [district.id for district in districts]))
        results = list(mongo.db.get_collection('demand_location').find({"streetId": { "$in": [street.id for street in streets] }})) 
        return jsonify(results)

    def save(self, demandLocation: DemandLocation): 
        getInfoByCepUrl = f"https://viacep.com.br/ws/{demandLocation.cep}/json/"
        try:
            response = requests.get(getInfoByCepUrl)
            data = response.json()
            streetName = data['logradouro']
            districtName = data['bairro']
            cityName = data['localidade']
            stateName = data['estado']

            street = self.__getStreet__(streetName, districtName, cityName, stateName)
            demand = Demand.query.filter(and_(Demand.name == demandLocation.demand, Demand.description == demandLocation.description)).first()

            if not demand:
                demand = Demand(demandLocation.demand, demandLocation.description)
                orm.session.add(demand)
                orm.session.commit()
                demand = Demand.query.filter(and_(Demand.name == demandLocation.demand, Demand.description == demandLocation.description))

            if not street:
                street = self.__saveAddress__(streetName, districtName, cityName, stateName)
            

            demandLocation.completeInfo(street.id, demand.id)
            mongo.db.get_collection('demand_location').insert_one(demandLocation.json())
            return demandLocation.get()
        except:
            print("ERRO")
            return None

    def __getStreet__(self, streetName: str, districtName: str, cityName:str, stateName:str):
        state = State.query.filter(State.name == stateName).first()
        city = (City.query.filter(and_(City.name == cityName, City.state_id == state.id)).first())
        district = District.query.filter(and_(District.name == districtName, District.city_id == city.id)).first()
        if not district:
            return None
        street = Street.query.filter(and_(Street.name == streetName, Street.district_id == district.id)).first()
        print(street)
        return street
        
    def __saveAddress__(self, streetName, districtName, cityName, stateName):
        state = State.query.filter(State.name == stateName).first()
        if not state:
            return None
        city = City.query.filter(and_(
            City.name == cityName,
            City.state_id == state.id
        )
        ).first()
        district = districtService.save(districtName, city.id)
        return streetService.save(streetName, district.id)