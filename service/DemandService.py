from typing import List
from model.DemandLocation import DemandLocation
from model.Demand import Demand
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
    def getAll(self) -> List[dict]:
        results = list(mongo.db.get_collection('demand_location').find())
        demandLocationList = [self.__setDemandLocation__(result) for result in results]
        return jsonify(demandLocationList)
    
    def getByCity(self, cityId:int) -> List[dict]:
        districts = list(District.query.filter(District.city_id == cityId))
        streets = list(Street.query.filter(Street.district_id in [district.id for district in districts]))
        results = list(mongo.db.get_collection('demand_location').find({"streetId": { "$in": [street.id for street in streets] }})) 
        return jsonify(results)

    def save(self, demandLocation: DemandLocation) -> DemandLocation: 
        streetName, districtName, cityName, stateName = self.__getAddressByViaCep__(demandLocation.cep)
        state = State.query.filter(State.name == stateName).first()
        city = City.query.filter(and_(City.name == cityName, City.state_id == state.id)).first()
        street = self.__saveAddress__(streetName, districtName, city)
        demand = self.__getDemand__(demandLocation, city)
        
        demandLocation.completeInfo(street.id, demand.id)
        mongo.db.get_collection('demand_location').insert_one(demandLocation.json())
        return jsonify(demandLocation.get())

    def saveDemand(self, title:str, description:str) -> dict:
        demand = self.__saveDemand__(title, description)
        return jsonify(demand.json())

    def __saveAddress__(self, streetName:str, districtName:str, city:City) -> Street:
        district = District.query.filter(and_(District.name == districtName, District.city_id == city.id)).first()
        if not district:
            district = districtService.save(districtName, city.id)
        street = Street.query.filter(and_(Street.name == streetName, Street.district_id == district.id)).first()
        if not street:
            street = streetService.save(streetName, district.id, city.id)
        return street
    
    def __getDemand__(self, demandLocation: DemandLocation, city: City) -> Demand:
        demand = Demand.query.filter(and_(
            Demand.name == demandLocation.demand,
            Demand.description == demandLocation.description)
        ).first()
        print(demand)
        if not demand:
            demand = self.__saveDemand__(demandLocation.demand, demandLocation.description)
        return demand

    def __setDemandLocation__(result: dict) -> dict:
        demand = Demand.query.filter(Demand.id == result['demandId'])
        street = Street.query.filter(Street.id == result['streetId']).first()
        district = District.query.filter(District.id == street.district_id)
        city = City.query.filter(City.id == district.city_id)
        state = State.query.filter(State.id == city.state_id)
        demandLocation = DemandLocation(demand.name, demand.description, result['observation'], None)
        return demandLocation.getRes(demand, street, district, city, state)
    
    def __getAddressByViaCep__(self, cep):
        getInfoByCepUrl = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(getInfoByCepUrl)
        data = response.json()
        streetName = data['logradouro']
        districtName = data['bairro']
        cityName = data['localidade']
        stateName = data['estado']

        return streetName, districtName, cityName, stateName
    
    def __saveDemand__(self, title:str, description:str) -> Demand:
        demand = Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()
        if demand != None:
            return demand
        demand = Demand(title, description)
        orm.session.add(demand)
        orm.session.commit()
        demand = Demand.query.filter(and_(Demand.name == title, Demand.description == description)).first()
        return demand