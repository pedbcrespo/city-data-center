from model.District import District 
from model.City import City 
from model.State import State 
from typing import List
from configuration.config import ormDatabase as orm
from service.StreetService import StreetService
from service.DistrictService import DistrictService
from service.CityService import CityService
from service.StateService import StateService

streetService = StreetService()
districtService = DistrictService()
cityService = CityService()
stateService = StateService()

class AddressService:
    def saveAddress(address: dict) -> None:
        city = cityService.getCity(address['uf'], address['city'])
        district = districtService.getByName(address['district'], city.id)
        if not district:
            district = districtService.save(address['district'], city.id)
        
        street = streetService.getByName(address['street'], district.id, city.id)
        if not street:
            street = streetService.save(address['street', district.id, city.id])

        
        