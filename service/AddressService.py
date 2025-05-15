from model.Address import Address
from typing import List
from configuration.config import ormDatabase as orm
from service.StreetService import StreetService
from service.DistrictService import DistrictService
from service.CityService import CityService
from service.StateService import StateService
import requests

streetService = StreetService()
districtService = DistrictService()
cityService = CityService()
stateService = StateService()

model = orm.Model

class AddressService:

    def saveCep(self, cep:str) -> Address:
        url = f"https://viacep.com.br/ws/{cep}/json/"
        try:
            response = requests.get(url)
            data = response.json()
            street = data['logradouro']
            district = data['bairro']
            city = data['localidade']
            state = data['estado']
            address = {'street': street, 'district': district, 'city': city, 'state': state}
            return self.__saveAddress__(address)
        except:
            print('ERRO NO PROCESSO DE BUSCA')
            return None

    def getAddressByStreetId(self, streetId: int) -> Address:
        street = streetService.getById(streetId)
        if not street:
            return None
        district = districtService.getById(street.districtId)
        city = cityService.getById(district.cityId)
        state = stateService.getById(city.stateId)
        address = Address(street, district, city, state)
        return address

    def saveAddressByObj(self, address: dict) -> Address:
        return self.__saveAddress__(address)

    def saveAddress(self, street:str, city:str, uf:str) -> List[Address]:
        url = f"https://viacep.com.br/ws/{uf}/{city}/{street}/json/"
        data = requests.get(url)
        addressList = []
        for info in data.json():
            street = info['logradouro']
            district = info['bairro']
            city = info['localidade']
            uf = info['uf']
            address = {'street': street, 'district': district, 'city': city, 'uf': uf}
            addressList.append(self.__saveAddress__(address))
        return addressList

    def __saveAddress__(self, address: dict) -> Address:
        state = stateService.getState(address['uf'])
        city = cityService.save(address['city'], state.id)
        district = districtService.save(address['district'], city.id)
        street = streetService.save(address['street'], district.id, city.id)
        objAddress = Address(street, district, city, state)
        return objAddress
        

        